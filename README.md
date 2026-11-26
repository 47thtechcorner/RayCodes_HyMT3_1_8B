<div align="center">
  <a href="https://youtu.be/TlCM3_i_6uI">
    <img src="https://img.youtube.com/vi/TlCM3_i_6uI/0.jpg" alt="Tencent's 1.3GB Hy-MT3 Beats Microsoft Translator Locally! (102 Languages)">
  </a>
  <h3>📺 <a href="https://youtu.be/TlCM3_i_6uI">Watch the full tutorial on YouTube</a></h3>
</div>

# Hy-MT3 1.8B — Local 102-Language Translation Suite

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://huggingface.co/tencent/Hy-MT3-1.8B)
[![Model Size](https://img.shields.io/badge/Parameters-1.8B_Dense-FFC107)](https://huggingface.co/tencent/Hy-MT3-1.8B)
[![Languages](https://img.shields.io/badge/Coverage-102_Languages-624AFF)](https://huggingface.co/tencent/Hy-MT3-1.8B)
[![Local Footprint](https://img.shields.io/badge/GGUF_Q4__K__M-1.35_GB-10B981)](https://huggingface.co/tencent/Hy-MT3-1.8B-GGUF)

> **Tencent's Hy-MT3-1.8B** is an ultra-lightweight, Apache 2.0 multilingual translation model supporting **102 languages** in a **1.35 GB** quantized footprint, engineered for structure-locked JSON localization, custom game glossaries, and OCR-tolerant image translation.

---

## 📊 Production Test Workflows

| Workflow | Capability Tested | Input Artifact | Expected Deliverable |
| --- | --- | --- | --- |
| Zero-Breakage App Localizer | Translates UI values without mutating keys | Nested English app locale with variables | Interactive Hindi dashboard with locked keys |
| Game Rich-Text QA Studio | Enforces custom glossaries and XML tags | Hindi RPG dialogue with color tags | Interactive English QA viewer checking tag preservation |
| Noisy OCR Receipt Translator | Recovers and translates messy scanned text | Real commercial paper receipt scan | Split-pane visual inspector with cleaned Hindi |

---

## Quick Start (Windows PowerShell)

### Step 1: Setup Environment, Download Weights & Register Runtime

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install ollama rapidocr-onnxruntime huggingface_hub

hf download tencent/Hy-MT3-1.8B-GGUF Hy-MT3-1.8B-Q4_K_M.gguf --local-dir models/hy-mt3-1.8b-gguf

ollama create hy-mt3 -f Modelfile
```

### Step 2: Run Production Pipeline

```powershell
python main.py
```

---

## Practical Use Cases

- 🛡️ **Offline Enterprise Localization**: Translate internal software strings and user interfaces with zero external API calls.
- 🎮 **Indie Game Dialogue Pipelines**: Localize rich-text combat logs and UI spreadsheets while preserving color tags and lore terms.
- 🧾 **Receipt & Document OCR Recovery**: Clean up noisy optical character recognition text from scanned receipts and screenshots.
- 🌍 **Low-Resource Regional Expansion**: Reach 64 newly added Indic, European, and regional languages from a single local binary.
- ⚡ **Edge & Laptop CI Checks**: Run automated localization verification inside local developer environments without cloud GPU costs.

## Future Feature Roadmap

- 🚀 **Batch Subtitle Style Engine**: Add `.srt` timestamp-locked translation with selectable formal and casual tone presets.
- 📊 **TransRubric Quality Scoring**: Integrate Tencent's open-source rubric evaluator for automated 0–100 translation grading.
- 🧩 **YAML & XML Schema Support**: Extend structure-locked parsing to Kubernetes configs, Android XML, and Markdown docs.
- 🔄 **Long-Document 8K Chunker**: Add automatic sliding-window chunking for multi-page technical manuals.

---
<sub>**Keywords**: hy-mt3, hy-mt3 1.8b, tencent hy-mt3, hy-mt3 gguf, hy-mt3 ollama, hunyuan translation, microsoft translator, google translate alternative, ocr translation, ollama translation, tencent hunyuan, hy-mt2</sub>
