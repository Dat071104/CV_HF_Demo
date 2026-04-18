import os
import glob
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

# Ensure all required asset directories exist on startup
DIRS = [
    "assets/faces", "assets/truncation", "assets/mixing",
    "assets/interpolation", "assets/versions", "assets/noise_variants"
]
for d in DIRS:
    os.makedirs(d, exist_ok=True)

# ─── Internal helpers ─────────────────────────────────────────────────────────

def _load_font(size=18):
    """Gracefully load a TrueType font; fall back to PIL default."""
    for name in ["arial.ttf", "DejaVuSans.ttf", "FreeSans.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            pass
    return ImageFont.load_default()

def create_fallback_placeholder(text, size=(512, 512), seed=None):
    """Dark gradient card with centred text — shown when an asset file is missing."""
    rng = np.random.default_rng(int(seed) % (2**31) if seed is not None else 0)
    if seed is not None:
        c1 = tuple(rng.integers(0, 40, 3).tolist())
        c2 = tuple(rng.integers(70, 140, 3).tolist())
    else:
        c1 = (15, 23, 42)
        c2 = (16, 90, 70)

    arr = np.zeros((size[1], size[0], 3), dtype=np.uint8)
    for y in range(size[1]):
        t = y / size[1]
        arr[y] = [int(c1[i]*(1-t) + c2[i]*t) for i in range(3)]

    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)
    font = _load_font(20)
    lines = text.split('\n')
    lh = 30
    y0 = max(10, (size[1] - len(lines)*lh) // 2)
    for line in lines:
        if not line.strip():
            y0 += lh
            continue
        try:
            tw = draw.textlength(line, font=font)
            x0 = (size[0] - tw) // 2
        except Exception:
            x0 = 20
        draw.text((x0, y0), line, fill=(210, 215, 220), font=font)
        y0 += lh
    return img

def get_real_face(seed):
    """Load one face from assets/faces/ using seed % count. Returns PIL image only."""
    files = []
    for ext in ("*.png", "*.jpg", "*.jpeg"):
        files.extend(glob.glob(os.path.join("assets", "faces", ext)))
    files = sorted(files)
    n = len(files)
    if n == 0:
        return create_fallback_placeholder(
            "No face assets found.\nRun:  python downloader.py", seed=seed)
    idx = int(seed) % n
    try:
        return Image.open(files[idx]).convert("RGB").resize((512, 512), Image.Resampling.LANCZOS)
    except Exception:
        return create_fallback_placeholder(f"Load error · index {idx}", seed=seed)

def _try_load(path, size=(512, 512)):
    """Return a PIL image from path, or None if file is missing / corrupt."""
    if os.path.exists(path):
        try:
            return Image.open(path).convert("RGB").resize(size, Image.Resampling.LANCZOS)
        except Exception:
            pass
    return None

def _stamp_label(img, text, color="#f9fafb"):
    """Draw a solid dark banner with coloured text at the very top of an image in-place."""
    draw = ImageDraw.Draw(img)
    font = _load_font(16)
    draw.rectangle([0, 0, img.width, 34], fill=(0, 0, 0))
    draw.text((8, 8), text, fill=color, font=font)
    return img

# ─── FIX-1: Tab 1 — Face Generator ───────────────────────────────────────────

def generate_face(seed):
    """
    Returns (PIL image, label_markdown).
    FIX-1: seed is mapped mod-50 so all values 0-49 are valid, higher values cycle.
    Label explicitly shows the mapping for transparency.
    """
    try:
        seed = int(seed)
    except Exception:
        seed = 0
    clamped = seed % 50
    img = get_real_face(clamped)
    label = (
        f"**Seed {seed} → Face #{clamped + 1} / 50**  \n"
        "Each seed maps to a unique point sampled from StyleGAN's 512-dimensional Z-space, "
        "projected to W-space by the 8-layer mapping network before synthesis."
    )
    return img, label

# ─── A+1: Noise Variants (same W, different stochastic noise B) ───────────────

def noise_variants_wrapper(seed):
    """
    Returns 3 PIL images at 256×256: same identity (W), different noise B.
    Uses pre-generated assets if available; applies numpy Gaussian noise proxy otherwise.
    """
    try:
        seed = int(seed) % 50
    except Exception:
        seed = 0

    base = get_real_face(seed)
    results = []
    for i in range(1, 4):
        path = os.path.join("assets", "noise_variants", f"seed{seed:02d}_n{i}.png")
        loaded = _try_load(path, (256, 256))
        if loaded is not None:
            results.append(loaded)
        else:
            # Proxy: add scaled Gaussian noise to high-frequency areas
            arr = np.array(base.resize((256, 256))).astype(np.float32)
            rng = np.random.default_rng(seed * 1000 + i * 7)
            noise = rng.normal(0, 5.0 + i * 3.0, arr.shape)
            noisy = np.clip(arr + noise, 0, 255).astype(np.uint8)
            results.append(Image.fromarray(noisy))

    return results[0], results[1], results[2]

# ─── FIX-2: Tab 2 — Truncation ────────────────────────────────────────────────

def truncate(seed, psi):
    """
    FIX-2: Loads a DIFFERENT pre-curated face image per ψ bracket.
    NO ImageEnhance.Color / GaussianBlur — those were theoretically wrong.
    The three bracketed images represent safe/balanced/wild faces from the pool.
    """
    try:
        seed = int(seed)
    except Exception:
        seed = 0

    if psi < 0.5:
        asset_path = os.path.join("assets", "truncation", "psi_low.png")
        fallback_seed = 3      # conservative-looking face
        label = (
            f"**ψ = {psi:.2f} — Safe zone**  \n"
            "W-vector pulled close to dataset mean **w̄**. Face is photorealistic but generic — "
            "low individuality, minimal artifact risk.  \n\n"
            "⚙️ *Demo note: showing a pre-selected face representative of the low-ψ range.  \n"
            "Actual truncation: **w' = w̄ + ψ(w − w̄)** — ψ=0 produces the literal dataset mean face.*"
        )
    elif psi <= 1.0:
        asset_path = os.path.join("assets", "truncation", "psi_mid.png")
        fallback_seed = 22     # balanced-looking face
        label = (
            f"**ψ = {psi:.2f} — Sweet spot**  \n"
            "NVIDIA production default. Balanced photorealism and identity diversity.  \n"
            "ψ=0.7 is used in all NVIDIA official published results.  \n\n"
            "⚙️ *Demo note: showing a pre-selected face representative of the mid-ψ range.  \n"
            "Actual truncation: **w' = w̄ + ψ(w − w̄)***"
        )
    else:
        asset_path = os.path.join("assets", "truncation", "psi_high.png")
        fallback_seed = 41     # distinctive/unusual face
        label = (
            f"**ψ = {psi:.2f} — Wild zone**  \n"
            "W-vector pushed **away** from mean (extrapolation beyond ψ=1.0).  \n"
            "High diversity and unusual features, but artifact risk increases significantly.  \n\n"
            "⚙️ *Demo note: showing a pre-selected face representative of the high-ψ range.  \n"
            "Actual truncation: **w' = w̄ + ψ(w − w̄)***  — ψ>1 extrapolates outside training distribution.*"
        )

    img = _try_load(asset_path)
    if img is None:
        img = get_real_face(fallback_seed)
    return img, label

# ─── FIX-3: Tab 3 — Style Mixing ─────────────────────────────────────────────

def _match_histograms(source, target):
    """Transfer colour distribution of source onto target (per-channel CDF matching)."""
    src, tgt = np.array(source), np.array(target)
    matched = np.empty_like(src)
    for ch in range(3):
        s_c, t_c = src[:, :, ch], tgt[:, :, ch]
        s_q = np.cumsum(np.histogram(s_c, 256, [0, 256])[0]).astype(float)
        s_q /= s_q[-1]
        t_q = np.cumsum(np.histogram(t_c, 256, [0, 256])[0]).astype(float)
        t_q /= t_q[-1]
        iv = np.interp(t_c.flatten(), np.arange(256), t_q)
        matched[:, :, ch] = np.interp(iv, s_q, np.arange(256)).reshape(s_c.shape)
    return Image.fromarray(matched.astype(np.uint8))

def style_mix(seed_a, seed_b, mode):
    """
    FIX-3: PRIMARY path = load mix_matrix.png (real StyleGAN output / paper Figure 3).
    FALLBACK = image compositing proxy with honest disclosure and column labels.
    """
    try:
        seed_a = int(seed_a) % 50
        seed_b = int(seed_b) % 50
    except Exception:
        seed_a, seed_b = 0, 1

    # PRIMARY: real mix grid from paper or pre-computed inference
    matrix_img = _try_load(os.path.join("assets", "mixing", "mix_matrix.png"), (900, 300))
    if matrix_img is not None:
        disclosure = (
            "✅ **Pre-computed from real StyleGAN2 inference** (Karras et al., CVPR 2020, Figure 3).  \n"
            "Each interior cell = coarse structure from row source (pose/shape, layers 4–8px) + "
            "fine style from column source (color/texture, layers 64–1024px).  \n"
            "**AdaIN(x, y) = y_s · (x − μ(x))/σ(x) + y_b** — y_s, y_b computed from W via affine A."
        )
        return matrix_img, disclosure

    # FALLBACK: image compositing proxy
    a = get_real_face(seed_a).resize((300, 300))
    b = get_real_face(seed_b).resize((300, 300))

    if "Coarse" in mode:
        mask = Image.new("L", (300, 300), 0)
        ImageDraw.Draw(mask).ellipse((45, 40, 255, 280), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(18))
        mixed = Image.composite(a, b, mask)
    elif "Middle" in mode:
        mixed = Image.blend(a, b, 0.5)
        mixed = ImageEnhance.Contrast(mixed).enhance(1.15)
    else:  # Fine
        mixed = _match_histograms(source=b, target=a)
        mixed = mixed.filter(ImageFilter.UnsharpMask(radius=2, percent=90))
        mixed = Image.blend(a, mixed, 0.65)

    # FIX-3: compose 3-column canvas with column labels stamped at bottom
    canvas = Image.new("RGB", (900, 300), (30, 41, 59))
    canvas.paste(a, (0, 0))
    canvas.paste(mixed, (300, 0))
    canvas.paste(b, (600, 0))

    draw = ImageDraw.Draw(canvas)
    font = _load_font(13)
    col_labels = [
        (0,   "Coarse source · layers 4–8px · pose, face shape"),
        (300, "Mixed result"),
        (600, "Fine source · layers 64–1024px · color, texture, pores"),
    ]
    for x, txt in col_labels:
        try:
            tw = draw.textlength(txt, font=font)
            tx = x + max(0, (300 - int(tw)) // 2)
        except Exception:
            tx = x + 10
        draw.rectangle([x, 266, x+300, 300], fill=(0, 0, 0))
        draw.text((tx, 270), txt, fill="#d1d5db", font=font)

    disclosure = (
        "⚙️ **Demo note:** Image compositing proxy — **not** actual AdaIN layer injection.  \n"
        "Real style mixing injects different W-vectors at specific synthesis layers:  \n"
        "**AdaIN(x, y) = y_s · (x − μ(x))/σ(x) + y_b**, where y_s, y_b come from W via learned affine A.  \n"
        "Limitation: nose/eyes always appear from Seed A in this proxy — "
        "real coarse injection would also transfer head pose from the source."
    )
    return canvas, disclosure

# ─── FIX-4: Tab 4 — Latent Interpolation ─────────────────────────────────────

def interpolate(seed_a, seed_b, alpha):
    """
    FIX-4: Pixel-space alpha blend with mandatory disclosure.
    Returns (blended_image, disclosure_markdown).
    """
    try:
        seed_a = int(seed_a) % 50
        seed_b = int(seed_b) % 50
        alpha  = float(np.clip(alpha, 0.0, 1.0))
    except Exception:
        seed_a, seed_b, alpha = 0, 1, 0.5

    img_a   = get_real_face(seed_a)
    img_b   = get_real_face(seed_b)
    blended = Image.blend(img_a, img_b, alpha)

    disclosure = (
        f"⚙️ **Demo note (α = {alpha:.2f}):** Pixel-space alpha blending — *not* W-space traversal.  \n"
        "True W-space interpolation: **w_mid = (1−α)·w_A + α·w_B** → StyleGAN synthesis → **realistic face**.  \n"
        "At α=0.5 this proxy shows a transparent double-exposure; "
        "real W-space midpoint produces a sharp, novel intermediate person with correct geometry.  \n"
        "Reference: rosinality/stylegan2-pytorch video interpolation demos."
    )
    return blended, disclosure

def load_interp_strip():
    """Return a pre-computed W-space interpolation strip image, or None if not present."""
    return _try_load(
        os.path.join("assets", "interpolation", "interp_strip.png"),
        size=(900, 180)
    )

# ─── FIX-5: Tab 5 — GAN Inversion (simulation only) ──────────────────────────

def invert_and_edit(img, edit_type, intensity):
    """
    FIX-5: Applies image-space transforms as a SIMULATION.
    Does NOT perform any GAN projection or latent-space operation.
    UI text in app.py makes this explicit.
    """
    if img is None:
        return None
    out = img.copy()
    if "Age" in edit_type:
        if intensity > 0:
            out = ImageEnhance.Color(out).enhance(max(0.1, 1.0 - intensity * 0.40))
            out = out.filter(ImageFilter.UnsharpMask(radius=2, percent=int(90 + intensity*90)))
            out = ImageEnhance.Brightness(out).enhance(max(0.5, 1.0 - intensity * 0.12))
        else:
            out = out.filter(ImageFilter.GaussianBlur(radius=abs(intensity) * 1.2))
            out = ImageEnhance.Color(out).enhance(min(2.0, 1.0 + abs(intensity) * 0.30))
            out = ImageEnhance.Brightness(out).enhance(min(1.4, 1.0 + abs(intensity) * 0.10))
    elif "Smile" in edit_type:
        out = ImageEnhance.Brightness(out).enhance(max(0.5, min(1.8, 1.0 + intensity * 0.18)))
        out = ImageEnhance.Contrast(out).enhance(max(0.5, min(1.8, 1.0 + intensity * 0.12)))
    elif "Lighting" in edit_type or "Sharpness" in edit_type:
        out = ImageEnhance.Sharpness(out).enhance(max(0.0, 1.0 + intensity * 3.5))
        out = ImageEnhance.Brightness(out).enhance(max(0.3, min(2.0, 1.0 + intensity * 0.25)))
    return out

# ─── FIX-6: Tab 6 — Version Comparison ───────────────────────────────────────

def _add_blob_artifacts(img):
    """
    FIX-6: Place blobs ONLY at anatomically correct locations:
    chin, ear boundaries, hair top — NOT on nose, eyes, or mouth.
    Matches actual StyleGAN1 artifact appearance from published papers.
    """
    arr    = np.array(img, dtype=np.float32)
    h, w   = arr.shape[:2]
    rng    = np.random.default_rng(42)
    result = arr.copy()

    # Zones: (cx_frac, cy_frac, r_min, r_max)
    # All x/y are fractions of image dimensions [0-1]
    zones = [
        (0.48, 0.87, 22, 36),   # chin centre
        (0.52, 0.91, 14, 24),   # just below chin
        (0.11, 0.52, 18, 28),   # left ear boundary
        (0.89, 0.52, 18, 28),   # right ear boundary
        (0.30, 0.07, 20, 30),   # hair top-left
        (0.70, 0.07, 20, 30),   # hair top-right
        (0.50, 0.04, 16, 26),   # hair top-centre
    ]

    for (cx_r, cy_r, r_min, r_max) in zones:
        cx  = int(cx_r * w)
        cy  = int(cy_r * h)
        rad = int(rng.integers(r_min, r_max))
        x0, x1 = max(0, cx-rad), min(w, cx+rad)
        y0, y1 = max(0, cy-rad), min(h, cy+rad)
        if x1 <= x0 or y1 <= y0:
            continue
        region_mean = arr[y0:y1, x0:x1].mean(axis=(0, 1))
        ys, xs = np.ogrid[:h, :w]
        mask   = ((xs - cx)**2 + (ys - cy)**2) <= rad**2
        blend  = 0.62
        result[mask] = result[mask] * (1 - blend) + region_mean * blend

    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))

def _get_v3_clean_face(base_img):
    """
    V3 returns a CLEAN face image — identical source to V2.
    The visual difference between V2 and V3 does NOT exist in still images.
    V3's innovation (alias-free equivariance) is only observable in video.
    Description text is rendered as gr.Markdown in app.py, NOT baked into pixels.
    """
    return base_img.copy()


def load_version_comparison(seed=7):
    """
    V1 — blob artifacts at anatomically correct locations (chin/ear/hair).
    V2 — clean base image (Weight Demodulation fix).
    V3 — clean face identical to V2. Description shown as gr.Markdown in app.py.
         The V2→V3 improvement is NOT visible in still images — only in video.
    """
    try:
        seed = int(seed) % 50
    except Exception:
        seed = 7

    base = get_real_face(seed)

    v1 = (_try_load(os.path.join("assets", "versions", "v1_artifact.png"))
          or _add_blob_artifacts(base.copy()))
    v2 = (_try_load(os.path.join("assets", "versions", "v2_clean.png"))
          or base.copy())
    v3 = (_try_load(os.path.join("assets", "versions", "v3_comparison.png"))
          or _get_v3_clean_face(base))

    _stamp_label(v1, "StyleGAN1 — Blob artifacts  (AdaIN stat encoding)", "#ef4444")
    _stamp_label(v2, "StyleGAN2 — Clean output  (Weight Demodulation)", "#10b981")
    _stamp_label(v3, "StyleGAN3 — Alias-Free GAN  (same still quality as V2)", "#3b82f6")

    return v1, v2, v3

