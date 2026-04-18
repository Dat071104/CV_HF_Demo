import gradio as gr
import utils
import random

# ─── Theme ────────────────────────────────────────────────────────────────────
theme = gr.themes.Default(
    primary_hue="emerald",
    neutral_hue="zinc",
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "sans-serif"],
).set(
    body_background_fill="#111827",
    block_background_fill="#1f2937",
    block_border_color="#374151",
    block_border_width="1px",
    body_text_color="#f9fafb",
    block_title_text_color="#ffffff",
    block_label_text_color="#d1d5db",
    input_background_fill="#374151",
    input_border_color="#4b5563",
    input_placeholder_color="#9ca3af",
    button_primary_background_fill="#10b981",
    button_primary_background_fill_hover="#059669",
    button_primary_text_color="#ffffff",
    button_secondary_background_fill="#374151",
    button_secondary_background_fill_hover="#4b5563",
    button_secondary_text_color="#f9fafb",
    slider_color="#10b981",
)

css = """
/* ══════════════════════════════════════════
   GLOBAL RESET — dark canvas
══════════════════════════════════════════ */
* { box-sizing: border-box; }

/* ── Body & Wrapper ── */
body, .gradio-container, .main, .wrap {
    background-color: #0f172a !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', ui-sans-serif, sans-serif !important;
}
.gradio-container { border-top: 4px solid #10b981 !important; }

/* ══════════════════════════════════════════
   TAB BAR — large, readable, bright
══════════════════════════════════════════ */
.tab-nav {
    background: #1e293b !important;
    border-bottom: 2px solid #334155 !important;
}
.tab-nav button {
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    color: #94a3b8 !important;
    padding: 12px 16px !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    letter-spacing: 0.01em !important;
    transition: color 0.2s, border-color 0.2s !important;
}
.tab-nav button:hover {
    color: #e2e8f0 !important;
    background: #1e293b !important;
}
.tab-nav button.selected {
    color: #10b981 !important;
    border-bottom: 3px solid #10b981 !important;
    background: #0f172a !important;
}

/* ══════════════════════════════════════════
   BLOCK / PANEL BACKGROUNDS
══════════════════════════════════════════ */
.block, .form, fieldset, .container,
[class*="block"], [class*="panel"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

/* ══════════════════════════════════════════
   HEADINGS & BODY TEXT in Markdown
══════════════════════════════════════════ */
h1, h2, h3, h4, h5, h6 {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
}
p, li, td, th { color: #cbd5e1 !important; }
strong, b { color: #f1f5f9 !important; }
em, i { color: #94a3b8 !important; }

/* Gradio's own markdown wrapper */
.prose, .prose p, .prose li,
.markdown-body, .markdown-body p, .markdown-body li {
    color: #cbd5e1 !important;
}
.prose h1, .prose h2, .prose h3,
.markdown-body h1, .markdown-body h2, .markdown-body h3 {
    color: #f1f5f9 !important;
}
.prose strong, .prose b,
.markdown-body strong, .markdown-body b {
    color: #f1f5f9 !important;
}

/* ── Inline Code Blocks (formula display) ── */
code, .prose code, .markdown-body code,
pre code, .prose pre code {
    background: #0f2942 !important;
    color: #7dd3fc !important;
    border: 1px solid #1e4976 !important;
    border-radius: 5px !important;
    padding: 2px 8px !important;
    font-size: 0.92em !important;
    font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace !important;
}
pre, .prose pre, .markdown-body pre {
    background: #0f2942 !important;
    border: 1px solid #1e4976 !important;
    border-radius: 8px !important;
    padding: 16px !important;
}
pre code {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* ── Blockquotes (demo notes) ── */
blockquote, .prose blockquote, .markdown-body blockquote {
    background: #1a2744 !important;
    border-left: 4px solid #3b82f6 !important;
    color: #93c5fd !important;
    border-radius: 0 6px 6px 0 !important;
    padding: 10px 16px !important;
    margin: 8px 0 !important;
}
blockquote p, blockquote li,
.prose blockquote p, .markdown-body blockquote p {
    color: #93c5fd !important;
}

/* ── Tables ── */
table { width: 100%; border-collapse: collapse; }
th {
    background: #1e3a5f !important;
    color: #7dd3fc !important;
    padding: 10px 14px !important;
    text-align: left !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #2563eb !important;
}
td {
    color: #cbd5e1 !important;
    padding: 9px 14px !important;
    border-bottom: 1px solid #334155 !important;
}
tr:nth-child(even) td { background: #162032 !important; }
tr:hover td { background: #1e3a5f !important; }

/* ══════════════════════════════════════════
   INPUT LABELS — the key visibility fix
══════════════════════════════════════════ */
/* Block-level label above inputs */
label, .label-wrap span, .svelte-1b6s6s0,
[class*="label"] > span,
.block > label > span,
fieldset > label,
.form label span {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

/* ══════════════════════════════════════════
   RADIO BUTTONS — the main bug fix
══════════════════════════════════════════ */
/* Container */
.radio-group, [data-testid="radio-group"],
fieldset[data-testid] {
    background: #162032 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    padding: 6px 8px !important;
}
/* Each radio option row */
.radio-group label,
fieldset label,
[data-testid="radio-group"] label {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 7px !important;
    padding: 10px 14px !important;
    margin: 4px 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    cursor: pointer !important;
    transition: background 0.15s, border-color 0.15s !important;
}
.radio-group label:hover,
fieldset label:hover {
    background: #1e3a5f !important;
    border-color: #3b82f6 !important;
}
/* Radio button label TEXT — the fix for white-on-white */
.radio-group label span,
fieldset label span,
[data-testid="radio-group"] label span,
input[type="radio"] + span,
.wrap span {
    color: #e2e8f0 !important;
    font-size: 0.93rem !important;
    font-weight: 500 !important;
}
/* Selected radio option */
.radio-group input[type="radio"]:checked + span,
fieldset input[type="radio"]:checked ~ span {
    color: #34d399 !important;
    font-weight: 700 !important;
}
/* Radio circle */
input[type="radio"] {
    accent-color: #10b981 !important;
    width: 16px !important;
    height: 16px !important;
}

/* ══════════════════════════════════════════
   NUMBER & TEXT INPUTS
══════════════════════════════════════════ */
input[type="number"], input[type="text"], textarea {
    background: #0f172a !important;
    color: #f1f5f9 !important;
    border: 1px solid #475569 !important;
    border-radius: 7px !important;
    padding: 10px 12px !important;
    font-size: 1rem !important;
}
input[type="number"]:focus,
input[type="text"]:focus,
textarea:focus {
    border-color: #10b981 !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(16,185,129,0.15) !important;
}

/* ══════════════════════════════════════════
   SLIDERS
══════════════════════════════════════════ */
input[type="range"] {
    accent-color: #10b981 !important;
}
input[type="range"]::-webkit-slider-runnable-track {
    background: #334155 !important;
    height: 4px !important;
    border-radius: 2px !important;
}
input[type="range"]::-webkit-slider-thumb {
    background: #10b981 !important;
    border: 2px solid #0f172a !important;
    width: 18px !important;
    height: 18px !important;
    border-radius: 50% !important;
}

/* ══════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════ */
button.primary, .btn-primary, [variant="primary"] {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(16,185,129,0.3) !important;
    transition: all 0.2s !important;
}
button.primary:hover, [variant="primary"]:hover {
    box-shadow: 0 4px 20px rgba(16,185,129,0.5) !important;
    filter: brightness(1.08) !important;
}
button.secondary, [variant="secondary"] {
    background: #1e293b !important;
    color: #94a3b8 !important;
    border: 1px solid #475569 !important;
    border-radius: 8px !important;
}
button.secondary:hover, [variant="secondary"]:hover {
    background: #334155 !important;
    color: #e2e8f0 !important;
    border-color: #94a3b8 !important;
}

/* ══════════════════════════════════════════
   IMAGES
══════════════════════════════════════════ */
.image-container img, .image-wrap img {
    border-radius: 10px !important;
    border: 2px solid #334155 !important;
}
/* Image upload area */
.upload-container, [data-testid="image"] {
    background: #162032 !important;
    border: 2px dashed #475569 !important;
    border-radius: 10px !important;
}

/* ══════════════════════════════════════════
   CARD COMPONENT
══════════════════════════════════════════ */
.card {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    padding: 22px !important;
    margin-bottom: 16px !important;
}

/* ══════════════════════════════════════════
   PRESENTER BIG BUTTON
══════════════════════════════════════════ */
.big-button {
    font-size: 1.4rem !important;
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 0 28px rgba(16,185,129,0.45) !important;
    letter-spacing: 0.03em !important;
}

/* ══════════════════════════════════════════
   DROPDOWN
══════════════════════════════════════════ */
.drop-shadow, [data-testid="dropdown"],
select, .svelte-select {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #475569 !important;
}

/* ══════════════════════════════════════════
   GRADIO INTERNAL — Misc fixes
══════════════════════════════════════════ */
/* Slider value display */
.slider-value, .number-value { color: #10b981 !important; font-weight: 700 !important; }
/* Info / description text below inputs */
.info, .description { color: #64748b !important; font-size: 0.8rem !important; }
/* Footer / watermark */
footer { display: none !important; }
"""

# ─── Module-level helpers for Gradio event handlers ───────────────────────────

def _random_seed_0_49():
    """FIX-1: Random seed clamped to 0–49 matching the 50-face asset pool."""
    return random.randint(0, 49)

def _load_default_versions():
    return utils.load_version_comparison(7)

def _quick_mix(seed_a, seed_b):
    return utils.style_mix(seed_a, seed_b, "Coarse (Bone/Pose · layers 4–8px)")

# ─── App ───────────────────────────────────────────────────────────────────────
with gr.Blocks(title="StyleGAN Architecture Lab") as demo:

    gr.Markdown(
        """<div style="text-align:center; padding:24px 0 8px;">
            <h1 style="font-size:2.2rem; font-weight:800; color:#10b981; margin:0;">
                🧠 StyleGAN: Latent Architecture Lab
            </h1>
            <p style="font-size:1.1rem; color:#9ca3af; margin-top:8px;">
                Interactive Hybrid Synthesis Engine &nbsp;·&nbsp; Presentation Edition
            </p>
        </div>"""
    )

    with gr.Tabs():

        # ── Tab 1 · Synthesizer ───────────────────────────────────────────────
        with gr.TabItem("1 · Synthesizer"):
            gr.Markdown(
                "## 🎲 Face Synthesis from Latent Space\n\n"
                "Each seed samples a unique point in 512-dimensional **Z-space**. "
                "The 8-layer mapping network projects Z → **W-space**, "
                "then the synthesis network renders the face at progressive resolutions."
            )
            with gr.Row():
                with gr.Column(scale=4):
                    # FIX-1: max=49 enforced in the UI
                    seed_input = gr.Number(
                        label="Latent Seed (0 – 49)", value=7,
                        precision=0, minimum=0, maximum=49
                    )
                    with gr.Row():
                        btn_generate = gr.Button("▶  Generate Face", variant="primary")
                        # FIX-1: random must use 0–49
                        btn_random   = gr.Button("🎲  Random Seed (0–49)")

                    gr.Markdown("---\n### 🎛️ A+1 — Stochastic Noise B Demo")
                    gr.Markdown(
                        "StyleGAN adds independent per-layer random noise **B ~ N(0,I)** "
                        "after each AdaIN operation.  \n"
                        "**W controls identity** (pose, shape, color) — the same across all 3.  \n"
                        "**B controls stochastic detail** (hair strands, skin texture, pore placement).  \n"
                        "This is unique to StyleGAN — no prior GAN had this separation."
                    )
                    btn_noise = gr.Button(
                        "🎲  Re-roll Noise Only  (same W identity, different B)",
                        variant="secondary"
                    )

                with gr.Column(scale=5):
                    preview_gen = gr.Image(
                        label="Synthesized Face", type="pil",
                        elem_classes=["image-container"]
                    )
                    # FIX-1: label shows Seed → Face mapping
                    seed_label = gr.Markdown("*Generate a face to see seed mapping.*")

            gr.Markdown("**Same W-code (identity), three different noise B samples:**")
            with gr.Row():
                noise1 = gr.Image(label="B variant 1 — hair/skin differ", type="pil",
                                   height=230, elem_classes=["image-container"])
                noise2 = gr.Image(label="B variant 2 — hair/skin differ", type="pil",
                                   height=230, elem_classes=["image-container"])
                noise3 = gr.Image(label="B variant 3 — hair/skin differ", type="pil",
                                   height=230, elem_classes=["image-container"])

            gr.Markdown(
                "> **Key insight:** If you covered the label, could you tell these apart?  \n"
                "> Probably not — because W is the same. Only fine stochastic details differ.  \n"
                "> This proves B and W are truly independent control signals."
            )

            # FIX-1: both buttons use 0–49 range
            btn_generate.click(fn=utils.generate_face, inputs=seed_input,
                               outputs=[preview_gen, seed_label])
            btn_random.click(fn=_random_seed_0_49, outputs=seed_input).then(
                fn=utils.generate_face, inputs=seed_input,
                outputs=[preview_gen, seed_label]
            )
            btn_noise.click(fn=utils.noise_variants_wrapper, inputs=seed_input,
                            outputs=[noise1, noise2, noise3])

        # ── Tab 2 · Truncation Trick ──────────────────────────────────────────
        with gr.TabItem("2 · Truncation Trick"):
            # FIX-2: Formula displayed prominently
            gr.Markdown(
                "## ✂️ The Truncation Trick (ψ)\n\n"
                "**Formula:** `w' = w̄ + ψ(w − w̄)`  \n"
                "— ψ = 0 → dataset mean face, ψ = 1 → free untruncated sample, "
                "ψ > 1 → extrapolation beyond training distribution  \n\n"
                "Truncating toward the mean **w̄** enforces photorealism at the cost of diversity.  \n"
                "NVIDIA uses **ψ = 0.7** for all published face results."
            )
            with gr.Row():
                with gr.Column():
                    t_seed = gr.Number(label="Seed (0–49)", value=7, precision=0,
                                       minimum=0, maximum=49)
                    t_psi  = gr.Slider(0.0, 1.5, value=0.7, step=0.05,
                                       label="ψ  (0.0 = dataset mean  →  1.5 = extrapolation)")
                    gr.Markdown(
                        "| ψ range | Zone | Effect |\n"
                        "|---------|------|--------|\n"
                        "| 0.0 – 0.5 | Safe | Close to mean, generic but artifact-free |\n"
                        "| 0.5 – 1.0 | Sweet spot | NVIDIA default — balanced quality/diversity |\n"
                        "| 1.0 – 1.5 | Wild | Extrapolation — unusual features, artifact risk |"
                    )
                    btn_trunc = gr.Button("▶  Apply Truncation", variant="primary")
                with gr.Column():
                    t_preview = gr.Image(label="Truncated Render", type="pil",
                                         elem_classes=["image-container"])
                    # FIX-2: disclosure label shown under image
                    t_label = gr.Markdown("*Adjust ψ and press Apply.*")

            btn_trunc.click(fn=utils.truncate, inputs=[t_seed, t_psi],
                            outputs=[t_preview, t_label])
            t_psi.release(fn=utils.truncate, inputs=[t_seed, t_psi],
                          outputs=[t_preview, t_label])
            t_seed.change(fn=utils.truncate, inputs=[t_seed, t_psi],
                          outputs=[t_preview, t_label])

        # ── Tab 3 · Style Mixing ──────────────────────────────────────────────
        with gr.TabItem("3 · Style Mixing"):
            # FIX-3 + A+2: AdaIN formula in header
            gr.Markdown(
                "## 🎨 Layer-Level Disentanglement\n\n"
                "StyleGAN injects style at **every synthesis layer** via AdaIN:  \n"
                "`AdaIN(x, y) = y_s · (x − μ(x))/σ(x) + y_b`  \n"
                "where **y_s** (scale) and **y_b** (bias) are computed from W-space "
                "via a learned affine transform A **— not learned directly from data.**  \n\n"
                "- **Coarse layers (4–8px):** control pose, head shape, face orientation  \n"
                "- **Middle layers (16–32px):** control hair style, facial structure  \n"
                "- **Fine layers (64–1024px):** control color, skin texture, pores  \n\n"
                "Mixing coarse from one person and fine from another → Figure 3, Karras et al. CVPR 2019."
            )
            with gr.Row():
                sm_a = gr.Number(label="Seed A — Structure source (0–49)", value=10,
                                  minimum=0, maximum=49)
                sm_b = gr.Number(label="Seed B — Style source (0–49)",     value=28,
                                  minimum=0, maximum=49)
            sm_mode = gr.Radio(
                ["Coarse (Bone/Pose · layers 4–8px)",
                 "Middle (Facial Layout · layers 16–32px)",
                 "Fine (Color/Texture · layers 64–1024px)"],
                value="Coarse (Bone/Pose · layers 4–8px)",
                label="Which layers to inject from Seed B"
            )
            btn_mix = gr.Button("▶  Execute Style Mix", variant="primary")
            gr.Markdown(
                "**Result layout:** `[ Seed A — coarse source ] | [ Mixed ] | [ Seed B — fine source ]`"
            )
            sm_preview    = gr.Image(label="Style Mix Result", type="pil",
                                      elem_classes=["image-container"])
            # FIX-3: disclosure label
            sm_disclosure = gr.Markdown("")

            btn_mix.click(fn=utils.style_mix, inputs=[sm_a, sm_b, sm_mode],
                          outputs=[sm_preview, sm_disclosure])

        # ── Tab 4 · Latent Interpolation ──────────────────────────────────────
        with gr.TabItem("4 · Interpolation"):
            gr.Markdown(
                "## 🔀 W-Space Latent Traversal\n\n"
                "True interpolation: **w_mid = (1−α)·w_A + α·w_B** → StyleGAN synthesis → realistic face.  \n"
                "The mapping network disentangles W-space so straight-line paths stay inside the image manifold.  \n"
                "**Low PPL** confirms this path is perceptually smooth — no jarring identity jumps.  \n\n"
                "PPL definition: E[d(G(lerp(w_A, w_A+ε)), G(lerp(w_A, w_B, t+ε)))/ε²]"
            )
            with gr.Row():
                with gr.Column():
                    i_a    = gr.Number(label="Origin Seed (α=0.0, 0–49)", value=5,
                                        minimum=0, maximum=49)
                    i_b    = gr.Number(label="Target Seed (α=1.0, 0–49)", value=22,
                                        minimum=0, maximum=49)
                    i_alpha = gr.Slider(0.0, 1.0, value=0.5, step=0.05,
                                        label="α — Position along interpolation path")
                    btn_interp = gr.Button("▶  Render Frame", variant="primary")
                with gr.Column():
                    i_preview    = gr.Image(label="Interpolated Frame", type="pil",
                                             elem_classes=["image-container"])
                    # FIX-4: disclosure label under output
                    i_disclosure = gr.Markdown("")

            gr.Markdown("### True W-Space Interpolation Reference")
            gr.Markdown(
                "If `assets/interpolation/interp_strip.png` is present, "
                "click below to load a pre-computed 5-frame strip showing true W-space interpolation output."
            )
            btn_load_strip  = gr.Button("Load Pre-Computed Reference Strip", variant="secondary")
            interp_strip_img = gr.Image(
                label="True W-space interpolation — pre-computed reference (5 frames)",
                type="pil", elem_classes=["image-container"]
            )

            btn_interp.click(fn=utils.interpolate, inputs=[i_a, i_b, i_alpha],
                             outputs=[i_preview, i_disclosure])
            i_alpha.release(fn=utils.interpolate, inputs=[i_a, i_b, i_alpha],
                            outputs=[i_preview, i_disclosure])
            btn_load_strip.click(fn=utils.load_interp_strip, outputs=interp_strip_img)

        # ── Tab 5 · GAN Inversion ─────────────────────────────────────────────
        with gr.TabItem("5 · GAN Inversion"):
            # FIX-5: Text says "simulation" — no claim of actual projection
            gr.Markdown(
                "## 💉 Semantic Editing via W+ Space\n\n"
                "Upload a face photo to explore semantic editing concepts.  \n\n"
                "> ⚙️ **Demo note:** This demo applies image-space transforms as a "
                "**simulation** of semantic steering.  \n"
                "> In a production system, a feed-forward encoder (pSp / e4e) first projects "
                "the photo into **W+ space (18×512 = 9,216 dims)** by minimising "
                "LPIPS perceptual loss + pixel MSE — no iterative optimization at inference.  \n"
                "> Semantic editing then adds pre-computed direction vectors:  \n"
                "> **w'⁺ = w⁺ + α · d_semantic** (InterfaceGAN, Shen et al. CVPR 2020)"
            )
            # FIX-5: W vs W+ comparison card
            with gr.Row():
                with gr.Column(elem_classes=["card"]):
                    gr.Markdown(
                        "### W-Space vs W+-Space\n\n"
                        "| Space | Dimensions | Description |\n"
                        "|-------|-----------|-------------|\n"
                        "| **W** | 512 | One shared vector broadcast identically to all 18 layers |\n"
                        "| **W+** | 18 × 512 = **9,216** | One independent vector *per synthesis layer* |\n\n"
                        "W+ has ~18× more capacity than W → can faithfully encode fine real-face "
                        "details that a single shared vector cannot represent.  \n"
                        "References: **pSp** (Richardson et al., CVPR 2021), "
                        "**e4e** (Tov et al., SIGGRAPH 2021)"
                    )
            with gr.Row():
                with gr.Column():
                    inv_upload    = gr.Image(label="📷  Upload Face Photo", type="pil")
                    inv_type      = gr.Radio(
                        ["Age", "Smile", "Lighting / Sharpness"],
                        label="Semantic Direction  (simulated via image transforms)",
                        value="Age"
                    )
                    inv_intensity = gr.Slider(-1.0, 1.0, value=0.0, step=0.1,
                                              label="Intensity  (← negative  ·  positive →)")
                    btn_invert = gr.Button("▶  Apply Simulated Edit", variant="primary")
                with gr.Column():
                    inv_result = gr.Image(
                        label="Simulated Steered Output  (image transforms, not GAN projection)",
                        type="pil", elem_classes=["image-container"]
                    )

            btn_invert.click(fn=utils.invert_and_edit,
                             inputs=[inv_upload, inv_type, inv_intensity],
                             outputs=inv_result)
            inv_intensity.release(fn=utils.invert_and_edit,
                                  inputs=[inv_upload, inv_type, inv_intensity],
                                  outputs=inv_result)

        # ── Tab 6 · V1 vs V2 vs V3 ───────────────────────────────────────────
        with gr.TabItem("6 · V1 vs V2 vs V3"):
            gr.Markdown("## 🏛️ Architecture Evolution")
            with gr.Row():
                with gr.Column(elem_classes=["card"]):
                    gr.Markdown(
                        "### StyleGAN 1  (CVPR 2019)\n\n"
                        "**Root cause:** AdaIN normalizes each feature map channel to zero mean "
                        "and unit variance — destroying absolute magnitude information.  \n"
                        "Generator learns a workaround: re-encodes lost statistics as "
                        "spatially localized blobs.  \n"
                        "**Water-droplet artifacts** appear at **chin, ear boundaries, hair "
                        "regions** — in flat-colour areas at 64px+ resolution, not on facial features."
                    )
                with gr.Column(elem_classes=["card"]):
                    gr.Markdown(
                        "### StyleGAN 2  (CVPR 2020)\n\n"
                        "**Fix:** Weight Demodulation — normalize convolution filter *weights* "
                        "**before** each forward pass using style scales s_i:  \n"
                        "`w'_ijk = s_i·w_ijk / √(Σ(s_i·w_ijk)² + ε)`  \n"
                        "Feature map statistics flow unchanged → no blob workaround needed.  \n"
                        "**FID: 4.40 → 2.84** on FFHQ-1024."
                    )
                with gr.Column(elem_classes=["card"]):
                    gr.Markdown(
                        "### StyleGAN 3  (NeurIPS 2021)\n\n"
                        "**Problem:** Texture Sticking — in video, hair/beard/skin textures "
                        "pin to screen pixel coordinates instead of face geometry.  \n"
                        "**Fix:** Alias-Free operations: low-pass filter after every "
                        "non-linearity, continuous-signal-theory-grounded convolutions.  \n"
                        "Achieves **translation and rotation equivariance** — "
                        "textures track face geometry in continuous motion."
                    )

            btn_versions = gr.Button("▶  Load Visual Comparison", variant="primary")
            # FIX-1 consistent: seed also 0–49
            v_seed = gr.Slider(0, 49, value=7, step=1,
                               label="Face seed for V1/V2 comparison (0–49)")
            with gr.Row():
                with gr.Column():
                    v1_img = gr.Image(
                        label="StyleGAN 1 — Blob artifacts at chin/ear/hair boundary",
                        height=400, show_label=True
                    )
                with gr.Column():
                    v2_img = gr.Image(
                        label="StyleGAN 2 — Clean output (Weight Demodulation)",
                        height=400, show_label=True
                    )
                with gr.Column():
                    v3_img = gr.Image(
                        label="StyleGAN 3 — Alias-Free GAN",
                        height=400, show_label=True
                    )
                    gr.Markdown("""
**StyleGAN3 — Alias-Free GAN (NeurIPS 2021)**

- ⚠️ **V2 bug:** Texture Sticking in video — hair/skin pins to screen pixels, not face geometry
- ✅ **V3 fix:** Low-pass filter after every non-linearity, continuous-signal-theory-grounded convolutions
- → Translation & rotation equivariance
- → Textures track face geometry in continuous motion
- → Same still-image FID as V2. **Innovation is purely in video equivariance.**

*Reference: Karras et al., NeurIPS 2021*
                    """)

            btn_versions.click(fn=utils.load_version_comparison, inputs=v_seed,
                               outputs=[v1_img, v2_img, v3_img])
            v_seed.release(fn=utils.load_version_comparison, inputs=v_seed,
                           outputs=[v1_img, v2_img, v3_img])

        # ── Tab 7 · Metrics & Theory ──────────────────────────────────────────
        with gr.TabItem("7 · Metrics & Theory"):
            gr.Markdown("## 📚 StyleGAN: Theory & Quantitative Evidence")

            # FIX-7: FID/PPL comparison table
            gr.Markdown(
                "### 📊 FID / PPL Benchmark\n\n"
                "| Model | FID ↓ | PPL ↓ | Resolution |\n"
                "|-------|-------|-------|------------|\n"
                "| DCGAN | ~40+ | N/A | 64² |\n"
                "| ProGAN | 8.04 | ~412 | 1024² |\n"
                "| StyleGAN 1 | 4.40 | ~212 | 1024² |\n"
                "| **StyleGAN 2 ★** | **2.84** | **~145** | **1024²** |\n\n"
                "*All FID measured on **FFHQ-1024** using official NVIDIA evaluation code.  \n"
                "FID ↓ = generated distribution closer to real. "
                "PPL ↓ = smoother W-space interpolation path.*"
            )

            with gr.Row():
                # FIX-7: FFHQ dataset card
                with gr.Column(elem_classes=["card"]):
                    gr.Markdown(
                        "### 🗄️ Training Data: FFHQ\n\n"
                        "**Flickr-Faces-HQ (FFHQ)** — 70,000 high-quality 1024×1024 face "
                        "images scraped from Flickr with Creative Commons licences.  \n"
                        "Wide coverage of age, ethnicity, accessories, and expression.  \n\n"
                        "FID 2.84 means StyleGAN2 samples are **statistically near-indistinguishable** "
                        "from FFHQ in InceptionV3 feature space — a remarkable result for a pure generative model.  \n\n"
                        "Subsets: FFHQ-256, FFHQ-512 available for lower-res experiments."
                    )
                with gr.Column(elem_classes=["card"]):
                    gr.Markdown(
                        "### 🧠 Key Architectural Components\n\n"
                        "**Mapping Network (Z → W):**  \n"
                        "8-layer MLP removes topological constraints imposed by Z~N(0,I). "
                        "W is learned to be disentangled — features vary independently.  \n\n"
                        "**AdaIN Style Injection:**  \n"
                        "`AdaIN(x,y) = y_s·(x−μ)/σ + y_b`  ·  y_s, y_b from W via affine A.  \n\n"
                        "**Stochastic Noise B:**  \n"
                        "Per-layer, per-pixel Gaussian noise added after AdaIN. Controls "
                        "hair strands, skin pores, micro-lighting — independent of identity.  \n\n"
                        "**Weight Demodulation (V2):**  \n"
                        "`w'_ijk = s_i·w_ijk / √(Σ(s_i·w_ijk)² + ε)` — normalizes filter "
                        "weights, not feature maps."
                    )

            # A+2: AdaIN step-by-step table
            gr.Markdown(
                "### ⚙️ AdaIN: Step-by-Step\n\n"
                "| Step | Operation | Description |\n"
                "|------|-----------|-------------|\n"
                "| 1 | **x** (raw) | Feature map output from previous conv layer |\n"
                "| 2 | **x_norm = (x − μ(x)) / σ(x)** | Normalize to zero mean, unit variance |\n"
                "| 3 | **x_scaled = y_s · x_norm** | Scale each channel by style scale y_s |\n"
                "| 4 | **x_out = x_scaled + y_b** | Shift each channel by style bias y_b |\n"
                "| 5 | **Output x_out** | Feature map now carries style from W |\n\n"
                "**Critical insight:** y_s and y_b are **not learned directly**.  \n"
                "They are computed from W (512-dim) via a *learned affine transform A* at each layer. "
                "Changing one dimension of W produces correlated style changes across all channels at that layer. "
                "Different layers have different A transforms → different semantic effects at different scales.  \n"
                "Origin: Huang & Belongie, *Arbitrary Style Transfer via AdaIN*, ICCV 2017."
            )

            # FIX-7: Full citation list (A+3)
            gr.Markdown(
                "### 📚 Key References\n\n"
                "1. Karras et al. *A Style-Based Generator Architecture for Generative Adversarial Networks.* CVPR 2019.\n"
                "2. Karras et al. *Analyzing and Improving the Image Quality of StyleGAN.* CVPR 2020.\n"
                "3. Karras et al. *Alias-Free Generative Adversarial Networks (StyleGAN3).* NeurIPS 2021.\n"
                "4. Richardson et al. *Encoding in Style: a StyleGAN Encoder for Image-to-Image Translation (pSp).* CVPR 2021.\n"
                "5. Tov et al. *Designing an Encoder for StyleGAN Image Manipulation (e4e).* SIGGRAPH 2021.\n"
                "6. Huang & Belongie. *Arbitrary Neural Artistic Stylization via AdaIN.* ICCV 2017.\n"
                "7. Shen et al. *Interpreting the Latent Space of GANs for Semantic Face Editing (InterfaceGAN).* CVPR 2020."
            )

        # ── Tab 8 · Presenter Mode ────────────────────────────────────────────
        with gr.TabItem("8 · Presenter Mode"):
            gr.Markdown(
                "<div style='text-align:center; padding:16px 0 8px;'>"
                "<h1 style='color:#10b981; font-size:2rem; font-weight:800;'>🎤 Live Presenter Sandbox</h1>"
                "<p style='color:#9ca3af; font-size:1rem;'>Distraction-free · Full-screen optimized</p>"
                "</div>"
            )

            # FIX-8: Recommended narrative arc table with stage labels
            gr.Markdown(
                "### 📋 Recommended 7-Minute Presentation Arc\n\n"
                "| Time | Stage | Tab | Key phrase |\n"
                "|------|-------|-----|------------|\n"
                "| 0:00 – 0:40 | **[Hook]** | **1 · Synthesizer** | *'These faces never existed — each seed is a coordinate in 512-D space'* |\n"
                "| 0:40 – 1:30 | **[Core insight]** | **3 · Style Mixing** | *'This is proof of disentanglement — coarse and fine are separated'* |\n"
                "| 1:30 – 2:20 | **[Consequence]** | **4 · Interpolation** | *'Because W is disentangled, traversal stays smooth'* |\n"
                "| 2:20 – 3:10 | **[Application]** | **5 · GAN Inversion** | *'Can we do this with YOUR face? Yes — via W+ encoding'* |\n"
                "| 3:10 – 4:00 | **[Evolution]** | **6 · V1→V2→V3** | *'Even NVIDIA had bugs to fix — here's how they did it'* |\n"
                "| 4:00 – 4:45 | **[Math]** | **2 · Truncation** | *'The quality dial: w\\' = w̄ + ψ(w − w̄)'* |\n"
                "| 4:45 – 7:00 | **[Evidence + Q&A]** | **7 · Metrics** | *'FID 2.84 vs ProGAN 8.04 — leave this table visible during Q&A'* |\n\n"
                "---"
            )

            # Big face generator (primary presenter control)
            gr.Markdown("### ⚡ [Hook] Face Generator")
            with gr.Row():
                p_seed = gr.Number(label="Seed (0–49)", value=7,
                                    minimum=0, maximum=49, scale=1)
                p_btn  = gr.Button("▶  GENERATE FACE", variant="primary",
                                    scale=2, elem_classes=["big-button"])
            p_img   = gr.Image(label="Output", elem_classes=["image-container"],
                                type="pil", height=480)
            p_label = gr.Markdown("")

            p_btn.click(fn=utils.generate_face, inputs=p_seed,
                        outputs=[p_img, p_label])

            # Quick style mix (presenter can skip to Tab 3 concept inline)
            gr.Markdown("---\n### 🎨 [Core insight] Quick Style Mix")
            with gr.Row():
                qm_a   = gr.Number(label="Seed A", value=5,  minimum=0, maximum=49, scale=1)
                qm_b   = gr.Number(label="Seed B", value=22, minimum=0, maximum=49, scale=1)
                qm_btn = gr.Button("🎨  Style Mix (Coarse)", variant="secondary", scale=2)
            qm_out  = gr.Image(label="[ A pose ] | [ Mixed ] | [ B texture ]",
                                type="pil", height=300, elem_classes=["image-container"])
            qm_disc = gr.Markdown("")

            qm_btn.click(fn=_quick_mix, inputs=[qm_a, qm_b],
                         outputs=[qm_out, qm_disc])

            # Quick version comparison (presenter can demo evolution inline)
            gr.Markdown("---\n### 🏛️ [Evolution] Quick V1 vs V2 vs V3")
            qv_btn = gr.Button("🏛️  Show V1 / V2 / V3 Comparison  (seed 7)", variant="secondary")
            with gr.Row():
                qv1 = gr.Image(label="V1 — Artifact", type="pil", height=260)
                qv2 = gr.Image(label="V2 — Clean",    type="pil", height=260)
                qv3 = gr.Image(label="V3 — Card",     type="pil", height=260)

            qv_btn.click(fn=_load_default_versions, outputs=[qv1, qv2, qv3])

# ─── Launch ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        theme=theme,
        css=css,
    )
