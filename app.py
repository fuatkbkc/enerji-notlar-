import streamlit as st
import uuid
from datetime import datetime

# Sayfa ayarları
st.set_page_config(page_title="Enerji Notları", page_icon="⚡", layout="wide")

# Şifre kontrolü
def check_password():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align:center;'>⚡ Enerji Notları</h1>", unsafe_allow_html=True)
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

# CSS
st.markdown("""
<style>
    .main-container { max-width: 900px; margin: auto; padding: 20px; }
    .header { text-align: center; margin: 20px 0; color: #2c3e50; }
    .search-box { margin: 20px 0; }
    .add-button { 
        position: fixed; bottom: 30px; right: 30px; 
        background: #e74c3c; color: white; font-size: 24px;
        width: 56px; height: 56px; border-radius: 50%;
        border: none; box-shadow: 0 4px 12px rgba(231,76,60,0.3);
        z-index: 1000; cursor: pointer;
    }
    .add-button:hover { background: #c0392b; transform: scale(1.1); }
    .content-card {
        background: white; border-radius: 12px; padding: 18px;
        margin: 15px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #3498db; cursor: pointer;
        transition: all 0.2s;
    }
    .content-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); }
    .content-title { font-size: 18px; font-weight: bold; margin: 0 0 8px; color: #2c3e50; }
    .content-preview { color: #7f8c8d; font-size: 14px; line-height: 1.5; }
    .content-full { margin-top: 15px; padding-top: 15px; border-top: 1px solid #eee; }
    .meta { font-size: 12px; color: #95a5a6; margin-top: 10px; }
    .action-btn { font-size: 12px; padding: 4px 8px; margin-right: 5px; }
    .no-results { text-align: center; color: #95a5a6; font-style: italic; padding: 30px; }
</style>
""", unsafe_allow_html=True)

# Session state
if 'contents' not in st.session_state:
    st.session_state.contents = []
if 'expanded' not in st.session_state:
    st.session_state.expanded = {}
if 'editing' not in st.session_state:
    st.session_state.editing = None
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# Header
st.markdown("<div class='header'><h2>⚡ Enerji Notları</h2></div>", unsafe_allow_html=True)
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# ARAMA ÇUBUĞU
search = st.text_input(
    "🔍 Arama yapın (başlıkta ara)",
    value=st.session_state.search_query,
    placeholder="Örn: elektrik, doğalgaz, almanya...",
    key="search_input",
    label_visibility="collapsed"
)
st.session_state.search_query = search.strip().lower()

# Floating + Buton
if st.button("+", key="add_fab", help="Yeni not ekle"):
    st.session_state.editing = "new"

# Yeni Ekleme / Düzenleme Formu
if st.session_state.editing:
    is_new = st.session_state.editing == "new"
    edit_content = None
    if not is_new:
        edit_content = next((c for c in st.session_state.contents if c["id"] == st.session_state.editing), None)

    with st.form(key="edit_form", clear_on_submit=True):
        title = st.text_input("Başlık *", value=edit_content["title"] if edit_content else "")
        content = st.text_area("İçerik *", height=150, value=edit_content["content"] if edit_content else "")

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
                    st.rerun()
        with col2:
            if st.form_submit_button("İptal", use_container_width=True):
                st.session_state.editing = None
                st.rerun()

# FİLTRELENMİŞ İÇERİKLER
filtered_contents = [
    c for c in st.session_state.contents
    if st.session_state.search_query == "" or st.session_state.search_query in c["title"].lower()
]

# Arama Sonucu Yoksa
if st.session_state.search_query and not filtered_contents:
    st.markdown(f"<div class='no-results'>'{st.session_state.search_query}' ile eşleşen not bulunamadı.</div>", unsafe_allow_html=True)
else:
    # Son eklenen en üstte
    for content in reversed(filtered_contents):
        content_id = content["id"]
        is_expanded = st.session_state.expanded.get(content_id, False)

        with st.container():
            # Kart başlığı (tıklanınca açılır)
            if st.button(
                f"**{content['title']}**",
                key=f"title_{content_id}",
                use_container_width=True,
                help="Tıkla → içerik açılsın"
            ):
                st.session_state.expanded[content_id] = True
                st.rerun()

            # Önizleme (kapalıyken)
            if not is_expanded:
                preview = content['content']
                if len(preview) > 120:
                    preview = preview[:120] + "..."
                st.markdown(f"<div class='content-preview'>{preview}</div>", unsafe_allow_html=True)

            # Açık ise tam içerik + butonlar
            if is_expanded:
                st.markdown(f"""
                <div class="content-full">
                    {content['content'].replace(chr(10), '<br>')}
                    <div class="meta">Eklenme: {content['date']}</div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns([1, 1, 3])
                with col1:
                    if st.button("✏️ Düzenle", key=f"edit_{content_id}"):
                        st.session_state.editing = content_id
                        st.rerun()
                with col2:
                    if st.button("↑ Kapat", key=f"collapse_{content_id}"):
                        st.session_state.expanded[content_id] = False
                        st.rerun()
                with col3:
                    if st.button("🗑️ Sil", key=f"delete_{content_id}"):
                        st.session_state.contents = [c for c in st.session_state.contents if c["id"] != content_id]
                        st.session_state.expanded.pop(content_id, None)
                        st.rerun()

                st.markdown("---")

st.markdown("</div>", unsafe_allow_html=True)

# Çıkış
with st.sidebar:
    if st.button("Çıkış Yap"):
        st.session_state.authenticated = False
        st.rerun()
