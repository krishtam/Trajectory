import pygame
import math

class ProgrammaticAssets:
    @staticmethod
    def get_surface(name, size=(256, 256), color=(180, 180, 180)):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        draw_func = getattr(ProgrammaticAssets, f"draw_{name}", None)
        if draw_func:
            draw_func(surf, color)
        else:
            # Fallback
            pygame.draw.rect(surf, color, (0, 0, size[0], size[1]), 2)
        return surf

    # --- SURGEON ASSETS ---

    @staticmethod
    def draw_stethoscope(surf, col):
        # Tubing
        pygame.draw.arc(surf, (40, 40, 40), (40, 40, 170, 170), 0, math.pi, 8)
        pygame.draw.line(surf, (40, 40, 40), (40, 125), (40, 200), 8)
        pygame.draw.line(surf, (40, 40, 40), (210, 125), (210, 200), 8)
        # Chest piece
        pygame.draw.circle(surf, (150, 150, 150), (125, 220), 30)
        pygame.draw.circle(surf, (200, 200, 200), (125, 220), 20)

    @staticmethod
    def draw_ecg_monitor(surf, col):
        pygame.draw.rect(surf, (30, 30, 35), (20, 50, 216, 156), border_radius=10)
        pygame.draw.rect(surf, (10, 10, 10), (35, 65, 186, 100))
        # Draw wave
        points = [(45, 115), (70, 115), (80, 80), (90, 150), (100, 115), (150, 115)]
        pygame.draw.lines(surf, (100, 255, 150), False, points, 2)

    @staticmethod
    def draw_surgical_lamp(surf, col):
        pygame.draw.circle(surf, (200, 200, 210), (128, 128), 100)
        for i in range(6):
            angle = i * (math.pi / 3)
            lx = 128 + 60 * math.cos(angle)
            ly = 128 + 60 * math.sin(angle)
            pygame.draw.circle(surf, (255, 255, 255), (int(lx), int(ly)), 25)

    @staticmethod
    def draw_iv_bag(surf, col):
        pygame.draw.rect(surf, (220, 230, 240, 150), (80, 40, 96, 160), border_radius=20)
        pygame.draw.line(surf, (100, 100, 100), (128, 10), (128, 40), 4)
        pygame.draw.rect(surf, (150, 180, 200), (110, 200, 36, 20))

    @staticmethod
    def draw_portrait_anesthesiologist_f(surf, col):
        pygame.draw.circle(surf, (230, 190, 170), (128, 128), 100) # Face
        pygame.draw.rect(surf, (100, 150, 200), (28, 28, 200, 60), border_radius=20) # Cap
        pygame.draw.rect(surf, (200, 230, 255), (60, 140, 136, 60), border_radius=5) # Mask
        # Eyes
        pygame.draw.circle(surf, (50, 50, 50), (90, 110), 8)
        pygame.draw.circle(surf, (50, 50, 50), (166, 110), 8)

    @staticmethod
    def draw_portrait_nurse_m(surf, col):
        pygame.draw.circle(surf, (210, 170, 150), (128, 128), 100)
        pygame.draw.rect(surf, (80, 120, 180), (28, 28, 200, 50)) # Cap
        pygame.draw.circle(surf, (40, 40, 40), (90, 110), 7)
        pygame.draw.circle(surf, (40, 40, 40), (166, 110), 7)

    @staticmethod
    def draw_portrait_resident_f(surf, col):
        pygame.draw.circle(surf, (240, 210, 190), (128, 128), 100)
        pygame.draw.arc(surf, (100, 70, 40), (28, 28, 200, 180), 0, math.pi, 20) # Hair
        pygame.draw.circle(surf, (60, 60, 80), (90, 110), 8)
        pygame.draw.circle(surf, (60, 60, 80), (166, 110), 8)

    # --- TRADER ASSETS ---

    @staticmethod
    def draw_trading_monitor(surf, col):
        pygame.draw.rect(surf, (40, 40, 45), (20, 40, 216, 160), border_radius=5) # Frame
        pygame.draw.rect(surf, (5, 5, 10), (30, 50, 196, 130)) # Screen
        # Candlesticks
        for i in range(5):
            x = 50 + i * 35
            pygame.draw.line(surf, (100, 255, 150), (x, 70), (x, 140), 2)
            pygame.draw.rect(surf, (100, 255, 150), (x-6, 85, 12, 40))

    @staticmethod
    def draw_bull_statue(surf, col):
        # Stylized Bull
        pygame.draw.ellipse(surf, (120, 100, 80), (40, 80, 160, 100)) # Body
        pygame.draw.circle(surf, (120, 100, 80), (200, 90), 40) # Head
        pygame.draw.arc(surf, (200, 200, 200), (180, 40, 60, 60), 0, math.pi/2, 6) # Horn

    @staticmethod
    def draw_bear_statue(surf, col):
        pygame.draw.circle(surf, (80, 70, 60), (128, 140), 80) # Body
        pygame.draw.circle(surf, (80, 70, 60), (128, 70), 50) # Head
        pygame.draw.circle(surf, (80, 70, 60), (90, 40), 20) # Ear

    @staticmethod
    def draw_agent_whale_icon(surf, col):
        pygame.draw.circle(surf, (30, 60, 100), (128, 128), 110)
        pygame.draw.ellipse(surf, (200, 220, 255), (40, 100, 180, 80)) # Whale body
        pygame.draw.polygon(surf, (200, 220, 255), [(40, 140), (10, 110), (10, 170)]) # Tail

    @staticmethod
    def draw_agent_fed_icon(surf, col):
        pygame.draw.circle(surf, (150, 120, 30), (128, 128), 110)
        pygame.draw.rect(surf, (255, 230, 150), (64, 64, 128, 128), 4)
        pygame.draw.circle(surf, (255, 230, 150), (128, 128), 40, 4)

    @staticmethod
    def draw_briefcase(surf, col):
        pygame.draw.rect(surf, (100, 70, 40), (40, 80, 176, 120), border_radius=5)
        pygame.draw.rect(surf, (60, 40, 20), (100, 60, 56, 20), 4) # Handle

    @staticmethod
    def draw_stock_certificate(surf, col):
        pygame.draw.rect(surf, (255, 255, 240), (40, 40, 176, 200))
        pygame.draw.rect(surf, (150, 120, 30), (40, 40, 176, 200), 8) # Border
        for i in range(5):
            pygame.draw.line(surf, (100, 100, 100), (60, 80 + i * 30), (196, 80 + i * 30), 2)

    @staticmethod
    def draw_surgical_mask(surf, col):
        pygame.draw.rect(surf, (100, 150, 200), (40, 80, 176, 100), border_radius=5)
        pygame.draw.line(surf, (255, 255, 255), (40, 80), (10, 40), 2)
        pygame.draw.line(surf, (255, 255, 255), (216, 80), (246, 40), 2)

    @staticmethod
    def draw_medical_chart(surf, col):
        pygame.draw.rect(surf, (150, 150, 160), (60, 40, 136, 180)) # Clipboard
        pygame.draw.rect(surf, (255, 255, 255), (70, 70, 116, 140)) # Paper
        pygame.draw.rect(surf, (100, 100, 100), (100, 35, 56, 25)) # Clip

    @staticmethod
    def draw_heart_icon(surf, col):
        # Heart shape
        points = [(128, 180), (60, 100), (80, 60), (128, 90), (176, 60), (196, 100)]
        pygame.draw.polygon(surf, (255, 50, 50), points)

    @staticmethod
    def draw_surgery_tools_icon(surf, col):
        pygame.draw.line(surf, (180, 180, 180), (60, 60), (196, 196), 10) # Scalpel
        pygame.draw.circle(surf, (180, 180, 180), (60, 60), 15)

    @staticmethod
    def draw_hospital_building_icon(surf, col):
        pygame.draw.rect(surf, (240, 240, 240), (64, 80, 128, 128))
        pygame.draw.rect(surf, (255, 0, 0), (110, 120, 36, 10)) # Red cross
        pygame.draw.rect(surf, (255, 0, 0), (123, 107, 10, 36))

    @staticmethod
    def draw_agent_algorithm_icon(surf, col):
        pygame.draw.circle(surf, (40, 180, 100), (128, 128), 110)
        pygame.draw.rect(surf, (200, 255, 220), (80, 80, 96, 96), 4)
        for i in range(4):
            pygame.draw.line(surf, (200, 255, 220), (128, 80), (128 + (i-1.5)*30, 50), 2)

    @staticmethod
    def draw_agent_analyst_icon(surf, col):
        pygame.draw.circle(surf, (120, 80, 180), (128, 128), 110)
        pygame.draw.circle(surf, (230, 200, 255), (110, 110), 40, 6) # Magnifier
        pygame.draw.line(surf, (230, 200, 255), (140, 140), (180, 180), 12)

    @staticmethod
    def draw_chart_up_icon(surf, col):
        pygame.draw.lines(surf, (100, 255, 150), False, [(60, 180), (100, 140), (140, 160), (200, 60)], 8)

    @staticmethod
    def draw_chart_down_icon(surf, col):
        pygame.draw.lines(surf, (255, 100, 100), False, [(60, 60), (120, 120), (160, 100), (200, 200)], 8)

    @staticmethod
    def draw_phone_receiver(surf, col):
        pygame.draw.arc(surf, (100, 100, 100), (40, 60, 176, 150), 0.2, 2.9, 20)

    @staticmethod
    def draw_generic_icon(surf, col):
        pygame.draw.circle(surf, col, (128, 128), 100, 2)
        pygame.draw.circle(surf, col, (128, 128), 70, 1)
