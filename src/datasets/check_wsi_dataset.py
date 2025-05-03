import os
import sys
import openslide
import argparse
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(PROJECT_ROOT)
  

def process_classification_report(cls_path, report_dir, output_csv_path):
    import json
    import csv
    import os

    # Load classification JSON
    with open(cls_path) as f:
        data = json.load(f)

    # Prepare output
    with open(output_csv_path, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["image", "label", "caption"])

        for case in data:
            case_id = case.get("submitter_id")
            diagnoses = case.get("diagnoses", [])
            label = diagnoses[0].get("primary_diagnosis", "N/A") if diagnoses else "N/A"

            # Load caption
            annotation_path = os.path.join(report_dir, case_id, "annotations.json")
            if os.path.exists(annotation_path):
                try:
                    with open(annotation_path, "r") as f:
                        ann = json.load(f)
                        caption = ann.get("caption", "")  # Adjust key if needed
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
        print(f"Error reading {wsi_path}: {e}")
        return None
    
def load_config(config_file):
    import yaml
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", default='tcga-brca', type=str)
    args = parser.parse_args()

    # Load dataset configuration
    config = load_config(f"./configs/data/{args.dataset_name}.yaml")
    wsi_dir = config["WSI_DIR"]
    classification_path = config["CLASSIFICATION_PATH"]  # JSON input
    report_dir = config["REPORT_DIR"]                    # report dir 
    csv_label_path = config["CSV_LABEL_PATH"]            # Output CSV

    # Generate classification CSV if missing
    if os.path.exists(csv_label_path): 
        import shutil 
        shutil.rmtree(csv_label_path, ignore_errors=True) 

    # if not os.path.exists(csv_label_path):
    process_classification_report(classification_path, report_dir, csv_label_path)
 
    # Load CSV into a DataFrame
    df_labels = pd.read_csv(csv_label_path)
    print(df_labels.head())
    print("\n[INFO] Unique primary_diagnosis labels:")
    print(df_labels["primary_diagnosis"].dropna().unique())
    print("\n[INFO] Number of unique primary_diagnosis labels:") 
    print(len(df_labels["primary_diagnosis"].dropna().unique()))

    # Print shape for one WSI file
    for filename in os.listdir(wsi_dir):
        if filename.endswith((".svs", ".tif", ".tiff")):
            full_path = os.path.join(wsi_dir, filename)
            get_wsi_shape(full_path)
            break  # Only inspect one WSI for now

    return df_labels

if __name__ == "__main__":
    main()
