from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from trajectory.core.seed_engine import EventPoolConfig
from trajectory.core.world_rng import WorldRNG
from typing import Optional, List

EVENT_NODES = ["MarketShock", "FundingEvent", "OpportunityWindow", "CompetitorAdvance", "RegulatoryChange"]

def build_event_network(config: EventPoolConfig) -> DiscreteBayesianNetwork:
    model = DiscreteBayesianNetwork([
        ("EconomyState", "MarketShock"),
        ("EconomyState", "FundingEvent"),
        ("PlayerPerformance", "OpportunityWindow"),
        ("PlayerPerformance", "CompetitorAdvance"),
        ("MarketShock", "RegulatoryChange"),
        ("MarketShock", "CompetitorAdvance"),
    ])

    # CPD for EconomyState (prior, no parents)
    # States: 0=contraction, 1=stable, 2=expansion
    cpd_economy = TabularCPD(
        variable="EconomyState", variable_card=3,
        values=[[0.3], [0.4], [0.3]]
    )

    # CPD for PlayerPerformance
    # States: 0=poor, 1=good
    cpd_player = TabularCPD(
        variable="PlayerPerformance", variable_card=2,
        values=[[0.5], [0.5]]
    )

    # CPD for MarketShock given EconomyState
    cpd_market_shock = TabularCPD(
        variable="MarketShock", variable_card=2,
        values=[[0.6, 0.9, 0.95],   # P(no shock)
                [0.4, 0.1, 0.05]],  # P(shock)
        evidence=["EconomyState"], evidence_card=[3]
    )

    # CPD for FundingEvent given EconomyState
    cpd_funding = TabularCPD(
        variable="FundingEvent", variable_card=2,
        values=[[0.8, 0.6, 0.4],
                [0.2, 0.4, 0.6]],
        evidence=["EconomyState"], evidence_card=[3]
    )

    # CPD for OpportunityWindow given PlayerPerformance
    cpd_opp = TabularCPD(
        variable="OpportunityWindow", variable_card=2,
        values=[[0.9, 0.6],
                [0.1, 0.4]],
        evidence=["PlayerPerformance"], evidence_card=[2]
    )

    # CPD for CompetitorAdvance given PlayerPerformance and MarketShock
    cpd_comp = TabularCPD(
        variable="CompetitorAdvance", variable_card=2,
        values=[[0.7, 0.4, 0.5, 0.2],
                [0.3, 0.6, 0.5, 0.8]],
        evidence=["PlayerPerformance", "MarketShock"], evidence_card=[2, 2]
    )

    # CPD for RegulatoryChange given MarketShock
    cpd_reg = TabularCPD(
        variable="RegulatoryChange", variable_card=2,
        values=[[0.9, 0.6],
                [0.1, 0.4]],
        evidence=["MarketShock"], evidence_card=[2]
    )

    model.add_cpds(cpd_economy, cpd_player, cpd_market_shock, cpd_funding, cpd_opp, cpd_comp, cpd_reg)
    assert model.check_model()
    return model

def sample_next_event(model: DiscreteBayesianNetwork, evidence: dict, rng: WorldRNG) -> Optional[str]:
    inference = VariableElimination(model)

    for event_node in EVENT_NODES:
        if event_node in evidence: continue

        result = inference.query(variables=[event_node], evidence=evidence)
        p_fires = result.values[1]

        if rng.uniform() < p_fires:
            return event_node

    return None
