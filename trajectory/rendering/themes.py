THEMES: dict = {
    "Expert/Cardiac Surgeon": {
        "background":      (10,  18,  30),
        "primary":         (46,  80, 144), # Medical Blue
        "accent":          (197, 227, 232), # Surgical Teal
        "text":            (220, 240, 255),
        "grid":            (25,  45,  65),
        "particle_color":  (46,  80, 144, 40),
        "particle_shape":  "circle",
        "particle_count":  40,
        "scene_objects":   ["stethoscope","ecg_monitor","surgical_lamp","iv_bag"],
        "procedural_main": "molecule_diagram", # Overhauled to medical later
        "terminology": {
            "resource": "Precision", "currency": "Hospital Reputation",
            "output": "Survival Rate", "threat": "Complication",
            "opportunity": "Research Breakthrough", "agent_authority": "Chief of Staff",
        }
    },
    "Allocator/Day Trader": {
        "background":      (5,   10,  15),
        "primary":         (28,  40,  51), # Financial Dark
        "accent":          (100, 255, 150), # Profit Green
        "text":            (255, 255, 255),
        "grid":            (15,  20,  35),
        "particle_color":  (100, 255, 150, 30),
        "particle_shape":  "line",
        "particle_count":  60,
        "scene_objects":   ["trading_monitor","stock_certificate","bull_statue","briefcase"],
        "procedural_main": "candlestick_chart",
        "terminology": {
            "resource": "Liquidity", "currency": "Portfolio Value",
            "output": "Alpha %", "threat": "Market Crash",
            "opportunity": "Alpha Window", "agent_authority": "Managing Director",
        }
    },
    "Builder/Entrepreneur": {
        "background":      (12,  20,  15),
        "primary":         (102, 187, 106),
        "accent":          (165, 214, 167),
        "text":            (220, 255, 225),
        "grid":            (25,  45,  30),
        "particle_color":  (102, 187, 106, 45),
        "particle_shape":  "circle",
        "particle_count":  50,
        "scene_objects":   ["rocket_ship","laptop_open","whiteboard","lightbulb"],
        "procedural_main": "growth_curve",
        "terminology": {
            "resource": "Runway", "currency": "Valuation",
            "output": "PMF Score", "threat": "Cash Burn Crisis",
            "opportunity": "Traction Signal", "agent_authority": "Lead Investor",
        }
    },
}

def get_theme(pillar: str, career: str) -> dict:
    key = f"{pillar}/{career}"
    if key in THEMES:
        return THEMES[key]
    # Fallback to pillar-only
    for theme_key in THEMES:
        if theme_key.startswith(pillar):
            return THEMES[theme_key]
    return THEMES["Expert/Cardiac Surgeon"]
