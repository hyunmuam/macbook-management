#!/usr/bin/env python3
"""원칙 문서(.md)를 HTML로 렌더링한다.

정본은 저장소 루트의 마크다운 문서다. 이 script는 생성만 하고 내용을 바꾸지 않는다.
표준 라이브러리만 사용한다.

사용법:
    python3 tools/render.py                       저장소 전체를 docs/ 로 렌더링한다
    python3 tools/render.py <repo> <out> [문서.md ...]
"""

import html
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------- 척추 절 역할
# AGENTS.md가 다섯 원칙 문서의 아홉 척추 절을 보장한다. 절 이름으로 렌더링을 분기한다.
SPINE = {
    "문서 목적": "purpose",
    "기본 환경": "env",
    "전체 구성": "structure",
    "구성 원칙": "principles",
    "설정 방법": "setup",
    "검증": "verify",
    "이후 사용 및 유지보수": "maintain",
    "현재 범위 밖의 항목": "scope",
    "핵심 요약": "summary",
}

SPINE_EXTRA = {"문서": "doclist", "적용 기준": "env"}

REPO_BLOB = "https://github.com/hyunmuam/macbook-management/blob/main"

DOC_TITLES = {
    "software-installation.md": "소프트웨어 설치 원칙",
    "directory-management.md": "디렉토리 관리 원칙",
    "development-environment.md": "개발환경 구성 원칙",
    "shell-configuration.md": "Shell 설정 원칙",
    "git-and-ssh.md": "Git과 GitHub SSH 설정 원칙",
    "reinstallation.md": "재설치 원칙",
}

# 핵심 요약을 문서 맨 위로 끌어올린다. 끄면 md와 같은 순서로 렌더링한다.
LIFT_SUMMARY = True


# -------------------------------------------------------------------- 인라인
def strip_num(text: str) -> tuple[str, str]:
    """`5.2.1 제목` -> ("5.2.1", "제목")"""
    m = re.match(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$", text)
    return (m.group(1), m.group(2)) if m else ("", text)


def slugify(text: str) -> str:
    """GitHub의 앵커 생성 규칙을 따른다. md 내부 앵커 링크를 그대로 쓰기 위해서다."""
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text.strip().lower())
    s = s.replace("`", "")
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    return re.sub(r"\s+", "-", s.strip())


def rewrite_href(url: str) -> str:
    if url.startswith(("http://", "https://", "#", "mailto:")):
        return url
    path, _, anchor = url.partition("#")
    if path.endswith(".md"):
        if path == "README.md":
            path = "index.html"
        elif path in DOC_TITLES:
            path = path[:-3] + ".html"
        else:
            # AGENTS.md처럼 사이트에 싣지 않는 문서는 저장소 원본을 가리킨다
            return f"{REPO_BLOB}/{url}"
    return path + ("#" + anchor if anchor else "")


def inline(text: str) -> str:
    codes: list[str] = []

    def stash(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{html.escape(rewrite_href(m.group(2)), quote=True)}">{m.group(1)}</a>',
        text,
    )
    return re.sub(
        r"\x00(\d+)\x00",
        lambda m: "<code>" + html.escape(codes[int(m.group(1))], quote=False) + "</code>",
        text,
    )


# --------------------------------------------------------------------- 파서
LIST_RE = re.compile(r"^[-*]\s+")
OLIST_RE = re.compile(r"^\d+\.\s+")


def parse_blocks(text: str) -> list[tuple]:
    lines = text.split("\n")
    blocks: list[tuple] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            lang, body = line[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            blocks.append(("code", lang, "\n".join(body)))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            blocks.append(("heading", len(m.group(1)), m.group(2).strip()))
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            blocks.append(("table", rows))
            continue
        for pattern, kind in ((LIST_RE, "ul"), (OLIST_RE, "ol")):
            if pattern.match(line):
                items = []
                while i < len(lines) and pattern.match(lines[i]):
                    items.append(pattern.sub("", lines[i]).strip())
                    i += 1
                blocks.append((kind, items))
                break
        else:
            para = []
            while (
                i < len(lines)
                and lines[i].strip()
                and not lines[i].startswith(("|", "```", "#"))
                and not LIST_RE.match(lines[i])
                and not OLIST_RE.match(lines[i])
            ):
                para.append(lines[i].strip())
                i += 1
            blocks.append(("p", " ".join(para)))
    return blocks


def split_table(rows: list[str]) -> tuple[list[str], list[list[str]]]:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head = cells[0]
    body = [r for r in cells[2:]] if len(cells) > 2 else []
    return head, body


# ------------------------------------------------------------------- 렌더링
# 코드블록은 성격이 셋이다. 실행할 명령, 파일에 넣을 설정 조각, 읽기만 하는 도식·출력.
CMD_LANGS = {"sh", "bash", "shell"}
SNIPPET_LANGS = {"zsh", "sshconfig", "yaml", "toml", "ini", "json", "ruby", "properties"}


def render_code(lang: str, body: str) -> str:
    escaped = html.escape(body, quote=False)
    if lang in CMD_LANGS or lang in SNIPPET_LANGS:
        cls, label, hint = (
            ("cmd", lang, "명령 복사")
            if lang in CMD_LANGS
            else ("snip", lang, "설정 조각 복사")
        )
        return (
            f'<div class="{cls}"><span class="lang">{html.escape(label)}</span>'
            f'<button class="copy" type="button" aria-label="{hint}">복사</button>'
            f"<pre><code>{escaped}</code></pre></div>"
        )
    lines = body.rstrip("\n").split("\n")
    if len(lines) == 1:  # `yyyymmdd_keyword.ext`처럼 한 줄짜리는 박스가 과하다
        return f'<p class="oneline"><code>{escaped}</code></p>'
    return f'<div class="map"><pre>{escaped}</pre></div>'


def render_table(rows: list[str]) -> str:
    head, body = split_table(rows)
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    trs = ""
    for r in body:
        tds = ""
        for i, c in enumerate(r):
            label = html.escape(re.sub(r"[`*]", "", head[i]), quote=True) if i < len(head) else ""
            tds += f'<td data-label="{label}">{inline(c)}</td>'
        trs += f"<tr>{tds}</tr>"
    return (
        f'<div class="table-scroll"><table><thead><tr>{th}</tr></thead>'
        f"<tbody>{trs}</tbody></table></div>"
    )


def render_env_cards(rows: list[str]) -> str:
    """`기본 환경`의 2열 표는 표보다 카드가 읽기 쉽다."""
    _, body = split_table(rows)
    if not body or any(len(r) != 2 for r in body):
        return render_table(rows)
    cards = "".join(
        f'<div class="spec"><dt>{inline(k)}</dt><dd>{inline(v)}</dd></div>'
        for k, v in body
    )
    return f'<dl class="specs">{cards}</dl>'


def render_env_bullets(items: list[str]) -> str:
    """`적용 기준`처럼 `항목: 값` 형태의 불릿은 표와 같은 카드로 렌더링한다."""
    pairs = []
    for it in items:
        key, sep, val = it.partition(": ")
        if not sep or "`" in key or len(key) > 24:
            return ""
        pairs.append((key, val))
    cards = "".join(
        f'<div class="spec"><dt>{inline(k)}</dt><dd>{inline(v)}</dd></div>' for k, v in pairs
    )
    return f'<dl class="specs">{cards}</dl>'


def render_scope_list(items: list[str]) -> str:
    """`현재 범위 밖의 항목`은 `대상: 이유` 형태다. 둘을 분리한다."""
    out = []
    for it in items:
        term, sep, why = it.partition(": ")
        if sep:
            out.append(f"<li><b>{inline(term)}</b><span>{inline(why)}</span></li>")
        else:
            out.append(f"<li><b>{inline(it)}</b></li>")
    return f'<ul class="scope">{"".join(out)}</ul>'


def render_doc_cards(rows: list[str]) -> str:
    """README의 문서 표는 허브 카드로 렌더링한다."""
    _, body = split_table(rows)
    if not body or any(len(r) != 2 for r in body):
        return render_table(rows)
    cards = []
    for name, duty in body:
        m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", name.strip())
        if not m:
            return render_table(rows)
        cards.append(
            f'<a class="doc-card" href="{html.escape(rewrite_href(m.group(2)), quote=True)}">'
            f"<b>{inline(m.group(1))}</b><span>{inline(duty)}</span></a>"
        )
    return f'<div class="doc-cards">{"".join(cards)}</div>'


def render_blocks(blocks: list[tuple], role: str) -> str:
    out = []
    seen_spec = False
    for b in blocks:
        kind = b[0]
        if kind == "heading":  # H4 이하. 목차에는 올리지 않고 본문에서만 구분한다
            text = b[2]
            num, label = strip_num(text)
            n = f'<span class="n">{num}</span>' if num else ""
            out.append(f'<h4 id="{slugify(text)}">{n}{inline(label)}</h4>')
        elif kind == "p":
            cls = ' class="note"' if role == "env" and seen_spec else ""
            out.append(f"<p{cls}>{inline(b[1])}</p>")
        elif kind == "code":
            out.append(render_code(b[1], b[2]))
        elif kind == "table":
            if role == "env":
                seen_spec = True
                out.append(render_env_cards(b[1]))
            elif role == "doclist":
                out.append(render_doc_cards(b[1]))
            else:
                out.append(render_table(b[1]))
        elif kind == "ul":
            if role == "env" and render_env_bullets(b[1]):
                seen_spec = True
                out.append(render_env_bullets(b[1]))
            elif role == "scope":
                out.append(render_scope_list(b[1]))
            else:
                cls = ' class="check"' if role == "verify" else ""
                lis = "".join(f"<li>{inline(x)}</li>" for x in b[1])
                out.append(f"<ul{cls}>{lis}</ul>")
        elif kind == "ol":
            lis = "".join(f"<li>{inline(x)}</li>" for x in b[1])
            out.append(f"<ol>{lis}</ol>")
    return "\n".join(out)


class Sub:
    def __init__(self, title: str):
        self.title = title
        self.id = slugify(title)
        self.blocks: list[tuple] = []
        self.num, self.label = strip_num(title)


class Section(Sub):
    def __init__(self, title: str):
        super().__init__(title)
        self.subs: list[Sub] = []
        self.role = SPINE.get(self.label) or SPINE_EXTRA.get(self.label, "other")


def build_sections(blocks: list[tuple]) -> tuple[str, list[Section]]:
    title, sections = "", []
    cur_sec = cur_sub = None
    for b in blocks:
        if b[0] == "heading":
            level, text = b[1], b[2]
            if level == 1:
                title = text
                continue
            if level == 2:
                cur_sec = Section(text)
                cur_sub = None
                sections.append(cur_sec)
                continue
            if level == 3 and cur_sec is not None:
                cur_sub = Sub(text)
                cur_sec.subs.append(cur_sub)
                continue
        if cur_sec is None:
            continue  # H1과 첫 H2 사이의 "README로 돌아가기"는 사이트 navigation이 대신한다
        (cur_sub or cur_sec).blocks.append(b)
    return title, sections


def render_section(sec: Section) -> str:
    body = [render_blocks(sec.blocks, sec.role)]
    for sub in sec.subs:
        inner = render_blocks(sub.blocks, sec.role)
        num = f'<span class="n">{sub.num}</span>' if sub.num else ""
        if sec.role == "principles":
            body.append(
                f'<article class="rule" id="{sub.id}">'
                f'<div class="rule-n">{sub.num}</div>'
                f'<div class="rule-b"><h3>{inline(sub.label)}</h3>{inner}</div></article>'
            )
        else:
            body.append(
                f'<div class="sub"><h3 id="{sub.id}">{num}{inline(sub.label)}</h3>{inner}</div>'
            )
    inner_html = "\n".join(x for x in body if x.strip())
    num = f'<span class="n">{sec.num}</span>' if sec.num else ""
    head = f"<h2>{num}{inline(sec.label)}</h2>"
    if sec.role == "scope":
        return (
            f'<section class="s-{sec.role}" id="{sec.id}">{head}'
            f'<details><summary>이 문서가 다루지 않는 것 펼치기</summary>'
            f"{inner_html}</details></section>"
        )
    return f'<section class="s-{sec.role}" id="{sec.id}">{head}{inner_html}</section>'


def doc_order() -> list:
    return [("index.html", "저장소 개요", "README.md")] + [
        (name[:-3] + ".html", title, name) for name, title in DOC_TITLES.items()
    ]


def render_pager(current: str) -> str:
    """문서는 README의 표 순서대로 읽는 것이 기본이다."""
    entries = doc_order()
    idx = next((i for i, e in enumerate(entries) if e[2] == current), None)
    if idx is None:
        return ""
    parts = []
    if idx > 0:
        href, title, _ = entries[idx - 1]
        parts.append(f'<a class="pg prev" href="{href}"><span>이전</span>{html.escape(title)}</a>')
    if idx < len(entries) - 1:
        href, title, _ = entries[idx + 1]
        parts.append(f'<a class="pg next" href="{href}"><span>다음</span>{html.escape(title)}</a>')
    return f'<nav class="pager">{"".join(parts)}</nav>' if parts else ""


def render_doc_nav(current: str) -> str:
    """문서 간 이동은 허브를 거치지 않는다."""
    entries = doc_order()
    items = []
    for href, title, src in entries:
        mark = ' class="cur" aria-current="page"' if src == current else ""
        items.append(f'<li><a href="{href}"{mark}>{html.escape(title)}</a></li>')
    items = "".join(items)
    return f'<nav class="docnav"><div class="toc-h">문서</div><ul>{items}</ul></nav>'


def render_toc(sections: list[Section]) -> str:
    items = []
    for sec in sections:
        subs = ""
        for s in sec.subs:
            deep = "".join(
                f'<li><a href="#{slugify(b[2])}">{inline(strip_num(b[2])[1])}</a></li>'
                for b in s.blocks
                if b[0] == "heading"
            )
            subs += (
                f'<li><a href="#{s.id}">{inline(s.label)}</a>'
                + (f"<ul>{deep}</ul>" if deep else "")
                + "</li>"
            )
        items.append(
            f'<li><a class="l2" href="#{sec.id}">'
            f'<span class="n">{sec.num}</span>{inline(sec.label)}</a>'
            + (f"<ul>{subs}</ul>" if subs else "")
            + "</li>"
        )
    return f'<nav class="toc"><div class="toc-h">목차</div><ul>{"".join(items)}</ul></nav>'


PAGE = """<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · macbook-management</title>
<link rel="stylesheet" href="assets/style.css">
</head><body>
<a class="skip" href="#main">본문으로</a>
<div class="shell">
<aside class="side">
  <a class="home" href="index.html">macbook-management</a>
  {docnav}
  {toc}
</aside>
<main id="main">
<header>
  <div class="eyebrow">{kicker} · {source}</div>
  <h1>{title}</h1>
  {standfirst}
</header>
{summary}
{sections}
{pager}
<footer>
  이 페이지는 <code>{source}</code>에서 생성되었다. 직접 수정하지 않는다.<br>
  내용을 바꿀 때는 마크다운 원본을 고치고 <code>tools/render.py</code>를 다시 실행한다.
</footer>
</main>
</div>
<script src="assets/page.js"></script>
</body></html>
"""


def render_doc(src: Path) -> str:
    blocks = parse_blocks(src.read_text(encoding="utf-8"))
    title, sections = build_sections(blocks)

    standfirst = ""
    for sec in sections:
        if sec.role == "purpose":
            for b in sec.blocks:
                if b[0] == "p":
                    standfirst = f'<p class="standfirst">{inline(b[1])}</p>'
                    break
            break

    summary_html, ordered = "", []
    for sec in sections:
        if sec.role == "summary" and LIFT_SUMMARY:
            html_sec = render_section(sec)
            # 원칙 링크 목록은 사이드바 목차의 `구성 원칙` 하위와 같은 목록이다.
            # 내용은 남기되 접어서 패널이 구조 트리만 보이게 한다.
            m = re.search(r"<ul>(?:(?!</ul>).)*</ul>", html_sec, re.S)
            if m and m.group(0).count("<a href=\"#") >= 3:
                n = m.group(0).count("<li>")
                html_sec = html_sec.replace(
                    m.group(0),
                    f"<details class=\"rules-fold\"><summary>원칙 {n}개 목록</summary>"
                    f"{m.group(0)}</details>",
                )
            summary_html = f'<div class="lifted">{html_sec}</div>'
        else:
            ordered.append(sec)

    return PAGE.format(
        kicker="저장소 개요" if src.name == "README.md" else "원칙 문서",
        title=html.escape(title),
        source=src.name,
        docnav=render_doc_nav(src.name),
        pager=render_pager(src.name),
        toc=render_toc(sections),
        standfirst=standfirst,
        summary=summary_html,
        sections="\n".join(render_section(s) for s in ordered),
    )


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else root
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "docs"
    names = sys.argv[3:] or ["README.md"] + list(DOC_TITLES)
    out.mkdir(parents=True, exist_ok=True)
    (out / ".nojekyll").touch()  # Jekyll 전처리를 우회한다
    assets_src = Path(__file__).resolve().parent / "assets"
    assets_dst = out / "assets"
    assets_dst.mkdir(exist_ok=True)
    for asset in sorted(assets_src.iterdir()):
        if asset.is_file():
            shutil.copyfile(asset, assets_dst / asset.name)
            print(f"복사: assets/{asset.name}")
    for name in names:
        src = repo / name
        if not src.exists():
            print(f"건너뜀 (없음): {name}")
            continue
        dst = out / ("index.html" if src.name == "README.md" else src.stem + ".html")
        dst.write_text(render_doc(src), encoding="utf-8")
        print(f"생성: {dst.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
