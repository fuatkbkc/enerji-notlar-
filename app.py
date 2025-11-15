import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa ayarı
st.set_page_config(
    page_title="Enerji Veri Blog",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS stilini ekle
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .header {
        background: linear-gradient(135deg, #2c3e50, #3498db);
        color: white;
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        text-align: center;
    }
    
    .nav-item:hover {
        background-color: #1abc9c;
        transform: translateY(-2px);
    }
    
    .featured-article {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #3498db;
    }
    
    .tabs-container {
        display: flex;
        margin-bottom: 20px;
        background: white;
        border-radius: 10px;
        padding: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .tab {
        padding: 12px 25px;
        background-color: #f8f9fa;
        border-radius: 8px;
        margin-right: 5px;
        cursor: pointer;
        transition: all 0.3s;
        flex: 1;
        text-align: center;
        font-weight: 500;
    }
    
    .tab.active {
        background-color: #3498db;
        color: white;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
    }
    
    .tab-content {
        display: none;
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .tab-content.active {
        display: block;
    }
    
    .content-section {
        margin-bottom: 25px;
    }
    
    .news-item {
        margin-bottom: 20px;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #3498db;
    }
    
    .highlight {
        background-color: #e8f4fd;
        padding: 20px;
        border-left: 4px solid #1abc9c;
        margin: 20px 0;
        border-radius: 8px;
    }
    
    .author {
        font-style: italic;
        color: #7f8c8d;
        text-align: right;
        margin-top: 20px;
        font-size: 14px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header bölümü
st.markdown("""
<div class="header">
    <div class="nav-container">
        <div class="nav-item" onclick="switchTab('content')">İçerik</div>
        <div class="nav-item" onclick="switchTab('image')">Görüntü</div>
    </div>
    <div class="logo">⚡ Enerji Veri Blog</div>
    <div class="nav-container">
        <div class="nav-item" onclick="logout()">Çıkış</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Öne çıkan makale
st.markdown("""
<div class="featured-article">
    <h1>Spot Piyasada Elektrik ve Doğal Gaz Fiyatları</h1>
    <p>Enerji piyasalarında günlük olarak belirlenen spot elektrik ve doğal gaz fiyatları, enerji maliyetlerinin yönetimi açısından büyük önem taşıyor. 18 Mayıs 2023 tarihli verilere göre, Enerji Piyasaları İşletme A.Ş. (EPİAŞ) tarafından işletilen Enerji Borsası İstanbul'da (EXIST) elektrik piyasasında işlem hacmi 847 milyon Türk lirası olarak gerçekleşti.</p>
    
    <div class="highlight">
        <p><strong>📊 Önemli Bilgi:</strong> 19 Mayıs Cuma günü için spot piyasada megavatsaat başına en yüksek elektrik fiyatı 2.600 Türk lirası olarak belirlendi. En düşük fiyat ise 1.424,34 lira ile sabah 06:00'da kaydedildi.</p>
    </div>
    
    <p>Doğal gaz piyasasında ise 17 Mayıs Çarşamba günü için spot piyasada 1.000 metreküp doğal gazın fiyatı 9.182,35 Türk lirası olarak belirlendi. Enerji fiyatlarındaki bu dalgalanmalar, hem üreticiler hem de tüketiciler için maliyet planlaması açısından kritik öneme sahip.</p>
    
    <p class="author">Yazar: Duvgu Aihan</p>
</div>
""", unsafe_allow_html=True)

# Sekmeler
col1, col2 = st.columns(2)

with col1:
    if st.button("📝 İçerik", use_container_width=True, key="content_btn"):
        st.session_state.active_tab = "content"

with col2:
    if st.button("🖼️ Görüntü", use_container_width=True, key="image_btn"):
        st.session_state.active_tab = "image"

# Varsayılan sekme
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "content"

# İçerik sekmesi
if st.session_state.active_tab == "content":
    st.markdown("### 📈 Enerji Piyasası Verileri")
    
    # Metrik kartlar
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Elektrik İşlem Hacmi",
            value="847 M TL",
            delta="-21.2%"
        )
    
    with col2:
        st.metric(
            label="En Yüksek Elektrik Fiyatı",
            value="2.600 TL/MWh",
            delta="+8.3%"
        )
    
    with col3:
        st.metric(
            label="Doğal Gaz Fiyatı",
            value="9.182 TL",
            delta="+2.1%"
        )
    
    # Haber içerikleri
    st.markdown("---")
    st.markdown("### 📰 Son Gelişmeler")
    
    with st.expander("18 Mayıs 2023 14:24 - Elektrik Fiyatları", expanded=True):
        st.write("""
        **Spot market electricity prices for Friday, May 19**
        
        Energy Exchange Istanbul (EXIST) data shows electricity market trade amounts to 847 million Turkish liras.
        
        The highest electricity price rate for one megawatt-hour on Türkiye's day-ahead spot market for Friday will be 2,600 Turkish liras at 8 p.m. (1700 GMT), according to official figures on Thursday.
        
        The lowest rate was set at 1,424.34 liras at 6 a.m. local time (0300 GMT).
        """)
    
    with st.expander("18 Mayıs 2023 14:14 - Doğal Gaz Fiyatları"):
        st.write("""
        **Spot market natural gas prices for Wednesday, May 17**
        
        1,000 cubic meters of natural gas on spot market costs 9,182.35 Turkish liras.
        
        Doğal gaz piyasasında spot fiyatlar döviz kuruna paralel olarak hareket etmektedir.
        """)
    
    with st.expander("Detaylı Piyasa Analizi"):
        st.write("""
        The Energy Exchange Istanbul (EXIST) data for the trade volume on Thursday's electricity market showed a decrease of 21.2% to 847 million liras compared to Wednesday.
        
        The arithmetical and weighted average electricity prices on the day-ahead spot market are calculated as 1,893.76 liras and 1,899.899 liras, respectively.
        
        US$1 equals 19.79 liras at 2.23 p.m. local time (1123 GMT) on Thursday.
        """)

# Görüntü sekmesi
elif st.session_state.active_tab == "image":
    st.markdown("### 📊 Görsel Veriler")
    
    # Örnek grafikler
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Elektrik Fiyat Dağılımı")
        # Örnek data
        data = pd.DataFrame({
            'Saat': list(range(24)),
            'Fiyat (TL/MWh)': [1424, 1450, 1480, 1520, 1600, 1650, 1700, 1800, 
                              1900, 2100, 2300, 2500, 2600, 2550, 2400, 2200,
                              2000, 1900, 1850, 1800, 1750, 1700, 1650, 1600]
        })
        st.line_chart(data, x='Saat', y='Fiyat (TL/MWh)')
    
    with col2:
        st.markdown("#### Günlük İşlem Hacmi")
        volume_data = pd.DataFrame({
            'Gün': ['Pzt', 'Salı', 'Çar', 'Per', 'Cum'],
            'Hacim (M TL)': [1074, 980, 895, 847, 820]
        })
        st.bar_chart(volume_data, x='Gün', y='Hacim (M TL)')
    
    st.markdown("---")
    st.markdown("#### 📈 Piyasa Göstergeleri")
    
    # Gösterge kartları
    indicators = {
        "Ortalama Elektrik Fiyatı": "1.893,76 TL",
        "Ağırlıklı Ortalama": "1.899,90 TL",
        "Dolar/TL Kuru": "19,79",
        "Piyasa Hacmi": "847 M TL"
    }
    
    cols = st.columns(4)
    for i, (key, value) in enumerate(indicators.items()):
        with cols[i]:
            st.info(f"**{key}**\n\n### {value}")

# JavaScript fonksiyonları için
st.markdown("""
<script>
function switchTab(tabName) {
    // Streamlit'te buton tıklama işlemi
    if (tabName === 'content') {
        window.parent.document.querySelector('[data-testid="baseButton-secondary"]').click();
    } else if (tabName === 'image') {
        window.parent.document.querySelector('[data-testid="baseButton-secondary"]').click();
    }
}

function logout() {
    alert('Çıkış yapılıyor...');
}
</script>
""", unsafe_allow_html=True)
