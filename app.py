import streamlit as st
import uuid
from datetime import datetime

# Sayfa ayarı
st.set_page_config(
    page_title="Enerji Verileri",
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
            if password == "enerji2024":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Hatalı şifre!")
        st.stop()

check_password()

# CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2c3e50, #3498db);
        color: white;
        padding: 15px 20px;
        text-align: center;
        margin-bottom: 20px;
        border-radius: 10px;
        margin-top: -10px;
    }
    
    .content-item {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #3498db;
    }
    
    .featured-item {
        border-left: 5px solid #e74c3c;
    }
    
    .news-item {
        border-left: 5px solid #2ecc71;
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
    
    .recent-sidebar {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    
    .recent-item {
        padding: 10px;
        margin: 5px 0;
        background: #f8f9fa;
        border-radius: 5px;
        border-left: 3px solid #3498db;
        cursor: pointer;
    }
    
    .recent-item:hover {
        background: #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'contents' not in st.session_state:
    st.session_state.contents = []

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "view"

if 'expanded_items' not in st.session_state:
    st.session_state.expanded_items = {}

if 'selected_content' not in st.session_state:
    st.session_state.selected_content = None

# Header
st.markdown("""
<div class="main-header">
    <div style="font-size: 32px; font-weight: bold;">⚡ Enerji Veri Blog</div>
</div>
""", unsafe_allow_html=True)

# Ana layout
main_col, sidebar_col = st.columns([3, 1])

with main_col:
    # Butonlar
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("📝 Yeni İçerik Ekle", use_container_width=True):
            st.session_state.active_tab = "add"
            st.session_state.selected_content = None
    
    with col2:
        if st.button("👁️ Tüm İçerikler", use_container_width=True):
            st.session_state.active_tab = "view"
            st.session_state.selected_content = None
    
    with col3:
        if st.button("🚪 Çıkış", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # İÇERİK GÖRÜNTÜLEME
    if st.session_state.active_tab == "view":
        if st.session_state.selected_content is not None:
            # Detay görünümü
            content = st.session_state.selected_content
            st.markdown("## 📖 İçerik Detayı")
            
            item_class = "content-item"
            if content["type"] == "featured":
                item_class += " featured-item"
            elif content["type"] == "news":
                item_class += " news-item"
            
            st.markdown(f"""
            <div class="{item_class}">
                <h2>{content['title']}</h2>
                {f"<h4 style='color: #666;'>{content['subtitle']}</h4>" if content.get('subtitle') else ""}
                <p><strong>🌍 Ülke:</strong> {content.get('country', 'Türkiye')} | <strong>📍 Bölge:</strong> {content.get('region', 'Ankara')}</p>
                <p><strong>📊 Enerji Kalemi:</strong> {content.get('energy_type', 'Elektrik')}</p>
                <p><strong>📅 Tarih:</strong> {content.get('date', '')}</p>
                <div style="margin: 20px 0; padding: 20px 0; border-top: 1px solid #eee; border-bottom: 1px solid #eee; line-height: 1.6;">
                    {content['content'].replace(chr(10), '<br>')}
                </div>
                {f'<div class="highlight"><strong>💡 Önemli Bilgi:</strong> {content.get("highlight", "")}</div>' if content.get("highlight") else ""}
                {f'<p><strong>👤 Yazar:</strong> {content.get("author", "")}</p>' if content.get("author") else ""}
            </div>
            """, unsafe_allow_html=True)
            
            # Butonlar
            col_back, col_space, col_delete = st.columns([2, 3, 1])
            with col_back:
                if st.button("⬅️ Geri", use_container_width=True):
                    st.session_state.selected_content = None
                    st.rerun()
            with col_delete:
                if st.button("🗑️ Sil", use_container_width=True):
                    st.session_state.contents = [c for c in st.session_state.contents if c["id"] != content["id"]]
                    st.session_state.selected_content = None
                    st.rerun()
        
        else:
            # Liste görünümü
            st.markdown("## 📋 Tüm İçerikler")
            
            if not st.session_state.contents:
                st.info("📝 Henüz içerik eklenmemiş. 'Yeni İçerik Ekle' butonuna tıklayın.")
            else:
                for i, content in enumerate(st.session_state.contents):
                    is_expanded = st.session_state.expanded_items.get(content["id"], False)
                    
                    item_class = "content-item"
                    if content["type"] == "featured":
                        item_class += " featured-item"
                    elif content["type"] == "news":
                        item_class += " news-item"
                    
                    # İçerik önizleme
                    content_preview = content['content']
                    if not is_expanded and len(content['content']) > 200:
                        content_preview = content['content'][:200] + "..."
                    
                    if is_expanded:
                        # Genişletilmiş görünüm
                        st.markdown(f"""
                        <div class="{item_class}">
                            <h3>{content['title']}</h3>
                            {f"<h5 style='color: #666;'>{content['subtitle']}</h5>" if content.get('subtitle') else ""}
                            <p><strong>🌍 Ülke:</strong> {content.get('country', 'Türkiye')} | <strong>📍 Bölge:</strong> {content.get('region', 'Ankara')}</p>
                            <p><strong>📊 Enerji Kalemi:</strong> {content.get('energy_type', 'Elektrik')} | <strong>📅 Tarih:</strong> {content.get('date', '')}</p>
                            <div style="margin: 15px 0; line-height: 1.6;">
                                {content['content'].replace(chr(10), '<br>')}
                            </div>
                            {f'<div class="highlight"><strong>💡 Önemli Bilgi:</strong> {content.get("highlight", "")}</div>' if content.get("highlight") else ""}
                            {f'<p><strong>👤 Yazar:</strong> {content.get("author", "")}</p>' if content.get("author") else ""}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_btn1, col_btn2, col_btn3 = st.columns([1, 3, 1])
                        with col_btn1:
                            if st.button("▲ Daralt", key=f"collapse_{i}", use_container_width=True):
                                st.session_state.expanded_items[content["id"]] = False
                                st.rerun()
                        with col_btn3:
                            if st.button("📖 Detay", key=f"detail_{i}", use_container_width=True):
                                st.session_state.selected_content = content
                                st.rerun()
                    
                    else:
                        # Daraltılmış görünüm
                        st.markdown(f"""
                        <div class="{item_class}">
                            <h3>{content['title']}</h3>
                            {f"<h5 style='color: #666;'>{content['subtitle']}</h5>" if content.get('subtitle') else ""}
                            <p><strong>🌍 Ülke:</strong> {content.get('country', 'Türkiye')} | <strong>📍 Bölge:</strong> {content.get('region', 'Ankara')}</p>
                            <p><strong>📊 Enerji Kalemi:</strong> {content.get('energy_type', 'Elektrik')} | <strong>📅 Tarih:</strong> {content.get('date', '')}</p>
                            <div style="margin: 15px 0; line-height: 1.6;">
                                {content_preview.replace(chr(10), '<br>')}
                            </div>
                            <div style="text-align: center; color: #3498db; font-weight: bold; margin-top: 10px;">
                                ▼ Daha fazla göster
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_btn1, col_btn2, col_btn3 = st.columns([1, 3, 1])
                        with col_btn1:
                            if st.button("▼ Genişlet", key=f"expand_{i}", use_container_width=True):
                                st.session_state.expanded_items[content["id"]] = True
                                st.rerun()
                        with col_btn3:
                            if st.button("📖 Detay", key=f"detail_small_{i}", use_container_width=True):
                                st.session_state.selected_content = content
                                st.rerun()
                    
                    # Silme butonu
                    if st.button(f"🗑️ Bu İçeriği Sil", key=f"delete_{i}", use_container_width=True):
                        if content["id"] in st.session_state.expanded_items:
                            del st.session_state.expanded_items[content["id"]]
                        st.session_state.contents.pop(i)
                        st.rerun()
                    
                    st.markdown("---")

    # İÇERİK EKLEME
    elif st.session_state.active_tab == "add":
        st.markdown("## ➕ Yeni İçerik Ekle")
        
        with st.form("add_content_form"):
            content_type = st.selectbox("İçerik Türü", ["featured", "news", "general"], 
                                      format_func=lambda x: {"featured": "📌 Öne Çıkan", "news": "📰 Haber", "general": "📄 Genel"}[x])
            
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Başlık *", placeholder="Spot Elektrik Fiyatları")
                country = st.selectbox("Ülke *", ["Türkiye", "Almanya", "Fransa", "İtalya", "İspanya", "Diğer"])
                energy_type = st.selectbox("Enerji Kalemi *", ["Elektrik", "Doğal Gaz", "Petrol", "Kömür", "Rüzgar", "Güneş", "Hidroelektrik", "Nükleer"])
            
            with col2:
                subtitle = st.text_input("Alt Başlık", placeholder="Mayıs 2023 Verileri")
                region = st.text_input("Bölge *", value="Ankara", placeholder="Bölge adı")
                date = st.text_input("Tarih *", value=datetime.now().strftime("%d %B %Y %H:%M"))
            
            content = st.text_area("İçerik *", height=150, placeholder="İçerik detaylarını buraya yazın...")
            
            if content_type == "featured":
                highlight = st.text_area("Önemli Bilgi", placeholder="Vurgulanacak önemli bilgi...")
                author = st.text_input("Yazar", placeholder="Yazar adı")
            
            col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
            with col_btn1:
                submitted = st.form_submit_button("✅ İçeriği Ekle", use_container_width=True)
            with col_btn2:
                if st.form_submit_button("❌ İptal", use_container_width=True):
                    st.session_state.active_tab = "view"
                    st.rerun()
            
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

with sidebar_col:
    # SON EKLENENLER
    st.markdown("### 📌 Son Eklenenler")
    
    if st.session_state.contents:
        recent_contents = st.session_state.contents[-5:][::-1]
        
        for content in recent_contents:
            if st.button(
                f"**{content['title']}**\n"
                f"_{content.get('date', '')}_\n"
                f"📍 {content.get('country', 'Türkiye')} - {content.get('region', 'Ankara')}",
                key=f"recent_{content['id']}",
                use_container_width=True
            ):
                st.session_state.selected_content = content
                st.rerun()
            st.markdown("---")
    else:
        st.info("Henüz içerik yok")
    
    # İSTATİSTİKLER
    if st.session_state.contents:
        st.markdown("### 📊 İstatistikler")
        total = len(st.session_state.contents)
        featured = len([c for c in st.session_state.contents if c["type"] == "featured"])
        news = len([c for c in st.session_state.contents if c["type"] == "news"])
        
        st.metric("Toplam İçerik", total)
        st.metric("Öne Çıkan", featured)
        st.metric("Haber", news)
