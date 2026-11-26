import html
import json
import re
import time
from pathlib import Path

import ollama  # pyright: ignore
from rapidocr_onnxruntime import RapidOCR  # pyright: ignore

MODEL_NAME = "hy-mt3"
INPUT_DIR, TEMPLATE_DIR, OUTPUT_DIR = Path("inputs"), Path("templates"), Path("outputs")


def query_hy_mt3(prompt: str) -> tuple[str, int, float]:
    """Query local Hy-MT3 Ollama model and return (text, tokens, elapsed_sec)."""
    start = time.time()
    try:
        resp = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
        dt = max(time.time() - start, 0.01)
        text = resp["message"]["content"].strip()
        tok = int(resp.get("eval_count") or max(len(text.split()), 1))
        return text, tok, dt
    except Exception as exc:
        return f"[Pending Ollama '{MODEL_NAME}': {exc}]", 0, max(time.time() - start, 0.01)


def format_rich_text(text: str) -> str:
    """Render <color>, <b>/<strong>, and {{var}}/%d placeholders into clean visual HTML."""
    safe = html.escape(text)
    safe = re.sub(r"&lt;color=(#[0-9A-Fa-f]{6})&gt;(.*?)&lt;/color&gt;", r'<span style="color:\1;font-weight:800">\2</span>', safe)
    safe = re.sub(r"&lt;(b|strong)&gt;(.*?)&lt;/\1&gt;", r"<strong>\2</strong>", safe)
    return re.sub(r"(\{\{[^}]+\}\}|\{[^}]+\}|%[ds])", r'<span class="var-chip">\1</span>', safe)


def render_html(tpl_name: str, out_name: str, replacements: dict[str, str]) -> str:
    content = (TEMPLATE_DIR / tpl_name).read_text(encoding="utf-8")
    for k, v in replacements.items():
        content = content.replace(f"{{{{{k}}}}}", v)
    out_path = OUTPUT_DIR / out_name
    out_path.write_text(content, encoding="utf-8")
    return str(out_path)


def flatten_kv(obj: dict, prefix: str = "") -> list[tuple[str, str]]:
    items = []
    for k, v in obj.items():
        key = f"{prefix}.{k}" if prefix else k
        items.extend(flatten_kv(v, key)) if isinstance(v, dict) else items.append((key, str(v)))
    return items


def render_kv_cards(pairs: list[tuple[str, str]]) -> str:
    return "\n".join(
        f'<div class="kv-item"><div class="kv-key">{html.escape(k)}</div>'
        f'<div class="kv-val">{format_rich_text(v)}</div></div>'
        for k, v in pairs
    )


def task_1_i18n_localizer() -> dict:
    """Task 1: Zero-Breakage i18n JSON App Localizer (English -> Hindi)."""
    raw_json = (INPUT_DIR / "1_i18n_localizer.json").read_text(encoding="utf-8")
    source_cards = render_kv_cards(flatten_kv(json.loads(raw_json)))
    prompt = (
        "### Task\nTranslate user-facing JSON values into Hindi.\n"
        "### Strict Rules\n1. Keep JSON structure and indentation exact.\n"
        "2. Translate ONLY user-facing values.\n3. NEVER translate keys, HTML tags, or {{var}}/%d/%s placeholders.\n\n"
        f"### Source Data\n{raw_json}"
    )
    out, tok, dt = query_hy_mt3(prompt)
    try:
        cleaned = re.sub(r"^```(?:json)?|```$", "", out, flags=re.M).strip()
        target_cards = render_kv_cards(flatten_kv(json.loads(cleaned)))
    except Exception:
        target_cards = render_kv_cards([("output", out)])

    out_path = render_html("1_i18n_localizer_template.html", "1_i18n_localizer.html", {
        "status_badge": "Live Ollama Output" if tok > 0 else "Pending Ollama Runtime",
        "lang_tabs": '<button class="tab-btn active" onclick="showLang(0)">English &rarr; Hindi</button>',
        "source_cards": source_cards,
        "target_panels": f'<div class="lang-panel active">{target_cards}</div>',
    })
    return {"task": "i18n App Localizer (EN→HI)", "deliverable": out_path, "tokens": tok, "time": dt}


def task_2_game_localization() -> dict:
    """Task 2: Game Rich-Text & Glossary Localization Studio (Hindi -> English)."""
    payload = json.loads((INPUT_DIR / "2_game_localization.json").read_text(encoding="utf-8"))
    target_lang = payload.get("target_lang", "English")
    gloss_txt = "\n".join(f"{k} translates to {v}" for k, v in payload["glossary"].items())
    gloss_pills = "\n".join(f'<span class="g-pill">{html.escape(k)} &rarr; {html.escape(v)}</span>' for k, v in payload["glossary"].items())
    src_block = "\n".join(payload["lines"])
    prompt = (
        f"Reference the following translations:\n{gloss_txt}\n\n"
        f"Accurately translate into {target_lang}. Retain the exact number of delimiters and tags without omitting or escaping them. "
        f"ONLY output the translated result:\n\n{src_block}"
    )
    out, tok, dt = query_hy_mt3(prompt)
    tag_ok = out.count("<color=") == src_block.count("<color=") and out.count("{") == src_block.count("{")
    badge_cls, badge_txt = ("qa-check", "Tags Matched") if tag_ok else ("qa-check warn", "Tag Mismatch")
    src_lines_html = "\n".join(f'<div class="qa-line">{format_rich_text(l)}</div>' for l in payload["lines"])
    out_lines_html = "\n".join(f'<div class="qa-line">{format_rich_text(l)}</div>' for l in out.splitlines() if l.strip())
    card = (
        f'<div class="qa-card"><div class="qa-head"><span class="qa-lang">Hindi &rarr; {target_lang}</span>'
        f'<span class="{badge_cls}">{badge_txt}</span></div><div class="qa-grid">'
        f'<div class="qa-box"><div class="qa-box-label">Source RPG Lines (Hindi)</div>{src_lines_html}</div>'
        f'<div class="qa-box"><div class="qa-box-label">Translated Output ({target_lang})</div>{out_lines_html}</div>'
        f'</div></div>'
    )
    out_path = render_html("2_game_localization_template.html", "2_game_localization.html", {
        "status_badge": "Live Ollama Output" if tok > 0 else "Pending Ollama Runtime",
        "glossary_pills": gloss_pills,
        "qa_cards": card,
    })
    return {"task": "Game Localization QA (HI→EN)", "deliverable": out_path, "tokens": tok, "time": dt}


def task_3_ocr_translator() -> dict:
    """Task 3: Noisy OCR Receipt & Sign Recovery Translator (English -> Hindi)."""
    ocr_res, _ = RapidOCR()(str(INPUT_DIR / "3_ocr_translator.png"))
    raw_lines = [item[1] for item in (ocr_res or [])]
    raw_text = "\n".join(raw_lines) or "[No OCR text detected]"
    prompt = f"Translate the following text into Hindi. Output ONLY the translated result:\n\n{raw_text}"
    out, tok, dt = query_hy_mt3(prompt)
    out_path = render_html("3_ocr_translator_template.html", "3_ocr_translator.html", {
        "status_badge": "Live Ollama Output" if tok > 0 else "Pending Ollama Runtime",
        "image_path": "../inputs/3_ocr_translator.png",
        "raw_ocr_cards": "\n".join(f'<div class="line-card">{html.escape(x)}</div>' for x in raw_lines),
        "translated_cards": "\n".join(f'<div class="line-card">{html.escape(x)}</div>' for x in out.splitlines() if x.strip()),
    })
    return {"task": "Noisy OCR Translator (EN→HI)", "deliverable": out_path, "tokens": tok, "time": dt}


def update_benchmark_report(results: list[dict]) -> None:
    rows = [
        "# Hy-MT3-1.8B Generation Benchmark Report", "",
        "| Task | Deliverable | Tokens Generated | Time (sec) | Speed (tok/s) | Model Memory Footprint |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in results:
        spd = f"{(r['tokens'] / r['time']):.1f}" if r["tokens"] > 0 and r["time"] > 0 else "0.0"
        rows.append(f"| {r['task']} | {r['deliverable']} | {r['tokens']} | {r['time']:.2f} | {spd} | 1.35 GB (Q4_K_M) |")
    (OUTPUT_DIR / "generation_benchmark_report.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


TASKS = [task_1_i18n_localizer, task_2_game_localization, task_3_ocr_translator]
if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    update_benchmark_report([fn() for fn in TASKS])
    print("Completed 3 Hy-MT3 workflows. Benchmark report saved to outputs/generation_benchmark_report.md")
