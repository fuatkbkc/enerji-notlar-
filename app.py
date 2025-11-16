import streamlit as st
import uuid
from datetime import datetime

# Sayfa ayarı
st.set_page_config(page_title="Enerji Notları", page_icon="⚡", layout="wide")

# Şifre kontrolü
def check_password():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div style="text-align:center; padding:50px;">
            <h1>⚡ Enerji Notları</h1>
            <p>Lütfen giriş yapın</p>
        </div>
        """, unsafe_allow_html=True)
        password = st.text_input("Şifre:", type="password", label_visibility="collapsed")
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("Giriş Yap", use_container_width=True):
                if password == "enerji2024":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Hatalı şifre!")
        st.stop()

check_password()

# CSS -  Tarzı
st.markdown("""
<style>
    .main-header {
        background: white;
        border-bottom: 1px solid #eee;
        padding: 15px 0;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .logo {
        font-size: 28px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
    }
    .nav-menu {
        text-align: center;
        margin: 15px 0;
        font-size: 15px;
    }
    .nav-menu a {
        margin: 0 15px;
        color: #7f8c8d;
        text-decoration: none;
    }
    .nav-menu a:hover {
        color: #3498db;
    }
    .section-title {
        color: #7f8c8d;
        text-transform: uppercase;
        font-size: 14px;
        font-weight: bold;
        margin: 30px 0 15px;
        padding-bottom: 5px;
        border-bottom: 1px solid #eee;
    }
    .card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 4px solid #ddd;
        transition: all 0.2s;
    }
    .card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .card.featured { border-left-color: #e74c3c; }
    .card.news { border-left-color: #2ecc71; }
    .card-title {
        font-size: 18px;
        font-weight: bold;
        margin: 0 0 8px;
        color: #2c3e50;
    }
    .card-subtitle {
        font-size: 14px;
        color: #7f8c8d;
        margin-bottom: 10px;
    }
    .card-meta {
        font-size: 13px;
        color: #95a5a6;
        margin-top: 10px;
    }
    .tag {
        display: inline-block;
        background: #ecf0f1;
        color: #7f8c8d;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 12px;
        margin-right: 5px;
    }
    .tag.featured { background: #fadbd8; color: #c0392b; }
    .tag.news { background: #d5f5e3; color: #27ae60; }
    .add-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: #e74c3c;
        color: white;
        border: none;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        font-size: 28px;
        box-shadow: 0 4px 12px rgba(231,76,60,0.4);
        cursor: pointer;
        z-index: 1000;
    }
    .add-button:hover {
        background: #c0392b;
        transform: scale(1.1);
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'contents' not in st.session_state:
    st.session_state.contents = []
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False

# Header - Enerji Notları
st.markdown("""
<div class="main-header">
    <div class="logo">Dragonomi</div>
    <div class="nav-menu">
        <a href="#">Sektör Notları</a>
        <a href="#">Emtia Notları</a>
        <a href="#">Şirket Notları</a>
        <a href="#">Finans Notları</a>
        <a href="#">Günlük Bültenler</a>
        <a href="#">Araştırma Raporları</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Floating Add Button
if st.button("+", key="add_floating", help="Yeni İçerik Ekle"):
    st.session_state.show_add_form = True

# İçerik Ekleme Formu (Modal tarzı)
if st.session_state.show_add_form:
    with st.container():
        st.markdown("## + Yeni İçerik Ekle")
        with st.form("add_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Başlık *", placeholder="Spot Elektrik Fiyatları")
                tags_input = st.text_input("Etiketler *", placeholder="Almanya, Elektrik, Yenilenebilir")
            with col2:
                subtitle = st.text_input("Alt Başlık", placeholder="Mayıs 2023 Verileri")
                date_input = st.text_input("Tarih", value=datetime.now().strftime("%d %B %Y %H:%M"))
            
            content = st.text_area("İçerik *", height=120, placeholder="Detaylı bilgi buraya...")
            
            content_type = st.selectbox("Tür", ["general", "featured", "news"],
                                      format_func=lambda x: {"featured": "Öne Çıkan", "news": "Haber", "general": "Genel"}[x])
            
            if content_type == "featured":
                highlight = st.text_area("Önemli Bilgi", placeholder="Vurgulanacak ana fikir...")
                author = st.text_input("Yazar", value="SADI KAYMAZ")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit = st.form_submit_button("İçeriği Ekle", use_container_width=True)
            with col_btn2:
                if st.form_submit_button("İptal", use_container_width=True):
                    st.session_state.show_add_form = False
                    st.rerun()
            
            if submit:
                if not title or not content or not tags_input:
                    st.error("Başlık, içerik ve etiketler zorunlu!")
                else:
                    # Etiketleri ayrıştır
                    tags = [t.strip() for t in tags_input.split(",") if t.strip()]
                    country = "Türkiye"
                    energy_type = "Elektrik"
                    region = "Ankara"
                    
                    country_options = ["Türkiye", "Almanya", "Fransa", "İtalya", "İspanya", "Çin"]
                    energy_options = ["Elektrik", "Doğal Gaz", "Petrol", "Kömür", "Rüzgar", "Güneş", "Hidroelektrik", "Nükleer", "Çelik", "Çimento"]
                    
                    for tag in tags:
                        if tag in country_options:
                            country = tag
                        elif tag in energy_options:
                            energy_type = tag
                        else:
                            region = tag  # fallback
                    
                    new_content = {
                        "id": str(uuid.uuid4()),
                        "type": content_type,
                        "title": title,
                        "subtitle": subtitle or "",
                        "content": content,
                        "country": country,
                        "region": region,
                        "energy_type": energy_type,
                        "date": date_input,
                        "author": author if content_type == "featured" else "SADI KAYMAZ",
                        "highlight": highlight if content_type == "featured" else ""
                    }
                    st.session_state.contents.append(new_content)
                    st.success("İçerik eklendi!")
                    st.session_state.show_add_form = False
                    st.rerun()

# Ana İçerik: EN SON EKLENENLER
st.markdown("<div class='section-title'>EN SON EKLENENLER</div>", unsafe_allow_html=True)

if not st.session_state.contents:
    st.info("Henüz içerik eklenmedi. Sağ alttaki '+' butonuna tıklayın.")
else:
    # Son 10 içeriği ters sıralı göster
    for content in reversed(st.session_state.contents[-10:]):
        card_class = {
            "featured": "card featured",
            "news": "card news",
            "general": "card"
        }[content["type"]]
        
        tag_class = {
            "featured": "tag featured",
            "news": "tag news",
            "general": "tag"
        }[content["type"]]
        
        tag_text = {
            "featured": "ÖNE ÇIKAN",
            "news": "HABER",
            "general": "SEKTÖR NOTLARI"
        }[content["type"]]

        # Görsel var mı? (Örnek için rastgele)
        has_image = "Çelik" in content["energy_type"] or "Çimento" in content["energy_type"]

        with st.container():
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            
            if has_image:
                col_img, col_text = st.columns([1, 3])
                with col_img:
                    st.image("https://via.placeholder.com/300x200/34495e/ffffff?text=Çelik+Üretim", use_column_width=True)
                with col_text:
                    pass
                st.markdown(f'<span class="{tag_class}">{tag_text}</span>', unsafe_allow_html=True)
                st.markdown(f"<h3 class='card-title'>{content['title']}</h3>", unsafe_allow_html=True)
                if content['subtitle']:
                    st.markdown(f"<p class='card-subtitle'>{content['subtitle']}</p>", unsafe_allow_html=True)
                preview = content['content']
                if len(preview) > 150:
                    preview = preview[:150] + "..."
                st.write(preview)
            else:
                st.markdown(f'<span class="{tag_class}">{tag_text}</span>', unsafe_allow_html=True)
                st.markdown(f"<h3 class='card-title'>{content['title']}</h3>", unsafe_allow_html=True)
                if content['subtitle']:
                    st.markdown(f"<p class='card-subtitle'>{content['subtitle']}</p>", unsafe_allow_html=True)
                preview = content['content']
                if len(preview) > 200:
                    preview = preview[:200] + "..."
                st.write(preview)
            
            st.markdown(f"""
            <div class='card-meta'>
                {content.get('author', 'SADI KAYMAZ')} • {content['date']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")

# Çıkış Butonu (sağ üst)
with st.sidebar:
    if st.button("Çıkış Yap"):
        st.session_state.authenticated = False
        st.rerun()
