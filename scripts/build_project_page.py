#!/usr/bin/env python3
import datetime as dt
import hashlib
import json
import math
import re
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES_ROOT = ROOT / "static" / "images"
REPORTS_DIR = ROOT / "reports"
DATA_DIR = ROOT / "data"
PROCESSED_DIR = ROOT / "static" / "processed" / "project"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"}

BODIES = [
    {"id": "sri-lanka-2026", "place": "Sri Lanka", "year": "2026", "layout": "horizontal-masonry-snap"},
    {"id": "raja-2024", "place": "Raja Ampat", "year": "2024", "layout": "horizontal-masonry-snap"},
    {"id": "ningaloo-2024", "place": "Ningaloo", "year": "2024", "layout": "horizontal-masonry-snap"},
    {"id": "tonga-2025", "place": "Tonga", "year": "2025", "layout": "horizontal-masonry-snap"},
    {"id": "ningaloo-2025", "place": "Ningaloo", "year": "2025", "layout": "horizontal-masonry-snap"},
]

SUBJECT_KEYWORDS = {
    "people": ["people", "crew", "guest", "sally", "johanna", "emma", "bumble", "sanch", "winkie", "blonde", "plow", "boatgals", "miesa", "ethan", "bwr"],
    "wildlife": ["whale", "shark", "manta", "turtle", "dolphin", "jellyfish", "batfish", "orca", "stingray", "fish", "puffers", "leopard"],
    "detail": ["coral", "bleech", "food", "close", "macro"],
    "wide": ["view", "journey", "safari", "arieal", "aerial", "landscape", "boat", "sea", "waterhabitat"],
}


def run(cmd):
    return subprocess.run(cmd, check=False, capture_output=True, text=True)


def list_images():
    files = []
    for p in IMAGES_ROOT.rglob("*"):
        if p.is_file() and p.suffix in IMAGE_EXTS:
            files.append(p)
    return sorted(files)


def read_sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_sips_dimensions(path):
    proc = run(["/usr/bin/sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)])
    width = None
    height = None
    for line in proc.stdout.splitlines():
        if "pixelWidth:" in line:
            width = int(line.split(":", 1)[1].strip())
        if "pixelHeight:" in line:
            height = int(line.split(":", 1)[1].strip())
    return width, height


def read_exif_date(path):
    proc = run(["/usr/bin/mdls", "-raw", "-name", "kMDItemContentCreationDate", str(path)])
    val = proc.stdout.strip()
    if not val or val == "(null)":
        return None
    return val


def near_hash(path):
    tmp_dir = ROOT / ".tmp_project_hash"
    tmp_dir.mkdir(exist_ok=True)
    out = tmp_dir / f"{hashlib.md5(str(path).encode()).hexdigest()}.jpg"
    run(["/usr/bin/sips", "-s", "format", "jpeg", "--resampleHeightWidthMax", "48", str(path), "--out", str(out)])
    if not out.exists():
        return None
    h = hashlib.sha1()
    with out.open("rb") as f:
        h.update(f.read())
    return h.hexdigest()


def orientation(width, height):
    if not width or not height:
        return "unknown"
    if width == height:
        return "square"
    return "landscape" if width > height else "portrait"


def infer_year_from_name(name):
    m = re.search(r"(20\d{2})", name)
    return m.group(1) if m else None


def group_body(rel_path, exif_date):
    low = rel_path.lower()
    exif_year = None
    if exif_date:
        m = re.search(r"(20\d{2})", exif_date)
        if m:
            exif_year = m.group(1)

    inferred = infer_year_from_name(low)
    year = inferred or exif_year

    has_sri = ("sri" in low and "lanka" in low) or "srilanka" in low
    has_raja = "raja" in low
    has_ning = "ningaloo" in low
    has_tonga = "tonga" in low

    if has_sri:
        return "sri-lanka-2026", "filename-location"
    if has_raja and (year == "2024" or year is None):
        return "raja-2024", "filename-location-year"
    if has_ning and year == "2024":
        return "ningaloo-2024", "filename-location-year"
    if has_tonga and year == "2025":
        return "tonga-2025", "filename-location-year"
    if has_ning and year == "2025":
        return "ningaloo-2025", "filename-location-year"

    return "unassigned", "uncertain"


def classify_subject(rel_path):
    low = rel_path.lower()
    for kind, words in SUBJECT_KEYWORDS.items():
        if any(w in low for w in words):
            return kind
    return "medium"


def score_image(meta):
    low = meta["filepath"].lower()
    score = 0
    subject = classify_subject(meta["filepath"])
    if subject == "wildlife":
        score += 4
    if subject == "people":
        score += 3
    if subject == "wide":
        score += 2
    if meta["orientation"] == "landscape":
        score += 2
    if "journey" in low or "safari" in low:
        score += 1
    if "value-" in low or "manifesto" in low:
        score -= 5
    if "malapasqua" in low or "komodo" in low or "colombia" in low or "jurien" in low:
        score -= 3
    return score


def alt_from_filename(rel_path):
    stem = Path(rel_path).stem
    stem = stem.replace(".", "-")
    words = re.sub(r"[^a-zA-Z0-9]+", " ", stem).strip().split()
    filtered = [w for w in words if not re.fullmatch(r"\d+", w) and w.lower() not in {"phish", "peopleinplace", "peopleinplaces", "waterhabitat", "journey"}]
    text = " ".join(filtered[:8]).strip()
    if not text:
        text = "Underwater and travel documentary moment"
    return text.capitalize()


def slug_for(rel_path):
    no_ext = str(Path(rel_path).with_suffix(""))
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", no_ext.strip("/"))
    return slug.lower().strip("-")


def unique_by_near_hash(candidates):
    buckets = {}
    for c in candidates:
        key = c.get("near_hash") or c["sha256"]
        prev = buckets.get(key)
        if prev is None:
            buckets[key] = c
            continue
        if score_image(c) > score_image(prev):
            buckets[key] = c
        elif score_image(c) == score_image(prev) and c["filesize"] > prev["filesize"]:
            buckets[key] = c
    return list(buckets.values())


def curate_body(candidates):
    uniq = unique_by_near_hash(candidates)
    for m in uniq:
        m["_score"] = score_image(m)
        m["_subject"] = classify_subject(m["filepath"])

    uniq.sort(key=lambda x: (x["_score"], x["filesize"]), reverse=True)
    total = len(uniq)
    target = min(36, total)
    if total >= 18:
        target = min(max(18, math.ceil(total * 0.7)), 30)

    groups = defaultdict(list)
    for m in uniq:
        groups[m["_subject"]].append(m)

    order = ["wide", "people", "wildlife", "detail", "medium"]
    selected = []
    while len(selected) < target:
        added = False
        for kind in order:
            if groups[kind]:
                selected.append(groups[kind].pop(0))
                added = True
                if len(selected) == target:
                    break
        if not added:
            break

    selected.sort(key=lambda x: (x.get("exif_date") or "", x["filepath"]))
    return selected


def pick_break_image(items, preferred_subjects=("wide", "wildlife", "people")):
    ranked = sorted(items, key=lambda x: (x["orientation"] == "landscape", x.get("_score", score_image(x)), x["filesize"]), reverse=True)
    for subj in preferred_subjects:
        for item in ranked:
            if classify_subject(item["filepath"]) == subj:
                return item
    return ranked[0] if ranked else None


def ensure_dirs():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def resize_jpg(src, dest, width):
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(["/usr/bin/sips", "-s", "format", "jpeg", "--resampleWidth", str(width), str(src), "--out", str(dest)])


def gather_referenced_images_elsewhere():
    refs = set()
    roots = [ROOT / "content", ROOT / "data", ROOT / "layouts", ROOT / "assets"]
    image_ref = re.compile(r'(?<![A-Za-z0-9])/?images/[A-Za-z0-9._/\-]+')
    skip_prefixes = [
        str((ROOT / "content" / "project").resolve()),
        str((ROOT / "content" / "en" / "project").resolve()),
        str((ROOT / "layouts" / "project").resolve()),
        str((ROOT / "layouts" / "partials" / "project").resolve()),
    ]
    skip_exact = {
        str((ROOT / "data" / "project.yaml").resolve()),
    }

    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            resolved = str(path.resolve())
            if resolved in skip_exact:
                continue
            if any(resolved.startswith(prefix) for prefix in skip_prefixes):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for match in image_ref.findall(text):
                normalized = match if match.startswith("/") else f"/{match}"
                suffix = Path(normalized).suffix.lower()
                if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
                    refs.add(normalized)
    return refs


def dedupe_keep_order(items):
    seen = set()
    out = []
    for item in items:
        key = item["filepath"]
        if key in seen:
            continue
        out.append(item)
        seen.add(key)
    return out


def pop_break_image(items, used_paths, preferred_subjects=("wide", "wildlife", "people")):
    ranked = sorted(items, key=lambda x: (x["orientation"] == "landscape", x.get("_score", score_image(x)), x["filesize"]), reverse=True)
    for subj in preferred_subjects:
        for candidate in ranked:
            if candidate["filepath"] in used_paths:
                continue
            if classify_subject(candidate["filepath"]) == subj:
                items.remove(candidate)
                used_paths.add(candidate["filepath"])
                return candidate
    for candidate in ranked:
        if candidate["filepath"] in used_paths:
            continue
        items.remove(candidate)
        used_paths.add(candidate["filepath"])
        return candidate
    return None


def top_up_body(items, pool, used_paths, minimum=18, maximum=36):
    if len(items) >= minimum:
        return items[:maximum]
    pool_unique = unique_by_near_hash(pool)
    pool_unique.sort(key=lambda x: (score_image(x), x["filesize"]), reverse=True)
    existing = {i["filepath"] for i in items}
    for candidate in pool_unique:
        fp = candidate["filepath"]
        if fp in existing or fp in used_paths:
            continue
        items.append(candidate)
        used_paths.add(fp)
        existing.add(fp)
        if len(items) >= minimum:
            break
    items.sort(key=lambda x: (x.get("exif_date") or "", x["filepath"]))
    return items[:maximum]


def build():
    ensure_dirs()
    image_files = list_images()
    referenced_elsewhere = gather_referenced_images_elsewhere()

    manifest = []
    near_groups = defaultdict(list)
    exact_groups = defaultdict(list)

    for path in image_files:
        rel = "/" + str(path.relative_to(ROOT / "static")).replace("\\", "/")
        size = path.stat().st_size
        width, height = parse_sips_dimensions(path)
        exif = read_exif_date(path)
        sha = read_sha256(path)
        n_hash = near_hash(path)
        grp, grp_reason = group_body(rel, exif)

        item = {
            "filepath": rel,
            "dimensions": {"width": width, "height": height},
            "filesize": size,
            "exif_date": exif,
            "orientation": orientation(width, height),
            "sha256": sha,
            "near_hash": n_hash,
            "group": grp,
            "group_reason": grp_reason,
            "subject": classify_subject(rel),
        }
        manifest.append(item)
        exact_groups[sha].append(rel)
        if n_hash:
            near_groups[n_hash].append(rel)

    exact_dups = {k: v for k, v in exact_groups.items() if len(v) > 1}
    near_dups = {k: v for k, v in near_groups.items() if len(v) > 1}

    by_group = defaultdict(list)
    for m in manifest:
        by_group[m["group"]].append(m)

    curated = {}
    body_pools = {}
    used_gallery = set()
    for body in BODIES:
        bid = body["id"]
        allowed = [m for m in by_group.get(bid, []) if m["filepath"] not in referenced_elsewhere]
        body_pools[bid] = allowed
        picks = curate_body(allowed)
        picks = [p for p in picks if p["filepath"] not in used_gallery]
        picks = dedupe_keep_order(picks)
        for p in picks:
            used_gallery.add(p["filepath"])
        curated[bid] = picks

    used_break = set()
    br1 = pop_break_image(curated["sri-lanka-2026"], used_break)
    br2 = pop_break_image(curated["raja-2024"], used_break)
    br3a = pop_break_image(curated["ningaloo-2024"], used_break)
    br3b = pop_break_image(curated["tonga-2025"], used_break)
    br4 = pop_break_image(curated["tonga-2025"], used_break, preferred_subjects=("people", "wildlife", "wide"))
    br5 = pop_break_image(curated["ningaloo-2025"], used_break, preferred_subjects=("wide", "wildlife", "people"))

    used_all = set(used_break)
    for body in BODIES:
        for item in curated[body["id"]]:
            used_all.add(item["filepath"])

    for body in BODIES:
        bid = body["id"]
        curated[bid] = top_up_body(curated[bid], body_pools[bid], used_all, minimum=18, maximum=36)

    breaks = [
        {"between": ["sri-lanka-2026", "raja-2024"], "type": "fullpage", "images": [br1] if br1 else []},
        {"between": ["raja-2024", "ningaloo-2024"], "type": "halfheight", "images": [br2] if br2 else []},
        {"between": ["ningaloo-2024", "tonga-2025"], "type": "pair", "images": [i for i in [br3a, br3b] if i]},
        {"between": ["tonga-2025", "ningaloo-2025"], "type": "halfheight", "images": [br4] if br4 else []},
        {"endcap": True, "type": "fullpage", "images": [br5] if br5 else []},
    ]

    selected_all = []
    seen = set()
    for body in BODIES:
        for item in curated[body["id"]]:
            if item["filepath"] not in seen:
                selected_all.append(item)
                seen.add(item["filepath"])
    for b in breaks:
        for item in b["images"]:
            if item and item["filepath"] not in seen:
                selected_all.append(item)
                seen.add(item["filepath"])

    derivative_map = {}
    for item in selected_all:
        rel = item["filepath"]
        src = ROOT / "static" / rel.lstrip("/")
        slug = slug_for(rel)
        deriv = {
            "fullpage_jpg": f"/processed/project/{slug}_fullpage.jpg",
            "large_jpg": f"/processed/project/{slug}_large.jpg",
            "grid_jpg": f"/processed/project/{slug}_grid.jpg",
            "thumb_jpg": f"/processed/project/{slug}_thumb.jpg",
            "fullpage_webp": None,
            "large_webp": None,
            "grid_webp": None,
            "thumb_webp": None,
            "alt": alt_from_filename(rel),
            "source": rel,
        }
        full_dest = ROOT / "static" / deriv["fullpage_jpg"].lstrip("/")
        large_dest = ROOT / "static" / deriv["large_jpg"].lstrip("/")
        grid_dest = ROOT / "static" / deriv["grid_jpg"].lstrip("/")
        thumb_dest = ROOT / "static" / deriv["thumb_jpg"].lstrip("/")
        resize_jpg(src, full_dest, 2600)
        resize_jpg(src, large_dest, 2000)
        resize_jpg(src, grid_dest, 1600)
        resize_jpg(src, thumb_dest, 700)
        if full_dest.exists() and large_dest.exists() and grid_dest.exists() and thumb_dest.exists():
            derivative_map[rel] = deriv

    lines = []
    lines.append("project:")
    lines.append('  title: "The Project"')
    lines.append('  intro: ""')
    lines.append("  bodies:")

    for body in BODIES:
        bid = body["id"]
        lines.append(f'    - id: "{bid}"')
        lines.append(f'      place: "{body["place"]}"')
        lines.append(f'      year: "{body["year"]}"')
        lines.append(f'      layout: "{body["layout"]}"')
        lines.append("      images:")
        for item in curated[bid]:
            if item["filepath"] not in derivative_map:
                continue
            d = derivative_map[item["filepath"]]
            alt_text = d["alt"].replace('"', "")
            lines.append(f'        - path: "{d["large_jpg"]}"')
            lines.append(f'          grid_path: "{d["grid_jpg"]}"')
            lines.append(f'          fullpage_path: "{d["fullpage_jpg"]}"')
            lines.append(f'          thumb_path: "{d["thumb_jpg"]}"')
            lines.append(f'          source: "{d["source"]}"')
            lines.append(f'          alt: "{alt_text}"')

    lines.append("  breaks:")
    for br in breaks:
        if br.get("endcap"):
            lines.append("    - endcap: true")
        else:
            a, b = br["between"]
            lines.append(f'    - between: ["{a}", "{b}"]')
        lines.append(f'      type: "{br["type"]}"')
        lines.append("      images:")
        for item in br["images"]:
            if not item:
                continue
            if item["filepath"] not in derivative_map:
                continue
            d = derivative_map[item["filepath"]]
            alt_text = d["alt"].replace('"', "")
            use_path = d["fullpage_jpg"] if br["type"] == "fullpage" else d["large_jpg"]
            lines.append(f'        - path: "{use_path}"')
            lines.append(f'          source: "{d["source"]}"')
            lines.append(f'          alt: "{alt_text}"')

    (DATA_DIR / "project.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest_payload = {
        "generated_at": dt.datetime.now().isoformat(),
        "root": "/static/images",
        "total_images": len(manifest),
        "excluded_referenced_elsewhere": sorted(referenced_elsewhere),
        "images": manifest,
        "duplicate_groups": {
            "exact_sha256": exact_dups,
            "near_hash": near_dups,
        },
        "group_counts": {k: len(v) for k, v in sorted(by_group.items())},
    }
    (REPORTS_DIR / "project-image-manifest.json").write_text(json.dumps(manifest_payload, indent=2), encoding="utf-8")

    md = []
    md.append("# Project Image Manifest")
    md.append("")
    md.append(f"Generated: {dt.datetime.now().isoformat()}")
    md.append("")
    md.append(f"Total images scanned: {len(manifest)}")
    md.append(f"Excluded (already referenced elsewhere): {len(referenced_elsewhere)}")
    md.append("")
    md.append("## Group counts")
    md.append("")
    for key, vals in sorted(by_group.items()):
        md.append(f"- {key}: {len(vals)}")
    md.append("")
    md.append("## Near duplicate groups")
    md.append("")
    near_list = [v for v in near_dups.values() if len(v) > 1]
    if not near_list:
        md.append("- None detected")
    else:
        for group in near_list:
            md.append(f"- group ({len(group)}):")
            for item in group:
                md.append(f"  - {item}")
    md.append("")
    md.append("## Detailed inventory")
    md.append("")
    md.append("| filepath | dimensions | size(bytes) | exif date | orientation | group |")
    md.append("|---|---:|---:|---|---|---|")
    for item in manifest:
        dims = f"{item['dimensions']['width']}x{item['dimensions']['height']}"
        md.append(f"| {item['filepath']} | {dims} | {item['filesize']} | {item['exif_date'] or ''} | {item['orientation']} | {item['group']} |")

    (REPORTS_DIR / "project-image-manifest.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    sel = []
    sel.append("# Project Image Selection")
    sel.append("")
    sel.append("## Grouping method")
    sel.append("")
    sel.append("- Grouped by location keywords in folder and filename.")
    sel.append("- Used year tokens in filenames and EXIF content creation date when present.")
    sel.append("- Images not confidently mapped were left in `unassigned`.")
    sel.append("- Excluded any image already referenced on other site pages.")
    sel.append("")
    sel.append("## Curation method")
    sel.append("")
    sel.append("- Removed exact and near duplicates using SHA-256 and resized-hash buckets.")
    sel.append("- Prioritized cinematic frames using filename cues for wildlife, people, wide scenes, and details.")
    sel.append("- Kept a mixed rhythm of landscape and portrait frames where available.")
    sel.append("")
    for body in BODIES:
        bid = body["id"]
        items = curated[bid]
        sel.append(f"## {body['place']} - {body['year']}")
        sel.append("")
        sel.append(f"- Layout: `{body['layout']}`")
        sel.append(f"- Selected images: {len(items)}")
        subject_counts = defaultdict(int)
        for i in items:
            subject_counts[classify_subject(i['filepath'])] += 1
        sel.append("- Variety mix: " + ", ".join(f"{k}={v}" for k, v in sorted(subject_counts.items())))
        sel.append("")
    sel.append("## Break images")
    sel.append("")
    for br in breaks:
        label = "endcap" if br.get("endcap") else f"{br['between'][0]} -> {br['between'][1]}"
        sel.append(f"- {label} ({br['type']}):")
        for item in br["images"]:
            sel.append(f"  - {item['filepath']} ({classify_subject(item['filepath'])}, {item['orientation']})")
    sel.append("")
    sel.append("## Notes")
    sel.append("")
    sel.append(f"- Unassigned images: {len(by_group.get('unassigned', []))}")
    sel.append(f"- Excluded as already used elsewhere: {len(referenced_elsewhere)}")
    sel.append("- WebP derivatives were not generated in this environment due missing local WebP encoder support.")

    (REPORTS_DIR / "project-image-selection.md").write_text("\n".join(sel) + "\n", encoding="utf-8")

    shutil.rmtree(ROOT / ".tmp_project_hash", ignore_errors=True)


if __name__ == "__main__":
    build()
