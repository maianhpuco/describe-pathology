from PIL import Image

def rescale_and_save_wsi(wsi_dir, save_dir, max_size=1024):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    wsi_extensions = (".svs", ".tif", ".tiff")
    wsi_files = [f for f in os.listdir(wsi_dir) if f.endswith(wsi_extensions)]

    for fname in wsi_files:
        wsi_path = os.path.join(wsi_dir, fname)
        try:
            slide = openslide.OpenSlide(wsi_path)

            # Use level with biggest downsample (lowest resolution)
            level = slide.get_best_level_for_downsample(32)
            img = slide.read_region((0, 0), level, slide.level_dimensions[level])
            img = img.convert("RGB")

            # Resize for visualization (keep aspect ratio)
            img.thumbnail((max_size, max_size), Image.LANCZOS)

            # Save as PNG
            save_path = os.path.join(save_dir, f"{os.path.splitext(fname)[0]}.png")
            img.save(save_path)
            print(f"[INFO] Saved resized image: {save_path}")

        except Exception as e:
            print(f"[ERROR] Failed to process {fname}: {e}")
