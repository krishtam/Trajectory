from PIL import Image, ImageDraw
import os

def create_placeholder(path, size=(256, 256), shape="rect"):
    img = Image.new("RGBA", size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Draw a neutral gray shape that will be colorized at runtime
    if shape == "rect":
        draw.rectangle([10, 10, size[0]-10, size[1]-10], fill=(180, 180, 180, 255))
    elif shape == "circle":
        draw.ellipse([10, 10, size[0]-10, size[1]-10], fill=(180, 180, 180, 255))
    elif shape == "triangle":
        draw.polygon([(size[0]//2, 10), (10, size[1]-10), (size[0]-10, size[1]-10)], fill=(180, 180, 180, 255))

    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)

ASSETS = {
    "icons": ["chemist", "doctor", "lawyer", "engineer", "trader", "investor", "fund_manager", "entrepreneur", "founder", "pm", "sales", "realestate", "bizdev", "manager", "logistics", "supplychain", "designer", "marketer", "creator"],
    "objects/expert": ["lab_beaker", "test_tube_rack", "periodic_fragment", "microscope", "stethoscope_coil", "pill_bottle", "legal_scales", "document_stack", "blueprint_roll", "circuit_chip"],
    "objects/allocator": ["trading_terminal", "coin_stack", "bar_chart_static", "briefcase", "bull_silhouette", "bear_silhouette", "bank_building", "candlestick_static"],
    "objects/builder": ["rocket_ship", "laptop_open", "kanban_board", "lightbulb", "whiteboard", "coffee_cup", "startup_office", "mvp_card"],
    "objects/connector": ["handshake", "house_building", "for_sale_sign", "phone_receiver", "business_card", "city_skyline", "contract_paper", "meeting_table"],
    "objects/operator": ["delivery_truck", "warehouse", "org_chart_fragment", "clipboard", "gear_large", "factory_building", "barcode", "shipping_box"],
    "objects/creator": ["camera", "paint_palette", "megaphone", "smartphone", "social_graph", "color_swatches", "ad_banner", "video_play_card"]
}

def generate_all():
    base_dir = "trajectory/assets"
    for category, items in ASSETS.items():
        for item in items:
            path = os.path.join(base_dir, category, f"{item}.png")
            shape = "rect"
            if "icon" in category: shape = "circle"
            if "beaker" in item or "flask" in item: shape = "triangle"
            create_placeholder(path, shape=shape)
    print("All placeholder assets generated.")

if __name__ == "__main__":
    generate_all()
