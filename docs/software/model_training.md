# RC Car Model Training

This page documents the **RC Car Model Training** application from the [RC-Car-Model-Training](https://github.com/kaanguler14/RC-Car-Model-Training) repository.  
It is a full machine‑learning platform for training **object detection** and **semantic segmentation** models for the TAVP autonomous RC car.

---
<iframe
  src="https://huggingface.co/datasets/TargetU/RcCArDataset/embed/viewer/default/train"
  frameborder="0"
  width="100%"
  height="560px"
></iframe>

## 🚀 Features

- **Multi‑model support**  
  - Detection: YOLOv8/YOLOv5, Faster R‑CNN, RetinaNet, SSD, DETR, Cascade R‑CNN, EfficientDet, FCOS, ATSS  
  - Segmentation: DeepLabV3, UNet, UNet++, PSPNet, HRNet, SegFormer, Mask2Former and other SMP/timm‑based models
- **Dataset augmentation**  
  - 15+ augmentation techniques (geometric, color, noise, MixUp/CutMix/Mosaic, elastic deformation, etc.)
- **MLflow integration**  
  - Experiment tracking, metric/log storage and model management
- **Streamlit UI**  
  - User‑friendly web UI with tabs for dataset import, validation, splitting, training, testing, profiling and deployment
- **Multi‑format support**  
  - LabelMe, Label Studio, YOLO and segmentation mask formats
- **Automatic format conversions**  
  - LabelMe ↔ Label Studio  
  - Original (`H1` / `H1_Annotations`) → Merged (`images_all` / `labels_all`)
- **Model deployment**  
  - ONNX and TensorRT export for Jetson Orin Nano deployment
- **Hyperparameter tuning**  
  - Optuna-based tuning for learning rate, batch size and weight decay

---

## 📋 Installation

### Requirements

- **Python**: 3.8+
- **PyTorch** with a compatible **CUDA** version (GPU training strongly recommended)
- Core dependencies are listed in `Documentation/requirements.txt`, including:
  - `torch`, `torchvision`
  - `opencv-python`, `Pillow`, `albumentations`
  - `numpy`, `pandas`, `scikit-learn`
  - `mlflow`, `PyYAML`, `streamlit`
  - `ultralytics`, `timm`, `segmentation-models-pytorch`, `transformers`, `mmsegmentation`
  - `datasets`, `huggingface_hub` (for Hugging Face dataset import)
  - `onnx`, `onnxruntime` (for model export)
  - `optuna` (for hyperparameter tuning)

#### Steps

```bash
git clone https://github.com/kaanguler14/RC-Car-Model-Training.git
cd RC-Car-Model-Training

# Virtual environment
python -m venv venv
source venv/bin/activate      # Linux/macOS
# or
venv\Scripts\activate         # Windows

# Dependencies
pip install -r Documentation/requirements.txt
```

> **Note:** ONNX, TensorRT, Detectron2, MMDetection and some segmentation backends may require additional manual installation steps. See comments in `Documentation/requirements.txt` for details.

---

## 🎯 Usage

### Streamlit UI (recommended)

```bash
cd RcCarModelTraining
streamlit run app/main.py
```

In the UI:

- Use the left sidebar **Task type** to switch between `Object Detection` and `Segmentation`.
- The main tabs provide:
  - **Dataset Import** – Download datasets from Hugging Face Hub (e.g. `TargetU/RcCArDataset`)
  - **Dataset Transformation** – LabelMe ↔ Label Studio conversion, H1/H1_Annotations → merged format, image rotation
  - **Dataset Validation** – Validate LabelMe, Label Studio, YOLO and segmentation formats
  - **Dataset Split** – Create train/val/test splits with configurable ratios
  - **Train** – Configure and run training
  - **Experiments** – View MLflow runs, metrics and compare experiments
  - **Test** – Evaluate trained models on test set
  - **Profiling** – Layer-by-layer model profiling (latency, memory)
  - **Deploy** – Export models to ONNX and TensorRT for Jetson Orin Nano

### Command‑line (CLI)

#### Training

```bash
cd RcCarModelTraining
python data/train.py --config configs/train_config.yaml
```

From the config:

- For detection: set `task_type: detection` and `detection.model_name: ...`
- For segmentation: set `task_type: segmentation` and `segmentation.model_name: ...`

The training script will:

- Load the dataset, apply augmentations and build DataLoaders.
- Train with mixed precision (AMP), early stopping and overfitting checks.
- Run validation after each epoch:
  - Detection: Precision, Recall, F1@0.5 IoU
  - Segmentation: Pixel accuracy, mIoU and per‑class IoU
- Save the best model (`*_best.pt`) and the last‑epoch model (`*_last.pt`).

#### Testing

```bash
python data/test.py \
    --task_type detection \
    --model_path outputs/run_name/detection_best.pt \
    --model_name yolov8n \
    --splits_dir splits \
    --test_labels_dir splits/test/labels \
    --num_classes 4
```

For segmentation:

```bash
python data/test.py \
    --task_type segmentation \
    --model_path outputs/run_name/segmentation_best.pt \
    --model_name unet \
    --splits_dir splits \
    --num_classes 4
```

#### Hyperparameter tuning (Optuna)

```bash
python data/tune.py \
    --task_type detection \
    --model_name yolov8n \
    --splits_dir splits \
    --epochs_per_trial 5 \
    --n_trials 20 \
    --optimize_metric f1
```

Options: `--tune_lr`, `--tune_batch_size`, `--tune_weight_decay`, `--fixed_lr`, `--fixed_batch_size`, etc. Best config is saved to `configs/train_config_best.yaml`.

#### Dataset utilities

```bash
# Original → Merged format conversion
python data/reorganize_to_merged.py

# Dataset validation
python data/validate_dataset.py --dataset-root Dataset --check-labelme
```

---

## 📁 Dataset Structure

The dataset is not stored in the repo; it lives in an external directory. Three main formats are supported.

### 1. Merged format (recommended)

```text
Dataset/
├── images_all/            # All images (with camera prefix)
│   ├── H1_frame_001.png
│   ├── H2_frame_001.png
│   └── ...
└── labels_all/            # All annotations (LabelMe JSON)
    ├── H1_frame_001.json
    ├── H2_frame_001.json
    └── classes.txt        # class_id class_name
```

This format:

- Can be automatically converted to YOLO `.txt` labels for detection.
- Is used to generate per‑pixel masks for segmentation.

### 2. Reorganized format

```text
Dataset/
├── images/                # All images
│   ├── H1_frame_001.png
│   └── ...
└── labels/                # All annotations
    ├── H1_frame_001.json
    └── ...
```

### 3. Original format (needs conversion)

```text
Dataset/
├── H1/                    # Images
│   ├── frame_001.png
│   └── ...
├── H1_Annotations/        # Annotations (LabelMe JSON)
│   ├── frame_001.json
│   └── ...
└── ...
```

This layout can be converted to the merged format either:

- **Via the UI**: in the `Dataset Transformation` tab using the “H1/H1_Annotations → images_all/labels_all” style actions, or
- **Via CLI**:

```bash
python data/reorganize_to_merged.py
```

### Splits and label/mask generation

- In `configs/train_config.yaml`, the `data` section defines:
  - `dataset_root`: root directory containing `images_all/` and `labels_all/`
  - `splits_dir`: contains `train.txt`, `val.txt` and optionally `splits/train`, `splits/val`
  - `detection_labels_root`: base directory for YOLO labels and `classes.txt`
  - `segmentation_masks_root`: base directory for segmentation masks and `classes.txt`
- Detection:
  - `data/train.py` automatically creates YOLO `.txt` files from `labels_all/*.json` when needed.
- Segmentation:
  - Mask PNGs are generated from JSONs under split label directories, and `classes.txt` is updated.

> **Detailed format documentation:** See `Documentation/DATASET_FORMAT.md`.

---

## ⚙️ Configuration (`configs/train_config.yaml`)

Key fields:

- **`task_type`**: `"detection"` or `"segmentation"`
- **`run_name`**: human‑readable name used by MLflow and output folders
- **`common`**:
  - `epochs`, `batch_size`, `img_size`, `lr`, `weight_decay`
  - `output_dir`, `preview_samples`
  - `early_stopping`: `enabled`, `patience`, `min_delta`, `monitor`
  - `overfitting_detection`: `loss_gap_threshold`, `metric_degradation_threshold`
- **`data`**:
  - Dataset and split paths (`dataset_root`, `splits_dir`, `detection_labels_root`, `segmentation_masks_root`)
- **`detection`**:
  - `model_name`: e.g. `yolov8n`, `fasterrcnn_resnet50_fpn`, `retinanet_resnet50_fpn`, `ssd300_vgg16`, `detr`, `cascade_rcnn`, …
- **`segmentation`**:
  - `model_name`: e.g. `unet`, `unet++`, `deeplabv3+`, `pspnet`, `fcn_resnet50`, `segformer`, `hrnet`, …
- **`augmentation`**:
  - Geometric: `horizontal_flip`, `rotation`, `scale`, `translation`, `crop_scale`
  - Color: `brightness`, `contrast`, `saturation`, `hue`
  - Noise/blur: `noise`, `blur`
  - Detection‑only: `mixup`, `cutmix`, `mosaic`
  - Segmentation‑only: `elastic`, `grid_distortion`

> **Suggestion:** Use **relative paths** instead of absolute Windows paths in the config. `data/train.py` resolves them relative to the project root.

---

## 🎨 Augmentation Overview

Through `AugmentationFactory` (see `data/dataset.py`):

- **Detection**:
  - Resize + normalize
  - Optional: flip, shift/scale/rotate, ColorJitter, blur/noise, RandomResizedCrop
  - Advanced: MixUp, CutMix, Mosaic (when enabled in the config)
- **Segmentation**:
  - Resize + normalize
  - Flip, shift/scale/rotate, ColorJitter
  - Noise/blur
  - Elastic deformation and grid distortion

---

## 📊 MLflow

To track experiments:

```bash
cd RcCarModelTraining
mlflow ui
```

- All runs are stored under the local `mlruns` directory.
- Each run logs:
  - Hyperparameters (common, data, augmentation, detection/segmentation)
  - Per‑epoch metrics (loss, F1, mIoU, etc.)
  - Best epoch summary
  - Saved PyTorch models and preview images

> **Detailed MLflow usage:** See `Documentation/MLFLOW_KULLANIMI.md`.

---

## 🚀 Deploy Tab (ONNX & TensorRT)

The **Deploy** tab in the Streamlit UI supports:

- **Model selection** – From `outputs/` or a custom path
- **ONNX export** – PyTorch → ONNX (YOLO, SMP, torchvision)
- **TensorRT export** – Via ONNX → TensorRT, torch2trt, or YOLO built-in
- **Benchmark** – Compare PyTorch, ONNX and TensorRT latency/FPS
- **Jetson tips** – FP16, batch size 1, workspace size, `nvpmodel`, `jetson_clocks`

Export options: input size (320–1024), precision (FP32/FP16/INT8), batch size, ONNX opset, dynamic axes.

---

## 📈 Profiling Tab

The **Profiling** tab provides:

- **Layer-by-layer profiling** – PyTorch profiler for latency and memory
- **Model comparison** – Detection, segmentation and classification models
- **Trace export** – JSON traces for external analysis

---

## 🤖 Supported Models (Summary)

### Detection

- YOLOv8, YOLOv5
- Faster R‑CNN, RetinaNet
- DETR, Cascade R‑CNN
- EfficientDet, FCOS, ATSS (via MMDetection integration)

### Segmentation

- DeepLabV3, UNet, UNet++
- SegFormer, Mask2Former
- PSPNet, HRNet
- SegNeXt, DDRNet, PIDNet, TopFormer (via MMSegmentation)
- BiSeNetV2, FPN, LinkNet, MAnet (SMP)

---

## 🧩 Role in the TAVP Stack

- This platform is the **offline learning** component of TAVP:
  - Trains detection/segmentation models from recorded data collected on the car.
  - Produces models that can be exported to ONNX/TensorRT and deployed on **Jetson Orin Nano**, feeding the vision and RL pipelines.

---

## 📚 Additional Documentation

| Document | Description |
|----------|-------------|
| `Documentation/DATASET_FORMAT.md` | Dataset formats, LabelMe/Label Studio, YOLO, segmentation masks |
| `Documentation/TEST_INFERENCE.md` | Segmentation inference with `test_segmentation.py` |
| `Documentation/MLFLOW_KULLANIMI.md` | MLflow usage, parameters and metrics |
| `APP_DOCUMENTATION.md` | Detailed Streamlit UI documentation |
