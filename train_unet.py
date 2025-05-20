
"""
train_unet.py

Launches training using nnU-Net v2 with preset environment variables.
Ensure nnU-Net is installed and configured before running.
"""

import os
import subprocess
from pathlib import Path

# Setup environment variables
BASE_DIR = Path("./dataset/MoNuSeg/TaskCSDS_CancerSegmentation").resolve()
os.environ["nnUNet_raw_data_base"] = str(BASE_DIR.parent)
os.environ["nnUNet_preprocessed"] = str(BASE_DIR.parent / "preprocessed")
os.environ["RESULTS_FOLDER"] = str(BASE_DIR.parent / "results")

# Optional: Show where things are being stored
print("Environment Setup:")
print(f"  RAW_DATA: {os.environ['nnUNet_raw_data_base']}")
print(f"  PREPROC : {os.environ['nnUNet_preprocessed']}")
print(f"  RESULTS : {os.environ['RESULTS_FOLDER']}")

# Make sure preprocessing and training folders exist
Path(os.environ["nnUNet_preprocessed"]).mkdir(parents=True, exist_ok=True)
Path(os.environ["RESULTS_FOLDER"]).mkdir(parents=True, exist_ok=True)

# Dataset ID
DATASET_NAME = "TaskCSDS_CancerSegmentation"

# Step 1: Preprocessing
print("\nRunning nnUNetv2 preprocessing...")
subprocess.run([
    "nnUNetv2_plan_and_preprocess",
    "-d", DATASET_NAME,
    "-c", "2d",
    "--verify_dataset_integrity"
], check=True)

# Step 2: Training (fold 0, 2D config)
print("\nStarting training...")
subprocess.run([
    "nnUNetv2_train",
    "-d", DATASET_NAME,
    "-c", "2d",
    "-f", "0"
], check=True)
