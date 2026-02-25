from PIL import Image, ImageDraw
import os

def create_placeholder(path, size=(256, 256), color=(180, 180, 180, 255), shape="rect"):
    img = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    if shape == "rect":
        draw.rectangle([10, 10, size[0]-10, size[1]-10], fill=color)
    elif shape == "circle":
        draw.ellipse([10, 10, size[0]-10, size[1]-10], fill=color)
    elif shape == "triangle":
        draw.polygon([(size[0]//2, 10), (10, size[1]-10), (size[0]-10, size[1]-10)], fill=color)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)

ASSETS = {
    "icons": ["chemist", "doctor", "lawyer", "engineer", "trader", "investor", "fund_manager", "entrepreneur", "founder", "pm", "sales", "realestate", "bizdev", "manager", "logistics", "supplychain", "designer", "marketer", "creator"],
    "objects/expert": [
        "stethoscope", "ecg_monitor", "surgical_lamp", "iv_bag", "surgical_mask", "medical_chart",
        "portrait_anesthesiologist_f", "portrait_nurse_m", "portrait_resident_f",
        "heart_icon", "surgery_tools_icon", "hospital_building_icon"
    ],
    "objects/allocator": [
        "trading_monitor", "stock_certificate", "bull_statue", "bear_statue", "briefcase", "phone_receiver",
        "agent_whale_icon", "agent_algorithm_icon", "agent_fed_icon", "agent_analyst_icon",
        "chart_up_icon", "chart_down_icon"
    ]
}

def generate_all():
    base_dir = "trajectory/assets"
    for category, items in ASSETS.items():
        for item in items:
            path = os.path.join(base_dir, category, f"{item}.png")
            shape = "rect"
            color = (180, 180, 180, 255)

            if "icon" in item or "portrait" in item or "icon" in category:
                shape = "circle"
            if "portrait" in item:
                color = (200, 180, 160, 255) # Flesh tone placeholder

            create_placeholder(path, shape=shape, color=color)
    print("Updated asset manifest generated.")

if __name__ == "__main__":
    generate_all()
