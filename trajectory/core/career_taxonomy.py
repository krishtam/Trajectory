CAREER_TAXONOMY = {
    "Expert": {
        "careers": ["Cardiac Surgeon", "Chemist", "Doctor", "Lawyer", "Engineer"],
        "resource": "Medical Accuracy",
        "currency_label": "Hospital Reputation",
        "output_label": "Survival Rate",
        "threat_type": "Complication",
        "leverage": "Surgical Precision",
        "income_type": "salary",
        "time_style": "high_tension",
    },
    "Allocator": {
        "careers": ["Day Trader", "Trader", "Investor", "Fund Manager"],
        "resource": "Buying Power",
        "currency_label": "Portfolio Value",
        "output_label": "Alpha %",
        "threat_type": "Market Crash",
        "leverage": "Information Edge",
        "income_type": "capital_gains",
        "time_style": "volatile",
    },
    "Builder": {
        "careers": ["Entrepreneur", "Startup Founder", "Product Manager"],
        "resource": "Runway",
        "currency_label": "Valuation",
        "output_label": "PMF Score",
        "threat_type": "Cash Burn",
        "leverage": "Vision + Execution",
        "income_type": "equity",
        "time_style": "volatile",
    },
    "Connector": {
        "careers": ["Sales", "Real Estate Agent", "Business Developer"],
        "resource": "Network",
        "currency_label": "Pipeline Value",
        "output_label": "Deals Closed",
        "threat_type": "Relationship Breakdown",
        "leverage": "Trust + Volume",
        "income_type": "commission",
        "time_style": "seasonal",
    },
    "Operator": {
        "careers": ["Manager", "Logistics Coordinator", "Supply Chain Director"],
        "resource": "Throughput",
        "currency_label": "Operational Budget",
        "output_label": "System Health",
        "threat_type": "Bottleneck Crisis",
        "leverage": "Efficiency + People",
        "income_type": "salary",
        "time_style": "slow_burn",
    },
    "Creator": {
        "careers": ["Designer", "Marketer", "Content Creator"],
        "resource": "Creative Energy",
        "currency_label": "Audience Reach",
        "output_label": "Engagement Score",
        "threat_type": "Algorithm Shift",
        "leverage": "Audience + IP",
        "income_type": "mixed",
        "time_style": "hit_driven",
    },
}

def resolve_pillar(career: str) -> str:
    for pillar, data in CAREER_TAXONOMY.items():
        if career in data["careers"]:
            return pillar
    raise ValueError(f"Career '{career}' not in taxonomy. Add it first.")
