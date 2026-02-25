from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from trajectory.core.seed_engine import EventPoolConfig
from trajectory.core.world_rng import WorldRNG
from typing import Optional, List

EVENT_NODES = ["MarketShock", "FedAnnouncement", "WhaleLiquidation", "SurgicalComplication", "AdminPressure", "BloodShortage"]

def build_event_network(config: EventPoolConfig) -> DiscreteBayesianNetwork:
    # Nodes:
    # EconomyState (0: Contraction, 1: Stable, 2: Expansion)
    # SurgicalComplication (0: No, 1: Yes)
    # AdminPressure (0: Low, 1: High)

    model = DiscreteBayesianNetwork([
        ("EconomyState", "MarketShock"),
        ("EconomyState", "FedAnnouncement"),
        ("MarketShock", "WhaleLiquidation"),
        ("SurgicalComplication", "AdminPressure"),
        ("AdminPressure", "BloodShortage")
    ])

    # Prior CPDs
    cpd_economy = TabularCPD(variable="EconomyState", variable_card=3, values=[[0.3], [0.4], [0.3]])
    cpd_comp = TabularCPD(variable="SurgicalComplication", variable_card=2, values=[[0.85], [0.15]])

    # Dependent CPDs
    cpd_shock = TabularCPD(
        variable="MarketShock", variable_card=2,
        values=[[0.6, 0.9, 0.95], [0.4, 0.1, 0.05]],
        evidence=["EconomyState"], evidence_card=[3]
    )

    cpd_fed = TabularCPD(
        variable="FedAnnouncement", variable_card=2,
        values=[[0.7, 0.5, 0.8], [0.3, 0.5, 0.2]],
        evidence=["EconomyState"], evidence_card=[3]
    )

    cpd_whale = TabularCPD(
        variable="WhaleLiquidation", variable_card=2,
        values=[[0.9, 0.6], [0.1, 0.4]],
        evidence=["MarketShock"], evidence_card=[2]
    )

    cpd_admin = TabularCPD(
        variable="AdminPressure", variable_card=2,
        values=[[0.9, 0.4], [0.1, 0.6]],
        evidence=["SurgicalComplication"], evidence_card=[2]
    )

    cpd_blood = TabularCPD(
        variable="BloodShortage", variable_card=2,
        values=[[0.95, 0.7], [0.05, 0.3]],
        evidence=["AdminPressure"], evidence_card=[2]
    )

    model.add_cpds(cpd_economy, cpd_comp, cpd_shock, cpd_fed, cpd_whale, cpd_admin, cpd_blood)
    assert model.check_model()
    return model

def sample_next_event(model: DiscreteBayesianNetwork, evidence: dict, rng: WorldRNG) -> Optional[str]:
    inference = VariableElimination(model)

    for event_node in EVENT_NODES:
        if event_node in evidence: continue

        try:
            result = inference.query(variables=[event_node], evidence=evidence)
            p_fires = result.values[1]

            if rng.uniform() < p_fires:
                return event_node
        except:
            continue

    return None
