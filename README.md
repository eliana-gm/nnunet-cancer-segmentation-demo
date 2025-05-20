
# Cancer Nuclei Segmentation using nnU-Net

This project demonstrates **nuclear segmentation on histopathological images** using the [nnU-Net](https://github.com/MIC-DKFZ/nnUNet), a powerful self-configuring deep learning model for biomedical image segmentation. Built as part of an academic research project, this codebase is tailored to highlight machine learning, image processing, and medical data preparation — aligned with real-world healthcare AI workflows.

## Summary

- **Dataset:** MoNuSeg 2018 (multi-organ nuclei segmentation)
- **Goal:** Segment cell nuclei in H&E-stained histopathology images
- **Model:** nnU-Net 2D (ensemble with Dice = 0.86)
- **Pipeline:** TIFF + XML → NIfTI conversion → nnUNet training → Evaluation

## Structure

```txt
nnunet-cancer-segmentation-demo/
├── prepare_data.py # Converts raw MoNuSeg images + XML to NIfTI
├── train_unet.py # Launches nnUNet preprocessing + training
├── requirements.txt # Python dependencies
├── dataset/
│ ├── MoNuSeg/ # Place your dataset here
│ └── README.md # Instructions for dataset setup
├── gui/
│ └── viewer.py # PyQt5 GUI for viewing image + mask overlays
├── assets/ # Add sample predictions, masks, screenshots here
└── README.md # This file
```

## How-To: Quickstart

### 1. Clone & install dependencies

```bash
git clone https://github.com/yourusername/nnunet-cancer-segmentation-demo.git
cd nnunet-cancer-segmentation-demo
pip install -r requirements.txt
```

### 2. Prepare the dataset

- Download the **MoNuSeg 2018 dataset** from [site](https://monuseg.grand-challenge.org/Data/)

- Place files in the following structure:

dataset/MoNuSeg/
|-- imagesTr/    # Training .tif images
|-- labelsTr/    # Corresponding .xml annotation files
├-- imagesTs/    # Test .tif images

Then run:

```bash

python prepare_data.py

```

---

### 3. Train the model

Make sure [nnU-Net v2](https://github.com/MIC-DKFZ/nnUNet) is installed and then:

```bash
python train_unet.py
```

This will:
- Set up environment variables
- Preprocess data
- Train on fold 0 using 2D configuration

---

### 4. Launch the PyQt5 GUI

To interactively view segmentation results with overlays:

```bash
python gui/viewer.py
```

This tool allows you to:
- Load a NIfTI-format image
- Load a predicted mask
- View them side-by-side or as a transparent overlay

## Results

- **Dice score (ensemble):** 0.86
- **IoU score (ensemble):** 0.76
- Visual overlays available in `assets/`

---

## Technologies Used

- Python, PyTorch
- nnU-Net v2
- TIAToolbox (stain normalization)
- OpenCV, Nibabel, PIL
- Medical data formats (TIFF, XML, NIfTI)

---

## Relevance to Medical Imaging & AI Roles

This project demonstrates:

- A **complete pipeline** covering data preprocessing, model training, and result evaluation for biomedical image segmentation
- Experience with **common medical formats** (TIFF, NIfTI, XML) and domain-specific workflows
- Practical understanding of **2D segmentation models**, distance maps, and performance tuning
- Clean, modular Python code designed for **collaboration and reproducibility**
- Alignment with real-world challenges in **clinical diagnostics, research, and health tech**


---

## References/Credit

- [MoNuSeg Challenge 2018](https://monuseg.grand-challenge.org/)
- [nnU-Net authors (Isensee et al.)](https://arxiv.org/abs/1809.10486)
- Code and results by *Eliana Matos (Fall 2024)*

---

## Contact

Reach out on GitHub or via email for collaboration, questions, or code review.
