import streamlit as st
import json
import os
import pathlib
import re
import html as _html

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="RISQ 3.2 Demo",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════
# CSS — Summit CI: navy #1A3672 / red #C22030
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
.main .block-container {
    max-width: 1200px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}
:root {
    --navy:      #1A3672;
    --navy-lite: #eef1f8;
    --red:       #C22030;
    --red-lite:  #fbeaea;
    --border:    #e2e6ef;
    --muted:     #8492a6;
    --text:      #1a1f36;
    --surface:   #f7f8fc;
}
.top-bar {
    height:3px;
    background:linear-gradient(90deg,var(--navy) 60%,var(--red) 100%);
    margin:-1rem -1rem 0;
}
.risq-header {
    display:flex; align-items:flex-end; justify-content:space-between;
    flex-wrap:wrap; gap:16px;
    padding:28px 0 22px; border-bottom:1px solid var(--border); margin-bottom:0;
}
.wm-eyebrow {
    font-size:.6rem; font-weight:700; letter-spacing:.24em;
    color:var(--muted); text-transform:uppercase; margin-bottom:6px;
}
.wm-main {
    font-size:2.6rem; font-weight:900; color:var(--navy);
    letter-spacing:-.04em; line-height:1; margin-bottom:8px;
}
.wm-ver {
    font-size:1.2rem; font-weight:700; color:var(--red);
    margin-left:6px; vertical-align:middle; letter-spacing:0;
}
.wm-sub {
    font-size:.68rem; font-weight:600; letter-spacing:.12em;
    color:var(--muted); text-transform:uppercase;
}
.kpi-row { display:flex; align-items:center; gap:0; }
.kpi { padding:0 28px; text-align:right; }
.kpi:last-child { padding-right:0; }
.kpi-n { font-size:2rem; font-weight:800; color:var(--navy); line-height:1; letter-spacing:-.03em; }
.kpi.danger .kpi-n { color:var(--red); }
.kpi-l { font-size:.58rem; font-weight:700; letter-spacing:.16em; color:var(--muted); text-transform:uppercase; margin-top:4px; }
.kpi-sep { width:1px; height:44px; background:var(--border); }
.hr-banner {
    background:var(--red); color:#fff; border-radius:6px;
    padding:10px 18px; font-weight:700; font-size:1rem;
    margin:8px 0 12px; letter-spacing:.02em;
}
.item-head {
    display:flex; align-items:center; gap:12px;
    padding:12px 0 10px; border-bottom:2px solid var(--navy-lite);
    margin:10px 0 4px;
}
.item-head.high { border-bottom-color:var(--red-lite); }
.item-no { font-size:1.35rem; font-weight:900; color:var(--navy); letter-spacing:-.01em; }
.item-head.high .item-no { color:var(--red); }
.hr-pill {
    background:var(--red); color:#fff; font-size:.68rem; font-weight:700;
    border-radius:4px; padding:3px 10px; letter-spacing:.06em; text-transform:uppercase;
}
.sec-header {
    font-size:.72rem; font-weight:700; letter-spacing:.12em;
    text-transform:uppercase; color:var(--muted); margin:18px 0 8px;
}
.sec-div { border:none; border-top:1px solid var(--border); margin:16px 0; }
.line-en { color:var(--text); font-size:1rem; line-height:1.85; }
.line-kr { color:var(--navy); font-size:1rem; line-height:1.85; }
.finding-item {
    background:#fff; border-left:3px solid #cbd5e1; border-radius:0 8px 8px 0;
    box-shadow:0 1px 4px rgba(0,0,0,.06);
    padding:16px 20px; margin-bottom:12px; font-size:1rem; color:var(--text); line-height:1.8;
}
.finding-item-high {
    background:var(--red-lite); border-left:3px solid var(--red); border-radius:0 8px 8px 0;
    box-shadow:0 1px 4px rgba(194,32,48,.1);
    padding:16px 20px; margin-bottom:12px; font-size:1rem; color:var(--text); line-height:1.8;
}
.high-tag {
    display:inline-block; background:var(--red); color:#fff; font-size:.68rem; font-weight:700;
    border-radius:3px; padding:2px 7px; margin-left:5px; vertical-align:middle; letter-spacing:.06em;
}
.kw-card {
    background:#fff; border-radius:10px; border-left:3px solid var(--navy);
    box-shadow:0 1px 6px rgba(0,0,0,.07); padding:14px 18px; margin-bottom:12px;
}
.hr-kw-card { border-left-color:var(--red); }
.kw-no { font-size:.8rem; font-weight:700; color:var(--navy); margin-bottom:6px; letter-spacing:.03em; }
.kw-hit { font-size:1rem; line-height:1.75; color:var(--text); }
mark { background:#fde68a; border-radius:2px; font-weight:700; padding:0 2px; }
.ch-badge {
    display:inline-block; background:var(--red); color:#fff; font-size:.68rem; font-weight:700;
    border-radius:4px; padding:2px 8px; margin-left:6px; letter-spacing:.04em;
}
.rv-label {
    font-size:.72rem; font-weight:600; letter-spacing:.1em;
    text-transform:uppercase; color:var(--muted); margin-bottom:8px;
}
.rv-chip {
    display:inline-block; background:#fff; border:1px solid var(--border); color:var(--navy);
    font-size:.82rem; font-weight:600; padding:3px 12px; border-radius:20px;
    margin:0 4px 4px 0; box-shadow:0 1px 3px rgba(0,0,0,.06);
}
.risq-footer {
    margin-top:60px; padding:14px 0; border-top:1px solid var(--border);
    text-align:center; font-size:.82rem; color:var(--muted);
}
@media print {
    [data-testid="stSidebar"], [data-testid="stToolbar"],
    [data-testid="stStatusWidget"], .risq-footer,
    button, [data-testid="stRadio"] { display:none !important; }
    .stApp { background:#fff !important; }
    .item-head { break-after:avoid; }
    .stExpander { break-inside:avoid; }
    * { color:#000 !important; }
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════
# PDF 경로 탐색 및 사전 로드
import os

_DOCS_CANDIDATES = [
    pathlib.Path(__file__).parent / "docs",
    pathlib.Path(os.getcwd()) / "docs",
    pathlib.Path("docs"),
]

@st.cache_data
def load_pdf_cache() -> dict:
    """시작 시 docs/ 내 모든 PDF를 메모리에 로드."""
    cache: dict = {}
    docs_dir = None
    for c in _DOCS_CANDIDATES:
        if c.exists() and c.is_dir():
            docs_dir = c
            break
    if docs_dir is None:
        return cache
    for fpath in docs_dir.iterdir():
        if fpath.suffix.lower() == ".pdf":
            cache[fpath.name] = fpath.read_bytes()
    return cache

_PDF_CACHE = load_pdf_cache()

def get_pdf_bytes(filename: str):
    return _PDF_CACHE.get(filename, None)


@st.cache_data
def load_data():
    with open("demo_risq_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

_raw     = load_data()
data     = [item for item in _raw if not item.get("Deleted", False)]
TOTAL    = len(data)
HR_COUNT = sum(1 for item in data if item.get("High Risk") is True)

# Verified: chapters 1-15 only (299 items). CH.16-17 absent from dataset.
CHAPTER_TITLES = {
    "1":  "CH.1 — General Information",
    "2":  "CH.2 — Certification & Personnel",
    "3":  "CH.3 — Navigation",
    "4":  "CH.4 — ISM System",
    "5":  "CH.5 — Pollution Prevention",
    "6":  "CH.6 — Ship Structure",
    "7":  "CH.7 — Fuel Management",
    "8":  "CH.8 — Cargo Operation",
    "9":  "CH.9 — Hatch Cover & Lifting",
    "10": "CH.10 — Mooring Operations",
    "11": "CH.11 — Radio & Communication",
    "12": "CH.12 — Security",
    "13": "CH.13 — Machinery Space",
    "14": "CH.14 — Hull & Superstructure",
    "15": "CH.15 — Health & Welfare",
}

SEARCH_FIELDS = {
    "Description": "Question",
    "Guide":        "Guide",
    "action(E)":    "Action (EN)",
    "action(K)":    "Action (KR)",
}


# ══════════════════════════════════════════════════════════════
# HELPERS — all at module level
# ══════════════════════════════════════════════════════════════
def get_field(item: dict, *keys) -> str:
    for k in keys:
        v = item.get(k, "")
        if v and str(v).strip() not in ("", "-"):
            return str(v)
    return ""


def render_bilingual(text, lang: str = "en") -> str:
    """
    lang: 'en' | 'kr'

    ① 불릿 감지: '. ' 또는 '-. ' 로 시작하는 텍스트만 불릿 렌더링
       일반 Question/Guide는 불릿 없이 단락으로 표시
    ② 언어 분리: EN 줄과 KR 줄을 언어 전환 시점에서 분리
    ③ KR 요청인데 KR 내용 없으면 EN 원문을 흐리게 표시 (토글 의미 유지)
    """
    if isinstance(text, list):
        text = "\n".join(str(t) for t in text)
    text = str(text).strip()
    if not text or text == "-":
        return "<span style='color:var(--muted);font-style:italic'>—</span>"

    citation_re = re.compile(r'^\(.*\d{4}\)', re.IGNORECASE)
    bullet_re   = re.compile(r'^\s*-?\.\s')
    is_bullet_text = bool(re.search(r'(^|\n)\s*-?\.\s', text))

    # ── 불릿 구조 텍스트 ─────────────────────────────────────────
    if is_bullet_text:
        items = []
        for raw in text.split("\n"):
            stripped = raw.strip()
            if not stripped:
                continue
            m = bullet_re.match(raw)
            if m:
                is_sub  = stripped.startswith("-.")
                marker  = "-. " if is_sub else ". "
                content = stripped[len(marker.strip()):].strip()
                items.append({"sub": is_sub, "bullet": True, "text": content})
            elif items:
                prev_kr = bool(re.search(r"[가-힣]", items[-1]["text"]))
                curr_kr = bool(re.search(r"[가-힣]", stripped))
                if prev_kr == curr_kr:
                    items[-1]["text"] += " " + stripped
                else:
                    items.append({"sub": False, "bullet": False, "text": stripped})
            else:
                items.append({"sub": False, "bullet": False, "text": stripped})

        parts = []
        for item in items:
            chunk   = item["text"].strip()
            is_kr   = bool(re.search(r"[가-힣]", chunk))
            is_cite = bool(citation_re.search(chunk))
            if lang == "en" and is_kr:
                continue
            if lang == "kr" and not is_kr and not is_cite:
                continue
            css    = "line-kr" if is_kr else "line-en"
            esc    = _html.escape(chunk)
            if item["bullet"]:
                indent = "margin-left:14px;" if item["sub"] else ""
                prefix = "• "
                parts.append(
                    f"<p class='{css}' style='margin:3px 0;{indent}white-space:normal;max-width:1100px;'>"
                    f"{prefix}{esc}</p>"
                )
            else:
                parts.append(
                    f"<p class='{css}' style='margin:3px 0;white-space:normal;max-width:1100px;'>{esc}</p>"
                )

        if parts:
            return "".join(parts)

        # KR 요청인데 KR 없음 → EN 폴백
        if lang == "kr":
            en_parts = []
            for item in items:
                chunk = item["text"].strip()
                if bool(re.search(r"[가-힣]", chunk)):
                    continue
                esc = _html.escape(chunk)
                if item["bullet"]:
                    indent = "margin-left:14px;" if item["sub"] else ""
                    en_parts.append(
                        f"<p class='line-en' style='margin:3px 0;{indent}color:var(--muted);white-space:normal;max-width:1100px;'>• {esc}</p>"
                    )
                else:
                    en_parts.append(
                        f"<p class='line-en' style='margin:3px 0;color:var(--muted);white-space:normal;max-width:1100px;'>{esc}</p>"
                    )
            return "".join(en_parts) if en_parts else "<span style='color:var(--muted);font-style:italic'>번역 준비 중</span>"
        return "<span style='color:var(--muted);font-style:italic'>—</span>"

    # ── 일반 단락 텍스트 (Question, Guide) ───────────────────────
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    items = []
    for line in lines:
        is_kr = bool(re.search(r"[가-힣]", line))
        if items:
            prev_kr = bool(re.search(r"[가-힣]", items[-1]["text"]))
            # 언어가 바뀌면 항상 새 항목
            # 같은 언어여도 각 줄은 독립 단락 (PDF 재파싱으로 이미 구조화됨)
            # 예외: 소문자로 시작하는 continuation 줄만 이전 줄에 합침
            is_continuation = (
                not is_kr and
                line and line[0].islower() and
                not re.match(r'^[1-9]\d?\.\s', line) and
                not line.startswith('>')
            )
            if prev_kr == is_kr and is_continuation:
                items[-1]["text"] += " " + line
            else:
                items.append({"text": line})
        else:
            items.append({"text": line})

    # 출처 위치 기반 필터: EN섹션 출처 → EN 모드에만, KR섹션 출처 → KR 모드에만
    first_kr_pos = next(
        (i for i, it in enumerate(items) if bool(re.search(r"[가-힣]", it["text"]))),
        len(items)
    )
    target = []
    for i, it in enumerate(items):
        is_kr   = bool(re.search(r"[가-힣]", it["text"]))
        is_cite = bool(citation_re.search(it["text"]))
        if lang == "en":
            if not is_kr and not is_cite:
                target.append(it)
            elif is_cite and i < first_kr_pos:
                target.append(it)
        elif lang == "kr":
            if is_kr:
                target.append(it)
            elif is_cite and i >= first_kr_pos:
                target.append(it)

    # KR 모드이고 KR이 있지만 EN보다 현저히 짧으면 (부분 번역)
    # → KR 표시 후 번역 안 된 EN 단락을 흐린 색으로 추가 표시
    en_items = [it for it in items if not bool(re.search(r"[가-힣]", it["text"]))]
    kr_items = [it for it in items if bool(re.search(r"[가-힣]", it["text"]))]
    en_total = sum(len(it["text"]) for it in en_items)
    kr_total = sum(len(it["text"]) for it in kr_items)
    is_partial_kr = (lang == "kr" and kr_items and en_total > 0
                     and kr_total < en_total * 0.1)

    def split_sentences(t):
        if not t.strip():
            return []
        lines = [p.strip() for p in t.split('\n') if p.strip()]
        result = []
        for line in lines:
            # 400자 초과 단락은 문장 단위로 추가 분리
            if len(line) > 400 and not line.startswith('>'):
                # 영문: 문장 끝(소문자/괄호 뒤 마침표 + 공백 + 대문자)
                parts = re.split(r'(?<=[a-z\)])\.\s+(?=[A-Z\(])', line)
                # 한국어: 종결 어미 뒤 분리
                if len(parts) == 1:
                    parts = re.split(r'(?<=[다라까요이며])\.\s+(?=[가-힣A-Z])', line)
                result.extend([p.strip() for p in parts if p.strip()])
            else:
                result.append(line)
        return result

    def render_line(s, css, muted=False):
        """
        줄 유형별 시각적 계층 처리:
        - > 불릿: 들여쓰기, 항목 간 간격 최소화
        - 1. 2. 숫자 목록: 들여쓰기, 항목 간 간격 최소화
        - 콜론 끝 도입부: 아래 여백 최소화 (다음 목록과 붙여서)
        - 일반 단락: 단락 간 충분한 여백
        - 괄호 인용: 작은 글씨, muted 색상
        """
        color = "color:var(--muted);" if muted else ""
        e = _html.escape(s)
        W = "max-width:1100px;"

        # > 불릿 항목
        if s.startswith('>'):
            content = s.lstrip('> ').strip()
            return (f"<p class='{css}' style='margin:0 0 2px 20px;"
                    f"white-space:normal;{W}{color}'>"
                    f"› {_html.escape(content)}</p>")

        # 숫자 목록 항목 (1. 2. 3. ...)
        if re.match(r'^[1-9]\d?\.\s', s):
            return (f"<p class='{css}' style='margin:0 0 2px 20px;"
                    f"white-space:normal;{W}{color}'>{e}</p>")

        # 괄호 인용 (Author, Year) 형식
        if re.match(r'^\(.*\d{4}.*\)$', s):
            return (f"<p class='{css}' style='margin:0 0 8px 0;"
                    f"font-size:.85em;white-space:normal;{W}"
                    f"color:var(--muted);font-style:italic'>{e}</p>")

        # 콜론으로 끝나는 도입 문장 → 다음 목록과 가깝게
        if s.rstrip().endswith(':'):
            return (f"<p class='{css}' style='margin:8px 0 2px 0;"
                    f"white-space:normal;{W}{color}'>{e}</p>")

        # 일반 단락
        return (f"<p class='{css}' style='margin:0 0 8px 0;"
                f"white-space:normal;{W}{color}'>{e}</p>")

    if target:
        css = "line-kr" if lang == "kr" else "line-en"
        result = []
        for it in target:
            for s in split_sentences(it["text"]):
                result.append(render_line(s, css))
        return "".join(result) if result else ""

    # KR 요청인데 KR 없음 → EN 폴백 (흐리게)
    if lang == "kr":
        en_items = [it for it in items if not bool(re.search(r"[가-힣]", it["text"]))]
        if en_items:
            result = []
            for it in en_items:
                for s in split_sentences(it["text"]):
                    result.append(render_line(s, "line-en", muted=True))
            if result:
                result.append(
                    "<span style='font-size:.72rem;color:var(--muted);"
                    "font-style:italic'>번역 준비 중</span>"
                )
                return "".join(result)

    return "<span style='color:var(--muted);font-style:italic'>—</span>"


def render_finding_history(findings) -> str:
    if not findings:
        return "<span style='color:var(--muted);font-style:italic'>No finding history on record.</span>"
    parts = []
    for entry in findings:
        if not entry:
            continue
        # Preserve internal line breaks (48 entries contain \n in real data)
        escaped = _html.escape(str(entry)).replace("\n", "<br>")
        is_high = "(HIGH)" in str(entry)
        css_cls = "finding-item-high" if is_high else "finding-item"
        escaped = re.sub(r"\(HIGH\)", '<span class="high-tag">HIGH</span>', escaped)
        parts.append(f"<div class='{css_cls}'>{escaped}</div>")
    return "".join(parts) if parts else \
        "<span style='color:var(--muted);font-style:italic'>No finding history on record.</span>"


def toggle_bookmark(no: str) -> None:
    bm = st.session_state.bookmarks
    if no in bm:
        bm.remove(no)
    else:
        bm.insert(0, no)
    st.session_state.bookmarks = bm



def render_company_prep(text: str) -> str:
    """
    회사준비사항 전용 렌더러.
    한/영 혼합 텍스트를 언어 필터 없이 그대로 표시.
    - '. ' / '-. ' 불릿 → 들여쓰기
    - 줄바꿈 → 단락 구분
    """
    if not text or not text.strip():
        return "<span style='color:var(--muted);font-style:italic'>—</span>"
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    parts = []
    for line in lines:
        e = _html.escape(line)
        if line.startswith('-. ') or line.startswith('-. '):
            parts.append(
                f"<p class='line-kr' style='margin:1px 0 1px 16px;"
                f"white-space:normal;max-width:1100px;'>• {_html.escape(line[3:])}</p>"
            )
        elif line.startswith('. '):
            parts.append(
                f"<p class='line-kr' style='margin:2px 0;white-space:normal;"
                f"max-width:1100px;'>• {_html.escape(line[2:])}</p>"
            )
        else:
            parts.append(
                f"<p class='line-kr' style='margin:0 0 6px 0;white-space:normal;"
                f"max-width:1100px;'>{e}</p>"
            )
    return "".join(parts)


def field_matches_all(field_text: str, keywords: list) -> bool:
    t = field_text.lower()
    return all(kw.lower() in t for kw in keywords)


def get_snippet(field_text: str, keywords: list, max_chars: int = 280) -> str:
    lines  = [ln.strip() for ln in field_text.split("\n") if ln.strip()]
    target = field_text[:max_chars]
    for line in lines:
        if any(kw.lower() in line.lower() for kw in keywords):
            target = line[:max_chars]
            break
    s = _html.escape(target)
    for kw in keywords:
        esc_kw = _html.escape(kw)
        s = re.sub(re.escape(esc_kw),
                   lambda m: f"<mark>{m.group(0)}</mark>",
                   s, flags=re.IGNORECASE)
    return s


def add_recently_viewed(no: str) -> None:
    rv = st.session_state.recently_viewed
    if no in rv:
        rv.remove(no)
    rv.insert(0, no)
    st.session_state.recently_viewed = rv[:8]


@st.dialog("RISQ Full Details", width="large")
def show_full_dialog(item: dict) -> None:
    """
    Modal popup for Tab3 'View full details' button.
    Streamlit 1.31+: @st.dialog keeps the modal open across reruns
    until the user closes it (X button or ESC) — no session_state
    management required.
    Verified available in Streamlit 1.45 (user's version).
    """
    no    = item.get("NO", "")
    is_hr = item.get("High Risk", False) is True

    head_cls = "item-head high" if is_hr else "item-head"
    hr_pill  = "<span class='hr-pill'>High Risk</span>" if is_hr else ""
    st.markdown(
        f"<div class='{head_cls}'>"
        f"<span class='item-no'>RISQ {_html.escape(no)}</span>"
        f"{hr_pill}</div>",
        unsafe_allow_html=True,
    )
    if is_hr:
        st.markdown(
            "<div class='hr-banner'>🚨 HIGH RISK ITEM</div>",
            unsafe_allow_html=True,
        )

    # Question
    st.markdown("<div class='sec-header'>Question</div>", unsafe_allow_html=True)
    q_kr = st.toggle("한국어", key=f"dlg_q_{no}")
    st.markdown(
        render_bilingual(item.get("Description", ""), "kr" if q_kr else "en"),
        unsafe_allow_html=True,
    )

    # Guide
    guide_val = get_field(item, "Guide")
    if guide_val:
        st.markdown(
            "<hr class='sec-div'><div class='sec-header'>Guide</div>",
            unsafe_allow_html=True,
        )
        g_kr = st.toggle("한국어", key=f"dlg_g_{no}")
        st.markdown(
            render_bilingual(guide_val, "kr" if g_kr else "en"),
            unsafe_allow_html=True,
        )

    # Action
    ae = get_field(item, "action(E)", "Action(E)")
    ak = get_field(item, "action(K)", "Action(K)")
    if ae or ak:
        st.markdown(
            "<hr class='sec-div'><div class='sec-header'>Action</div>",
            unsafe_allow_html=True,
        )
        a_kr = st.toggle("한국어", key=f"dlg_a_{no}")
        content  = ak if a_kr else ae
        fallback = ae if a_kr else ak
        st.markdown(
            render_bilingual(content or fallback, "kr" if a_kr else "en"),
            unsafe_allow_html=True,
        )

    # 회사준비사항
    cp = item.get("company_prep", "")
    if cp and cp.strip():
        st.markdown(
            "<hr class='sec-div'><div class='sec-header'>🏢 회사준비사항</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            render_company_prep(cp),
            unsafe_allow_html=True,
        )

    # Finding History
    fh       = item.get("Finding History", [])
    fh_count = len([f for f in fh if f]) if isinstance(fh, list) else 0
    st.markdown(
        f"<hr class='sec-div'>"
        f"<div class='sec-header'>Finding History ({fh_count})</div>",
        unsafe_allow_html=True,
    )
    st.markdown(render_finding_history(fh), unsafe_allow_html=True)

    # Related Documents (dialog)
    rd_list = item.get("related_documents", [])
    if rd_list:
        st.markdown("<hr class='sec-div'><div class='sec-header'>📎 Related Documents</div>",
                    unsafe_allow_html=True)
        for d_idx, doc in enumerate(rd_list):
            fname     = doc.get("filename", "")
            title     = doc.get("title", fname)
            desc      = doc.get("desc", "")
            pdf_bytes = get_pdf_bytes(fname)
            st.markdown(
                f"<div style='font-weight:600;color:var(--navy);margin:8px 0 2px'>"
                f"📄 {_html.escape(title)}</div>"
                f"<div style='font-size:.8rem;color:var(--muted);margin-bottom:6px'>"
                f"{_html.escape(desc)}</div>",
                unsafe_allow_html=True,
            )
            dc1, dc2 = st.columns(2)
            with dc1:
                if pdf_bytes:
                    st.download_button(
                        label="⬇️  다운로드",
                        data=pdf_bytes,
                        file_name=fname,
                        mime="application/pdf",
                        key=f"dlg_dl_{no}_{d_idx}",
                        use_container_width=True,
                    )
            with dc2:
                pv_key = f"dlg_pv_{no}_{d_idx}"
                if pv_key not in st.session_state:
                    st.session_state[pv_key] = False
                if st.button("👁️  바로보기", key=f"dlg_pvbtn_{no}_{d_idx}",
                             use_container_width=True):
                    st.session_state[pv_key] = not st.session_state[pv_key]
            if st.session_state.get(pv_key) and pdf_bytes:
                import base64 as _b64
                b64 = _b64.b64encode(pdf_bytes).decode()
                st.components.v1.html(
                    f"""<!DOCTYPE html><html><head>
                    <style>
                    body{{margin:0;padding:0;background:#525659;font-family:sans-serif}}
                    #bar{{background:#3a3a3a;padding:7px 12px;display:flex;
                         align-items:center;gap:10px;color:#fff;font-size:13px}}
                    #bar button{{background:#555;color:#fff;border:none;
                         padding:4px 12px;border-radius:4px;cursor:pointer}}
                    #bar button:hover{{background:#888}}
                    #wrap{{overflow:auto;height:560px;text-align:center;padding:10px}}
                    canvas{{box-shadow:0 2px 8px rgba(0,0,0,.4)}}
                    </style></head><body>
                    <div id="bar">
                      <button onclick="prev()">◀ 이전</button>
                      <span id="pi">로딩 중...</span>
                      <button onclick="next()">다음 ▶</button>
                    </div>
                    <div id="wrap"><canvas id="c"></canvas></div>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
                    <script>
                    pdfjsLib.GlobalWorkerOptions.workerSrc=
                      'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
                    var b64="{b64}",doc=null,cur=1;
                    var bin=atob(b64),arr=new Uint8Array(bin.length);
                    for(var i=0;i<bin.length;i++)arr[i]=bin.charCodeAt(i);
                    pdfjsLib.getDocument({{data:arr.buffer}}).promise.then(function(d){{
                      doc=d;render(1);
                    }});
                    function render(n){{
                      doc.getPage(n).then(function(p){{
                        var vp=p.getViewport({{scale:1.4}});
                        var cv=document.getElementById('c');
                        cv.height=vp.height;cv.width=vp.width;
                        p.render({{canvasContext:cv.getContext('2d'),viewport:vp}});
                        document.getElementById('pi').textContent=n+' / '+doc.numPages;
                        cur=n;
                      }});
                    }}
                    function prev(){{if(cur>1)render(cur-1);}}
                    function next(){{if(doc&&cur<doc.numPages)render(cur+1);}}
                    </script></body></html>""",
                    height=660, scrolling=False,
                )


@st.dialog("RISQ Details", width="large")
def show_section_dialog(item: dict, section: str) -> None:
    """Section-specific popup for Tab2 (Question / Guide / Action only)."""
    no    = item.get("NO", "")
    is_hr = item.get("High Risk", False) is True
    head_cls = "item-head high" if is_hr else "item-head"
    hr_pill  = "<span class='hr-pill'>High Risk</span>" if is_hr else ""
    st.markdown(
        f"<div class='{head_cls}'><span class='item-no'>RISQ {_html.escape(no)}</span>{hr_pill}</div>",
        unsafe_allow_html=True,
    )
    if is_hr:
        st.markdown("<div class='hr-banner'>🚨 HIGH RISK ITEM</div>", unsafe_allow_html=True)
    if section == "Question":
        st.markdown("<div class='sec-header'>Question</div>", unsafe_allow_html=True)
        q_kr = st.toggle("한국어", key=f"sd_q_{no}")
        st.markdown(render_bilingual(item.get("Description", ""), "kr" if q_kr else "en"), unsafe_allow_html=True)
    elif section == "Guide":
        st.markdown("<div class='sec-header'>Guide</div>", unsafe_allow_html=True)
        g_kr = st.toggle("한국어", key=f"sd_g_{no}")
        st.markdown(render_bilingual(get_field(item, "Guide"), "kr" if g_kr else "en"), unsafe_allow_html=True)
    elif section == "Action":
        ae = get_field(item, "action(E)", "Action(E)")
        ak = get_field(item, "action(K)", "Action(K)")
        st.markdown("<div class='sec-header'>Action</div>", unsafe_allow_html=True)
        a_kr     = st.toggle("한국어", key=f"sd_a_{no}")
        content  = ak if a_kr else ae
        fallback = ae if a_kr else ak
        st.markdown(render_bilingual(content or fallback, "kr" if a_kr else "en"), unsafe_allow_html=True)


def open_full_dialog(item: dict) -> None:
    """on_click callback: sets dialog flag BEFORE script reruns."""
    st.session_state.dialog_item    = item
    st.session_state.dialog_section = "full"


def open_section_dialog(item: dict, section: str) -> None:
    """on_click callback: sets dialog flag BEFORE script reruns."""
    st.session_state.dialog_item    = item
    st.session_state.dialog_section = section


# ══════════════════════════════════════════════════════════════
# SESSION STATE — initialised once at startup
# ══════════════════════════════════════════════════════════════
if "recently_viewed" not in st.session_state:
    st.session_state.recently_viewed = []
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []   # list of NO strings
if "font_size" not in st.session_state:
    st.session_state.font_size = 15
if "nav_idx" not in st.session_state:
    st.session_state.nav_idx = 0

# dialog_item / dialog_section: set by on_click callbacks,
# consumed BEFORE st.radio() renders.
if "dialog_item" not in st.session_state:
    st.session_state.dialog_item    = None
    st.session_state.dialog_section = "full"


# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="top-bar"></div>
<div class="risq-header">
    <div>
        <div class="wm-eyebrow">Summit Marine Service</div>
        <div class="wm-main">RISQ <span class="wm-ver">3.2</span></div>
        <div class="wm-sub">RightShip Inspection Support System</div>
    </div>
    <div class="kpi-row">
        <div class="kpi">
            <div class="kpi-n">{TOTAL}</div>
            <div class="kpi-l">Items</div>
        </div>
        <div class="kpi-sep"></div>
        <div class="kpi danger">
            <div class="kpi-n">{HR_COUNT}</div>
            <div class="kpi-l">High Risk</div>
        </div>
        <div class="kpi-sep"></div>
        <div class="kpi">
            <div class="kpi-n">{len(CHAPTER_TITLES)}</div>
            <div class="kpi-l">Chapters</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# DIALOG TRIGGER — executed BEFORE st.radio() renders.
# on_click callbacks set dialog_item; here we consume it once.
# Calling the dialog here (before tabs) prevents Streamlit from
# resetting the active tab during the rerun.
# ══════════════════════════════════════════════════════════════
if st.session_state.dialog_item is not None:
    _item    = st.session_state.dialog_item
    _section = st.session_state.dialog_section
    st.session_state.dialog_item    = None
    st.session_state.dialog_section = "full"
    if _section == "full":
        show_full_dialog(_item)
    else:
        show_section_dialog(_item, _section)


# ══════════════════════════════════════════════════════════════
# NAVIGATION — st.radio preserves selection in session_state,
# guaranteed across any rerun including dialog button clicks.
# ══════════════════════════════════════════════════════════════
PAGE_SEARCH      = "🔎  Search by RISQ No."
PAGE_KW          = "🔍  Keyword Search"
PAGE_HR          = f"🚩  High Risk ({HR_COUNT})"
PAGE_BOOKMARKS   = f"⭐  즐겨찾기 ({len(st.session_state.bookmarks)})"

# ④ 사이드바 글자 크기 슬라이더
with st.sidebar:
    st.markdown("#### ⚙️ 설정")
    font_size = st.slider("글자 크기", min_value=12, max_value=22, value=st.session_state.font_size, step=1)
    if font_size != st.session_state.font_size:
        st.session_state.font_size = font_size
    st.markdown(
        f"<style>.stApp, .line-en, .line-kr, p {{ font-size:{font_size}px !important; }}</style>",
        unsafe_allow_html=True,
    )

page = st.radio(
    "nav",
    [PAGE_SEARCH, PAGE_KW, PAGE_HR, PAGE_BOOKMARKS],
    horizontal=True,
    label_visibility="collapsed",
    key="main_nav",
)

# ── 6개 항목 빠른 선택 버튼 (모든 탭에서 항상 표시) ──────────────
st.markdown(
    "<div style='font-size:.78rem;color:var(--muted);margin:10px 0 4px'>"
    "📌 Demo Items</div>",
    unsafe_allow_html=True,
)
DEMO_NOS = [x["NO"] for x in data if not x.get("Deleted")]
_btn_cols = st.columns(len(DEMO_NOS))
for _i, _no in enumerate(DEMO_NOS):
    _item = next((x for x in data if x["NO"] == _no), {})
    _is_hr = _item.get("High Risk") is True
    _label = f"⚠ {_no}" if _is_hr else _no
    if _btn_cols[_i].button(_label, key=f"demo_quick_{_no}", use_container_width=True):
        st.session_state["_search_jump"] = _no
        st.session_state["main_nav"]     = PAGE_SEARCH
        st.rerun()

st.markdown("<hr style='margin:4px 0 20px;border-color:var(--border)'>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# PAGE 1 — Search by RISQ No.
# ──────────────────────────────────────────────────────────────
if page == PAGE_SEARCH:
    risq_no = st.text_input(
        "RISQ No.",
        placeholder="e.g.  2.5 · 4.16 · 9.9   or   4  (prefix → all of Chapter 4)",
        label_visibility="collapsed",
    )

    # 최근 검색 기록 표시
    if not risq_no and st.session_state.search_history:
        st.markdown(
            "<div style='font-size:.76rem;color:var(--muted);margin-bottom:4px'>최근 검색</div>",
            unsafe_allow_html=True,
        )
        cols = st.columns(min(len(st.session_state.search_history), 8))
        for i, h in enumerate(st.session_state.search_history[:8]):
            if cols[i].button(h, key=f"sh_{h}_{i}"):
                st.session_state["_search_jump"] = h
                st.rerun()

    # 검색 기록 클릭으로 재실행
    if "_search_jump" in st.session_state:
        risq_no = st.session_state.pop("_search_jump")

    if risq_no:
        query = risq_no.strip()

        # 검색 기록 저장 (중복 제거, 최대 8개)
        hist = st.session_state.search_history
        if query in hist:
            hist.remove(query)
        hist.insert(0, query)
        st.session_state.search_history = hist[:8]

        matches = [
            item for item in data
            if item.get("NO") == query
            or item.get("NO", "").startswith(query + ".")
        ]

        if len(matches) == 1:
            add_recently_viewed(matches[0].get("NO", ""))

        if not matches:
            # Deleted 항목 확인
            deleted_matches = [
                item for item in _raw
                if (item.get("NO") == query
                    or item.get("NO", "").startswith(query + "."))
                and item.get("Deleted", False)
            ]
            if deleted_matches:
                for d in deleted_matches:
                    st.markdown(
                        f"<div style='border-left:4px solid var(--muted);"
                        f"background:var(--surface);padding:14px 18px;"
                        f"border-radius:0 8px 8px 0;margin-bottom:10px;'>"
                        f"<span style='font-size:1.1rem;font-weight:700;"
                        f"color:var(--muted)'>RISQ {_html.escape(d.get('NO',''))}"
                        f"</span>&nbsp;&nbsp;"
                        f"<span style='background:var(--muted);color:#fff;"
                        f"font-size:.72rem;font-weight:700;border-radius:4px;"
                        f"padding:3px 10px;letter-spacing:.06em;'>"
                        f"DELETED FROM RISQ 3.2</span></div>",
                        unsafe_allow_html=True,
                    )
            else:
                st.warning(f"**{_html.escape(query)}** 항목을 찾을 수 없습니다.")
                # 유사 항목 제안
                sec = query.split(".")[0]
                similar = [
                    item for item in data
                    if item.get("NO", "").startswith(sec + ".")
                    and item.get("NO") != query
                ][:6]
                if similar:
                    st.markdown(
                        f"<div style='font-size:.8rem;color:var(--muted);margin-top:8px'>"
                        f"Section {sec}의 항목들:</div>",
                        unsafe_allow_html=True,
                    )
                    scols = st.columns(min(len(similar), 6))
                    for i, sit in enumerate(similar):
                        sno = sit.get("NO", "")
                        if scols[i].button(sno, key=f"sim_{sno}"):
                            st.session_state["_search_jump"] = sno
                            st.rerun()
        else:
            st.caption(f"{len(matches)} item(s) found")

        # ① 이전/다음 네비게이션 (복수 결과 시)
        if len(matches) > 1:
            if f"nav_idx_{query}" not in st.session_state:
                st.session_state[f"nav_idx_{query}"] = 0
            idx = st.session_state[f"nav_idx_{query}"]
            idx = max(0, min(idx, len(matches) - 1))

            nc1, nc2, nc3, nc4 = st.columns([1, 1, 3, 1])
            if nc1.button("← 이전", key=f"prev_{query}", disabled=(idx == 0)):
                st.session_state[f"nav_idx_{query}"] = idx - 1
                st.rerun()
            if nc2.button("다음 →", key=f"next_{query}", disabled=(idx == len(matches) - 1)):
                st.session_state[f"nav_idx_{query}"] = idx + 1
                st.rerun()
            nc3.markdown(
                f"<div style='padding:6px 0;color:var(--muted);font-size:.85rem'>"
                f"{idx + 1} / {len(matches)}</div>",
                unsafe_allow_html=True,
            )
            matches = [matches[idx]]

        for item in matches:
                no    = item.get("NO", "")
                is_hr = item.get("High Risk", False) is True
                is_bm = no in st.session_state.bookmarks

                head_cls = "item-head high" if is_hr else "item-head"
                hr_pill  = "<span class='hr-pill'>High Risk</span>" if is_hr else ""
                bm_label = "⭐" if is_bm else "☆"
                hc1, hc2 = st.columns([8, 1])
                hc1.markdown(
                    f"<div class='{head_cls}'>"
                    f"<span class='item-no'>RISQ {_html.escape(no)}</span>"
                    f"{hr_pill}</div>",
                    unsafe_allow_html=True,
                )
                hc2.button(
                    bm_label, key=f"bm_{no}",
                    on_click=toggle_bookmark, args=(no,),
                    use_container_width=True,
                )
                if is_hr:
                    st.markdown(
                        "<div class='hr-banner'>🚨 HIGH RISK — confirm evidence is ready</div>",
                        unsafe_allow_html=True,
                    )

                # Question — individual 한국어 toggle
                with st.expander("📋  Question", expanded=(len(matches) == 1)):
                    q_kr = st.toggle("한국어", key=f"tq_{no}")
                    st.markdown(
                        render_bilingual(item.get("Description", ""), "kr" if q_kr else "en"),
                        unsafe_allow_html=True,
                    )

                # Guide — individual 한국어 toggle
                guide_val = get_field(item, "Guide")
                if guide_val:
                    with st.expander("📖  Guide"):
                        g_kr = st.toggle("한국어", key=f"tg_{no}")
                        rendered = render_bilingual(guide_val, "kr" if g_kr else "en")
                        st.markdown(rendered, unsafe_allow_html=True)

                # Action — individual 한국어 toggle
                action_e = get_field(item, "action(E)", "Action(E)")
                action_k = get_field(item, "action(K)", "Action(K)")
                if action_e or action_k:
                    # 색상 뱃지 생성
                    ac = item.get("action_color", {})
                    COLOR_STYLE = {
                        "blue": ("🔵", "#0000FF", "신규/개정"),
                        "sky":  ("🔷", "#00B0F0", "참고"),
                        "red":  ("🔴", "#FF0000", "주의"),
                    }
                    color_badge = ""
                    if ac:
                        active_colors = set(ac.values())
                        for ckey in ["red", "sky", "blue"]:
                            if ckey in active_colors:
                                icon, hex_c, label = COLOR_STYLE[ckey]
                                color_badge = (
                                    f" <span style='font-size:.72rem;background:{hex_c}22;"
                                    f"color:{hex_c};border:1px solid {hex_c}88;"
                                    f"border-radius:4px;padding:2px 6px;margin-left:4px;"
                                    f"font-weight:700'>{icon} {label}</span>"
                                )
                                break

                    expander_label = "✅  Action"
                    with st.expander(expander_label):
                        if color_badge:
                            st.markdown(
                                f"<div style='margin-bottom:6px'>{color_badge}</div>",
                                unsafe_allow_html=True,
                            )
                        a_kr = st.toggle("한국어", key=f"ta_{no}")
                        content  = action_k if a_kr else action_e
                        fallback = action_e if a_kr else action_k
                        rendered_a = render_bilingual(content or fallback, "kr" if a_kr else "en")
                        st.markdown(rendered_a, unsafe_allow_html=True)

                # 회사준비사항
                cp = item.get("company_prep", "")
                if cp and cp.strip():
                    with st.expander("🏢  회사준비사항"):
                        st.markdown(
                            render_company_prep(cp),
                            unsafe_allow_html=True,
                        )

                # Finding History (no toggle — bilingual naturally displayed)
                fh = item.get("Finding History", [])
                fh_count = len([f for f in fh if f]) if isinstance(fh, list) else 0
                fh_label = (
                    f"📂  Finding History ({fh_count} record{'s' if fh_count != 1 else ''})"
                    if fh_count else "📂  Finding History"
                )
                with st.expander(fh_label):
                    st.markdown(render_finding_history(fh), unsafe_allow_html=True)

                # Related Documents
                rd_list = item.get("related_documents", [])
                rd_label = f"📎  Related Documents ({len(rd_list)})" if rd_list else "📎  Related Documents"
                with st.expander(rd_label):
                    if not rd_list:
                        st.caption("No related documents available.")
                    else:
                        for d_idx, doc in enumerate(rd_list):
                            fname = doc.get("filename", "")
                            title = doc.get("title", fname)
                            desc  = doc.get("desc", "")
                            pdf_bytes = get_pdf_bytes(fname)
                            st.markdown(
                                f"<div style='font-weight:600;color:var(--navy);"
                                f"margin:10px 0 2px'>📄 {_html.escape(title)}</div>"
                                f"<div style='font-size:.8rem;color:var(--muted);"
                                f"margin-bottom:8px'>{_html.escape(desc)}</div>",
                                unsafe_allow_html=True,
                            )
                            dc1, dc2 = st.columns(2)
                            with dc1:
                                if pdf_bytes:
                                    st.download_button(
                                        label="⬇️  다운로드",
                                        data=pdf_bytes,
                                        file_name=fname,
                                        mime="application/pdf",
                                        key=f"dl_{no}_{d_idx}",
                                        use_container_width=True,
                                    )
                                else:
                                    st.warning("파일 없음")
                            with dc2:
                                pv_key = f"pv_{no}_{d_idx}"
                                if pv_key not in st.session_state:
                                    st.session_state[pv_key] = False
                                if st.button("👁️  바로보기", key=f"pvbtn_{no}_{d_idx}",
                                             use_container_width=True):
                                    st.session_state[pv_key] = not st.session_state[pv_key]
                            if st.session_state.get(pv_key) and pdf_bytes:
                                import base64 as _b64
                                b64 = _b64.b64encode(pdf_bytes).decode()
                                st.components.v1.html(
                                    f"""<!DOCTYPE html><html><head>
                                    <style>
                                    body{{margin:0;padding:0;background:#525659;font-family:sans-serif}}
                                    #bar{{background:#3a3a3a;padding:7px 12px;display:flex;
                                         align-items:center;gap:10px;color:#fff;font-size:13px}}
                                    #bar button{{background:#555;color:#fff;border:none;
                                         padding:4px 12px;border-radius:4px;cursor:pointer}}
                                    #bar button:hover{{background:#888}}
                                    #wrap{{overflow:auto;height:560px;text-align:center;padding:10px}}
                                    canvas{{box-shadow:0 2px 8px rgba(0,0,0,.4)}}
                                    </style></head><body>
                                    <div id="bar">
                                      <button onclick="prev()">◀ 이전</button>
                                      <span id="pi">로딩 중...</span>
                                      <button onclick="next()">다음 ▶</button>
                                    </div>
                                    <div id="wrap"><canvas id="c"></canvas></div>
                                    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
                                    <script>
                                    pdfjsLib.GlobalWorkerOptions.workerSrc=
                                      'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
                                    var b64="{b64}",doc=null,cur=1;
                                    var bin=atob(b64),arr=new Uint8Array(bin.length);
                                    for(var i=0;i<bin.length;i++)arr[i]=bin.charCodeAt(i);
                                    pdfjsLib.getDocument({{data:arr.buffer}}).promise.then(function(d){{
                                      doc=d;render(1);
                                    }});
                                    function render(n){{
                                      doc.getPage(n).then(function(p){{
                                        var vp=p.getViewport({{scale:1.4}});
                                        var cv=document.getElementById('c');
                                        cv.height=vp.height;cv.width=vp.width;
                                        p.render({{canvasContext:cv.getContext('2d'),viewport:vp}});
                                        document.getElementById('pi').textContent=n+' / '+doc.numPages;
                                        cur=n;
                                      }});
                                    }}
                                    function prev(){{if(cur>1)render(cur-1);}}
                                    function next(){{if(doc&&cur<doc.numPages)render(cur+1);}}
                                    </script></body></html>""",
                                    height=660, scrolling=False,
                                )
                            st.divider()

                st.divider()

    else:
        if st.session_state.recently_viewed:
            st.markdown(
                "<div class='rv-label'>Recently viewed</div>",
                unsafe_allow_html=True,
            )
            chips = " ".join(
                f"<span class='rv-chip'>{_html.escape(n)}</span>"
                for n in st.session_state.recently_viewed
            )
            st.markdown(chips, unsafe_allow_html=True)
            st.markdown("")
        st.info(
            "Enter a RISQ number above.  \n"
            "**Exact**: `4.16`  |  **Chapter prefix**: `4` → all of Chapter 4"
        )


# ──────────────────────────────────────────────────────────────
# TAB 2 — 3-section filter (Question / Guide / Action merged)
# ──────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────
# PAGE 2 — Keyword Search
# ──────────────────────────────────────────────────────────────
elif page == PAGE_KW:
    # ⑥ 섹션 필터
    sec_filter_opts = ["전체 섹션"] + [
        f"Section {k} — {v.split('—')[-1].strip()}"
        for k, v in sorted(CHAPTER_TITLES.items(), key=lambda x: int(x[0]))
    ]
    sec_filter = st.selectbox(
        "섹션 필터", sec_filter_opts, label_visibility="collapsed",
        key="kw_sec_filter",
    )
    selected_sec_key = None
    if sec_filter != "전체 섹션":
        selected_sec_key = sec_filter.split(" — ")[0].replace("Section ", "").strip()

    kw_raw = st.text_input(
        "Keyword",
        placeholder="e.g.  ECDIS · fire · UKC mooring  (space = AND search)",
        label_visibility="collapsed",
        key="kw_search_input",
    )

    keywords = [k for k in kw_raw.strip().split() if k]

    if keywords:
        # 섹션 필터 적용
        search_pool = [
            item for item in data
            if selected_sec_key is None
            or item.get("NO", "").split(".")[0] == selected_sec_key
        ]
        results: dict = {"Question": [], "Guide": [], "Action": []}
        seen_action: set = set()

        for item in search_pool:
            no    = item.get("NO", "")
            is_hr = item.get("High Risk", False) is True

            desc = item.get("Description", "")
            if isinstance(desc, str) and field_matches_all(desc, keywords):
                results["Question"].append({
                    "no": no, "snippet": get_snippet(desc, keywords),
                    "hr": is_hr, "item": item,
                })

            guide = item.get("Guide", "")
            if isinstance(guide, str) and field_matches_all(guide, keywords):
                results["Guide"].append({
                    "no": no, "snippet": get_snippet(guide, keywords),
                    "hr": is_hr, "item": item,
                })

            if no not in seen_action:
                ae = item.get("action(E)", "")
                ak = item.get("action(K)", "")
                ae_match = isinstance(ae, str) and field_matches_all(ae, keywords)
                ak_match = isinstance(ak, str) and field_matches_all(ak, keywords)
                if ae_match or ak_match:
                    seen_action.add(no)
                    snip_src = ae if ae_match else ak
                    results["Action"].append({
                        "no": no, "snippet": get_snippet(snip_src, keywords),
                        "hr": is_hr, "item": item,
                    })

        def sort_key(r):
            no = r["no"]
            parts = re.findall(r'\d+', no)
            nums = [int(p) for p in parts]
            return (0 if r["hr"] else 1, nums)

        for sec in results:
            results[sec].sort(key=sort_key)

        total_kw = sum(len(v) for v in results.values())

        if total_kw == 0:
            kw_display = " AND ".join(f'"{_html.escape(k)}"' for k in keywords)
            st.warning(f"No results for {kw_display}.")
        else:
            kw_display = "  +  ".join(f'**"{k}"**' for k in keywords)
            st.caption(f"{total_kw} match(es) for {kw_display}")

            available = [s for s in ["Question", "Guide", "Action"] if results[s]]
            chosen = st.radio(
                "Section",
                available,
                horizontal=True,
                label_visibility="collapsed",
                format_func=lambda s: f"{s}  ({len(results[s])})",
                key=f"kwf_{abs(hash(kw_raw)) % 10**9}",
            )

            n = len(results[chosen])
            st.markdown(
                f"<h4 style='margin:16px 0 10px;color:var(--navy)'>{chosen}"
                f"&nbsp;<small style='font-weight:400;color:var(--muted)'>"
                f"({n} match{'es' if n != 1 else ''})</small></h4>",
                unsafe_allow_html=True,
            )
            for r in results[chosen][:30]:
                hr_badge = " <span class='ch-badge'>HIGH RISK</span>" if r["hr"] else ""
                hr_cls   = " hr-kw-card" if r["hr"] else ""
                st.markdown(
                    f"<div class='kw-card{hr_cls}'>"
                    f"<div class='kw-no'>RISQ {_html.escape(r['no'])}{hr_badge}</div>"
                    f"<div class='kw-hit'>{r['snippet']}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                # on_click: sets flag BEFORE rerun → dialog opens before tabs
                st.button(
                    f"📋  Full details — RISQ {r['no']}  →",
                    key=f"t2btn_{r['no']}_{chosen}",
                    on_click=open_section_dialog,
                    args=(r["item"], chosen),
                )

    elif kw_raw.strip():
        st.info("Type a complete keyword to search.")
    else:
        st.info(
            "Enter keywords to search across questions, guides and actions.  \n"
            "**Tip:** Space between words = AND search — e.g. `ECDIS UKC`"
        )


# ──────────────────────────────────────────────────────────────
# PAGE 3 — High Risk Items
# on_click=open_full_dialog sets dialog flag before rerun.
# st.radio key="main_nav" is preserved in session_state →
# page stays on High Risk Items after any button click.
# ──────────────────────────────────────────────────────────────
elif page == PAGE_HR:
    hr_items = [item for item in data if item.get("High Risk") is True]

    if not hr_items:
        st.info("No high-risk items found in data.")
    else:
        chapter_map: dict = {}
        for hr_item in hr_items:
            no_str = hr_item.get("NO", "")
            ch_key = no_str.split(".")[0] if "." in no_str else no_str
            chapter_map.setdefault(ch_key, []).append(hr_item)

        for ch in sorted(chapter_map.keys(), key=lambda x: int(x)):
            ch_items  = chapter_map[ch]
            ch_title  = CHAPTER_TITLES.get(ch, f"CH.{ch}")
            n_items   = len(ch_items)
            exp_label = f"{ch_title}  ({n_items} item{'s' if n_items != 1 else ''})"

            with st.expander(exp_label):
                n_cols   = min(n_items, 8)
                btn_cols = st.columns(n_cols)
                for idx, ch_item in enumerate(ch_items):
                    btn_no = ch_item.get("NO", "")
                    btn_cols[idx % n_cols].button(
                        btn_no,
                        key=f"hrbtn_{ch}_{btn_no}",
                        use_container_width=True,
                        on_click=open_full_dialog,
                        args=(ch_item,),
                    )






# ──────────────────────────────────────────────────────────────
# PAGE ⑤ — 즐겨찾기
# ──────────────────────────────────────────────────────────────
elif page == PAGE_BOOKMARKS:
    bm_nos = st.session_state.bookmarks
    if not bm_nos:
        st.info("⭐ 즐겨찾기한 항목이 없습니다. 검색 결과에서 '☆ 즐겨찾기' 버튼을 눌러 추가하세요.")
    else:
        st.markdown(
            f"<div style='font-size:.82rem;color:var(--muted);margin-bottom:12px'>"
            f"총 {len(bm_nos)}개 항목</div>",
            unsafe_allow_html=True,
        )
        dm = {x["NO"]: x for x in data}
        if st.button("🗑️  전체 즐겨찾기 초기화", key="bm_clear"):
            st.session_state.bookmarks = []
            st.rerun()

        for no in bm_nos:
            item = dm.get(no)
            if not item:
                continue
            is_hr = item.get("High Risk", False) is True
            head_cls = "item-head high" if is_hr else "item-head"
            hr_pill  = "<span class='hr-pill'>High Risk</span>" if is_hr else ""

            bc1, bc2 = st.columns([6, 1])
            bc1.markdown(
                f"<div class='{head_cls}'>"
                f"<span class='item-no'>RISQ {_html.escape(no)}</span>"
                f"{hr_pill}</div>",
                unsafe_allow_html=True,
            )
            bc2.button(
                "⭐ 해제", key=f"bm_rm_{no}",
                on_click=toggle_bookmark, args=(no,),
                use_container_width=True,
            )
            with st.expander("📋  Question"):
                st.markdown(
                    render_bilingual(item.get("Description", ""), "en"),
                    unsafe_allow_html=True,
                )
            st.button(
                f"🔍 Full Details — RISQ {no}  →",
                key=f"bm_detail_{no}",
                on_click=open_full_dialog,
                args=(item,),
            )
            st.divider()


# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="risq-footer">
    © 2026 RightShip RISQ 3.2 Demo &nbsp;|&nbsp; For demonstration purposes only
</div>
""", unsafe_allow_html=True)
