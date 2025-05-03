import os
import sys
import openslide
import argparse
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(PROJECT_ROOT)
  
def process_classification_report(report_path, output_csv_path):
    import json
    import csv

    with open(report_path) as f:
        data = json.load(f)

    with open(output_csv_path, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["case_id", "primary_diagnosis"])

        for case in data:
            case_id = case.get("submitter_id")
            diagnoses = case.get("diagnoses", [])
            if diagnoses:
                diagnosis = diagnoses[0].get("primary_diagnosis", "N/A")
                writer.writerow([case_id, diagnosis])

    print(f"[INFO] Wrote label CSV to: {output_csv_path}")

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
    csv_label_path = config["CSV_LABEL_PATH"]            # Output CSV

    # Generate classification CSV if missing
    if not os.path.exists(csv_label_path):
        process_classification_report(classification_path, csv_label_path)

    # Load CSV into a DataFrame
    df_labels = pd.read_csv(csv_label_path)
    print(df_labels.head())

    # Print shape for one WSI file
    for filename in os.listdir(wsi_dir):
        if filename.endswith((".svs", ".tif", ".tiff")):
            full_path = os.path.join(wsi_dir, filename)
            get_wsi_shape(full_path)
            break  # Only inspect one WSI for now

    return df_labels

if __name__ == "__main__":
    main()
