# 🌟 StyleGAN Application | Final A+ Presentation Tier

This repository represents the fully finished, robust, production-ready GUI intended for live classroom presentations regarding StyleGAN topologies.

## ✨ The Core Philosophy
This app ditches fake placeholder gradients for **Real Asset Hybrids**. It runs ultra-fast and error-free on typical CPUs and zero-tier Hugging Face Spaces by executing deterministic interpolation and filtering mechanics across a real pool of high-quality pre-generated datasets. 

## 🛠️ Deployment Instructions

### 1. Auto-Fetch Real Face Assets (DO THIS FIRST)
We have included an automated script that securely pulls 50 genuine, highly-realistic GAN-generated faces straight to your local system.

```bash
pip install -r requirements.txt
python downloader.py
```
*Wait ~1 minute for all 50 faces to assemble in your `assets/faces/` directory.*

### 2. Launch Local Sandbox
Once assets are downloaded, simply boot the server:
```bash
python app.py
```
Open `http://localhost:7860` for a gorgeous presentation view.

### 3. Deploy to Hugging Face Spaces (Grading/External Access)
1. In HF Spaces, create a new **Gradio** project.
2. Ensure you have run `python downloader.py` locally!
3. Upload all files **including the `assets` folder that `downloader.py` populated.**
4. HF Spaces will immediately detect the `app.py` root and begin hosting instantly. Because it is optimized for CPU logic with pre-cached assets, it will be incredibly fast.

## ⚠️ Troubleshooting & Resilience
*   **What if Hugging Face deletes my images?** The `utils.py` backend contains a failsafe. If images are totally missing, it won't crash; it automatically substitutes with abstract mathematical placeholder matrices so the presentation can continue.
*   **How do I replace faces?** Just go into `assets/faces/` and drag in your own `000.png` -> `049.png` sequences.
*   **Dependencies failing?** Ensure you are on Python 3.10 to 3.13.

## 🎓 The Offline Backup Strategy
*Always do this the night before.*
Open the local demo (`localhost:7860`), start OBS or Mac Screen Recording, and talk through the demo while recording. Upload this video file to Google Drive and keep a copy on your desktop. If the university wifi collapses entirely, play the video in VLC player and talk over it.
