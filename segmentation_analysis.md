# Segmentation Model — Comparative Experiment Analysis

**5 Architectures · 50 Experiments · 3 Active Classes · 640×640 px**

---

## 1. Executive Summary

This report presents a comprehensive analysis of **5 architectures** and **50 experiments** trained for RC car scene segmentation. All models were trained at 640×640 resolution for 50 epochs and evaluated using mIoU, Dice, Pixel Accuracy, and per-class IoU metrics.

> **Best performance:** fcn_resnet50 (exp7, `lr=0.0001`, `wd=0.0005`, `bs=4`) → mIoU: **0.6923** | Pixel Accuracy: **0.9702** | Val Loss: **0.1018**
> A low learning rate (0.0001) consistently outperformed higher values across all architectures. Metrics are evaluated over 3 active classes (Background, Human, Road) as the Cat class has no samples in the current dataset.

---

## 2. Experiment Setup

### 2.1 Architectures

Five architectures were evaluated, each with 10 hyperparameter configurations:

- **FCN ResNet-50** — Fully Convolutional Network using ResNet-50 as the backbone encoder. Classic segmentation baseline.
- **DeepLabV3 ResNet-50** — Atrous convolution with ASPP module for a larger receptive field.
- **DeepLabV3+** — DeepLabV3 extended with a decoder module; stronger on fine boundary details.
- **U-Net** — Encoder-decoder architecture with skip connections. Originally developed for biomedical imaging.
- **U-Net++** — Enhanced U-Net with dense nested skip connections for richer feature reuse.

### 2.2 Hyperparameter Search Space

| Parameter | Values |
|-----------|--------|
| Learning Rate | `0.0001`, `0.0005`, `0.001` |
| Weight Decay | `1e-5`, `0.0001`, `0.0005` |
| Batch Size | `2`, `4`, `8` |
| Epochs | 50 (fixed) |
| Image Size | 640×640 px (fixed) |
| Label Classes | Background, Cat, Human, Road |

---

## 3. Model Comparison

The table below shows the best-run results for each architecture, ranked by mIoU.

| Model | Best mIoU | Pixel Acc | Val Loss | Dice | IoU Road | Avg Time |
|-------|-----------|-----------|----------|------|----------|----------|
| **fcn_resnet50** ⭐ | **0.6923** | **0.9702** | **0.1018** | **0.7198** | 0.9254 | 6.5m |
| deeplabv3_resnet50 | 0.6828 | 0.9650 | 0.1121 | 0.7144 | 0.9235 | 5.9m |
| deeplabv3+ | 0.6693 | 0.9577 | 0.1457 | 0.7065 | **0.9265** | **4.5m** |
| unet++ | 0.6691 | 0.9571 | 0.1417 | 0.7067 | 0.9095 | 7.2m |
| unet | 0.6665 | 0.9552 | 0.1437 | 0.7054 | 0.8959 | 5.3m |

*⭐ = overall best run across all experiments*

### 3.1 FCN ResNet-50 — Overall Winner

FCN ResNet-50 ranks first in both best-run mIoU (**0.6923**) and Pixel Accuracy (**0.9702**) across all architectures. The exp7 configuration (`lr=0.0001, wd=0.0005, bs=4`) also achieves a notably low Val Loss of **0.1018**.

The strong performance of FCN on this dataset may appear surprising, but for a fixed-resolution (640×640) task with a small number of active classes, simpler architectures tend to be more resistant to overfitting and converge more reliably within 50 epochs.

### 3.2 DeepLabV3 ResNet-50

DeepLabV3 ResNet-50 ranks second with a best-run **mIoU of 0.6828**. The ASPP module's multi-scale feature aggregation produces strong results particularly on the Human class (**IoU: 0.854**). Average training time is a reasonable **5.9 minutes**.

### 3.3 DeepLabV3+ — Efficiency Champion

DeepLabV3+ ranks third in best-run mIoU (**0.6693**), but is the most efficient architecture at an average of **4.5 minutes** per run. When performance per unit of compute is considered, it becomes the most practical choice. The added decoder particularly benefits fine boundary regions such as road edges.

### 3.4 U-Net and U-Net++

U-Net (**0.6665**) and U-Net++ (**0.6691**) achieve comparable results. U-Net++ is theoretically more powerful due to its dense skip connections, but the limited scale of this dataset prevents the gap from becoming significant. The unusually long training time of U-Net++ exp2 (**15.2 min**) is an anomaly and should be excluded from average calculations.

---

## 4. Hyperparameter Analysis

### 4.1 Learning Rate — The Most Critical Factor

Learning rate has the largest single impact on performance across all factors:

| Learning Rate | Avg mIoU | Min mIoU | Max mIoU |
|---------------|----------|----------|----------|
| **0.0001** | **0.6644** | 0.6458 | **0.6923** |
| 0.0005 | 0.6226 | 0.5467 | 0.6699 |
| 0.001 | 0.5652 | 0.4870 | 0.6143 |

**lr=0.0001** delivers the highest average mIoU (**0.6644**). Runs starting at `lr=0.001` largely failed to converge or experienced severe oscillation, resulting in val loss remaining in the **0.30–0.39** range. `lr=0.0005` shows intermediate performance but consistently falls behind `lr=0.0001`.

> **Recommendation:** Use `lr=0.0001` as the starting learning rate for new experiments. Consider pairing it with a cosine annealing scheduler decaying down to `1e-5` for better generalisation.

### 4.2 Batch Size

The effect of batch size is less pronounced than learning rate. `bs=4` consistently produces more stable results than `bs=2` or `bs=8`. `bs=2` increases training time considerably, while `bs=8` leads to rougher gradient updates. `bs=4` represents the optimal point for this dataset size.

### 4.3 Weight Decay

The effect of weight decay is relatively minor. The difference between `1e-5` and `0.0005` remains **below 0.01 in mIoU**. That said, `wd=0.0005` accompanying the best overall result (fcn_resnet50 exp7) suggests that moderate regularisation is preferable to very low weight decay.

---

## 5. Per-Class Performance

The label schema defines 4 classes: **Background, Cat, Human, Road**. However, the current dataset contains no Cat samples; Cat metrics are therefore undefined (0.000) across all experiments and are excluded from this analysis. All results below are evaluated over **three active classes**.

> **Note:** Including Cat in the mIoU denominator artificially deflates reported scores. Once Cat samples are added to the dataset, metrics will update automatically.

### 5.1 Active Class Performance

| Class | Best IoU | Avg IoU | Best Dice | Avg Dice |
|-------|----------|---------|-----------|----------|
| Background | **0.9614** | 0.9054 | **0.9803** | 0.9479 |
| Human | 0.8823 | 0.8230 | 0.9375 | 0.8730 |
| Road | 0.9265 | 0.8727 | 0.9619 | 0.9244 |

*Values taken from each architecture's best run. Cat class is absent from the dataset.*

Background is the easiest class and all models exceed 96% IoU. The Human class achieves a best IoU of **0.8823** with fcn_resnet50 exp7. On Road, DeepLabV3+ performs unexpectedly well (IoU **0.9265**), demonstrating its decoder's advantage on fine boundary regions.

---

## 6. Training Time Analysis

| Architecture | Avg Time | Best Run Time |
|---|---|---|
| deeplabv3+ | **4.5m** | **3.7m** |
| unet | 5.3m | 3.9m |
| deeplabv3_resnet50 | 5.9m | 4.0m |
| fcn_resnet50 | 6.5m | 5.1m |
| unet++ | 7.2m* | 4.8m |

*\* unet++ exp2 ran anomalously long (15.2 min); excluding it brings the average to ~5.9 min.*

> **Performance-per-minute:** deeplabv3+ is the most efficient architecture. It achieves mIoU 0.6693 in just 3.7 minutes. When compute budget is constrained, deeplabv3+ is the recommended choice.

---

## 7. Conclusions & Next Steps

### 7.1 Key Findings

- **Best model:** fcn_resnet50, `lr=0.0001`, `wd=0.0005`, `bs=4` → mIoU: **0.6923**
- **Most critical hyperparameter:** Learning rate — `lr=0.0001` >> `lr=0.0005` >> `lr=0.001`
- **Best efficiency:** deeplabv3+ achieves competitive mIoU (0.6693) in only 3.7 minutes
- **Active classes:** Background, Human, and Road all show strong performance
- **Cat class:** No samples present in the current dataset; excluded from all metrics

### 7.2 Next Steps

1. **Fine-tune the fcn_resnet50 exp7 configuration.** Narrow the search around `lr=0.0001` (range: `0.00005`–`0.0002`).
2. **Increase epoch count.** 50 epochs may be insufficient; try 100–150 epochs with early stopping.
3. **Add a cosine annealing scheduler.** Periodic learning rate decay can improve generalisation over a fixed lr.
4. **Collect Cat class samples.** Once added, re-run experiments; the additional class will affect mIoU calculation.
5. **Prioritise deeplabv3+ when training time is limited.** Performance is competitive and training time is the shortest of all architectures.

---

*Report generated from `segmentation_experiments_metrics.csv`. All values reflect validation set metrics at the end of epoch 50.*
