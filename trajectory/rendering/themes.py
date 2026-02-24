THEMES: dict = {
    "Expert/Chemist": {
        "background":      (10,  18,  30),
        "primary":         (41,  182, 246),
        "accent":          (129, 212, 250),
        "text":            (220, 240, 255),
        "grid":            (25,  45,  65),
        "particle_color":  (41,  182, 246, 40),
        "particle_shape":  "hexagon",
        "particle_count":  60,
        "scene_objects":   ["lab_beaker","test_tube_rack","periodic_table_fragment","microscope"],
        "procedural_main": "molecule_diagram",
        "terminology": {
            "resource": "Lab Hours", "currency": "Grant Funding",
            "output": "Publications", "threat": "Research Obsolescence",
            "opportunity": "Breakthrough Window", "agent_authority": "Lab Director",
        }
    },
    "Allocator/Trader": {
        "background":      (15,  12,  20),
        "primary":         (255, 171, 64),
        "accent":          (255, 213, 140),
        "text":            (255, 245, 220),
        "grid":            (35,  28,  45),
        "particle_color":  (255, 171, 64, 35),
        "particle_shape":  "line",
        "particle_count":  80,
        "scene_objects":   ["trading_terminal","bull_silhouette","briefcase","coin_stack"],
        "procedural_main": "candlestick_chart",
        "terminology": {
            "resource": "Capital", "currency": "Portfolio Value",
            "output": "Returns %", "threat": "Market Shock",
            "opportunity": "Alpha Window", "agent_authority": "Fund Manager",
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
    "Connector/Sales": {
        "background":      (20,  15,  12),
        "primary":         (239, 108, 77),
        "accent":          (255, 171, 145),
        "text":            (255, 240, 235),
        "grid":            (45,  30,  25),
        "particle_color":  (239, 108, 77, 50),
        "particle_shape":  "dot",
        "particle_count":  70,
        "scene_objects":   ["handshake","business_card","contract_paper","phone_receiver"],
        "procedural_main": "network_graph",
        "terminology": {
            "resource": "Attention", "currency": "Pipeline Value",
            "output": "Deals Closed", "threat": "Relationship Breakdown",
            "opportunity": "High-Value Lead", "agent_authority": "VP Sales",
        }
    },
    "Operator/Manager": {
        "background":      (18,  18,  22),
        "primary":         (171, 71,  188),
        "accent":          (213, 145, 223),
        "text":            (240, 230, 255),
        "grid":            (35,  30,  45),
        "particle_color":  (171, 71,  188, 30),
        "particle_shape":  "square",
        "particle_count":  55,
        "scene_objects":   ["org_chart_fragment","clipboard","gear_large","delivery_truck"],
        "procedural_main": "org_chart",
        "terminology": {
            "resource": "Throughput", "currency": "Operational Budget",
            "output": "System Health", "threat": "Bottleneck Crisis",
            "opportunity": "Efficiency Gain", "agent_authority": "CXO",
        }
    },
    "Creator/Designer": {
        "background":      (20,  12,  18),
        "primary":         (236, 64,  122),
        "accent":          (248, 145, 180),
        "text":            (255, 230, 240),
        "grid":            (45,  25,  38),
        "particle_color":  (236, 64,  122, 55),
        "particle_shape":  "scatter",
        "particle_count":  90,
        "scene_objects":   ["paint_palette","color_swatches","smartphone","camera"],
        "procedural_main": "audience_curve",
        "terminology": {
            "resource": "Creative Energy", "currency": "Audience Reach",
            "output": "Engagement Score", "threat": "Algorithm Shift",
            "opportunity": "Viral Moment", "agent_authority": "Platform Algorithm",
        }
    },
}

def get_theme(pillar: str, career: str) -> dict:
    key = f"{pillar}/{career}"
    if key in THEMES:
        return THEMES[key]
    # Fallback to pillar-only if career specific theme not found
    for theme_key in THEMES:
        if theme_key.startswith(pillar):
            return THEMES[theme_key]
    return THEMES["Expert/Chemist"]
