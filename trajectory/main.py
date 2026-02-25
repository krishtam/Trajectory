import pygame
import sys
import numpy as np
from enum import Enum

from trajectory.core.career_taxonomy import resolve_pillar
from trajectory.core.seed_engine import WorldConfig
from trajectory.core.simulation import WorldState
from trajectory.core.world_rng import WorldRNG
from trajectory.core.bayesian_network import build_event_network, sample_next_event
from trajectory.core.narrative import NarrativeEngine

from trajectory.ml.quality_model import load_quality_model, get_good_seed
from trajectory.ml.difficulty_calibrator import DifficultyCalibrator

from trajectory.rendering.themes import get_theme
from trajectory.rendering.asset_loader import AssetLoader
from trajectory.rendering.particles import ParticleSystem
from trajectory.rendering.scene_objects import place_scene_objects
from trajectory.rendering.renderer import render_frame

from trajectory.rendering.challenges.signal_reading import SignalReadingChallenge
from trajectory.rendering.challenges.resource_allocation import ResourceAllocationChallenge
from trajectory.rendering.challenges.sequence_judgment import SequenceJudgmentChallenge
from trajectory.rendering.challenges.pressure_response import PressureResponseChallenge
from trajectory.rendering.challenges.negotiation import NegotiationChallenge

from trajectory.screens.career_select import CareerSelectScreen
from trajectory.screens.world_boot import WorldBootScreen
from trajectory.screens.end_screen import EndScreen

class GameState(Enum):
    CAREER_SELECT = 1
    WORLD_BOOT = 2
    WORLD_VIEW = 3
    CHALLENGE = 4
    END_SCREEN = 5

class TrajectoryGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Trajectory - Probabilistic Career Simulation")
        self.clock = pygame.time.Clock()
        self.state = GameState.CAREER_SELECT

        self.quality_model = load_quality_model()
        self.asset_loader = AssetLoader()
        self.narrative_engine = NarrativeEngine()

        self.current_screen = CareerSelectScreen()
        self.world_state = None
        self.theme = None
        self.scene_objects = []
        self.particles = None
        self.event_network = None
        self.calibrator = DifficultyCalibrator()

        self.active_challenge = None
        self.notification = None
        self.notification_start = 0
        self.difficulty_adj = [0,0,0,0,0]

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update(events)
            self.draw()
            self.clock.tick(60)

    def update(self, events):
        if self.state == GameState.CAREER_SELECT:
            result = self.current_screen.update(events)
            if result:
                pillar, career = result
                seed, config = get_good_seed(pillar, career, self.quality_model)
                self.world_state = WorldState(config)
                self.theme = get_theme(pillar, career)
                self.state = GameState.WORLD_BOOT
                self.current_screen = WorldBootScreen(config)

        elif self.state == GameState.WORLD_BOOT:
            if self.current_screen.update(events):
                # Init world view
                self.scene_objects = place_scene_objects(self.world_state.config, self.theme, self.asset_loader)
                rng = WorldRNG(self.world_state.config.seed + 777)
                self.particles = ParticleSystem(rng, self.theme, 1280, 720)
                self.event_network = build_event_network(self.world_state.config.events)

                # Start Day 1 Narrative
                self.world_state.narrative_text = self.narrative_engine.get_day_text(self.world_state.config.career, 0)

                self.state = GameState.WORLD_VIEW
                self.last_cycle_time = pygame.time.get_ticks()

        elif self.state == GameState.WORLD_VIEW:
            now = pygame.time.get_ticks()
            if self.notification and now - self.notification_start > 3000:
                self.notification = None

            if now - self.last_cycle_time > 12000: # 12s of immersion/story reading
                self.last_cycle_time = now

                # Check cycle limit
                if self.world_state.cycle >= self.world_state.max_cycles:
                    self.state = GameState.END_SCREEN
                    self.current_screen = EndScreen(self.world_state.check_win(), self.world_state)
                    return

                # Sample Event
                evidence = self.world_state.to_evidence_dict()
                event = sample_next_event(self.event_network, evidence, WorldRNG(self.world_state.config.seed + self.world_state.cycle))
                if event:
                    self.world_state.apply_event(event, self.world_state.config)
                    self.notification = f"PROTOCOL ALERT: {event.upper()}"
                    self.notification_start = now

                # Start Challenge
                self.start_challenge()

        elif self.state == GameState.CHALLENGE:
            result = self.active_challenge.update(events)
            if result:
                # Update Calibrator
                feats = np.array([0, 0, result.performance, 0, self.world_state.pressure_level, self.world_state.cycle / 5.0])
                self.calibrator.update(feats, result.performance)
                self.difficulty_adj = self.calibrator.predict_difficulty_adjustment(feats)

                self.world_state.apply_challenge_outcome(result.performance, self.world_state.config)
                self.world_state.cycle += 1

                if self.world_state.cycle < self.world_state.max_cycles:
                    self.world_state.narrative_text = self.narrative_engine.get_day_text(self.world_state.config.career, self.world_state.cycle)

                self.active_challenge = None
                self.state = GameState.WORLD_VIEW
                self.last_cycle_time = pygame.time.get_ticks()

        elif self.state == GameState.END_SCREEN:
            if self.current_screen.update(events):
                self.state = GameState.CAREER_SELECT
                self.current_screen = CareerSelectScreen()

    def start_challenge(self):
        self.state = GameState.CHALLENGE
        rng = WorldRNG(self.world_state.config.seed + self.world_state.cycle * 100)
        c_type = self.world_state.cycle % 5
        if c_type == 0:
            self.active_challenge = SignalReadingChallenge(self.world_state.config, self.theme, rng)
        elif c_type == 1:
            self.active_challenge = ResourceAllocationChallenge(self.world_state.config, self.theme, rng)
        elif c_type == 2:
            self.active_challenge = SequenceJudgmentChallenge(self.world_state.config, self.theme, rng)
        elif c_type == 3:
            self.active_challenge = PressureResponseChallenge(self.world_state.config, self.theme, rng)
        else:
            self.active_challenge = NegotiationChallenge(self.world_state.config, self.theme, rng)

    def draw(self):
        if self.state in [GameState.CAREER_SELECT, GameState.WORLD_BOOT, GameState.END_SCREEN]:
            self.current_screen.draw(self.screen)
        else:
            # Transfer local main state to world state for renderer
            self.world_state.notification = self.notification
            self.world_state.active_challenge = self.active_challenge
            render_frame(self.screen, self.world_state, self.theme, self.scene_objects, self.particles)
        pygame.display.flip()

if __name__ == "__main__":
    game = TrajectoryGame()
    game.run()
