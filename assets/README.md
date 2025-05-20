## Results Summary

### Performance Across Folds vs. Ensemble

![Performance Metrics](assets/performance_metrics.png)

> **Note:** Due to the resolution of the original figure from the research report, some graph text may appear small or poorly legible on screen. Please refer to the summary below for key performance values, the figure description in the performance_metrics.png file itself, or open the image in a new tab to zoom in.

> **Summary:**

- **Fold average Dice:** 0.77
- **Ensemble Dice:** 0.86
- **Fold average IoU:** 0.63
- **Ensemble IoU:** 0.76

### Effect of Watershed Post-processing

![Watershed Comparison](assets/watershed_comparison.png)

Watershed segmentation reduced performance drastically. Dice and IoU dropped close to zero across all statistical measures.

### Visual Comparison: Input vs Ground Truth vs Prediction vs Watershed

![Qualitative Results](assets/qualitative_results.jpg)

The nnU-Net model captured boundaries well compared to ground truth. Watershed post-processing introduced under-segmentation artifacts.
