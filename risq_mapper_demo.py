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
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap');
:root{--navy:#0a2540;--blue:#1a56db;--red:#e02424;--sky:#00b0f0;
      --amber:#d97706;--surface:#f8fafc;--border:#e2e8f0;
      --text:#1e293b;--muted:#64748b;}
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;}
.demo-banner{background:linear-gradient(135deg,#0a2540 0%,#1a56db 100%);
  border-radius:12px;padding:20px 28px;margin-bottom:20px;display:flex;align-items:center;gap:16px;}
.demo-title{color:#fff;font-size:1.4rem;font-weight:700;margin:0;}
.demo-sub{color:#93c5fd;font-size:.82rem;margin:3px 0 0;}
.demo-badge{background:rgba(255,255,255,.18);color:#fff;font-size:.7rem;font-weight:700;
  letter-spacing:.08em;padding:4px 12px;border-radius:20px;
  border:1px solid rgba(255,255,255,.3);margin-left:auto;white-space:nowrap;}
.item-head{background:var(--surface);border-left:4px solid var(--blue);
  border-radius:0 8px 8px 0;padding:12px 18px;margin-bottom:8px;}
.item-head.high{border-left-color:var(--red);background:#fff5f5;}
.item-no{font-size:1.1rem;font-weight:700;color:var(--navy);font-family:'IBM Plex Mono',monospace;}
.hr-pill{display:inline-block;background:var(--red);color:#fff;font-size:.68rem;
  font-weight:700;border-radius:4px;padding:3px 8px;margin-left:10px;
  letter-spacing:.06em;vertical-align:middle;}
.rd-card{background:#fff;border:1px solid var(--border);border-radius:10px;
  padding:14px 16px;margin:6px 0;}
.rd-title{font-weight:600;color:var(--navy);font-size:.92rem;}
.rd-desc{color:var(--muted);font-size:.8rem;margin-top:3px;}
.fh-entry{background:#fffbeb;border-left:3px solid var(--amber);
  border-radius:0 6px 6px 0;padding:10px 14px;font-size:.84rem;
  color:var(--text);margin:5px 0;white-space:pre-wrap;}
.kw-card{background:#fff;border:1px solid var(--border);border-radius:8px;
  padding:12px 16px;margin:8px 0;}
.kw-no{font-size:.8rem;font-weight:700;color:var(--navy);margin-bottom:4px;
  font-family:'IBM Plex Mono',monospace;}
mark{background:#fef08a;border-radius:2px;padding:0 2px;}
.line-en,.line-kr{display:block;margin:2px 0;}
.line-bullet{display:block;margin:2px 0 2px 14px;}
.line-sub{display:block;margin:2px 0 2px 28px;color:var(--muted);font-size:.91em;}
.line-cite{display:block;margin:7px 0;font-size:.79rem;color:var(--muted);font-style:italic;}
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
active = [x for x in data if not x.get("Deleted")]

# docs 절대경로
DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

def get_pdf_bytes(filename):
    path = os.path.join(DOCS_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return f.read()

def get_pdf_b64(filename):
    b = get_pdf_bytes(filename)
    return base64.b64encode(b).decode() if b else None

# ══════════════════════════════════════════════════════════════
# RENDER HELPERS
# ══════════════════════════════════════════════════════════════
citation_re = re.compile(r'^\(.*\d{4}.*\)', re.IGNORECASE)

def has_kr(t): return bool(re.search(r'[가-힣]', str(t or '')))
def is_cite(t): return bool(citation_re.search(t.strip()))

def render_text(text, lang="en"):
    if not text or text.strip() in ("-", "NII", "Deleted", ""):
        return "<span style='color:var(--muted);font-style:italic'>—</span>"
    lines = text.split("\n")
    items_en, items_kr = [], []
    for line in lines:
        s = line.strip()
        if not s: continue
        if has_kr(s): items_kr.append(s)
        else: items_en.append(s)

    pool = items_en if lang == "en" else (items_kr if items_kr else items_en)
    parts = []
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
        elif re.match(r'^\d+\.', s):
            parts.append(f"<span class='line-bullet'>{esc}</span>")
        else:
            parts.append(f"<span class='line-en'>{esc}</span>")
    return "".join(parts) or "<span style='color:var(--muted)'>—</span>"

def render_rd(item):
    docs = item.get("related_documents", [])
    if not docs: return
    for doc in docs:
        fname = doc["filename"]
        title = doc["title"]
        desc  = doc.get("desc", "")
        st.markdown(
            f"<div class='rd-card'>"
            f"<div class='rd-title'>📄 {_html.escape(title)}</div>"
            f"<div class='rd-desc'>{_html.escape(desc)}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        pdf_bytes = get_pdf_bytes(fname)

        # 다운로드
        with col1:
            if pdf_bytes:
                st.download_button(
                    label="⬇️  다운로드",
                    data=pdf_bytes,
                    file_name=fname,
                    mime="application/pdf",
                    key=f"dl_{item['NO']}_{fname}",
                    use_container_width=True,
                )
            else:
                st.warning("파일 없음")

        # 바로보기 토글
        with col2:
            pk = f"pv_{item['NO']}_{fname}"
            if pk not in st.session_state:
                st.session_state[pk] = False
            if st.button("👁️  바로보기", key=f"btn_{pk}", use_container_width=True):
                st.session_state[pk] = not st.session_state[pk]

        if st.session_state.get(pk):
            b64 = get_pdf_b64(fname)
            if b64:
                st.components.v1.html(
                    f"""<!DOCTYPE html><html><body style="margin:0;padding:0;overflow:hidden">
                    <embed src="data:application/pdf;base64,{b64}"
                           type="application/pdf"
                           width="100%" height="600"
                           style="display:block;border:none">
                    </body></html>""",
                    height=620,
                    scrolling=False,
                )
            else:
                st.error("파일을 불러올 수 없습니다.")

def render_item(item, prefix=""):
    no   = item["NO"]
    is_hr = item.get("High Risk") is True
    head_cls = "item-head high" if is_hr else "item-head"
    hr_pill  = "<span class='hr-pill'>⚠ HIGH RISK</span>" if is_hr else ""

    st.markdown(
        f"<div class='{head_cls}'>"
        f"<span class='item-no'>RISQ {_html.escape(no)}</span>{hr_pill}</div>",
        unsafe_allow_html=True,
    )

    # Question
    with st.expander("📋  Question"):
        lang_q = st.radio("언어", ["EN", "한국어"], horizontal=True,
                          key=f"{prefix}qlang_{no}", label_visibility="collapsed")
        st.markdown(render_text(item.get("Description",""), "kr" if lang_q=="한국어" else "en"),
                    unsafe_allow_html=True)

    # Guide
    guide = item.get("Guide","")
    if guide and guide not in ("-",""):
        with st.expander("📖  Guide"):
            lang_g = st.radio("언어", ["EN", "한국어"], horizontal=True,
                              key=f"{prefix}glang_{no}", label_visibility="collapsed")
            st.markdown(render_text(guide, "kr" if lang_g=="한국어" else "en"),
                        unsafe_allow_html=True)

    # Action
    ae = item.get("action(E)","")
    ak = item.get("action(K)","")
    if ae or ak:
        ac = item.get("action_color", {})
        COLOR_INFO = {"blue":("🔵","#1a56db","신규/개정"),
                      "sky": ("🔷","#00b0f0","참고"),
                      "red": ("🔴","#e02424","주의")}
        badge = ""
        for ck in ["red","sky","blue"]:
            if ck in ac.values():
                icon, hx, lbl = COLOR_INFO[ck]
                badge = (f"<span style='font-size:.72rem;background:{hx}22;color:{hx};"
                         f"border:1px solid {hx}88;border-radius:4px;padding:2px 8px;"
                         f"display:inline-block;font-weight:700;margin-bottom:6px'>"
                         f"{icon} {lbl}</span><br>")
                break
        with st.expander("✅  Action"):
            if badge:
                st.markdown(badge, unsafe_allow_html=True)
            lang_a = st.radio("언어", ["EN", "한국어"], horizontal=True,
                              key=f"{prefix}alang_{no}", label_visibility="collapsed")
            content = ak if lang_a=="한국어" else ae
            fallback = ae if lang_a=="한국어" else ak
            st.markdown(render_text(content or fallback, "kr" if lang_a=="한국어" else "en"),
                        unsafe_allow_html=True)

    # Company Prep
    cp = item.get("company_prep","")
    if cp and cp.strip():
        with st.expander("🏢  회사준비사항"):
            for line in cp.split("\n"):
                if line.strip():
                    st.markdown(f"<span class='line-en'>{_html.escape(line)}</span>",
                                unsafe_allow_html=True)

    # Finding History
    fh = item.get("Finding History",[])
    if fh:
        with st.expander(f"🗂  Finding History  ({len(fh)}건)"):
            for entry in fh:
                if isinstance(entry, str):
                    st.markdown(f"<div class='fh-entry'>{_html.escape(entry)}</div>",
                                unsafe_allow_html=True)

    # Related Documents
    rd = item.get("related_documents",[])
    if rd:
        with st.expander(f"📎  Related Documents  ({len(rd)}개)"):
            render_rd(item)

# ══════════════════════════════════════════════════════════════
# HEADER
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

# ══════════════════════════════════════════════════════════════
# NAVIGATION
# ══════════════════════════════════════════════════════════════
hr_count = sum(1 for x in active if x.get("High Risk") is True)

page = st.radio(
    "nav",
    [f"🔎  Search by RISQ No.",
     f"🔍  Keyword Search",
     f"🚩  High Risk ({hr_count})"],
    horizontal=True,
    label_visibility="collapsed",
    key="main_nav",
)

st.markdown("---")

DEMO_NOS = [x["NO"] for x in active]

# ══════════════════════════════════════════════════════════════
# PAGE 1 — Search by RISQ No.
# ══════════════════════════════════════════════════════════════
if page.startswith("🔎"):
    risq_no = st.text_input(
        "RISQ No.",
        placeholder="예: 2.9 / 3.7 / 4.16",
        label_visibility="collapsed",
        key="search_no_input",
    )

    if not risq_no:
        st.markdown("<div style='font-size:.82rem;color:var(--muted);margin:8px 0 4px'>수록 항목</div>",
                    unsafe_allow_html=True)
        cols = st.columns(len(DEMO_NOS))
        for i, no in enumerate(DEMO_NOS):
            if cols[i].button(no, key=f"quick_{no}"):
                st.session_state["_jump"] = no
                st.rerun()

    if "_jump" in st.session_state:
        risq_no = st.session_state.pop("_jump")

    if risq_no:
        q = risq_no.strip()
        matches = [x for x in active if x["NO"] == q or x["NO"].startswith(q + ".")]
        if not matches:
            st.warning(f"**{_html.escape(q)}** 항목이 데모에 없습니다. 수록: {', '.join(DEMO_NOS)}")
        for item in matches:
            render_item(item)
            st.divider()

# ══════════════════════════════════════════════════════════════
# PAGE 2 — Keyword Search
# ══════════════════════════════════════════════════════════════
elif page.startswith("🔍"):
    kw_raw = st.text_input(
        "Keyword",
        placeholder="예: UKC  /  gas detector  /  ECDIS  (space = AND 검색)",
        label_visibility="collapsed",
        key="kw_input",
    )
    keywords = [k for k in kw_raw.strip().split() if k]

    if keywords:
        results = []
        for item in active:
            text_pool = " ".join([
                item.get("Description",""),
                item.get("action(E)",""),
                item.get("action(K)",""),
            ])
            if all(k.lower() in text_pool.lower() for k in keywords):
                # snippet
                for fld in ["Description","action(E)"]:
                    v = item.get(fld,"")
                    if v and all(k.lower() in v.lower() for k in keywords):
                        lines = [l.strip() for l in v.split("\n") if l.strip()]
                        snip = next((l for l in lines
                                     if any(k.lower() in l.lower() for k in keywords)),
                                    lines[0] if lines else "")
                        # highlight
                        esc = _html.escape(snip[:200])
                        for kw in keywords:
                            esc = re.sub(re.escape(_html.escape(kw)),
                                         lambda m: f"<mark>{m.group(0)}</mark>",
                                         esc, flags=re.IGNORECASE)
                        results.append((item, esc))
                        break

        st.markdown(f"<div style='font-size:.82rem;color:var(--muted);margin-bottom:8px'>"
                    f"{len(results)}개 결과</div>", unsafe_allow_html=True)
        for item, snippet in results:
            no   = item["NO"]
            is_hr = item.get("High Risk") is True
            hr_badge = "<span class='hr-pill'>⚠ HIGH RISK</span>" if is_hr else ""
            st.markdown(
                f"<div class='kw-card'>"
                f"<div class='kw-no'>RISQ {_html.escape(no)}{hr_badge}</div>"
                f"<div style='font-size:.84rem;color:var(--text)'>{snippet}…</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            if st.button(f"상세 보기 → RISQ {no}", key=f"kw_detail_{no}"):
                st.session_state["_jump"] = no
                st.session_state["main_nav"] = "🔎  Search by RISQ No."
                st.rerun()

# ══════════════════════════════════════════════════════════════
# PAGE 3 — High Risk
# ══════════════════════════════════════════════════════════════
elif page.startswith("🚩"):
    hr_items = [x for x in active if x.get("High Risk") is True]
    st.markdown(f"<p style='color:var(--muted);font-size:.85rem;margin-bottom:16px'>"
                f"High Risk 항목 {len(hr_items)}개</p>",
                unsafe_allow_html=True)
    for item in hr_items:
        render_item(item, prefix="hr_")
        st.divider()

# ══════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div style="margin-top:60px;padding:14px 0;border-top:1px solid var(--border);
text-align:center;font-size:.82rem;color:var(--muted)">
© 2026 RightShip RISQ 3.2 Demo &nbsp;|&nbsp; For demonstration purposes only
</div>
""", unsafe_allow_html=True)
