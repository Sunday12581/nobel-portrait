#!/usr/bin/env python3
"""Build an offline, single-person portrait page. Never generates or invents a face."""
import argparse
import base64
import html
import io
import json
import mimetypes
from pathlib import Path
from string import Template

TEXT_FIELDS = ("name", "prize", "birth", "birthplace", "affiliation", "affiliation_address", "motivation")
INVENTABLE = set(TEXT_FIELDS) | {"year", "prize_share"}
LABELS = {
    "zh": {
        "brand_label": "诺贝尔风格肖像 · 个人创作", "nav_label": "页面导航", "sidebar_label": "人物目录",
        "profile_label": "人物介绍", "facts_label": "人物资料", "motivation_label": "获奖理由", "downloads_label": "下载肖像",
        "overview_label": "概览", "creative_badge": "创作获奖情景", "creative_note_short": "单人物创作档案",
        "born_label": "出生：", "affiliation_label": "获奖时单位：", "motivation_label_full": "获奖理由：", "share_label": "奖项份额：",
        "citation_label": "关于本作品", "creative_note": "个人创作展示，非官方获奖记录。标注“创作设定”的人物资料由 AI 根据本次创作需求补全。",
        "back_label": "返回页首", "invented": "创作设定", "portrait_alt": "{name}的黑墨与赭金色手绘风格肖像",
        "credit": "AI 生成肖像 · 用户照片转绘", "download": "下载",
    },
    "en": {
        "brand_label": "Nobel-style portrait · personal creative work", "nav_label": "Page navigation", "sidebar_label": "Profile contents",
        "profile_label": "Profile", "facts_label": "Facts", "motivation_label": "Prize motivation", "downloads_label": "Download portrait",
        "overview_label": "Summary", "creative_badge": "Imagined award scenario", "creative_note_short": "A single-person creative profile",
        "born_label": "Born: ", "affiliation_label": "Affiliation at the time of the award: ", "motivation_label_full": "Prize motivation: ", "share_label": "Prize share: ",
        "citation_label": "About this work", "creative_note": "Personal creative work; not an official award record. Fields marked Imagined were authored by AI for this creative scenario.",
        "back_label": "Go to the top of the page", "invented": "Imagined", "portrait_alt": "Black-ink and ochre-gold illustrated portrait of {name}",
        "credit": "AI-generated portrait based on the supplied photograph", "download": "Download",
    },
}

def read_profile(path):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("Profile must be a JSON object")
    for key in TEXT_FIELDS:
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"Missing or invalid text field: {key}")
    year = data.get("year")
    if isinstance(year, bool) or not isinstance(year, (int, str)) or not str(year).isdigit() or not 1 <= int(year) <= 9999:
        raise ValueError("year must be an integer from 1 to 9999")
    data["year"] = int(year)
    language = data.get("language", "zh")
    if not isinstance(language, str) or language not in LABELS:
        raise ValueError("language must be zh or en")
    data["language"] = language
    invented = data.get("invented_fields")
    if not isinstance(invented, list) or any(not isinstance(k, str) or k not in INVENTABLE for k in invented):
        raise ValueError("invented_fields must be an explicit list of supported field names")
    data["invented_fields"] = list(dict.fromkeys(invented))
    if "prize_share" not in data:
        data["prize_share"] = "1/1"
        if "prize_share" not in data["invented_fields"]:
            data["invented_fields"].append("prize_share")
    if not isinstance(data["prize_share"], str) or not data["prize_share"].strip():
        raise ValueError("prize_share must be a nonempty string")
    if "portrait_credit" in data and (not isinstance(data["portrait_credit"], str) or not data["portrait_credit"].strip()):
        raise ValueError("portrait_credit must be a nonempty string")
    return {key: data[key] for key in (*TEXT_FIELDS, "year", "language", "invented_fields", "prize_share", "portrait_credit") if key in data}

def image_bytes(path, keep_original):
    suffix = path.suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise ValueError("Portrait must be PNG, JPEG or WebP")
    raw = path.read_bytes()
    if keep_original:
        return {"portrait" + suffix: (raw, mimetypes.guess_type(path.name)[0])}, None
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise ValueError("PNG/JPG export requires Pillow. Use --keep-original to build without conversion.") from exc
    with Image.open(io.BytesIO(raw)) as opened:
        opened.load()
        image = ImageOps.exif_transpose(opened)
        if image.mode in {"RGBA", "LA"} or "transparency" in image.info:
            rgba = image.convert("RGBA")
            image = Image.new("RGB", rgba.size, (244, 241, 233))
            image.paste(rgba, mask=rgba.getchannel("A"))
        else:
            image = image.convert("RGB")
        # Copy pixels without source EXIF, metadata or thumbnails; never resize.
        clean = Image.new("RGB", image.size)
        clean.paste(image)
        png, jpg = io.BytesIO(), io.BytesIO()
        clean.save(png, format="PNG", optimize=True)
        clean.save(jpg, format="JPEG", quality=95, subsampling=0)
        return {"portrait.png": (png.getvalue(), "image/png"), "portrait.jpg": (jpg.getvalue(), "image/jpeg")}, clean.size

def render(profile, images, embed):
    labels = LABELS[profile["language"]]
    esc = lambda value: html.escape(str(value), quote=True)
    values = {key: esc(value) for key, value in labels.items()}
    values.update({key: esc(profile[key]) for key in (*TEXT_FIELDS, "year", "prize_share")})
    for key in INVENTABLE:
        values[key + "_mark"] = (' <span class="invented">' + esc(labels["invented"]) + '</span>') if key in profile["invented_fields"] else ""
    values["lang"] = profile["language"]
    values["title"] = esc(f'{profile["name"]} — {profile["prize"]} {profile["year"]}')
    values["description"] = esc(f'{profile["name"]} · {profile["prize"]} {profile["year"]} · {labels["creative_badge"]}')
    values["portrait_alt"] = esc(labels["portrait_alt"].format(name=profile["name"]))
    values["portrait_credit"] = esc(profile.get("portrait_credit", labels["credit"]))
    values["citation_text"] = values["title"] + ". " + esc(labels["creative_note_short"]) + "."
    sources = {name: ("data:" + mime + ";base64," + base64.b64encode(raw).decode("ascii")) if embed else name for name, (raw, mime) in images.items()}
    values["portrait_src"] = sources[next(iter(images))]
    values["download_links"] = "\n".join(
        '<a href="' + sources[name] + '" download="' + esc(name) + '">' + esc(labels["download"] + " " + name.rsplit(".", 1)[-1].upper()) + '</a>'
        for name in images
    )
    template = Path(__file__).resolve().parents[1] / "assets" / "page-template.html"
    return Template(template.read_text(encoding="utf-8")).substitute(values)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--portrait", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--keep-original", action="store_true", help="Copy input format instead of PNG/JPG conversion; no Pillow dependency")
    args = parser.parse_args()
    try:
        profile = read_profile(args.profile)
        images, size = image_bytes(args.portrait, args.keep_original)
        pages = {"index.html": render(profile, images, False), "standalone.html": render(profile, images, True)}
        if args.out.exists() and (not args.out.is_dir() or any(args.out.iterdir())):
            raise ValueError("Output directory must be new or empty; choose a new version to avoid overwriting")
        args.out.mkdir(parents=True, exist_ok=True)
        for name, (raw, _) in images.items():
            (args.out / name).write_bytes(raw)
        for name, content in pages.items():
            (args.out / name).write_text(content, encoding="utf-8")
        (args.out / "profile.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output": str(args.out.resolve()), "files": [*pages, *images, "profile.json"], "portrait_size": size, "embedded_page": "standalone.html"}, ensure_ascii=False))
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f"Error: {exc}\n")

if __name__ == "__main__":
    main()
