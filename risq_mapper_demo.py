import streamlit as st
import json
import os
import base64
import html as _html
import re

st.set_page_config(
    page_title="RISQ 3.2 Demo",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

:root {
    --navy:   #0a2540;
    --blue:   #1a56db;
    --red:    #e02424;
    --sky:    #00b0f0;
    --amber:  #d97706;
    --green:  #059669;
    --surface:#f8fafc;
    --border: #e2e8f0;
    --text:   #1e293b;
    --muted:  #64748b;
}

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

.demo-banner {
    background: linear-gradient(135deg, #0a2540 0%, #1a56db 100%);
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.demo-title { color: #fff; font-size: 1.5rem; font-weight: 700; margin: 0; }
.demo-sub   { color: #93c5fd; font-size: .85rem; margin: 4px 0 0; }
.demo-badge {
    background: rgba(255,255,255,.15);
    color: #fff;
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .08em;
    padding: 4px 10px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,.3);
    margin-left: auto;
    white-space: nowrap;
}

.item-head {
    background: var(--surface);
    border-left: 4px solid var(--blue);
    border-radius: 0 8px 8px 0;
    padding: 12px 18px;
    margin-bottom: 8px;
}
.item-head.high { border-left-color: var(--red); background: #fff5f5; }
.item-no { font-size: 1.15rem; font-weight: 700; color: var(--navy); font-family: 'IBM Plex Mono', monospace; }
.hr-pill {
    display: inline-block;
    background: var(--red);
    color: #fff;
    font-size: .68rem;
    font-weight: 700;
    border-radius: 4px;
    padding: 3px 8px;
    margin-left: 10px;
    letter-spacing: .06em;
    vertical-align: middle;
}

.rd-card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 18px;
    margin: 8px 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.rd-title { font-weight: 600; color: var(--navy); font-size: .95rem; }
.rd-desc  { color: var(--muted); font-size: .82rem; }
.rd-actions { display: flex; gap: 8px; margin-top: 4px; }

.fh-entry {
    background: #fffbeb;
    border-left: 3px solid var(--amber);
    border-radius: 0 6px 6px 0;
    padding: 10px 14px;
    font-size: .85rem;
    color: var(--text);
    margin: 6px 0;
    white-space: pre-wrap;
}

.line-en { display: block; margin: 2px 0; }
.line-kr { display: block; margin: 2px 0; color: var(--text); }
.line-bullet { display: block; margin: 2px 0 2px 14px; }
.line-sub { display: block; margin: 2px 0 2px 28px; color: var(--muted); font-size: .92em; }
.line-cite {
    display: block; margin: 8px 0;
    font-size: .8rem; color: var(--muted); font-style: italic;
}

.pdf-viewer-wrap {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin-top: 10px;
    background: #f1f5f9;
}

.stExpander > div > div { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    with open("demo_risq_data.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()
dm   = {x["NO"]: x for x in data}

DOCS_DIR = "docs"

def get_pdf_b64(filename: str):
    path = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_pdf_bytes(filename: str):
    path = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return f.read()

# ══════════════════════════════════════════════════════════════
# RENDER HELPERS
# ══════════════════════════════════════════════════════════════
citation_re = re.compile(r'^\(.*\d{4}.*\)', re.IGNORECASE)

def render_text(text: str, lang: str = "en") -> str:
    if not text or text in ("-", "NII", "Deleted"):
        return "<span style='color:var(--muted);font-style:italic'>—</span>"
    lines = text.split("\n")
    parts = []
    def has_kr(t): return bool(re.search(r'[가-힣]', t))
    def is_cite(t): return bool(citation_re.search(t.strip()))

    items_en, items_kr, items_cite_en, items_cite_kr = [], [], [], []
    for line in lines:
        s = line.strip()
        if not s: continue
        if is_cite(s):
            if has_kr(s): items_cite_kr.append(s)
            else: items_cite_en.append(s)
        elif has_kr(s): items_kr.append(s)
        else: items_en.append(s)

    pool = items_en + items_cite_en if lang == "en" else items_kr + items_cite_kr
    if not pool and lang == "kr": pool = items_en  # fallback

    for s in pool:
        esc = _html.escape(s)
        if is_cite(s):
            parts.append(f"<span class='line-cite'>{esc}</span>")
        elif s.startswith(">"):
            inner = _html.escape(s[1:].lstrip())
            parts.append(f"<span class='line-bullet'>&rsaquo; {inner}</span>")
        elif re.match(r'-{1,2}\.\s', s):
            inner = _html.escape(re.sub(r'^-{1,2}\.\s*', '', s))
            parts.append(f"<span class='line-sub'>&ndash; {inner}</span>")
        else:
            parts.append(f"<span class='line-en'>{esc}</span>")
    return "".join(parts) if parts else "<span style='color:var(--muted)'>—</span>"

def render_rd_section(item: dict):
    docs = item.get("related_documents", [])
    if not docs: return
    st.markdown("##### 📎 Related Documents")
    for doc in docs:
        fname = doc["filename"]
        title = doc["title"]
        desc  = doc.get("desc", "")
        pdf_bytes = get_pdf_bytes(fname)
        b64 = get_pdf_b64(fname)

        with st.container():
            st.markdown(
                f"<div class='rd-card'>"
                f"<div class='rd-title'>📄 {_html.escape(title)}</div>"
                f"<div class='rd-desc'>{_html.escape(desc)}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns([1, 1])
            with c1:
                if pdf_bytes:
                    st.download_button(
                        label="⬇️  다운로드",
                        data=pdf_bytes,
                        file_name=fname,
                        mime="application/pdf",
                        key=f"dl_{fname}",
                        use_container_width=True,
                    )
            with c2:
                preview_key = f"preview_{fname}"
                if preview_key not in st.session_state:
                    st.session_state[preview_key] = False
                if st.button("👁️  바로보기", key=f"view_{fname}", use_container_width=True):
                    st.session_state[preview_key] = not st.session_state[preview_key]

            if st.session_state.get(preview_key) and b64:
                st.markdown(
                    f"<div class='pdf-viewer-wrap'>"
                    f"<iframe src='data:application/pdf;base64,{b64}' "
                    f"width='100%' height='600px' "
                    f"style='border:none;display:block'></iframe>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

def render_fh(item: dict):
    fh_list = item.get("Finding History", [])
    if not fh_list: return
    for entry in fh_list:
        if isinstance(entry, str):
            st.markdown(
                f"<div class='fh-entry'>{_html.escape(entry)}</div>",
                unsafe_allow_html=True,
            )

def render_item(item: dict):
    no   = item["NO"]
    is_hr = item.get("High Risk", False) is True

    head_cls = "item-head high" if is_hr else "item-head"
    hr_pill  = "<span class='hr-pill'>⚠ HIGH RISK</span>" if is_hr else ""

    st.markdown(
        f"<div class='{head_cls}'>"
        f"<span class='item-no'>RISQ {_html.escape(no)}</span>"
        f"{hr_pill}</div>",
        unsafe_allow_html=True,
    )

    # Question
    with st.expander("📋  Question"):
        desc = item.get("Description", "")
        lang = "kr" if st.toggle("한국어", key=f"qkr_{no}") else "en"
        st.markdown(render_text(desc, lang), unsafe_allow_html=True)

    # Guide
    guide = item.get("Guide", "")
    if guide and guide not in ("-", ""):
        with st.expander("📖  Guide"):
            lang = "kr" if st.toggle("한국어", key=f"gkr_{no}") else "en"
            st.markdown(render_text(guide, lang), unsafe_allow_html=True)

    # Action
    ae = item.get("action(E)", "")
    ak = item.get("action(K)", "")
    if ae or ak:
        ac = item.get("action_color", {})
        COLOR_INFO = {
            "blue": ("🔵", "#1a56db", "신규/개정"),
            "sky":  ("🔷", "#00b0f0", "참고"),
            "red":  ("🔴", "#e02424", "주의"),
        }
        badge = ""
        for ck in ["red","sky","blue"]:
            if ck in ac.values():
                icon, hx, lbl = COLOR_INFO[ck]
                badge = (f"<span style='font-size:.72rem;background:{hx}22;"
                         f"color:{hx};border:1px solid {hx}88;"
                         f"border-radius:4px;padding:2px 8px;margin-bottom:6px;"
                         f"display:inline-block;font-weight:700'>{icon} {lbl}</span><br>")
                break
        with st.expander("✅  Action"):
            if badge:
                st.markdown(badge, unsafe_allow_html=True)
            lang = "kr" if st.toggle("한국어", key=f"akr_{no}") else "en"
            content = ak if lang == "kr" else ae
            st.markdown(render_text(content or (ae if lang=="kr" else ak), lang), unsafe_allow_html=True)

    # Company Prep
    cp = item.get("company_prep", "")
    if cp and cp.strip():
        with st.expander("🏢  회사준비사항"):
            for line in cp.split("\n"):
                if line.strip():
                    st.markdown(
                        f"<span class='line-en'>{_html.escape(line)}</span>",
                        unsafe_allow_html=True,
                    )

    # Finding History
    fh = item.get("Finding History", [])
    if fh:
        with st.expander(f"🗂  Finding History ({len(fh)}건)"):
            render_fh(item)

    # Related Documents
    rd = item.get("related_documents", [])
    if rd:
        with st.expander(f"📎  Related Documents ({len(rd)}개)"):
            render_rd_section(item)

# ══════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="demo-banner">
  <div>
    <p class="demo-title">🔍 RightShip RISQ 3.2</p>
    <p class="demo-sub">Inspection Support System — Interactive Demo</p>
  </div>
  <span class="demo-badge">DEMO MODE</span>
</div>
""", unsafe_allow_html=True)

# 탭: Search / High Risk
tab_search, tab_hr = st.tabs(["🔎 Search by RISQ No.", "🚩 High Risk (2)"])

# ── Search Tab ─────────────────────────────────────────────
with tab_search:
    DEMO_NOS = [x["NO"] for x in data]

    risq_no = st.text_input(
        "RISQ No.",
        placeholder="예: 2.9  /  3.7  /  4.16",
        label_visibility="collapsed",
    )

    if not risq_no:
        st.markdown(
            "<div style='margin:12px 0 6px;font-size:.82rem;color:var(--muted)'>"
            "데모 수록 항목</div>",
            unsafe_allow_html=True,
        )
        cols = st.columns(len(DEMO_NOS))
        for i, no in enumerate(DEMO_NOS):
            if cols[i].button(no, key=f"quick_{no}"):
                st.session_state["_jump"] = no
                st.rerun()

    if "_jump" in st.session_state:
        risq_no = st.session_state.pop("_jump")

    if risq_no:
        q = risq_no.strip()
        matches = [x for x in data if x["NO"] == q or x["NO"].startswith(q + ".")]
        if not matches:
            st.warning(f"**{_html.escape(q)}** 항목이 데모에 없습니다. 수록 항목: " + ", ".join(DEMO_NOS))
        for item in matches:
            render_item(item)
            st.divider()

# ── High Risk Tab ──────────────────────────────────────────
with tab_hr:
    hr_items = [x for x in data if x.get("High Risk") is True]
    st.markdown(
        f"<p style='color:var(--muted);font-size:.85rem;margin-bottom:16px'>"
        f"High Risk 항목 {len(hr_items)}개</p>",
        unsafe_allow_html=True,
    )
    for item in hr_items:
        render_item(item)
        st.divider()

# Footer
st.markdown("""
<div style="margin-top:60px;padding:14px 0;border-top:1px solid var(--border);
text-align:center;font-size:.82rem;color:var(--muted)">
© 2026 RightShip RISQ 3.2 Demo &nbsp;|&nbsp; For demonstration purposes only
</div>
""", unsafe_allow_html=True)
