
import streamlit as st
import numpy as np
import random
import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from io import BytesIO

st.set_page_config(page_title="Web-based Generative Poster", layout="wide")

# -----------------------------
# Utilities
# -----------------------------
def seed_all(seed: int):
    random.seed(seed)
    np.random.seed(seed)

def fig_to_bytes(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    buf.seek(0)
    return buf

# -----------------------------
# Shared palettes (Week 4 style)
# -----------------------------
PALETTES_W4 = [
    ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"],
    ["#F7C8E0", "#FFDDCC", "#FFE6EB", "#D6F5F5", "#C9E4FF"],
    ["#FDE2E4", "#FAD2E1", "#E2ECE9", "#BEE1E6", "#C6DEF1"],
]
PALETTES_W4B = [
    ["#FF4C4C", "#FFD93D", "#6BCB77", "#4D96FF", "#FF6F91"],  # bright pastel
    ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"],  # soft pastel
]

# -----------------------------
# Week 4 Part A - Flowers
# -----------------------------
def generate_flower(center=(0.5,0.5), petals=8, radius=0.2, points=50):
    curves = []
    angles = np.linspace(0, 2*np.pi, petals, endpoint=False)
    for a in angles:
        t = np.linspace(0,1,points)
        x = center[0] + t * radius * np.cos(a) + np.random.normal(0, 0.01, size=points)
        y = center[1] + t * radius * np.sin(a) + np.random.normal(0, 0.01, size=points)
        curves.append((x, y))
    return curves

def draw_flowers(flowers, layers, wobble, palette_index, title="🌸 Spring Abstract"):
    fig = plt.figure(figsize=(6,6))
    colors = PALETTES_W4[palette_index % len(PALETTES_W4)]
    for flower in flowers:
        for x, y in flower:
            for l in range(layers):
                x_shifted = x + np.random.normal(0, wobble, size=len(x))
                y_shifted = y + np.random.normal(0, wobble, size=len(y))
                plt.plot(
                    x_shifted, y_shifted,
                    color=random.choice(colors),
                    linewidth=3 + (layers - l),
                    alpha=0.6,
                    solid_capstyle='round'
                )
    plt.xlim(0,1); plt.ylim(0,1); plt.axis('off')
    plt.title(f"{title} | Layers: {layers}, Wobble: {wobble:.3f}, Palette: {palette_index}")
    return fig

# -----------------------------
# Week 4 Part B - Spheres
# -----------------------------
def generate_sphere(center=(0.5,0.5), radius=0.05, points=100):
    t = np.linspace(0, 2*np.pi, points)
    x = center[0] + radius * np.cos(t)
    y = center[1] + radius * np.sin(t)
    return x, y

def draw_spheres(spheres, layers, shadow_offset, palette_index, title="🍓 Fruity 3D Poster"):
    fig = plt.figure(figsize=(6,6))
    colors = PALETTES_W4B[palette_index % len(PALETTES_W4B)]
    for x, y in spheres:
        for l in range(layers):
            x_shadow = x + shadow_offset*(layers-l)
            y_shadow = y - shadow_offset*(layers-l)
            plt.fill(x_shadow, y_shadow, color='gray', alpha=0.2)
            plt.fill(x, y, color=random.choice(colors), alpha=0.9)
    plt.xlim(0,1); plt.ylim(0,1); plt.axis('off')
    plt.title(f"{title} | Layers: {layers}, Shadow: {shadow_offset}, Palette: {palette_index}")
    return fig

# -----------------------------
# Week 5 - Blob + CSV Palette
# -----------------------------
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2*math.pi, points, endpoint=False)
    radii  = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def make_palette(k=6, mode="pastel", base_h=0.60, csv_df=None):
    cols = []
    if mode == "csv" and csv_df is not None and len(csv_df) > 0:
        return [(row.r, row.g, row.b) for row in csv_df.itertuples()]
    for _ in range(k):
        if mode == "pastel":
            h = random.random(); s = random.uniform(0.15,0.35); v = random.uniform(0.9,1.0)
        elif mode == "vivid":
            h = random.random(); s = random.uniform(0.8,1.0);  v = random.uniform(0.8,1.0)
        elif mode == "mono":
            h = base_h;         s = random.uniform(0.2,0.6);   v = random.uniform(0.5,1.0)
        else: # random
            h = random.random(); s = random.uniform(0.3,1.0); v = random.uniform(0.5,1.0)
        cols.append(tuple(hsv_to_rgb([h,s,v])))
    return cols

def draw_blobs(n_layers=8, wobble=0.15, palette_mode="pastel", seed=0, csv_df=None):
    seed_all(seed)
    fig, ax = plt.subplots(figsize=(6,8))
    ax.axis('off')
    ax.set_facecolor((0.97,0.97,0.97))
    palette = make_palette(6, mode=palette_mode, csv_df=csv_df)
    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob((cx,cy), r=rr, wobble=wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.3, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))
    ax.text(0.05, 0.95, f"Interactive Poster • {palette_mode}",
            transform=ax.transAxes, fontsize=12, weight="bold")
    return fig

def show_palette_bar(palette):
    fig = plt.figure(figsize=(6, 1.2))
    for i, c in enumerate(palette):
        plt.fill_between([i, i+1], 0, 1, color=c)
        plt.text(i+0.5, -0.1, f"{i+1}", ha="center", va="top")
    plt.axis("off")
    return fig

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Controls")
mode = st.sidebar.selectbox(
    "Mode",
    ["Week4 • Flowers", "Week4 • Spheres", "Week5 • Blobs (CSV)"],
    index=2
)
seed = st.sidebar.number_input("Seed", min_value=0, max_value=99999, value=0, step=1)
seed_all(int(seed))

# -----------------------------
# Session state for shapes
# -----------------------------
if "flowers" not in st.session_state:
    st.session_state.flowers = [generate_flower()]
if "spheres" not in st.session_state:
    st.session_state.spheres = [generate_sphere()]

# -----------------------------
# Mode: Flowers
# -----------------------------
if mode.startswith("Week4 • Flowers"):
    st.title("🌸 Week 4 Part A — Spring Abstract (Flowers)")
    c1, c2 = st.columns([2,1])
    with c2:
        layers = st.slider("Layers", 1, 8, 3)
        wobble = st.slider("Wobble", 0.0, 0.05, 0.01, 0.005)
        palette_index = st.slider("Palette Index", 0, len(PALETTES_W4)-1, 0)
        st.subheader("Add Flower")
        fx = st.slider("X", 0.0, 1.0, 0.5, 0.01)
        fy = st.slider("Y", 0.0, 1.0, 0.5, 0.01)
        petals = st.slider("Petals", 5, 12, 8)
        radius = st.slider("Radius", 0.05, 0.30, 0.20, 0.01)
        if st.button("Add Flower"):
            st.session_state.flowers.append(generate_flower(center=(fx, fy), petals=petals, radius=radius))
        if st.button("Reset Flowers"):
            st.session_state.flowers = [generate_flower()]
    with c1:
        fig = draw_flowers(st.session_state.flowers, layers, wobble, palette_index)
        st.pyplot(fig, clear_figure=True)
        st.download_button("Download PNG", data=fig_to_bytes(fig), file_name="poster_flowers.png", mime="image/png")

# -----------------------------
# Mode: Spheres
# -----------------------------
elif mode.startswith("Week4 • Spheres"):
    st.title("🍓 Week 4 Part B — Fruity 3D Poster (Spheres)")
    c1, c2 = st.columns([2,1])
    with c2:
        layers = st.slider("Layers", 1, 10, 5)
        shadow_offset = st.slider("Shadow Offset", 0.0, 0.05, 0.02, 0.005)
        palette_index = st.slider("Palette Index", 0, len(PALETTES_W4B)-1, 0)
        st.subheader("Add Sphere")
        sx = st.slider("X", 0.0, 1.0, 0.5, 0.01)
        sy = st.slider("Y", 0.0, 1.0, 0.5, 0.01)
        sr = st.slider("Radius", 0.01, 0.15, 0.05, 0.005)
        if st.button("Add Sphere"):
            st.session_state.spheres.append(generate_sphere(center=(sx, sy), radius=sr))
        if st.button("Reset Spheres"):
            st.session_state.spheres = [generate_sphere()]
    with c1:
        fig = draw_spheres(st.session_state.spheres, layers, shadow_offset, palette_index)
        st.pyplot(fig, clear_figure=True)
        st.download_button("Download PNG", data=fig_to_bytes(fig), file_name="poster_spheres.png", mime="image/png")

# -----------------------------
# Mode: Blobs + CSV Palette
# -----------------------------
else:
    st.title("🫧 Week 5 — Interactive Blobs with CSV Palette")
    c1, c2 = st.columns([2,1])

    # Load CSV: either uploaded by user or bundled sample
    with c2:
        st.subheader("Palette Source")
        palette_mode = st.selectbox("Palette Mode", ["pastel","vivid","mono","random","csv"], index=4)
        uploaded = st.file_uploader("Upload palette.csv (columns: name,r,g,b)", type=["csv"])
        csv_df = None
        if uploaded is not None:
            try:
                csv_df = pd.read_csv(uploaded)
            except Exception as e:
                st.error(f"CSV read error: {e}")
        else:
            # fallback to bundled sample palette.csv in repo
            try:
                csv_df = pd.read_csv("palette.csv")
            except Exception:
                csv_df = None

        n_layers = st.slider("Layers", 3, 20, 8)
        wobble = st.slider("Wobble", 0.01, 1.0, 0.15, 0.01)
        base_h = st.slider("Mono Base Hue (0~1)", 0.0, 1.0, 0.60, 0.01)
        if palette_mode != "mono":
            base_h = None

    with c1:
        fig = draw_blobs(n_layers=n_layers, wobble=wobble, palette_mode=palette_mode, seed=seed, csv_df=csv_df)
        st.pyplot(fig, clear_figure=True)
        st.download_button("Download PNG", data=fig_to_bytes(fig), file_name="poster_blobs.png", mime="image/png")

    # Show palette preview when available
    if palette_mode == "csv" and csv_df is not None and len(csv_df) > 0:
        palette_list = [(row.r, row.g, row.b) for row in csv_df.itertuples()]
        with st.expander("CSV Palette Preview"):
            figbar = show_palette_bar(palette_list)
            st.pyplot(figbar, clear_figure=True)

st.caption("Made with Streamlit • Week 4 & 5 → Week 9 Web-based Poster")
