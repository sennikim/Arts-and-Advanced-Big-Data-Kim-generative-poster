
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random, math, os
from matplotlib.colors import hsv_to_rgb
from io import BytesIO

st.set_page_config(page_title="Arts & Advanced Big Data – Kim Seyeon", layout="wide")
st.title("🎨 Arts & Advanced Big Data — Kim Seyeon")
st.caption("Week 2–5 + Final integrated as a single web app (Streamlit)")


# ==================== Common generators ====================
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2*math.pi, points, endpoint=False)
    radii  = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def flower(center=(0.5,0.5), petals=8, radius=0.2, points=50):
    curves = []
    angles = np.linspace(0, 2*np.pi, petals, endpoint=False)
    for a in angles:
        t = np.linspace(0,1,points)
        x = center[0] + t * radius * np.cos(a) + np.random.normal(0, 0.01, size=points)
        y = center[1] + t * radius * np.sin(a) + np.random.normal(0, 0.01, size=points)
        curves.append((x, y))
    return curves

def sphere(center=(0.5,0.5), radius=0.05, points=100):
    t = np.linspace(0, 2*np.pi, points)
    x = center[0] + radius * np.cos(t)
    y = center[1] + radius * np.sin(t)
    return x, y


# ==================== CSV Palette Manager (Week 5) ====================
PALETTE_FILE = "palette.csv"

def init_palette_file():
    if not os.path.exists(PALETTE_FILE):
        df_init = pd.DataFrame([
            {"name":"sky", "r":0.4, "g":0.7, "b":1.0},
            {"name":"sun", "r":1.0, "g":0.8, "b":0.2},
            {"name":"forest", "r":0.2, "g":0.6, "b":0.3},
            {"name":"cloud", "r":0.9, "g":0.9, "b":0.95},
            {"name":"ocean", "r":0.1, "g":0.3, "b":0.8},
        ])
        df_init.to_csv(PALETTE_FILE, index=False)

def read_palette():
    init_palette_file()
    return pd.read_csv(PALETTE_FILE)

def add_color(name, r, g, b):
    df = read_palette()
    df = pd.concat([df, pd.DataFrame([{"name":name,"r":r,"g":g,"b":b}])], ignore_index=True)
    df.to_csv(PALETTE_FILE, index=False)

def update_color(name, r=None, g=None, b=None):
    df = read_palette()
    if name in df["name"].values:
        idx = df.index[df["name"]==name][0]
        if r is not None: df.at[idx,"r"] = r
        if g is not None: df.at[idx,"g"] = g
        if b is not None: df.at[idx,"b"] = b
        df.to_csv(PALETTE_FILE, index=False)

def delete_color(name):
    df = read_palette()
    df = df[df["name"]!=name]
    df.to_csv(PALETTE_FILE, index=False)

def load_csv_palette():
    df = read_palette()
    return [(row.r, row.g, row.b) for row in df.itertuples()]

def make_palette(k=6, mode="pastel", base_h=0.60, csv_override=None):
    if mode == "csv":
        if csv_override is not None:
            return csv_override
        return load_csv_palette()
    cols = []
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

def show_palette(palette):
    fig, ax = plt.subplots(figsize=(6,1.6))
    for i, c in enumerate(palette):
        ax.fill_between([i, i+1], 0, 1, color=c)
        ax.text(i+0.5, -0.08, f"{i+1}", ha="center", va="top")
    ax.axis("off")
    st.pyplot(fig)


# ==================== Utility ====================
def fig_to_bytes(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    buf.seek(0)
    return buf


# ==================== Sidebar Navigation ====================
page = st.sidebar.radio("Navigate", [
    "Week 2 – Generative Poster",
    "Week 3 – Parameter Practice",
    "Week 4 – Flowers / Spheres",
    "Week 5 – CSV Palette Poster",
    "Final – Integrated Studio",
])


# ==================== WEEK 2 ====================
if page == "Week 2 – Generative Poster":
    st.header("Week 2 – Generative Poster Project")
    st.write("Random pastel blobs with reproducibility (seed).")

    seed = st.sidebar.number_input("Seed", min_value=0, max_value=99999, value=42, step=1)
    n_layers = st.sidebar.slider("Layers", 1, 20, 10)
    wobble_min, wobble_max = st.sidebar.slider("Wobble Range", 0.0, 1.0, (0.1, 0.4), 0.01)

    # generate_palette equivalent
    random.seed(seed); np.random.seed(seed)
    palette = [tuple(0.7 + 0.3*np.array([random.random() for _ in range(3)])) for _ in range(n_layers)]

    fig, ax = plt.subplots(figsize=(6,8))
    ax.axis("off")
    ax.set_facecolor((0.98, 0.97, 0.95))
    for i in range(n_layers):
        wobble = random.uniform(wobble_min, wobble_max)
        radius = 1.2 - i * 0.08
        x, y = blob(r=radius, wobble=wobble)
        color = palette[i % len(palette)]
        ax.fill(x, y, color=color, alpha=0.4 + i*0.05, edgecolor=(0,0,0,0))

    st.pyplot(fig)
    st.download_button("Download PNG", data=fig_to_bytes(fig), file_name="week2_poster.png", mime="image/png")


# ==================== WEEK 3 ====================
elif page == "Week 3 – Parameter Practice":
    st.header("Week 3 – Parameter Practice")
    st.write("Replicate Tasks with adjustable layers/wobble/radius.")

    preset = st.sidebar.selectbox("Preset", ["Task 1 (Default)", "Task 2 • ver1", "Task 2 • ver2", "Task 3 • Pastel", "Task 3 • Vivid", "Task 3 • Monochrome Blue"])
    seed = st.sidebar.number_input("Seed", min_value=0, max_value=99999, value=0, step=1)
    random.seed(seed); np.random.seed(seed)

    # Defaults
    n_layers = 8; wobble_lo, wobble_hi = 0.05, 0.25; r_lo, r_hi = 0.15, 0.45
    palette_style = "random"

    if preset == "Task 2 • ver1":
        n_layers = 3; wobble_lo, wobble_hi = 0.01, 0.05; r_lo, r_hi = 0.15, 0.35
    elif preset == "Task 2 • ver2":
        n_layers = 20; wobble_lo, wobble_hi = 0.2, 0.5; r_lo, r_hi = 0.25, 0.6
    elif preset == "Task 3 • Pastel":
        palette_style = "pastel"
    elif preset == "Task 3 • Vivid":
        palette_style = "vivid"
    elif preset == "Task 3 • Monochrome Blue":
        palette_style = "mono_blue"

    # palette
    if palette_style == "pastel":
        base_colors = [(1.0,0.8,0.8),(1.0,0.9,0.7),(0.8,1.0,0.8),(0.7,0.9,1.0),(0.9,0.8,1.0)]
    elif palette_style == "vivid":
        base_colors = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1)]
    elif palette_style == "mono_blue":
        base_colors = [(0.2,0.4,1.0),(0.3,0.5,1.0),(0.4,0.6,1.0),(0.5,0.7,1.0),(0.6,0.8,1.0)]
    else:
        base_colors = [(random.random(),random.random(),random.random()) for _ in range(6)]
    palette = random.choices(base_colors, k=6)

    fig, ax = plt.subplots(figsize=(7,10))
    ax.axis("off")
    ax.set_facecolor((0.98,0.98,0.97))

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(r_lo, r_hi)
        x, y = blob(center=(cx,cy), r=rr, wobble=random.uniform(wobble_lo, wobble_hi))
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    st.pyplot(fig)
    st.download_button("Download PNG", data=fig_to_bytes(fig), file_name="week3_poster.png", mime="image/png")


# ==================== WEEK 4 ====================
elif page == "Week 4 – Flowers / Spheres":
    st.header("Week 4 – Flowers / Spheres")
    mode = st.sidebar.radio("Mode", ["Flowers", "Spheres"])
    seed = st.sidebar.number_input("Seed", min_value=0, max_value=99999, value=0, step=1)
    random.seed(seed); np.random.seed(seed)

    if mode == "Flowers":
        layers = st.sidebar.slider("Layers", 1, 12, 3)
        wobble = st.sidebar.slider("Wobble", 0.0, 0.1, 0.01, 0.005)
        palette_index = st.sidebar.selectbox("Palette", [0,1,2], index=0)
        palettes = [
            ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"],
            ["#F7C8E0", "#FFDDCC", "#FFE6EB", "#D6F5F5", "#C9E4FF"],
            ["#FDE2E4", "#FAD2E1", "#E2ECE9", "#BEE1E6", "#C6DEF1"],
        ]
        colors = palettes[palette_index % len(palettes)]

        n_flowers = st.sidebar.slider("How many flowers?", 1, 12, 3)
        centers = [(random.random(), random.random()) for _ in range(n_flowers)]

        fig, ax = plt.subplots(figsize=(6,6))
        for c in centers:
            f = flower(center=c, petals=random.randint(5,12), radius=random.uniform(0.1,0.25))
            for x, y in f:
                for l in range(layers):
                    xs = x + np.random.normal(0, wobble, size=len(x))
                    ys = y + np.random.normal(0, wobble, size=len(y))
                    ax.plot(xs, ys, color=random.choice(colors), linewidth=3 + (layers-l), alpha=0.6, solid_capstyle='round')
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
        ax.set_title(f"🌸 Spring Abstract | Layers: {layers}, Wobble: {wobble:.3f}, Palette: {palette_index}")
        st.pyplot(fig)
        st.download_button("Download PNG", data=fig_to_bytes(fig), file_name="week4_flowers.png", mime="image/png")

    else:  # Spheres
        layers = st.sidebar.slider("Layers", 1, 10, 5)
        shadow_offset = st.sidebar.slider("Shadow Offset", 0.0, 0.08, 0.02, 0.005)
        palette_index = st.sidebar.selectbox("Palette", [0,1], index=0)
        palettes = [
            ["#FF4C4C", "#FFD93D", "#6BCB77", "#4D96FF", "#FF6F91"],  # bright pastel
            ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"],  # soft pastel
        ]
        colors = palettes[palette_index % len(palettes)]

        n_spheres = st.sidebar.slider("How many spheres?", 1, 20, 6)
        fig, ax = plt.subplots(figsize=(6,6))
        for _ in range(n_spheres):
            x, y = sphere(center=(random.random(), random.random()), radius=random.uniform(0.03, 0.1))
            for l in range(layers):
                xsh = x + shadow_offset*(layers-l)
                ysh = y - shadow_offset*(layers-l)
                ax.fill(xsh, ysh, color='gray', alpha=0.2)
            ax.fill(x, y, color=random.choice(colors), alpha=0.9)
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
        ax.set_title(f"🍓 Fruity 3D Poster | Layers: {layers}, Shadow: {shadow_offset}, Palette: {palette_index}")
        st.pyplot(fig)
        st.download_button("Download PNG", data=fig_to_bytes(fig), file_name="week4_spheres.png", mime="image/png")


# ==================== WEEK 5 ====================
elif page == "Week 5 – CSV Palette Poster":
    st.header("Week 5 – CSV Palette Manager + Poster")
    seed = st.sidebar.number_input("Seed", min_value=0, max_value=99999, value=0, step=1)
    random.seed(seed); np.random.seed(seed)

    mode = st.sidebar.selectbox("Palette Mode", ["pastel","vivid","mono","random","csv"], index=0)
    k = st.sidebar.slider("Palette Size (k)", 3, 12, 6)
    n_layers = st.sidebar.slider("Layers", 3, 20, 8)
    wobble = st.sidebar.slider("Wobble", 0.01, 1.0, 0.15, 0.01)

    st.subheader("Palette CSV")
    init_palette_file()
    uploaded = st.file_uploader("Upload palette.csv (name,r,g,b)", type=["csv"])
    csv_override = None
    if uploaded is not None:
        try:
            dfu = pd.read_csv(uploaded)
            csv_override = [(r.r, r.g, r.b) for r in dfu.itertuples()]
            st.success("Custom CSV palette loaded from upload.")
        except Exception as e:
            st.error(f"CSV parse error: {e}")

    if st.checkbox("Show / Edit palette.csv on server", value=False):
        df = read_palette()
        st.dataframe(df, use_container_width=True)
        with st.expander("Quick Add / Update / Delete"):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1: nm = st.text_input("name", "")
            with col2: r = st.number_input("r (0-1)", 0.0, 1.0, 0.5, 0.01)
            with col3: g = st.number_input("g (0-1)", 0.0, 1.0, 0.5, 0.01)
            with col4: b = st.number_input("b (0-1)", 0.0, 1.0, 0.5, 0.01)
            with col5:
                if st.button("Add / Update"):
                    if nm in df["name"].values:
                        update_color(nm, r, g, b); st.success(f"Updated {nm}")
                    else:
                        add_color(nm, r, g, b); st.success(f"Added {nm}")
        with st.expander("Delete Color"):
            delname = st.text_input("name to delete", "")
            if st.button("Delete"):
                delete_color(delname); st.warning(f"Deleted {delname}")

    palette = make_palette(k=k, mode=mode, csv_override=csv_override)
    st.markdown("**Palette Preview**")
    show_palette(palette)

    fig, ax = plt.subplots(figsize=(6,8))
    ax.axis("off")
    ax.set_facecolor((0.97,0.97,0.97))

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x, y = blob((cx,cy), r=rr, wobble=wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.3, 0.6)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    ax.text(0.05, 0.95, f"Interactive Poster • {mode}", transform=ax.transAxes, fontsize=12, weight="bold")
    st.pyplot(fig)
    st.download_button("Download PNG", data=fig_to_bytes(fig), file_name="week5_csv_poster.png", mime="image/png")


# ==================== FINAL ====================
elif page == "Final – Integrated Studio":
    st.header("Final – Generative Poster Studio (Blob / Flower / Sphere + Palettes + Seed)")
    seed = st.sidebar.number_input("Seed", min_value=0, max_value=99999, value=42, step=1)
    random.seed(seed); np.random.seed(seed)

    shape = st.sidebar.selectbox("Shape", ["Blob","Flower","Sphere"], index=0)
    palette_mode = st.sidebar.selectbox("Palette Mode", ["pastel","vivid","mono","csv","random"], index=0)
    n_layers = st.sidebar.slider("Layers", 3, 20, 8)
    wobble = st.sidebar.slider("Wobble (for Blob)", 0.01, 0.5, 0.15, 0.01)

    uploaded = st.file_uploader("Optional: Upload custom palette.csv for this page", type=["csv"], key="final_csv")
    csv_override = None
    if uploaded is not None:
        try:
            dfu = pd.read_csv(uploaded)
            csv_override = [(r.r, r.g, r.b) for r in dfu.itertuples()]
            st.success("Custom CSV palette loaded for Final page.")
        except Exception as e:
            st.error(f"CSV parse error: {e}")

    palette = make_palette(k=6, mode=palette_mode, csv_override=csv_override)
    st.markdown("**Palette Preview**")
    show_palette(palette)

    fig, ax = plt.subplots(figsize=(6,8))
    ax.axis("off")
    ax.set_facecolor((0.98,0.98,0.97))

    for _ in range(n_layers):
        color = random.choice(palette)
        alpha = random.uniform(0.3,0.6)
        if shape == "Blob":
            cx, cy = random.random(), random.random()
            rr = random.uniform(0.15, 0.45)
            x, y = blob((cx,cy), r=rr, wobble=wobble)
            ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))
        elif shape == "Flower":
            curves = flower(center=(random.random(),random.random()), petals=random.randint(5,12), radius=random.uniform(0.1,0.25))
            for x, y in curves:
                ax.plot(x, y, color=color, linewidth=3, alpha=alpha)
        else: # Sphere
            x, y = sphere(center=(random.random(),random.random()), radius=random.uniform(0.03,0.1))
            ax.fill(x, y, color=color, alpha=alpha)

    ax.text(0.05,0.95,"Generative Poster Studio", fontsize=14, weight='bold', transform=ax.transAxes)
    ax.text(0.05,0.91,f"Shape: {shape} • Palette: {palette_mode} • Seed: {seed}", fontsize=10, transform=ax.transAxes)
    st.pyplot(fig)
    st.download_button("Download PNG", data=fig_to_bytes(fig), file_name="final_poster.png", mime="image/png")
