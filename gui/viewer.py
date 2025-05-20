
"""
viewer.py

Simple PyQt5 GUI for loading and visualizing medical images and segmentation masks (NIfTI).
"""

import sys
import nibabel as nib
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import tempfile
import os

class NiftiViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NIfTI Image + Mask Viewer")
        self.image_data = None
        self.mask_data = None

        # Widgets
        self.img_label = QLabel("Image not loaded")
        self.load_img_btn = QPushButton("Load Image (.nii.gz)")
        self.load_mask_btn = QPushButton("Load Mask (.nii.gz)")
        self.overlay_btn = QPushButton("Show Overlay")

        self.load_img_btn.clicked.connect(self.load_image)
        self.load_mask_btn.clicked.connect(self.load_mask)
        self.overlay_btn.clicked.connect(self.show_overlay)

        layout = QVBoxLayout()
        layout.addWidget(self.img_label)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.load_img_btn)
        btn_layout.addWidget(self.load_mask_btn)
        btn_layout.addWidget(self.overlay_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open NIfTI Image", "", "NIfTI Files (*.nii *.nii.gz)")
        if path:
            img = nib.load(path).get_fdata()
            self.image_data = img[..., 0] if img.ndim == 3 else img
            self.display_image(self.image_data, "gray")

    def load_mask(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open NIfTI Mask", "", "NIfTI Files (*.nii *.nii.gz)")
        if path:
            mask = nib.load(path).get_fdata()
            self.mask_data = mask[..., 0] if mask.ndim == 3 else mask
            self.display_image(self.mask_data, "Reds")

    def show_overlay(self):
        if self.image_data is None or self.mask_data is None:
            self.img_label.setText("Load both image and mask.")
            return
        overlay = np.ma.masked_where(self.mask_data <= 0, self.mask_data)
        fig, ax = plt.subplots()
        ax.imshow(self.image_data, cmap="gray")
        ax.imshow(overlay, cmap="Reds", alpha=0.5)
        ax.axis("off")

        # Save temp image to show in QLabel
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            fig.savefig(tmp.name, bbox_inches="tight", pad_inches=0)
            tmp_path = tmp.name
        plt.close(fig)

        self.set_label_pixmap(tmp_path)
        os.remove(tmp_path)

    def display_image(self, array, cmap="gray"):
        fig, ax = plt.subplots()
        ax.imshow(array, cmap=cmap)
        ax.axis("off")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            fig.savefig(tmp.name, bbox_inches="tight", pad_inches=0)
            tmp_path = tmp.name
        plt.close(fig)

        self.set_label_pixmap(tmp_path)
        os.remove(tmp_path)

    def set_label_pixmap(self, image_path):
        image = QImage(image_path)
        pixmap = QPixmap.fromImage(image)
        self.img_label.setPixmap(pixmap.scaled(512, 512))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = NiftiViewer()
    viewer.resize(600, 600)
    viewer.show()
    sys.exit(app.exec_())
