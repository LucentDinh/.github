#!/usr/bin/env python3
"""Generate LucentDinh/.github/profile/README.md from public repositories in the org."""
import json
import os
import pathlib
import urllib.request

ORG = os.environ.get("GITHUB_ORG", "LucentDinh")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

GROUPS = [
    ("video-production", "AI Video, Dựng Phim & Livestream"),
    ("voice-audio", "Giọng Nói AI, TTS & Audiobook"),
    ("social-content", "Mạng Xã Hội, Content & Xuất Bản"),
    ("agent-coding", "AI Agent, Coding & Điều Phối"),
    ("ui-design", "UI/UX, Thiết Kế & Visualization"),
    ("ocr-rag-knowledge", "OCR, Document AI, RAG & Tri Thức"),
    ("browser-automation", "Browser, Scraping, Download & Tiện Ích"),
    ("domain-security", "Bảo Mật, HealthTech, FinTech & Khác"),
]

CORE_HIGHLIGHTS = [
    ("CLIProxyAPI", "Proxy API tương thích OpenAI/Gemini/Claude/Codex tích hợp OAuth & load-balancing."),
    ("Concat", "Trình dựng video local-first đa nền tảng viết bằng Rust, hỗ trợ JSON-RPC & MCP."),
    ("CapCap", "Ứng dụng Windows bản địa hóa & lồng tiếng video ngắn tối ưu tiếng Việt."),
    ("creatorhub", "Bảng điều khiển theo dõi, thu thập và phân phối nội dung đa nền tảng."),
    ("lemo-opuscar", "Bộ 99+ phong cách dựng phim bằng code cho Claude Code."),
    ("ShardBrowser", "Trình duyệt anti-detect mã nguồn mở trên Chromium phục vụ automation."),
    ("CloakBrowser", "Chromium stealth vượt bot detection thay thế trực tiếp cho Playwright."),
    ("VoiceStudio", "Studio nhân bản giọng nói & lồng tiếng AI chạy hoàn toàn local."),
    ("ZeroTTS", "Engine TTS tiếng Việt zero-shot nhẹ, chạy real-time trên CPU."),
    ("platform-policy-skills", "Bộ Codex skills kiểm duyệt nội dung theo chính sách YouTube, TikTok & TikTok Shop."),
]


def fetch_public_repos() -> list[dict]:
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{ORG}/repos?type=public&per_page=100&page={page}"
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "LucentDinh-Profile-Sync"}
        if TOKEN:
            headers["Authorization"] = f"Bearer {TOKEN}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            batch = json.loads(resp.read().decode("utf-8"))
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return [r for r in repos if not r.get("private") and r.get("name") != ".github"]


def render_markdown(repos: list[dict]) -> str:
    group_keys = [k for k, _ in GROUPS]
    buckets: dict[str, list[dict]] = {k: [] for k in group_keys}
    buckets["other"] = []

    for r in repos:
        topics = r.get("topics") or []
        matched = next((g for g in group_keys if g in topics), "other")
        buckets[matched].append(r)

    total_public = len(repos)
    lines = [
        f"# {ORG} — Vibecode & AI Automation Hub",
        "",
        "Kho lưu trữ và tuyển chọn các dự án **AI Video Production**, **Agentic Coding**, **OCR / RAG** và **Browser Automation** của team **LucentDinh**.",
        "",
        f"> Đang quản lý **{total_public} public repositories** được phân loại theo **8 nhóm lĩnh vực** (`group`), **4 cấp độ ưu tiên** (`tier`) và **3 trạng thái nguồn** (`ownership`).",
        "",
        "```mermaid",
        "flowchart LR",
        '    R["Browser & Scraping"] --> A["AI Agent & Scripts"]',
        '    A --> V["AI Video & Voice TTS"]',
        '    U["UI/UX & Diagrams"] --> V',
        '    D["OCR & RAG Knowledge"] --> A',
        '    V --> S["Social Distribution & Audit"]',
        '    Sec["Security & Domain Apps"] --> A',
        "```",
        "",
        "## Lọc nhanh theo Phân loại (Custom Properties & Topics)",
        "",
        "| Nhóm (`props.group`) | Mô tả | Số repo | Lọc nhanh |",
        "| :--- | :--- | :-: | :--- |",
    ]

    for gkey, glabel in GROUPS:
        cnt = len(buckets[gkey])
        p_url = f"https://github.com/orgs/{ORG}/repositories?q=props.group%3A{gkey}"
        t_url = f"https://github.com/orgs/{ORG}/repositories?q=topic%3A{gkey}"
        lines.append(f"| `{gkey}` | {glabel} | {cnt} | [Property]({p_url}) · [Topic]({t_url}) |")

    if buckets["other"]:
        lines.append(f"| `other` | Chưa gắn nhóm | {len(buckets['other'])} | [Repositories](https://github.com/orgs/{ORG}/repositories) |")

    lines.extend([
        "",
        "**Lọc theo mức độ ưu tiên (`props.tier`) & nguồn (`props.ownership`):**",
        f"- **Tier:** [Core (`core`)](https://github.com/orgs/{ORG}/repositories?q=props.tier%3Acore) · "
        f"[Đang phát triển (`active-dev`)](https://github.com/orgs/{ORG}/repositories?q=props.tier%3Aactive-dev) · "
        f"[Agent Skills (`skill-pack`)](https://github.com/orgs/{ORG}/repositories?q=props.tier%3Askill-pack) · "
        f"[Tham khảo (`watchlist`)](https://github.com/orgs/{ORG}/repositories?q=props.tier%3Awatchlist)",
        f"- **Ownership:** [Team tự viết (`original`)](https://github.com/orgs/{ORG}/repositories?q=props.ownership%3Aoriginal) · "
        f"[Có tùy biến (`customized`)](https://github.com/orgs/{ORG}/repositories?q=props.ownership%3Acustomized) · "
        f"[Fork chuẩn upstream (`upstream-fork`)](https://github.com/orgs/{ORG}/repositories?q=props.ownership%3Aupstream-fork)",
        "",
        "---",
        "",
        "## Dự án Nòng cốt (Core Highlights)",
        "",
        "| Repository | Vai trò chính |",
        "| :--- | :--- |",
    ])

    by_name = {r["name"]: r for r in repos}
    for cname, cdesc in CORE_HIGHLIGHTS:
        if cname in by_name:
            lang = by_name[cname].get("language") or "-"
            lines.append(f"| [{cname}](https://github.com/{ORG}/{cname}) (`{lang}`) | {cdesc} |")

    lines.extend([
        "",
        "---",
        "",
        "## Danh mục đầy đủ theo Nhóm *(Bấm để mở rộng)*",
        "",
    ])

    all_sections = list(GROUPS) + ([("other", "Chưa phân nhóm")] if buckets["other"] else [])
    for gkey, glabel in all_sections:
        items = sorted(buckets[gkey], key=lambda x: x["name"].lower())
        lines.extend([
            f"<details>",
            f"<summary><strong>{glabel}</strong> (<code>{gkey}</code> — {len(items)} repos)</summary>",
            "",
            f"> Lọc nhanh: [props.group:{gkey}](https://github.com/orgs/{ORG}/repositories?q=props.group%3A{gkey}) · [topic:{gkey}](https://github.com/orgs/{ORG}/repositories?q=topic%3A{gkey})",
            "",
            "| Repository | Ngôn ngữ | Mô tả |",
            "| :--- | :-: | :--- |",
        ])
        for info in items:
            rname = info["name"]
            lang = info.get("language") or "-"
            desc = (info.get("description") or "").replace("|", "\\|").replace("\n", " ").strip()
            if len(desc) > 130:
                desc = desc[:127] + "..."
            lines.append(f"| [{rname}](https://github.com/{ORG}/{rname}) | `{lang}` | {desc or '-'} |")
        lines.extend([
            "",
            "</details>",
            "",
        ])

    return "\n".join(lines).rstrip() + "\n"


if __name__ == "__main__":
    data = fetch_public_repos()
    out = pathlib.Path("profile/README.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(data), encoding="utf-8")
    print(f"Updated profile/README.md with {len(data)} public repos.")
