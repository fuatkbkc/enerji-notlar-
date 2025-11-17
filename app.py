import streamlit as st
import uuid
from datetime import datetime
import json
import os

# ===================== KALICI KAYIT =====================
DATA_FILE = "enerji_notlari.json"

def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.contents, f, ensure_ascii=False, indent=2)
    except:
        pass

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# ===================== SAYFA AYARLARI =====================
st.set_page_config(page_title="Enerji Notları", page_icon="Lightning", layout="wide")

# ===================== ŞİFRE KONTROLÜ =====================
def check_password():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align:center;'>Lightning Enerji Notları</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Giriş yapın</p>", unsafe_allow_html=True)
        password = st.text_input("Şifre:", type="password", label_visibility="collapsed")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Giriş Yap", use_container_width=True):
                if password == "enerji2024":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Hatalı şifre!")
        st.stop()

check_password()

# ===================== VERİ YÜKLEME =====================
if 'contents' not in st.session_state:
    st.session_state.contents = load_data()

if 'expanded' not in st.session_state:
    st.session_state.expanded = {}
if 'editing' not in st.session_state:
    st.session_state.editing = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# ===================== CSS + FAB BUTON =====================
st.markdown("""
<style>
    .main-container { max-width: 900px; margin: auto; padding: 20px 20px 80px 20px; }
    .header { text-align: center; margin: 30px 0; color: #2c3e50; }
    .content-preview { color: #7f8c8d; font-size: 14px; line-height: 1.5; }
    .content-full { margin-top: 15px; padding-top: 15px; border-top: 1px solid #eee; }
    .meta { font-size: 12px; color: #95a5a6; margin-top: 10px; }
    .no-results { text-align: center; color: #95a5a6; font-style: italic; padding: 40px; }
    
    /* Floating Action Button */
    .fab {
        position: fixed !important;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
    }
    .fab > button {
        background: #e74c3c !important;
        color: white !important;
        border: none !important;
        width: 64px !important;
        height: 64px !important;
        border-radius: 50% !important;
        font-size: 32px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(231,76,60,0.5) !important;
    }
    .fab > button:hover {
        background: #c0392b !important;
        transform: scale(1.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================== FAB BUTON (TEK VE DOĞRU) =====================
with st.container():
    st.markdown('<div class="fab">', unsafe_allow_html=True)
    if st.button("+", key="fab_add_new"):
        st.session_state.editing = "new"
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("<div class='header'><h2>Lightning Enerji Notları</h2></div>", unsafe_allow_html=True)
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# ===================== ARAMA ÇUBUĞU =====================
search = st.text_input(
    "Arama (başlıkta)",
    value=st.session_state.search_query,
    placeholder="Örn: elektrik, almanya, fiyat...",
    key="search_input",
    label_visibility="collapsed"
)
st.session_state.search_query = search.strip().lower()

# ===================== YENİ / DÜZENLE FORMU =====================
if st.session_state.editing:
    is_new = st.session_state.editing == "new"
    edit_content = None
    if not is_new:
        edit_content = next((c for c in st.session_state.contents if c["id"] == st.session_state.editing), None)

    with st.form("edit_form", clear_on_submit=True):
        title = st.text_input("Başlık *", value=edit_content["title"] if edit_content else "")
        content = st.text_area("İçerik *", height=200, value=edit_content["content"] if edit_content else "")

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Kaydet", use_container_width=True):
                if not title.strip() or not content.strip():
                    st.error("Başlık ve içerik boş olamaz!")
                else:
                    new_item = {
                        "id": str(uuid.uuid4()) if is_new else edit_content["id"],
                        "title": title.strip(),
                        "content": content.strip(),
                        "date": datetime.now().strftime("%d %B %Y %H:%M")
                    }
                    if is_new:
                        st.session_state.contents.append(new_item)
                    else:
                        idx = next(i for i, c in enumerate(st.session_state.contents) if c["id"] == edit_content["id"])
                        st.session_state.contents[idx] = new_item
                    st.session_state.editing = None
                    st.success("Kaydedildi!")
                    save_data()
                    st.rerun()
        with col2:
            if st.form_submit_button("İptal", use_container_width=True):
                st.session_state.editing = None
                st.rerun()

# ===================== İÇERİK LİSTESİ =====================
filtered = [
    c for c in st.session_state.contents
    if not st.session_state.search_query or st.session_state.search_query in c["title"].lower()
]

if st.session_state.search_query and not filtered:
    st.markdown(f"<div class='no-results'>'{search}' ile eşleşen not bulunamadı.</div>", unsafe_allow_html=True)
elif not st.session_state.contents:
    st.info("Henüz not eklenmedi. Sağ alttaki kırmızı '+' butonuna tıklayın.")
else:
    for content in reversed(filtered):
        cid = content["id"]
        expanded = st.session_state.expanded.get(cid, False)

        with st.container():
            if st.button(f"**{content['title']}**", key=f"open_{cid}", use_container_width=True):
                st.session_state.expanded[cid] = True
                st.rerun()

            if not expanded:
                preview = content['content'][:140] + ("..." if len(content['content']) > 140 else "")
                st.markdown(f"<div class='content-preview'>{preview}</div>", unsafe_allow_html=True)

            if expanded:
                st.markdown(f"<div class='content-full'>{content['content'].replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='meta'>Eklenme: {content['date']}</div>", unsafe_allow_html=True)

                c1, c2, c3 = st.columns([1, 1, 4])
                with c1:
                    if st.button("Düzenle", key=f"edit_{cid}"):
                        st.session_state.editing = cid
                        st.rerun()
                with c2:
                    if st.button("Kapat", key=f"close_{cid}"):
                        st.session_state.expanded[cid] = False
                        st.rerun()
                with c3:
                    if st.button("Sil", key=f"del_{cid}"):
                        st.session_state.contents = [c for c in st.session_state.contents if c["id"] != cid]
                        st.session_state.expanded.pop(cid, None)
                        save_data()
                        st.rerun()
                st.markdown("---")

st.markdown("</div>", unsafe_allow_html=True)

# ===================== OTOMATİK KAYDET =====================
save_data()

# ===================== ÇIKIŞ =====================
with st.sidebar:
    st.markdown("### Ayarlar")
    if st.button("Çıkış Yap"):
        st.session_state.authenticated = False
        st.rerun()
