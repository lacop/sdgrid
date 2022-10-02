# Stable Diffusion Image Grid

Source for https://sdgrid.lacop.dev/ - an experiment showing a large collection of Stable Diffusion images.

~Shamelessly stolen~ Heavily inspired by https://generrated.com/.

## Instructions

This is a collection of scripts held together by duct tape, but it works fine for this one-off experiment. To generate more images (or recreate the whole thing from scratch):

1. Setup Stable Diffusion.
   
   Specifically this is using https://github.com/AUTOMATIC1111/stable-diffusion-webui at `3f417566b0bda8eab05d247567aebf001c1d1725`. Fetch the same version if you want reproducible results.
1. Pull this repo.
1. Edit `inputs/topics.csv` and `inputs/styles.csv` as you like.
1. Start up the SD webui (`python launch.py`) and start generating missing images:
   ```
   python scripts/dream.py
   ```
   Adjust env vars as needed. The script will check the output directory for any
   existing images and skip generating those, so if you add a few more styles to
   `styles.csv` it will only do the neccessary work.
1. Generate the webpage. You can do this while the images are being generated.
   ```
   python scripts/generate_webpage.py
   API_KEY=... LOCAL_HTML_DIR=html ./scripts/upload.py
   ```
1. Convert the results to jpg and generate thumbnails. Upload the results to CDN.
   
   ```
   ./scripts/prepare_images.sh
   API_KEY=... LOCAL_IMAGE_DIR=images ./scripts/upload.py
   ```

   This assumes you use [Bunny CDN](https://bunny.net) which I picked for no
   particular reason.