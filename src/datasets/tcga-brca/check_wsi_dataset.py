import os
import sys
import argparse
import openslide
import pandas as pd
import json
import csv
import yaml
import random 
from PIL import Image 
# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(PROJECT_ROOT)

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config

def process_classification_report(cls_path, report_dir, output_csv_path):
    # Load classification JSON
    with open(cls_path) as f:
        data = json.load(f)

    # Write combined CSV with image, label, and caption
    with open(output_csv_path, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["image", "label", "caption"])

        for case in data:
            case_id = case.get("submitter_id")
            diagnoses = case.get("diagnoses", [])
            label = diagnoses[0].get("primary_diagnosis", "N/A") if diagnoses else "N/A"

            # Load caption from plain text file
            annotation_path = os.path.join(report_dir, case_id, "annotation")
            if os.path.exists(annotation_path):
                try:
                    with open(annotation_path, "r") as f:
                        caption = f.read().strip()
                except Exception as e:
                    print(f"[WARN] Could not read caption for {case_id}: {e}")
                    caption = ""
            else:
                print(f"[WARN] Annotation not found for {case_id}")
                caption = ""

            writer.writerow([case_id, label, caption])

    print(f"[INFO] Wrote combined CSV to: {output_csv_path}")

def get_wsi_shape(wsi_path):
    try:
        slide = openslide.OpenSlide(wsi_path)
        width, height = slide.dimensions
        print(f"WSI file: {os.path.basename(wsi_path)}")
        print(f"Dimensions (Width x Height): {width} x {height}")
        print(f"Number of levels: {slide.level_count}")
        return width, height
    except Exception as e:
        print(f"[ERROR] Failed to read WSI {wsi_path}: {e}")
        return None





def rescale_and_save_random_wsi(wsi_dir, save_dir, max_size=1024, num_samples=10):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    wsi_extensions = (".svs", ".tif", ".tiff")
    wsi_files = [f for f in os.listdir(wsi_dir) if f.endswith(wsi_extensions)]

    if len(wsi_files) == 0:
        print("[WARN] No WSI files found.")
        return

    selected_files = random.sample(wsi_files, min(num_samples, len(wsi_files)))

    for fname in selected_files:
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

 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", default="tcga-brca", type=str)
    args = parser.parse_args()

    # Load configuration
    config_path = f"./configs/data/{args.dataset_name}.yaml"
    config = load_config(config_path)

    wsi_dir = config["WSI_DIR"]
    classification_path = config["CLASSIFICATION_PATH"]
    report_dir = config["REPORT_DIR"]
    csv_label_path = config["CSV_LABEL_PATH"]
    visualization_dir = config.get("VISUALIZATION_DIR")


    # Remove existing label CSV if it exists
    # if os.path.exists(csv_label_path):
    #     print(f"[INFO] Removing old CSV at {csv_label_path}")
    #     os.remove(csv_label_path)

    # Generate new CSV
    if not os.path.exists(csv_label_path):
        process_classification_report(classification_path, report_dir, csv_label_path)

    # Load CSV into DataFrame
    df_labels = pd.read_csv(csv_label_path)
    print("\n[INFO] Sample rows:")
    print(df_labels.head())

    # Print unique labels
    print("\n[INFO] Unique diagnosis labels:")
    print(df_labels["label"].dropna().unique())
    print(f"[INFO] Total number of unique labels: {df_labels['label'].nunique()}")
     # Count available vs. missing captions
    num_total = len(df_labels)
    num_available = df_labels["caption"].notna() & df_labels["caption"].str.strip().astype(bool)
    num_available = num_available.sum()
    num_missing = num_total - num_available

    print(f"\n[INFO] Captions summary:")
    print(f"  Available reports : {num_available}")
    print(f"  Missing reports   : {num_missing}") 
    wsi_extensions = (".svs", ".tif", ".tiff")
    wsi_files = [f for f in os.listdir(wsi_dir) if f.endswith(wsi_extensions)]
    num_wsi = len(wsi_files)

    # Number of classification entries
    num_classified = len(df_labels)

    print(f"\n[INFO] WSI & Classification Summary:")
    print(f"  WSI files found        : {num_wsi}")
    print(f"  Classification entries : {num_classified}") 
    
    # Print shape info for one WSI
    for filename in os.listdir(wsi_dir):
        if filename.endswith((".svs", ".tif", ".tiff")):
            full_path = os.path.join(wsi_dir, filename)
            get_wsi_shape(full_path)
            break

    rescale_and_save_random_wsi(wsi_dir, visualization_dir, max_size=512, num_samples=10) 

if __name__ == "__main__":
    main()
