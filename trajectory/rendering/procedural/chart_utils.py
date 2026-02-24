import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import pygame
from PIL import Image

def generate_chart_surface(data: list, theme: dict,
                             chart_type: str = "line",
                             size_px: tuple = (400, 200)) -> pygame.Surface:
    """Renders a matplotlib chart to a pygame Surface."""
    figsize = (size_px[0]/100, size_px[1]/100)
    bg = tuple(c/255 for c in theme["background"])
    fg = tuple(c/255 for c in theme["primary"])

    fig, ax = plt.subplots(figsize=figsize, facecolor=bg)
    ax.set_facecolor(bg)

    if chart_type == "line":
        ax.plot(data, color=fg, linewidth=2, antialiased=True)
        ax.fill_between(range(len(data)), data, alpha=0.15, color=fg)
    elif chart_type == "candlestick":
        # data = list of (open, high, low, close) tuples
        for i, (o, h, l, c) in enumerate(data):
            color = fg if c >= o else (0.9, 0.3, 0.3)
            ax.plot([i, i], [l, h], color=color, linewidth=1)
            ax.add_patch(plt.Rectangle((i-0.3, min(o,c)), 0.6, abs(c-o),
                                        facecolor=color, edgecolor=color))
    elif chart_type == "bar":
        ax.bar(range(len(data)), data, color=fg, alpha=0.8)

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(tuple(c/255 for c in theme["grid"]))

    plt.tight_layout(pad=0.1)

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight",
                facecolor=fig.get_facecolor(), transparent=False)
    buf.seek(0)
    plt.close(fig)

    pil_img = Image.open(buf)
    mode = pil_img.mode
    raw = pil_img.tobytes()
    surface = pygame.image.fromstring(raw, pil_img.size, mode)
    return surface
