import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

# Sayfa ayarları
st.set_page_config(
    page_title="Enerji Veri Blog",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Modern CSS
st.markdown("""
<style>
    /* Ana arkaplan */
    .stApp {
        background-color: #f8f6f0 !important;
    }
    
    /* Ana stil */
    .main {
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
        background-color: transparent;
    }
    
    /* Geniş Header */
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        width: 100%;
        padding: 0;
    }
    
    /* Filtre Container - Simetrik ve Geniş */
    .filter-container {
        width: 100%;
        max-width: 900px;
        margin: 0 auto 2rem auto;
        padding: 1.5rem;
        background: #fefefe;
        border-radius: 12px;
        border: 1px solid #e8e6e1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Filtre Grid - Eşit Genişlik */
    .filter-grid {
        display: flex;
        gap: 1rem;
        justify-content: center;
        align-items: end;
    }
    
    .filter-item {
        flex: 1;
        min-width: 0;
    }
    
    /* Filtre Başlıkları */
    .filter-label {
        font-size: 0.9rem;
        color: #5d6d7e;
        margin-bottom: 0.5rem;
        font-weight: 500;
        text-align: center;
    }
    
    /* Selectbox Stilleri */
    .stSelectbox>div>div>div {
        border-radius: 8px;
        border: 1px solid #d5dbdb;
        background: white;
    }
    
    /* İçerik Alanı */
    .content-container {
        width: 100%;
        max-width: 900px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    /* Bölüm Başlıkları */
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin: 2rem 0 1.5rem 0;
        font-weight: 600;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
        text-align: center;
        width: 100%;
    }
    
    /* Blog Kartları */
    .blog-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e8e6e1;
        transition: all 0.3s ease;
        cursor: pointer;
        width: 100%;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    .blog-card:hover {
        border-color: #3498db;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .blog-title {
        font-size: 1.3rem;
        color: #2c3e50;
        font-weight: 600;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .blog-meta {
        font-size: 0.9rem;
        color: #7f8c8d;
        margin-bottom: 0.5rem;
    }
    
    .blog-tags {
        font-size: 0.8rem;
        color: #2980b9;
        background: #ebf5fb;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        display: inline-block;
        margin-right: 0.5rem;
        margin-top: 0.5rem;
        border: 1px solid #d6eaf8;
    }
    
    .blog-date {
        color: #95a5a6;
        font-weight: 500;
    }
    
    /* Boş İçerik Mesajı */
    .empty-message {
        text-align: center;
        padding: 3rem 2rem;
        color: #7f8c8d;
        font-size: 1.1rem;
        background: #fefefe;
        border-radius: 12px;
        border: 2px dashed #d5dbdb;
        max-width: 900px;
        margin: 0 auto;
    }
    
    /* Butonlar */
    .stButton>button {
        border-radius: 8px;
        height: 3rem;
        font-weight: 600;
        border: none;
        background: #3498db;
        color: white;
        transition: all 0.3s ease;
        padding: 0 1.5rem;
    }
    
    .stButton>button:hover {
        background: #2980b9;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Form elemanları */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #d5dbdb;
        padding: 0.75rem;
        background: white;
    }
    
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 1px solid #d5dbdb;
        background: white;
    }
</style>
""", unsafe_allow_html=True)

# Veri dosyası
DATA_FILE = Path(__file__).parent / "blog_data.json"

# Kullanıcı şifresi
APP_PASSWORD = "enerji2024"

# Veri yükleme ve kaydetme - HATA DÜZELTİLMİŞ
def load_data():
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Eski JSON yapısını yeni yapıya dönüştür
                if "Bölgeler" not in data["basliklar"]:
                    data["basliklar"]["Bölgeler"] = [
                        "Tüm Dünya", "AB", "Avrupa", "Asya", "Orta Asya", "Afrika", 
                        "Ortadoğu", "Kuzey Amerika", "Güney Amerika", "Avustralya & Okyanusya"
                    ]
                    save_data(data)  # Yeni yapıyı kaydet
                return data
        else:
            initial_data = {
                "basliklar": {
                    "Bölgeler": [
                        "Tüm Dünya", "AB", "Avrupa", "Asya", "Orta Asya", "Afrika", 
                        "Ortadoğu", "Kuzey Amerika", "Güney Amerika", "Avustralya & Okyanusya"
                    ],
                    "Ülkeler": [
                        "Almanya", "Türkiye", "ABD", "Fransa", "Çin", "Rusya", 
                        "Japonya", "İngiltere", "İtalya", "İspanya", "Hindistan",
                        "Brezilya", "Kanada", "Güney Kore", "Avustralya"
                    ],
                    "Enerji Kaynakları": [
                        "Doğal Gaz", "Kömür", "Petrol", "Nükleer", "Hidroelektrik",
                        "Güneş", "Rüzgar", "Biyokütle", "Jeotermal", "Hidrojen"
                    ],
                    "Kategoriler": [
                        "Üretim", "Tüketim", "İthalat", "İhracat", "Fiyat", 
                        "Kapasite", "Yatırım", "Politika", "Teknoloji", "Piyasa"
                    ]
                },
                "icerikler": []
            }
            save_data(initial_data)
            return initial_data
    except Exception as e:
        st.error(f"Veri yükleme hatası: {e}")
        # Hata durumunda temel yapıyı dön
        return {
            "basliklar": {
                "Bölgeler": ["Tüm Dünya", "AB", "Avrupa", "Asya"],
                "Ülkeler": ["Almanya", "Türkiye", "ABD"],
                "Enerji Kaynakları": ["Doğal Gaz", "Kömür", "Petrol"],
                "Kategoriler": ["Üretim", "Tüketim", "İthalat"]
            },
            "icerikler": []
        }

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Kaydetme hatası: {e}")
        return False

# Şifre kontrolü
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div style="max-width: 400px; margin: 100px auto; padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid #e8e6e1;">
            <h2 style="text-align: center; color: #2c3e50; margin-bottom: 2rem;">⚡ Enerji Veri Blog</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            password = st.text_input("", placeholder="Şifreyi giriniz...", type="password")
            
            if st.button("Giriş Yap"):
                if password == APP_PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Hatalı şifre!")
        return False
    return True

# Ana uygulama
def main():
    if not check_password():
        return
    
    # Üst navigasyon
    col1, col2, col3, col4, col5 = st.columns([2,1,1,1,1])
    
    with col1:
        st.markdown('<div class="main-header">⚡ Enerji Veri Blog</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("📊 Görüntüle"):
            st.session_state.current_page = "view"
            st.rerun()
    
    with col4:
        if st.button("📝 Yeni"):
            st.session_state.current_page = "add"
            st.rerun()
    
    with col5:
        if st.button("🚪 Çıkış"):
            st.session_state.authenticated = False
            st.rerun()
    
    st.markdown("---")
    
    # Sayfa yönlendirme
    if "current_page" not in st.session_state:
        st.session_state.current_page = "view"
    
    if st.session_state.current_page == "view":
        show_content()
    else:
        add_content()

# İçerik Görüntüleme - HATA DÜZELTİLMİŞ
def show_content():
    data = load_data()
    
    # Eski yapı kontrolü ve dönüşüm
    if "Bölgeler" not in data["basliklar"]:
        data["basliklar"]["Bölgeler"] = [
            "Tüm Dünya", "AB", "Avrupa", "Asya", "Orta Asya", "Afrika", 
            "Ortadoğu", "Kuzey Amerika", "Güney Amerika", "Avustralya & Okyanusya"
        ]
        save_data(data)
    
    # Simetrik Filtre Container - 4 sütun
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    st.markdown('<div class="filter-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="filter-label">🌍 BÖLGE</div>', unsafe_allow_html=True)
        bolge_filter = st.selectbox("bolge_select", ["Tümü"] + data["basliklar"]["Bölgeler"], label_visibility="collapsed")
    
    with col2:
        st.markdown('<div class="filter-label">📍 ÜLKE</div>', unsafe_allow_html=True)
        ulke_filter = st.selectbox("ulke_select", ["Tümü"] + data["basliklar"]["Ülkeler"], label_visibility="collapsed")
    
    with col3:
        st.markdown('<div class="filter-label">⚡ KAYNAK</div>', unsafe_allow_html=True)
        enerji_filter = st.selectbox("enerji_select", ["Tümü"] + data["basliklar"]["Enerji Kaynakları"], label_visibility="collapsed")
    
    with col4:
        st.markdown('<div class="filter-label">📊 KATEGORİ</div>', unsafe_allow_html=True)
        kategori_filter = st.selectbox("kategori_select", ["Tümü"] + data["basliklar"]["Kategoriler"], label_visibility="collapsed")
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # İçerikleri filtreleme
    filtered_content = data["icerikler"]
    
    if bolge_filter != "Tümü":
        filtered_content = [c for c in filtered_content if c.get("bolge") == bolge_filter]
    
    if ulke_filter != "Tümü":
        filtered_content = [c for c in filtered_content if c.get("ulke") == ulke_filter]
    
    if enerji_filter != "Tümü":
        filtered_content = [c for c in filtered_content if c.get("enerji_kaynagi") == enerji_filter]
    
    if kategori_filter != "Tümü":
        filtered_content = [c for c in filtered_content if c.get("kategori") == kategori_filter]
    
    # İçerik container
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">EN SON</div>', unsafe_allow_html=True)

    if not filtered_content:
        st.info("🤷‍♂️ Henüz içerik bulunmuyor. İlk içeriği eklemek için 'Yeni' butonuna tıklayın.")
        return
    
    for content in reversed(filtered_content):
        # Tarihi formatla
        date_obj = datetime.strptime(content["tarih"], "%Y-%m-%d %H:%M:%S")
        formatted_date = date_obj.strftime("%d %b %Y").upper()
        
        with st.container():
            # Etiketleri oluştur
            tags = []
            if content.get("bolge"):
                tags.append(content["bolge"])
            if content.get("ulke"):
                tags.append(content["ulke"])
            if content.get("enerji_kaynagi"):
                tags.append(content["enerji_kaynagi"])
            if content.get("kategori"):
                tags.append(content["kategori"])
            
            tags_html = "".join([f'<span class="blog-tags">{tag}</span>' for tag in tags])
            
            st.markdown(f"""
            <div class="blog-card">
                <div class="blog-title">{content['icerik_baslik']}</div>
                <div class="blog-meta">
                    <span class="blog-date">{formatted_date}</span>
                </div>
                <div>{tags_html}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Detayları göster/gizle
            with st.expander("", expanded=False):
                if content.get("bolge"):
                    st.write("**🌍 Bölge:**", content["bolge"])
                if content.get("ulke"):
                    st.write("**📍 Ülke:**", content["ulke"])
                if content.get("enerji_kaynagi"):
                    st.write("**⚡ Enerji Kaynağı:**", content["enerji_kaynagi"])
                if content.get("kategori"):
                    st.write("**📊 Kategori:**", content["kategori"])
                st.markdown("---")
                st.write(content["icerik_metin"])
                
                if st.button(f"🗑️ Sil", key=f"sil_{content['id']}"):
                    data["icerikler"] = [c for c in data["icerikler"] if c["id"] != content["id"]]
                    save_data(data)
                    st.success("İçerik silindi!")
                    st.rerun()
    
    # Daha fazla butonu
    st.markdown("---")
    st.markdown('<div style="text-align: center; margin: 2rem 0; color: #3498db; font-weight: 600;">DAHA FAZLA İÇERİK</div>', unsafe_allow_html=True)

# Yeni İçerik Ekleme
def add_content():
    st.markdown('<div class="section-header">YENİ İÇERİK EKLE</div>', unsafe_allow_html=True)
    
    data = load_data()
    
    with st.form("yeni_icerik_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            bolge = st.selectbox("🌍 Bölge (İsteğe Bağlı)", [""] + data["basliklar"]["Bölgeler"])
            ulke = st.selectbox("📍 Ülke (İsteğe Bağlı)", [""] + data["basliklar"]["Ülkeler"])
        
        with col2:
            enerji_kaynagi = st.selectbox("⚡ Enerji Kaynağı (İsteğe Bağlı)", [""] + data["basliklar"]["Enerji Kaynakları"])
            kategori = st.selectbox("📊 Kategori (İsteğe Bağlı)", [""] + data["basliklar"]["Kategoriler"])
        
        icerik_baslik = st.text_input("📝 Başlık *", placeholder="Örn: Çin - Elektrik üretimi")
        icerik_metin = st.text_area("📄 İçerik *", height=150, 
                                   placeholder="Detaylı içeriği buraya yazın...")
        
        st.markdown("**\* Zorunlu alanlar**")
        
        submitted = st.form_submit_button("📤 İçeriği Yayınla", use_container_width=True)
        
        if submitted:
            if not icerik_baslik or not icerik_metin:
                st.error("Lütfen başlık ve içerik alanlarını doldurun!")
            else:
                yeni_icerik = {
                    "id": len(data["icerikler"]) + 1,
                    "bolge": bolge if bolge else "",
                    "ulke": ulke if ulke else "",
                    "enerji_kaynagi": enerji_kaynagi if enerji_kaynagi else "",
                    "kategori": kategori if kategori else "",
                    "icerik_baslik": icerik_baslik,
                    "icerik_metin": icerik_metin,
                    "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                data["icerikler"].append(yeni_icerik)
                if save_data(data):
                    st.success("🎉 İçerik başarıyla yayınlandı!")
                    st.session_state.current_page = "view"
                    st.rerun()

if __name__ == "__main__":
    main()
