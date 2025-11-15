import streamlit as st
import json
import uuid
from datetime import datetime

# Sayfa ayarı
st.set_page_config(
    page_title="Enerji Veri Blog",
    page_icon="⚡",
    layout="wide"
)

# Şifre kontrolü
def check_password():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("🔐 Enerji Veri Blog - Giriş")
        password = st.text_input("Şifre:", type="password")
        if st.button("Giriş Yap"):
            if password == "enerji2024":  # Bu şifreyi değiştirebilirsiniz
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Hatalı şifre!")
        st.stop()

# Şifreyi kontrol et
check_password()

# CSS stilini ekle
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #2c3e50, #3498db);
        color: white;
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        border-radius: 10px;
    }
    
    .logo {
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        flex: 1;
    }
    
    .nav-container {
        display: flex;
        gap: 10px;
    }
    
    .nav-item {
        padding: 10px 20px;
        background-color: rgba(255,255,255,0.1);
        border-radius: 25px;
        text-align: center;
    }
    
    .featured-article {
        background: white;
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #3498db;
    }
    
    .news-item {
        background: white;
        padding: 20px;
        margin: 15px 0;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #2c3e50;
    }
    
    .highlight {
        background-color: #e8f4fd;
        padding: 15px;
        border-left: 4px solid #1abc9c;
        margin: 15px 0;
        border-radius: 5px;
    }
    
    .content-form {
        background: white;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'contents' not in st.session_state:
    st.session_state.contents = []

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "view"

# Header
st.markdown("""
<div class="header">
    <div class="logo">⚡ Enerji Veri Blog</div>

   
</div>
""", unsafe_allow_html=True)

# Yönetim butonları
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if st.button("📝 Yeni İçerik Ekle", use_container_width=True):
        st.session_state.active_tab = "add"

with col2:
    if st.button("İçerikleri Görüntüle", use_container_width=True):
        st.session_state.active_tab = "view"

with col3:
    if st.button("Çıkış", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# İçerik görüntüleme
if st.session_state.active_tab == "view":
    st.markdown("## 📋 Mevcut İçerikler")
    
    if not st.session_state.contents:
        st.info("📝 Henüz içerik eklenmemiş. Yeni içerik eklemek için 'Yeni İçerik Ekle' butonuna tıklayın.")
    else:
        for i, content in enumerate(st.session_state.contents):
            with st.container():
                if content["type"] == "featured":
                    st.markdown(f"""
                    <div class="featured-article">
                        <h2>{content['title']}</h2>
                        <p><strong>Ülke:</strong> {content.get('country', 'Türkiye')} | <strong>Bölge:</strong> {content.get('region', 'Ankara')}</p>
                        <p>{content['content']}</p>
                        <div class="highlight">
                            <p><strong>📊 Enerji Kalemi:</strong> {content.get('energy_type', 'Elektrik')}</p>
                            <p><strong>💡 Önemli Bilgi:</strong> {content.get('highlight', '')}</p>
                        </div>
                        <p><strong>👤 Yazar:</strong> {content.get('author', '')} | <strong>📅 Tarih:</strong> {content.get('date', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="news-item">
                        <h3>{content['title']}</h3>
                        <p><strong>Ülke:</strong> {content.get('country', 'Türkiye')} | <strong>Bölge:</strong> {content.get('region', 'Ankara')}</p>
                        <p><strong>📊 Enerji Kalemi:</strong> {content.get('energy_type', 'Elektrik')}</p>
                        <p><strong>📅 Tarih:</strong> {content.get('date', '')}</p>
                        <p>{content['content']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Silme butonu
                col1, col2 = st.columns([4, 1])
                with col2:
                    if st.button(f"🗑️ Sil", key=f"delete_{i}", use_container_width=True):
                        st.session_state.contents.pop(i)
                        st.rerun()
                
                st.markdown("---")

# İçerik ekleme formu
elif st.session_state.active_tab == "add":
    st.markdown("## ➕ Yeni İçerik Ekle")
    
    with st.form("add_content_form", clear_on_submit=True):
        st.markdown('<div class="content-form">', unsafe_allow_html=True)
        
        content_type = st.selectbox("İçerik Türü", ["featured", "news", "general"], 
                                  format_func=lambda x: {"featured": "📌 Öne Çıkan", "news": "📰 Haber", "general": "📄 Genel"}[x])
        
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Başlık *", placeholder="Örn: Spot Elektrik Fiyatları")
            country = st.selectbox("Ülke *", ["Türkiye", "Almanya", "Fransa", "İtalya", "İspanya", "Diğer"])
            energy_type = st.selectbox("Enerji Kalemi *", ["Elektrik", "Doğal Gaz", "Petrol", "Kömür", "Rüzgar", "Güneş", "Hidroelektrik", "Nükleer"])
        
        with col2:
            subtitle = st.text_input("Alt Başlık", placeholder="Örn: Mayıs 2023 Verileri")
            region = st.text_input("Bölge *", value="Ankara", placeholder="Bölge adı")
            date = st.text_input("Tarih *", value=datetime.now().strftime("%d %B %Y %H:%M"))
        
        content = st.text_area("İçerik *", height=150, placeholder="İçerik detaylarını buraya yazın...")
        
        if content_type == "featured":
            highlight = st.text_area("Önemli Bilgi", placeholder="Vurgulanacak önemli bilgiyi yazın...")
            author = st.text_input("Yazar", placeholder="Yazar adı")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            submitted = st.form_submit_button("✅ İçeriği Ekle", use_container_width=True)
        with col2:
            clear = st.form_submit_button("🔄 Formu Temizle", use_container_width=True)
        with col3:
            cancel = st.form_submit_button("❌ İptal", use_container_width=True)
        
        if submitted:
            if not title or not content:
                st.error("❌ Lütfen başlık ve içerik alanlarını doldurun!")
            else:
                new_content = {
                    "id": str(uuid.uuid4()),
                    "type": content_type,
                    "title": title,
                    "subtitle": subtitle,
                    "content": content,
                    "country": country,
                    "region": region,
                    "energy_type": energy_type,
                    "date": date
                }
                
                if content_type == "featured":
                    new_content["highlight"] = highlight
                    new_content["author"] = author
                
                st.session_state.contents.append(new_content)
                st.success("✅ İçerik başarıyla eklendi!")
                st.session_state.active_tab = "view"
                st.rerun()
        
        if cancel:
            st.session_state.active_tab = "view"
            st.rerun()

# Basit istatistik gösterimi (sadece sayı)
if st.session_state.contents:
    st.sidebar.markdown("### 📊 Özet")
    st.sidebar.metric("Toplam İçerik", len(st.session_state.contents))
    
    # İçerik türlerine göre filtreleme
    energy_types = list(set([content.get('energy_type', 'Elektrik') for content in st.session_state.contents]))
    selected_energy = st.sidebar.selectbox("Enerji Kalemine Göre Filtrele", ["Tümü"] + energy_types)
    
    if selected_energy != "Tümü":
        filtered_contents = [c for c in st.session_state.contents if c.get('energy_type') == selected_energy]
        st.sidebar.metric(f"{selected_energy} İçerikleri", len(filtered_contents))

# Çıkış için JavaScript
st.markdown("""
<script>
function logout() {
    // Streamlit'te çıkış işlemi
    window.parent.document.querySelector('.nav-item').click();
}
</script>
""", unsafe_allow_html=True)
