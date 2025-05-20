"""
prepare_data.py

Prepares the MoNuSeg dataset for training with nnU-Net by converting:
- TIFF images to NIfTI format
- XML annotations to distance maps (also in NIfTI format)

It processes both training and test data, and automatically creates the output
directories and the dataset.json file required by nnU-Net.

Expected input folder structure:
dataset/MoNuSeg/
|--- imagesTr/    # Training images (.tif)
|--- labelsTr/    # Training annotations (.xml)
|--- imagesTs/    # Test images (.tif) AND test annotations (.xml)
"""

import os
import json
import numpy as np
import cv2
import nibabel as nib
from PIL import Image
import xml.etree.ElementTree as ET
from pathlib import Path

# --- Configuration ---
DATASET_NAME = "TaskCSDS_CancerSegmentation"
DATASET_DIR = Path("dataset/MoNuSeg")
OUTPUT_DIR = DATASET_DIR / DATASET_NAME

# Ensure necessary directories exist
for subdir in ["imagesTr", "imagesTs", "labelsTr", "labelsTs"]:
    (OUTPUT_DIR / subdir).mkdir(parents=True, exist_ok=True)

def create_binary_mask(xml_file, image_size):
    mask = np.zeros(image_size, dtype=np.uint8)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for region in root.findall('.//Region'):
        vertices = []
        for vertex in region.find("Vertices").findall("Vertex"):
            x = int(float(vertex.attrib["X"]))
            y = int(float(vertex.attrib["Y"]))
            vertices.append([x, y])
        vertices = np.array([vertices], dtype=np.int32)
        cv2.fillPoly(mask, vertices, 1)
    return mask

def create_distance_map(binary_mask):
    dist = cv2.distanceTransform(binary_mask.astype(np.uint8), cv2.DIST_L2, 5)
    return (dist - np.min(dist)) / (np.max(dist) - np.min(dist) + 1e-8)

def convert_images_and_labels():
    image_size = (1000, 1000)

    print("Converting training images...")
    for tif in (DATASET_DIR / "imagesTr").glob("*.tif"):
        img = Image.open(tif)
        img_np = np.array(img)[..., None]
        nii = nib.Nifti1Image(img_np, affine=np.eye(4))
        nib.save(nii, OUTPUT_DIR / "imagesTr" / (tif.stem + ".nii.gz"))

    print("Converting training labels...")
    for xml in (DATASET_DIR / "labelsTr").glob("*.xml"):
        mask = create_binary_mask(xml, image_size)
        dist_map = create_distance_map(mask)
        nii = nib.Nifti1Image(dist_map, affine=np.eye(4))
        nib.save(nii, OUTPUT_DIR / "labelsTr" / (xml.stem + ".nii.gz"))

    print("Converting testing images...")
    for tif in (DATASET_DIR / "imagesTs").glob("*.tif"):
        img = Image.open(tif)
        img_np = np.array(img)[..., None]
        nii = nib.Nifti1Image(img_np, affine=np.eye(4))
        nib.save(nii, OUTPUT_DIR / "imagesTs" / (tif.stem + ".nii.gz"))

    print("Converting testing labels...")
    for xml in (DATASET_DIR / "imagesTs").glob("*.xml"):
        mask = create_binary_mask(xml, image_size)
        dist_map = create_distance_map(mask)
        nii = nib.Nifti1Image(dist_map, affine=np.eye(4))
        nib.save(nii, OUTPUT_DIR / "labelsTs" / (xml.stem + ".nii.gz"))

def generate_dataset_json():
    training = []
    for img_file in sorted((OUTPUT_DIR / "imagesTr").glob("*.nii.gz")):
        case_id = img_file.stem
        training.append({
            "image": f"./imagesTr/{case_id}.nii.gz",
            "label": f"./labelsTr/{case_id}.nii.gz"
        })

    test = [f"./imagesTs/{p.stem}.nii.gz" for p in (OUTPUT_DIR / "imagesTs").glob("*.nii.gz")]

    dataset_json = {
        "name": DATASET_NAME,
        "description": "Segmentation task for cancer nuclei using distance maps.",
        "reference": "",
        "licence": "",
        "release": "1.0",
        "modality": {"0": "RGB"},
        "labels": {"0": "background", "1": "nuclei"},
        "numTraining": len(training),
        "numTest": len(test),
        "training": training,
        "test": test
    }

    with open(OUTPUT_DIR / "dataset.json", 'w') as f:
        json.dump(dataset_json, f, indent=4)
    print("dataset.json generated.")

if __name__ == "__main__":
    convert_images_and_labels()
    generate_dataset_json()
