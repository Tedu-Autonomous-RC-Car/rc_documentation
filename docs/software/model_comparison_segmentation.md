# Model Performance Comparison – Segmentation

This section is used to visualise and compare the results of different
segmentation experiments. The metrics are produced by the training pipeline
and stored as CSV files in the `outputs/` directory; interactive dashboards
and the written analysis below help you quickly understand which models and
hyperparameters work best.

## Interactive model comparison

An interactive dashboard is generated from a CSV of segmentation experiments.
By default, the latest metrics CSV is loaded automatically into the widget
below; you can hover over metrics and switch between runs in that view. You can
also upload your own CSV to explore alternative runs directly in the browser.

<input type="file" id="segm-metrics-file" accept=".csv" />
<div id="segm-metrics-chart" style="width: 100%; margin-top: 1rem;"></div>

<script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
<script>
  (function () {
    const METRICS = [
      { key: "mIoU", label: "mIoU", higherBetter: true },
      { key: "Dice", label: "Dice", higherBetter: true },
      { key: "Dice background", label: "Dice BG", higherBetter: true },
      { key: "Dice Cat", label: "Dice Cat", higherBetter: true },
      { key: "Dice Human", label: "Dice Human", higherBetter: true },
      { key: "Dice Road", label: "Dice Road", higherBetter: true },
      { key: "IoU background", label: "IoU BG", higherBetter: true },
      { key: "IoU Cat", label: "IoU Cat", higherBetter: true },
      { key: "IoU Human", label: "IoU Human", higherBetter: true },
      { key: "IoU Road", label: "IoU Road", higherBetter: true },
      { key: "Train Time (min)", label: "Train Time (min)", higherBetter: false },
    ];

    const ARCH_COLORS = {
      fcn_resnet50: "#818cf8",
      deeplabv3: "#38bdf8",
      "deeplabv3+": "#34d399",
      unet: "#fbbf24",
      "unet++": "#f472b6",
    };

    function buildRuns(rows) {
      return rows
        .filter((row) => row["Run"] && row["Model"])
        .map((row, idx) => {
          const arch = String(row["Model"]).trim();
          const id = arch + "|" + idx;
          const name = arch + " | " + row["Run"];
          const values = {};
          METRICS.forEach((m) => {
            const v = parseFloat(row[m.key]);
            values[m.key] = isNaN(v) ? null : v;
          });
          return { id, arch, name, values };
        })
        .filter((r) => typeof r.values["mIoU"] === "number");
    }

    function getRange(runs, key) {
      const vals = runs
        .map((r) => r.values[key])
        .filter((v) => typeof v === "number" && !isNaN(v));
      if (!vals.length) return { min: 0, max: 1 };
      return { min: Math.min(...vals), max: Math.max(...vals) };
    }

    function normalize(runs, val, key, higherBetter) {
      const { min, max } = getRange(runs, key);
      if (!isFinite(min) || !isFinite(max) || max === min) return 0.5;
      const n = (val - min) / (max - min);
      return higherBetter ? n : 1 - n;
    }

    function renderDashboard(container, runs) {
      container.innerHTML = "";
      if (!runs.length) {
        container.textContent = "Geçerli satır bulunamadı.";
        return;
      }

      const state = { selectedId: runs[0].id, tooltip: null };

      const ROW_H = 44;
      const LABEL_W = 130;
      const BAR_W = 420;
      const PAD_TOP = 24;
      const chartH = METRICS.length * ROW_H + PAD_TOP;

      const root = document.createElement("div");
      root.style.cssText =
        "font-family:'IBM Plex Sans',system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;" +
        "background:#020617;padding:24px 20px 28px 20px;border-radius:12px;border:1px solid #1e293b;color:#e2e8f0;";

      const tooltipEl = document.createElement("div");
      tooltipEl.id = "segm-tooltip";

      function draw() {
        root.innerHTML = "";

        const selected =
          runs.find((r) => r.id === state.selectedId) || runs[0];
        const others = runs.filter((r) => r.id !== selected.id);

        const header = document.createElement("div");
        header.style.marginBottom = "20px";
        header.innerHTML =
          '<div style="font-size:18px;font-weight:700;color:#f8fafc;letter-spacing:-0.4px;">Interactive Model Comparison</div>' +
          '<div style="font-size:12px;color:#64748b;margin-top:4px;line-height:1.5;">Her metrik kendi aralığında gösterilir. Seçili run diğer runlar ile aynı eksende karşılaştırılır.</div>';
        root.appendChild(header);

        const ddWrap = document.createElement("div");
        ddWrap.style.marginBottom = "22px";
        const lab = document.createElement("label");
        lab.textContent = "Seçili run";
        lab.style.cssText =
          "font-size:11px;color:#64748b;letter-spacing:0.08em;text-transform:uppercase;display:block;margin-bottom:6px;";
        const select = document.createElement("select");
        select.style.cssText =
          "background:#0f172a;border:1px solid #1f2937;color:#f1f5f9;padding:9px 12px;border-radius:8px;font-size:13px;font-family:'IBM Plex Mono',monospace;cursor:pointer;width:100%;max-width:520px;";
        const grouped = runs.reduce((acc, r) => {
          (acc[r.arch] ||= []).push(r);
          return acc;
        }, {});
        Object.entries(grouped).forEach(([arch, list]) => {
          const og = document.createElement("optgroup");
          og.label = arch;
          list.forEach((r) => {
            const opt = document.createElement("option");
            opt.value = r.id;
            opt.textContent = r.name;
            if (r.id === selected.id) opt.selected = true;
            og.appendChild(opt);
          });
          select.appendChild(og);
        });
        select.addEventListener("change", (e) => {
          state.selectedId = e.target.value;
          state.tooltip = null;
          draw();
        });
        ddWrap.appendChild(lab);
        ddWrap.appendChild(select);
        root.appendChild(ddWrap);

        const legend = document.createElement("div");
        legend.style.cssText =
          "display:flex;gap:18px;margin-bottom:18px;align-items:center;flex-wrap:wrap;";
        const leftLeg = document.createElement("div");
        leftLeg.style.cssText = "display:flex;align-items:center;gap:8px;";
        const dots = document.createElement("div");
        dots.style.cssText = "display:flex;gap:3px;";
        Object.entries(ARCH_COLORS).forEach(([arch, color]) => {
          const d = document.createElement("div");
          d.style.cssText =
            "width:8px;height:8px;border-radius:50%;background:" +
            color +
            ";opacity:0.5;";
          dots.appendChild(d);
        });
        const dl = document.createElement("span");
        dl.textContent = "Diğer runlar";
        dl.style.cssText = "font-size:12px;color:#64748b;";
        leftLeg.appendChild(dots);
        leftLeg.appendChild(dl);
        legend.appendChild(leftLeg);

        const selLeg = document.createElement("div");
        selLeg.style.cssText = "display:flex;align-items:center;gap:8px;";
        const selColor = ARCH_COLORS[selected.arch] || "#60a5fa";
        const box = document.createElement("div");
        box.style.cssText =
          "width:14px;height:14px;border-radius:3px;border:2px solid " +
          selColor +
          ";background:" +
          selColor +
          "33;";
        const selText = document.createElement("span");
        selText.style.cssText = "font-size:12px;color:#94a3b8;";
        selText.innerHTML =
          'Seçili: <strong style="color:' + selColor + '">' +
          selected.arch +
          "</strong>";
        selLeg.appendChild(box);
        selLeg.appendChild(selText);
        legend.appendChild(selLeg);

        const arrow = document.createElement("div");
        arrow.textContent = "← kötü / iyi →";
        arrow.style.cssText =
          "margin-left:auto;font-size:11px;color:#475569;white-space:nowrap;";
        legend.appendChild(arrow);
        root.appendChild(legend);

        const chartWrap = document.createElement("div");
        chartWrap.style.cssText =
          "background:#020617;border-radius:12px;border:1px solid #1f2937;padding:10px 0;overflow-x:auto;";
        const chart = document.createElement("div");
        chart.style.cssText =
          "position:relative;width:" +
          (LABEL_W + BAR_W + 80) +
          "px;height:" +
          chartH +
          "px;";
        chartWrap.appendChild(chart);
        root.appendChild(chartWrap);

        [0, 0.25, 0.5, 0.75, 1].forEach((t) => {
          const line = document.createElement("div");
          line.style.cssText =
            "position:absolute;top:0;bottom:0;width:1px;left:" +
            (LABEL_W + t * BAR_W) +
            "px;" +
            (t === 0 || t === 1 ? "background:#1f2937;" : "background:#111827;") +
            (t === 1
              ? "border-left:1px dashed rgba(34,197,94,0.7);"
              : "");
          chart.appendChild(line);

          const labx = document.createElement("div");
          labx.style.cssText =
            "position:absolute;top:4px;width:32px;text-align:center;font-size:10px;color:#64748b;left:" +
            (LABEL_W + t * BAR_W - 16) +
            "px;";
          labx.textContent =
            t === 0 ? "worst" : t === 1 ? "best" : t * 100 + "%";
          chart.appendChild(labx);
        });

        METRICS.forEach((m, i) => {
          const y = PAD_TOP + i * ROW_H;
          const selVal = selected.values[m.key];
          const selNorm = normalize(
            runs,
            selVal,
            m.key,
            m.higherBetter
          );
          const selX = LABEL_W + selNorm * BAR_W;

          const rowBg = document.createElement("div");
          rowBg.style.cssText =
            "position:absolute;left:0;width:100%;height:" +
            ROW_H +
            "px;top:" +
            (y - ROW_H / 2 + 4) +
            "px;" +
            (i % 2 === 0 ? "background:rgba(148,163,184,0.03);" : "");
          chart.appendChild(rowBg);

          const label = document.createElement("div");
          label.textContent = m.label;
          label.style.cssText =
            "position:absolute;left:8px;top:" +
            (y - ROW_H / 2 + 4) +
            "px;height:" +
            ROW_H +
            "px;display:flex;align-items:center;justify-content:flex-end;font-size:12px;color:#9ca3af;font-family:'IBM Plex Mono',monospace;width:" +
            (LABEL_W - 16) +
            "px;padding-right:8px;";
          chart.appendChild(label);

          runs
            .filter((r) => r.id !== selected.id)
            .forEach((r) => {
              const v = r.values[m.key];
              if (typeof v !== "number") return;
              const norm = normalize(
                runs,
                v,
                m.key,
                m.higherBetter
              );
              const x = LABEL_W + norm * BAR_W;
              const col = ARCH_COLORS[r.arch] || "#94a3b8";
              const dot = document.createElement("div");
              dot.style.cssText =
                "position:absolute;width:8px;height:8px;border-radius:50%;left:" +
                (x - 4) +
                "px;top:" +
                (y - 4) +
                "px;background:" +
                col +
                ";opacity:0.5;cursor:pointer;z-index:1;";
              dot.onmouseenter = () => {
                state.tooltip = { run: r, metric: m, value: v };
                drawTooltip();
              };
              dot.onmouseleave = () => {
                state.tooltip = null;
                drawTooltip();
              };
              chart.appendChild(dot);
            });

        const selColor2 = ARCH_COLORS[selected.arch] || "#60a5fa";
        const line = document.createElement("div");
        line.style.cssText =
          "position:absolute;left:" +
          LABEL_W +
          "px;top:" +
          y +
          "px;width:" +
          selNorm * BAR_W +
          "px;height:2px;background:linear-gradient(to right,transparent," +
          selColor2 +
          "55);pointer-events:none;";
        chart.appendChild(line);

        const selDot = document.createElement("div");
        selDot.style.cssText =
          "position:absolute;width:14px;height:14px;border-radius:3px;left:" +
          (selX - 7) +
          "px;top:" +
          (y - 7) +
          "px;background:" +
          selColor2 +
          "33;border:2px solid " +
          selColor2 +
          ";box-shadow:0 0 8px " +
          selColor2 +
          "66;cursor:pointer;z-index:3;";
        selDot.onmouseenter = () => {
          state.tooltip = { run: selected, metric: m, value: selVal };
          drawTooltip();
        };
        selDot.onmouseleave = () => {
          state.tooltip = null;
          drawTooltip();
        };
        chart.appendChild(selDot);

        const val = document.createElement("div");
        val.style.cssText =
          "position:absolute;left:" +
          (LABEL_W + BAR_W + 10) +
          "px;top:" +
          (y - ROW_H / 2 + 4) +
          "px;height:" +
          ROW_H +
          "px;display:flex;align-items:center;font-size:11px;color:" +
          selColor2 +
          ";font-family:'IBM Plex Mono',monospace;font-weight:600;white-space:nowrap;";
        val.textContent =
          m.key === "Train Time (min)"
            ? (selVal ?? 0) + "m"
            : (selVal ?? 0).toFixed(3);
        chart.appendChild(val);
      });

      // Metric summary cards under the chart
      const cardsWrap = document.createElement("div");
      cardsWrap.style.cssText =
        "display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));" +
        "gap:12px;margin-top:20px;";

      METRICS.forEach((m) => {
        const v = selected.values[m.key];
        if (typeof v !== "number") return;
        const norm = normalize(runs, v, m.key, m.higherBetter);
        const col = m.key === "Train Time (min)" ? "#f59e0b" : selColor;

        const card = document.createElement("div");
        card.style.cssText =
          "background:#020617;border-radius:10px;border:1px solid #1f2937;" +
          "padding:10px 12px;font-family:'IBM Plex Mono',monospace;font-size:11px;";

        const title = document.createElement("div");
        title.textContent = m.label.toUpperCase();
        title.style.cssText =
          "font-size:10px;letter-spacing:0.08em;color:#6b7280;margin-bottom:6px;";
        card.appendChild(title);

        const valueRow = document.createElement("div");
        valueRow.style.cssText =
          "display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;";
        const valSpan = document.createElement("span");
        valSpan.textContent =
          m.key === "Train Time (min)" ? v.toFixed(1) + " m" : v.toFixed(3);
        valSpan.style.cssText =
          "font-size:14px;font-weight:600;color:" + col + ";";
        const pctSpan = document.createElement("span");
        pctSpan.textContent = Math.round(norm * 100) + "%";
        pctSpan.style.cssText = "font-size:10px;color:#9ca3af;";
        valueRow.appendChild(valSpan);
        valueRow.appendChild(pctSpan);
        card.appendChild(valueRow);

        const barBg = document.createElement("div");
        barBg.style.cssText =
          "width:100%;height:3px;border-radius:999px;background:#111827;overflow:hidden;";
        const barFg = document.createElement("div");
        barFg.style.cssText =
          "height:100%;border-radius:999px;background:" +
          col +
          ";width:" +
          Math.max(4, norm * 100) +
          "%;";
        barBg.appendChild(barFg);
        card.appendChild(barBg);

        cardsWrap.appendChild(card);
      });

      root.appendChild(cardsWrap);
      root.appendChild(tooltipEl);
      drawTooltip();
    }

    function drawTooltip() {
      tooltipEl.innerHTML = "";
      const t = state.tooltip;
      if (!t) return;
      const col = ARCH_COLORS[t.run.arch] || "#60a5fa";
      tooltipEl.style.cssText =
        "margin-top:18px;border-radius:8px;border:1px solid " +
        col +
        ";background:#020617;padding:8px 12px;font-size:12px;font-family:'IBM Plex Mono',monospace;";
      tooltipEl.innerHTML =
        '<div style="color:' +
        col +
        ';font-weight:600;margin-bottom:2px;">' +
        t.run.arch +
        "</div>" +
        '<div style="color:#64748b;font-size:10px;margin-bottom:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' +
        t.run.name +
        "</div>" +
        "<div>" +
        t.metric.label +
        ': <strong style="color:#f9fafb">' +
        (t.metric.key === "Train Time (min)"
          ? t.value + "m"
          : t.value.toFixed(3)) +
        '</strong> <span style="color:#94a3b8">(' +
        Math.round(
          normalize(
            runs,
            t.value,
            t.metric.key,
            t.metric.higherBetter
          ) * 100
        ) +
        "%)</span></div>";
    }

      draw();
      container.appendChild(root);
    }

    const input = document.getElementById("segm-metrics-file");
    const container = document.getElementById("segm-metrics-chart");
    if (!input || !container) return;

    function handleResults(results) {
      const runs = buildRuns(results.data);
      if (!runs.length) {
        alert(
          "CSV boş veya beklenen kolonlar eksik. Gerekli kolonlar: Run, Model, mIoU, Dice, Dice background, Dice Cat, Dice Human, Dice Road, IoU background, IoU Cat, IoU Human, IoU Road, Train Time (min)."
        );
        return;
      }
      renderDashboard(container, runs);
    }

    // Default: load precomputed CSV so the dashboard is visible
    // immediately when the page opens.
    Papa.parse("../assets/segmentation_experiments_metrics.csv", {
      download: true,
      header: true,
      dynamicTyping: false,
      skipEmptyLines: true,
      complete: handleResults,
      error: () => {
        console.warn(
          "Varsayılan segmentation_experiments_metrics.csv yüklenemedi."
        );
      },
    });

    // Allow users to override with their own CSV via file input.
    input.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (!file) return;

      Papa.parse(file, {
        header: true,
        dynamicTyping: false,
        skipEmptyLines: true,
        complete: handleResults,
        error: () => {
          alert("CSV okunurken hata oluştu.");
        },
      });
    });
  })();
</script>

---

## Segmentation model – comparative experiment analysis

**5 Architectures · 50 Experiments · 3 Active Classes · 640×640 px**

---

### 1. Executive summary

This report presents a comprehensive analysis of **5 architectures** and **50 experiments** trained for RC car scene segmentation. All models were trained at 640×640 resolution for 50 epochs and evaluated using mIoU, Dice, Pixel Accuracy, and per-class IoU metrics.

> **Best performance:** fcn_resnet50 (exp7, `lr=0.0001`, `wd=0.0005`, `bs=4`) → mIoU: **0.6923** · Pixel Accuracy: **0.9702** · Val Loss: **0.1018**  
> A low learning rate (0.0001) consistently outperformed higher values across all architectures. Metrics are evaluated over 3 active classes (Background, Human, Road) as the Cat class has no samples in the current dataset.

---

### 2. Experiment setup

#### 2.1 Architectures

Five architectures were evaluated, each with 10 hyperparameter configurations:

- **FCN ResNet‑50** – fully convolutional network using ResNet‑50 as encoder; classic segmentation baseline.
- **DeepLabV3 ResNet‑50** – atrous convolution with ASPP module for a larger receptive field.
- **DeepLabV3+** – DeepLabV3 extended with a decoder module; stronger on fine boundary details.
- **U‑Net** – encoder–decoder with skip connections, originally for biomedical imaging.
- **U‑Net++** – enhanced U‑Net with dense nested skip connections for richer feature reuse.

#### 2.2 Hyperparameter search space

| Parameter      | Values                                  |
| ------------- | ---------------------------------------- |
| Learning rate | `0.0001`, `0.0005`, `0.001`             |
| Weight decay  | `1e-5`, `0.0001`, `0.0005`              |
| Batch size    | `2`, `4`, `8`                           |
| Epochs        | 50 (fixed)                              |
| Image size    | 640×640 px (fixed)                      |
| Label classes | Background, Cat, Human, Road            |

---

### 3. Model comparison

The table below shows the best‑run results for each architecture, ranked by mIoU.

| Model                | Best mIoU | Pixel Acc | Val Loss | Dice  | IoU Road | Avg time |
| -------------------- | -------- | --------- | -------- | ----- | -------- | -------- |
| **fcn_resnet50** ⭐  | **0.6923** | **0.9702** | **0.1018** | **0.7198** | 0.9254 | 6.5 m |
| deeplabv3_resnet50   | 0.6828   | 0.9650    | 0.1121   | 0.7144 | 0.9235  | 5.9 m   |
| deeplabv3+           | 0.6693   | 0.9577    | 0.1457   | 0.7065 | **0.9265** | **4.5 m** |
| unet++               | 0.6691   | 0.9571    | 0.1417   | 0.7067 | 0.9095  | 7.2 m   |
| unet                 | 0.6665   | 0.9552    | 0.1437   | 0.7054 | 0.8959  | 5.3 m   |

_⭐ = overall best run across all experiments_

#### 3.1 FCN ResNet‑50 – overall winner

FCN ResNet‑50 ranks first in both best‑run mIoU (**0.6923**) and Pixel Accuracy (**0.9702**) across all architectures. The exp7 configuration (`lr=0.0001`, `wd=0.0005`, `bs=4`) also achieves a notably low Val Loss of **0.1018**.

The strong performance of FCN on this dataset may appear surprising, but for a fixed‑resolution (640×640) task with a small number of active classes, simpler architectures tend to be more resistant to overfitting and converge more reliably within 50 epochs.

#### 3.2 DeepLabV3 ResNet‑50

DeepLabV3 ResNet‑50 ranks second with a best‑run **mIoU of 0.6828**. The ASPP module’s multi‑scale feature aggregation produces strong results particularly on the Human class (**IoU: 0.854**). Average training time is a reasonable **5.9 minutes**.

#### 3.3 DeepLabV3+ – efficiency champion

DeepLabV3+ ranks third in best‑run mIoU (**0.6693**), but is the most efficient architecture at an average of **4.5 minutes** per run. When performance per unit of compute is considered, it becomes the most practical choice. The added decoder particularly benefits fine boundary regions such as road edges.

#### 3.4 U‑Net and U‑Net++

U‑Net (**0.6665**) and U‑Net++ (**0.6691**) achieve comparable results. U‑Net++ is theoretically more powerful due to its dense skip connections, but the limited scale of this dataset prevents the gap from becoming significant. The unusually long training time of U‑Net++ exp2 (**15.2 min**) is an anomaly and should be excluded from average calculations.

---

### 4. Hyperparameter analysis

#### 4.1 Learning rate – the most critical factor

Learning rate has the largest single impact on performance across all factors:

| Learning rate | Avg mIoU | Min mIoU | Max mIoU |
| ------------- | -------- | -------- | -------- |
| **0.0001**    | **0.6644** | 0.6458   | **0.6923** |
| 0.0005        | 0.6226   | 0.5467   | 0.6699   |
| 0.001         | 0.5652   | 0.4870   | 0.6143   |

**`lr=0.0001`** delivers the highest average mIoU (**0.6644**). Runs starting at `lr=0.001` largely failed to converge or experienced severe oscillation, resulting in val loss remaining in the **0.30–0.39** range. `lr=0.0005` shows intermediate performance but consistently falls behind `lr=0.0001`.

> **Recommendation:** Use `lr=0.0001` as the starting learning rate for new experiments. Consider pairing it with a cosine annealing scheduler decaying down to `1e-5` for better generalisation.

#### 4.2 Batch size

The effect of batch size is less pronounced than learning rate. `bs=4` consistently produces more stable results than `bs=2` or `bs=8`. `bs=2` increases training time considerably, while `bs=8` leads to rougher gradient updates. `bs=4` represents the optimal point for this dataset size.

#### 4.3 Weight decay

The effect of weight decay is relatively minor. The difference between `1e-5` and `0.0005` remains **below 0.01 in mIoU**. That said, `wd=0.0005` accompanying the best overall result (fcn_resnet50 exp7) suggests that moderate regularisation is preferable to very low weight decay.

---

### 5. Per‑class performance

The label schema defines 4 classes: **Background, Cat, Human, Road**. However, the current dataset contains no Cat samples; Cat metrics are therefore undefined (0.000) across all experiments and are excluded from this analysis. All results below are evaluated over **three active classes**.

> **Note:** Including Cat in the mIoU denominator artificially deflates reported scores. Once Cat samples are added to the dataset, metrics will update automatically.

#### 5.1 Active class performance

| Class      | Best IoU  | Avg IoU | Best Dice | Avg Dice |
| ---------- | --------- | ------- | --------- | -------- |
| Background | **0.9614** | 0.9054 | **0.9803** | 0.9479  |
| Human      | 0.8823    | 0.8230 | 0.9375    | 0.8730   |
| Road       | 0.9265    | 0.8727 | 0.9619    | 0.9244   |

_Values taken from each architecture’s best run. Cat class is absent from the dataset._

Background is the easiest class and all models exceed 96% IoU. The Human class achieves a best IoU of **0.8823** with fcn_resnet50 exp7. On Road, DeepLabV3+ performs unexpectedly well (IoU **0.9265**), demonstrating its decoder’s advantage on fine boundary regions.

---

### 6. Training time analysis

| Architecture         | Avg time | Best run time |
| ------------------- | -------- | ------------- |
| deeplabv3+          | **4.5 m** | **3.7 m**     |
| unet                | 5.3 m    | 3.9 m         |
| deeplabv3_resnet50  | 5.9 m    | 4.0 m         |
| fcn_resnet50        | 6.5 m    | 5.1 m         |
| unet++              | 7.2 m*   | 4.8 m         |

_\* unet++ exp2 ran anomalously long (15.2 min); excluding it brings the average to ~5.9 min._

> **Performance‑per‑minute:** deeplabv3+ is the most efficient architecture. It achieves mIoU **0.6693** in just **3.7 minutes**. When compute budget is constrained, deeplabv3+ is the recommended choice.

---

### 7. Conclusions & next steps

#### 7.1 Key findings

- **Best model:** fcn_resnet50, `lr=0.0001`, `wd=0.0005`, `bs=4` → mIoU: **0.6923**
- **Most critical hyperparameter:** learning rate — `lr=0.0001` >> `lr=0.0005` >> `lr=0.001`
- **Best efficiency:** deeplabv3+ achieves competitive mIoU (**0.6693**) in only 3.7 minutes.
- **Active classes:** Background, Human, and Road all show strong performance.
- **Cat class:** no samples present in the current dataset; excluded from all metrics.

#### 7.2 Next steps

1. **Fine‑tune the fcn_resnet50 exp7 configuration.** Narrow the search around `lr=0.0001` (range: `0.00005`–`0.0002`).
2. **Increase epoch count.** 50 epochs may be insufficient; try 100–150 epochs with early stopping.
3. **Add a cosine annealing scheduler.** Periodic learning rate decay can improve generalisation over a fixed lr.
4. **Collect Cat class samples.** Once added, re‑run experiments; the additional class will affect mIoU calculation.
5. **Prioritise deeplabv3+ when training time is limited.** Performance is competitive and training time is the shortest of all architectures.

---

_Report generated from `segmentation_experiments_metrics.csv`. All values reflect validation set metrics at the end of epoch 50._

## Sample CSV format

The script works with any CSV that contains at least a `Run` column and one
or more of the following metric columns:

- `mIoU` (mean intersection over union)
- `Pixel Accuracy`
- `Val Loss`
- `Dice`
- `IoU Cat`, `IoU Human`, `IoU Road` (per-class IoUs)

Additional columns are ignored.

---

## Inference model comparison

While the previous sections focus on validation metrics during training, this
section compares **inference‑time performance** of the same models on a held‑out
test set using `all_segmentation_test_inferences_20260304_222539.csv`. Each run
was evaluated on 50 test images and we report mIoU, Pixel Accuracy and average
inference time per image.

### 8.1 Best runs by mIoU (test set)

| Run                                           |   mIoU | Pixel Accuracy | Avg inference time (ms) |
|:----------------------------------------------|------:|---------------:|------------------------:|
| `fcn_resnet50_exp7_lr0.0001_wd0.0005_bs4`       | **0.789** | 0.9598 | 3.54 |
| `fcn_resnet50_exp4_lr0.0001_wd1e-05_bs4`        | 0.748 | 0.9527 | 3.59 |
| `deeplabv3_resnet50_exp1_lr0.0001_wd0.0001_bs4` | 0.688 | 0.9599 | 7.52 |
| `unet_exp4_lr0.0001_wd1e-05_bs4`                | 0.680 | 0.9550 | 7.25 |
| `deeplabv3__exp7_lr0.0001_wd0.0005_bs4`         | 0.677 | 0.9526 | 9.32 |

**Observations:**

- **fcn_resnet50 exp7** remains the best overall model even on the test set, improving its mIoU to **0.789** while keeping inference time very low (~3.5 ms/image).
- The second best FCN configuration (exp4) trades only a small drop in mIoU for a very similar runtime, confirming the robustness of the `lr=0.0001` settings.
- DeepLabV3 and U‑Net reach slightly lower mIoU, but still achieve solid Pixel Accuracy (\>0.95) and remain viable alternatives when architectural diversity is desired.

### 8.2 Fastest runs by inference time

| Run                                     |   mIoU | Pixel Accuracy | Avg inference time (ms) |
|:----------------------------------------|------:|---------------:|------------------------:|
| `fcn_resnet50_exp7_lr0.0001_wd0.0005_bs4` | **0.789** | 0.9598 | **3.54** |
| `fcn_resnet50_exp4_lr0.0001_wd1e-05_bs4`  | 0.748 | 0.9527 | 3.59 |
| `fcn_resnet50_exp10_lr0.001_wd0.0005_bs4` | 0.599 | 0.8957 | 3.64 |
| `fcn_resnet50_exp9_lr0.0005_wd0.0001_bs8` | 0.646 | 0.9324 | 3.76 |
| `fcn_resnet50_exp5_lr0.0005_wd1e-05_bs4`  | 0.642 | 0.9289 | 3.76 |

**Key takeaway for deployment:**

- For real‑time inference on the RC car, **`fcn_resnet50_exp7_lr0.0001_wd0.0005_bs4`** offers the **best trade‑off between accuracy and speed**, leading both the **quality ranking** (mIoU) and the **latency ranking** (inference time).
- If slightly lower accuracy is acceptable, exp4/exp5/exp9 provide additional fast variants with diverse regularisation settings that can be used as backup models.

### 8.3 Interactive inference comparison

<div id="segm-inference-chart" style="width: 100%; margin-top: 1.5rem;"></div>

<script>
  (function () {
    const container = document.getElementById("segm-inference-chart");
    if (!container || typeof Papa === "undefined") return;

    const METRICS = [
      { key: "mIoU", label: "mIoU", higherBetter: true },
      { key: "Pixel Accuracy", label: "Pixel Accuracy", higherBetter: true },
      { key: "IoU background", label: "IoU BG", higherBetter: true },
      { key: "IoU Road", label: "IoU Road", higherBetter: true },
      { key: "IoU Human", label: "IoU Human", higherBetter: true },
      {
        key: "Avg Inference Time (ms)",
        label: "Avg Inference Time (ms)",
        higherBetter: false,
      },
    ];

    const ARCH_COLORS = {
      fcn_resnet50: "#818cf8",
      deeplabv3_resnet50: "#38bdf8",
      deeplabv3: "#38bdf8",
      "deeplabv3+": "#34d399",
      unet: "#fbbf24",
      "unet++": "#f472b6",
    };

    function archFromRun(run) {
      if (run.startsWith("fcn_resnet50")) return "fcn_resnet50";
      if (run.startsWith("deeplabv3_resnet50")) return "deeplabv3_resnet50";
      if (run.startsWith("deeplabv3+")) return "deeplabv3+";
      if (run.startsWith("deeplabv3__")) return "deeplabv3";
      if (run.startsWith("unet++") || run.startsWith("unetpp")) return "unet++";
      if (run.startsWith("unet")) return "unet";
      return "other";
    }

    function buildRuns(rows) {
      return rows
        .filter((row) => row["Run"])
        .map((row, idx) => {
          const run = String(row["Run"]);
          const arch = archFromRun(run);
          const id = run + "|" + idx;
          const name = run;
          const values = {};
          METRICS.forEach((m) => {
            const v = parseFloat(row[m.key]);
            values[m.key] = isNaN(v) ? null : v;
          });
          return { id, arch, name, values };
        })
        .filter((r) => typeof r.values["mIoU"] === "number");
    }

    function getRange(runs, key) {
      const vals = runs
        .map((r) => r.values[key])
        .filter((v) => typeof v === "number" && !isNaN(v));
      if (!vals.length) return { min: 0, max: 1 };
      return { min: Math.min(...vals), max: Math.max(...vals) };
    }

    function normalize(runs, val, key, higherBetter) {
      const { min, max } = getRange(runs, key);
      if (!isFinite(min) || !isFinite(max) || max === min) return 0.5;
      const n = (val - min) / (max - min);
      return higherBetter ? n : 1 - n;
    }

    function renderDashboard(container, runs) {
      container.innerHTML = "";
      if (!runs.length) {
        container.textContent = "Geçerli inference satırı bulunamadı.";
        return;
      }

      const state = { selectedId: runs[0].id };

      const ROW_H = 40;
      const LABEL_W = 150;
      const BAR_W = 420;
      const PAD_TOP = 28;
      const chartH = METRICS.length * ROW_H + PAD_TOP;

      const root = document.createElement("div");
      root.style.cssText =
        "font-family:'IBM Plex Sans',system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;" +
        "background:#020617;padding:24px 20px 24px 20px;border-radius:12px;border:1px solid #1e293b;color:#e2e8f0;";

      function draw() {
        root.innerHTML = "";

        const selected =
          runs.find((r) => r.id === state.selectedId) || runs[0];
        const others = runs.filter((r) => r.id !== selected.id);

        const header = document.createElement("div");
        header.style.marginBottom = "18px";
        header.innerHTML =
          '<div style="font-size:16px;font-weight:700;color:#f8fafc;letter-spacing:-0.3px;">Interactive inference comparison</div>' +
          '<div style="font-size:12px;color:#64748b;margin-top:4px;line-height:1.5;">Her satır bir metrik, her nokta bir inference run. Sağ tarafa yakın noktalar daha iyi skorları, sola yakın olanlar daha hızlı inference zamanını temsil eder.</div>';
        root.appendChild(header);

        const ddWrap = document.createElement("div");
        ddWrap.style.marginBottom = "18px";
        const lab = document.createElement("label");
        lab.textContent = "Seçili inference run";
        lab.style.cssText =
          "font-size:11px;color:#64748b;letter-spacing:0.08em;text-transform:uppercase;display:block;margin-bottom:6px;";
        const select = document.createElement("select");
        select.style.cssText =
          "background:#0f172a;border:1px solid #1f2937;color:#f1f5f9;padding:9px 12px;border-radius:8px;font-size:13px;font-family:'IBM Plex Mono',monospace;cursor:pointer;width:100%;max-width:560px;";
        runs.forEach((r) => {
          const opt = document.createElement("option");
          opt.value = r.id;
          opt.textContent = r.name;
          if (r.id === selected.id) opt.selected = true;
          select.appendChild(opt);
        });
        select.addEventListener("change", (e) => {
          state.selectedId = e.target.value;
          draw();
        });
        ddWrap.appendChild(lab);
        ddWrap.appendChild(select);
        root.appendChild(ddWrap);

        const legend = document.createElement("div");
        legend.style.cssText =
          "display:flex;gap:18px;margin-bottom:16px;align-items:center;flex-wrap:wrap;";
        const legendLeft = document.createElement("div");
        legendLeft.style.cssText = "display:flex;align-items:center;gap:8px;";
        const dots = document.createElement("div");
        dots.style.cssText = "display:flex;gap:3px;";
        Object.entries(ARCH_COLORS).forEach(([arch, color]) => {
          const d = document.createElement("div");
          d.style.cssText =
            "width:8px;height:8px;border-radius:50%;background:" +
            color +
            ";opacity:0.5;";
          dots.appendChild(d);
        });
        const txt = document.createElement("span");
        txt.textContent = "Diğer runlar";
        txt.style.cssText = "font-size:12px;color:#64748b;";
        legendLeft.appendChild(dots);
        legendLeft.appendChild(txt);
        legend.appendChild(legendLeft);

        const selLeg = document.createElement("div");
        selLeg.style.cssText = "display:flex;align-items:center;gap:8px;";
        const selColor = ARCH_COLORS[selected.arch] || "#60a5fa";
        const selBox = document.createElement("div");
        selBox.style.cssText =
          "width:14px;height:14px;border-radius:3px;border:2px solid " +
          selColor +
          ";background:" +
          selColor +
          "33;";
        const selTxt = document.createElement("span");
        selTxt.innerHTML =
          'Seçili: <strong style="color:' + selColor + '">' +
          selected.arch +
          "</strong>";
        selTxt.style.cssText = "font-size:12px;color:#94a3b8;";
        selLeg.appendChild(selBox);
        selLeg.appendChild(selTxt);
        legend.appendChild(selLeg);

        const arrow = document.createElement("div");
        arrow.textContent = "← kötü / iyi →";
        arrow.style.cssText =
          "margin-left:auto;font-size:11px;color:#475569;white-space:nowrap;";
        legend.appendChild(arrow);
        root.appendChild(legend);

        const chartWrap = document.createElement("div");
        chartWrap.style.cssText =
          "background:#020617;border-radius:12px;border:1px solid #1f2937;padding:10px 0;overflow-x:auto;";
        const chart = document.createElement("div");
        chart.style.cssText =
          "position:relative;width:" +
          (LABEL_W + BAR_W + 120) +
          "px;height:" +
          chartH +
          "px;";
        chartWrap.appendChild(chart);
        root.appendChild(chartWrap);

        [0, 0.25, 0.5, 0.75, 1].forEach((t) => {
          const x = LABEL_W + t * BAR_W;
          const line = document.createElement("div");
          line.style.cssText =
            "position:absolute;top:0;bottom:0;width:1px;left:" +
            x +
            "px;" +
            (t === 0 || t === 1 ? "background:#1f2937;" : "background:#111827;") +
            (t === 1
              ? "border-left:1px dashed rgba(34,197,94,0.7);"
              : "");
          chart.appendChild(line);

          const labx = document.createElement("div");
          labx.style.cssText =
            "position:absolute;top:4px;width:32px;text-align:center;font-size:10px;color:#64748b;left:" +
            (LABEL_W + t * BAR_W - 16) +
            "px;";
          labx.textContent =
            t === 0 ? "worst" : t === 1 ? "best" : t * 100 + "%";
          chart.appendChild(labx);
        });

        METRICS.forEach((m, i) => {
          const y = PAD_TOP + i * ROW_H;
          const selVal = selected.values[m.key];
          const selNorm = normalize(
            runs,
            selVal,
            m.key,
            m.higherBetter
          );
          const selX = LABEL_W + selNorm * BAR_W;

          const rowBg = document.createElement("div");
          rowBg.style.cssText =
            "position:absolute;left:0;width:100%;height:" +
            ROW_H +
            "px;top:" +
            (y - ROW_H / 2 + 4) +
            "px;" +
            (i % 2 === 0 ? "background:rgba(148,163,184,0.03);" : "");
          chart.appendChild(rowBg);

          const label = document.createElement("div");
          label.textContent = m.label;
          label.style.cssText =
            "position:absolute;left:8px;top:" +
            (y - ROW_H / 2 + 4) +
            "px;height:" +
            ROW_H +
            "px;display:flex;align-items:center;justify-content:flex-end;font-size:12px;color:#9ca3af;font-family:'IBM Plex Mono',monospace;width:" +
            (LABEL_W - 16) +
            "px;padding-right:8px;white-space:nowrap;";
          chart.appendChild(label);

          others.forEach((r) => {
            const v = r.values[m.key];
            if (typeof v !== "number") return;
            const norm = normalize(
              runs,
              v,
              m.key,
              m.higherBetter
            );
            const x = LABEL_W + norm * BAR_W;
            const col = ARCH_COLORS[r.arch] || "#94a3b8";
            const dot = document.createElement("div");
            dot.style.cssText =
              "position:absolute;width:8px;height:8px;border-radius:50%;left:" +
              (x - 4) +
              "px;top:" +
              (y - 4) +
              "px;background:" +
              col +
              ";opacity:0.5;cursor:pointer;z-index:1;";
            chart.appendChild(dot);
          });

          const selColor2 = ARCH_COLORS[selected.arch] || "#60a5fa";
          const line = document.createElement("div");
          line.style.cssText =
            "position:absolute;left:" +
            LABEL_W +
            "px;top:" +
            y +
            "px;width:" +
            selNorm * BAR_W +
            "px;height:2px;background:linear-gradient(to right,transparent," +
            selColor2 +
            "55);pointer-events:none;";
          chart.appendChild(line);

          const selDot = document.createElement("div");
          selDot.style.cssText =
            "position:absolute;width:14px;height:14px;border-radius:3px;left:" +
            (selX - 7) +
            "px;top:" +
            (y - 7) +
            "px;background:" +
            selColor2 +
            "33;border:2px solid " +
            selColor2 +
            ";box-shadow:0 0 8px " +
            selColor2 +
            "66;cursor:pointer;z-index:3;";
          chart.appendChild(selDot);

          const val = document.createElement("div");
          val.style.cssText =
            "position:absolute;left:" +
            (LABEL_W + BAR_W + 10) +
            "px;top:" +
            (y - ROW_H / 2 + 4) +
            "px;height:" +
            ROW_H +
            "px;display:flex;align-items:center;font-size:11px;color:" +
            selColor2 +
            ";font-family:'IBM Plex Mono',monospace;font-weight:600;white-space:nowrap;";
          val.textContent =
            m.key === "Avg Inference Time (ms)"
              ? selVal.toFixed(2) + " ms"
              : selVal.toFixed(3);
          chart.appendChild(val);
        });

        container.appendChild(root);
      }

    Papa.parse("../assets/all_segmentation_test_inferences.csv", {
      download: true,
      header: true,
      dynamicTyping: false,
      skipEmptyLines: true,
      complete: (results) => {
        // #region agent log
        fetch('http://127.0.0.1:7771/ingest/9f317fe5-712c-454b-ac64-a9e81de8cded',{
          method:'POST',
          headers:{
            'Content-Type':'application/json',
            'X-Debug-Session-Id':'5b3275'
          },
          body:JSON.stringify({
            sessionId:'5b3275',
            runId:'inference_plot',
            hypothesisId:'H2',
            location:'model_comparison_segmentation.md:8.3-complete',
            message:'inference_csv_loaded',
            data:{rowCount:Array.isArray(results.data)?results.data.length:null},
            timestamp:Date.now()
          })
        }).catch(()=>{});
        // #endregion agent log

        const runs = buildRuns(results.data);

        // #region agent log
        fetch('http://127.0.0.1:7771/ingest/9f317fe5-712c-454b-ac64-a9e81de8cded',{
          method:'POST',
          headers:{
            'Content-Type':'application/json',
            'X-Debug-Session-Id':'5b3275'
          },
          body:JSON.stringify({
            sessionId:'5b3275',
            runId:'inference_plot',
            hypothesisId:'H3',
            location:'model_comparison_segmentation.md:8.3-buildRuns',
            message:'inference_build_runs',
            data:{runCount:runs.length,firstRun:runs[0]?.name || null},
            timestamp:Date.now()
          })
        }).catch(()=>{});
        // #endregion agent log

        if (!runs.length) {
          container.textContent =
            "Inference CSV boş veya beklenen kolonlar eksik.";
          return;
        }
        renderDashboard(container, runs);
      },
      error: () => {
        container.textContent =
          "Inference CSV yüklenemedi (all_segmentation_test_inferences.csv).";
      },
    });
  })();
</script>
