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
    .main-header {
        background: linear-gradient(135deg, #2c3e50, #3498db);
        color: white;
        padding: 12px 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 25px;
        border-radius: 10px;
        margin-top: -20px;
    }
    
    .logo {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
    }
    
    .content-item {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 5px solid #3498db;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .content-item:hover {
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .content-item.collapsed {
        max-height: 120px;
        overflow: hidden;
    }
    
    .content-item.expanded {
        max-height: none;
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
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .recent-item {
        padding: 12px;
        margin: 8px 0;
        background: #f8f9fa;
        border-radius: 8px;
        cursor: pointer;
        border-left: 3px solid #3498db;
        transition: all 0.2s ease;
    }
    
    .recent-item:hover {
        background: #e9ecef;
        transform: translateX(5px);
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'contents' not in st.session_state:
    st.session_state.contents = []

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "view"

if 'expanded_items' not in st.session_state:
    st.session_state.expanded_items = {}

if 'selected_content' not in st.session_state:
    st.session_state.selected_content = None

# Header - Daha yukarı taşındı
st.markdown("""
<div class="main-header">
    <div class="logo">⚡ Enerji Veri Blog</div>
</div>
""", unsafe_allow_html=True)

# Ana içerik ve sidebar layout
main_col, sidebar_col = st.columns([3, 1])

with main_col:
    # Yönetim butonları
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if st.button("📝 Yeni İçerik Ekle", use_container_width=True):
            st.session_state.active_tab = "add"

    with col2:
        if st.button("👁️ İçerikleri Gör", use_container_width=True):
            st.session_state.active_tab = "view"

    with col3:
        if st.button("🚪 Çıkış", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # İçerik görüntüleme
    if st.session_state.active_tab == "view":
        if st.session_state.selected_content is not None:
            # Seçili içeriği detaylı göster
            content = st.session_state.selected_content
            st.markdown("## 📖 İçerik Detayı")
            
            if content["type"] == "featured":
                st.markdown(f"""
                <div class="content-item expanded">
                    <h2>{content['title']}</h2>
                    {f"<h4>{content['subtitle']}</h4>" if content.get('subtitle') else ""}
                    <p><strong>🌍 Ülke:</strong> {content.get('country', 'Türkiye')} | <strong>📍 Bölge:</strong> {content.get('region', 'Ankara')}</p>
                    <p><strong>📊 Enerji Kalemi:</strong> {content.get('energy_type', 'Elektrik')}</p>
                    <p><strong>📅 Tarih:</strong> {content.get('date', '')}</p>
                    <div style="margin: 20px 0; padding: 20px 0; border-top: 1px solid #eee; border-bottom: 1px solid #eee;">
                        {content['content']}
                    </div>
                    {f'<div class="highlight"><strong>💡 Önemli Bilgi:</strong> {content.get("highlight", "")}</div>' if content.get("highlight") else ""}
                    {f'<p><strong>👤 Yazar:</strong> {content.get("author", "")}</p>' if content.get("author") else ""}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="content-item expanded">
                    <h2>{content['title']}</h2>
                    {f"<h4>{content['subtitle']}</h4>" if content.get('subtitle') else ""}
                    <p><strong>🌍 Ülke:</strong> {content.get('country', 'Türkiye')} | <strong>📍 Bölge:</strong> {content.get('region', 'Ankara')}</p>
                    <p><strong>📊 Enerji Kalemi:</strong> {content.get('energy_type', 'Elektrik')}</p>
                    <p><strong>📅 Tarih:</strong> {content.get('date', '')}</p>
                    <div style="margin: 20px 0; padding: 20px 0; border-top: 1px solid #eee; border-bottom: 1px solid #eee;">
                        {content['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Geri butonu ve silme butonu
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
            # Tüm içerikleri listele (wrap özelliği ile)
            st.markdown("## 📋 Tüm İçerikler")
            
            if not st.session_state.contents:
                st.info("📝 Henüz içerik eklenmemiş. Yeni içerik eklemek için 'Yeni İçerik Ekle' butonuna tıklayın.")
            else:
                for i, content in enumerate(st.session_state.contents):
                    is_expanded = st.session_state.expanded_items.get(content["id"], False)
                    item_class = "content-item expanded" if is_expanded else "content-item collapsed"
                    if content["type"] == "featured":
                        item_class += " featured-item"
                    elif content["type"] == "news":
                        item_class += " news-item"
                    
                    # İçerik özeti
                    content_preview = content['content'][:150] + "..." if len(content['content']) > 150 else content['content']
                    
                    st.markdown(f"""
                    <div class="{item_class}" onclick="expandContent('{content['id']}')">
                        <h3>{content['title']}</h3>
                        {f"<h5>{content['subtitle']}</h5>" if content.get('subtitle') else ""}
                        <p><strong>🌍 Ülke:</strong> {content.get('country', 'Türkiye')} | <strong>📍 Bölge:</strong> {content.get('region', 'Ankara')}</p>
                        <p><strong>📊 Enerji Kalemi:</strong> {content.get('energy_type', 'Elektrik')} | <strong>📅 Tarih:</strong> {content.get('date', '')}</p>
                        <p>{content_preview}</p>
                        {f'<div class="highlight"><strong>💡 Önemli Bilgi:</strong> {content.get("highlight", "")}</div>' if content.get("highlight") and is_expanded else ""}
                        {f'<p><strong>👤 Yazar:</strong> {content.get("author", "")}</p>' if content.get("author") and is_expanded else ""}
                        <p><em>{'👇 Tıklayarak daralt' if is_expanded else '👇 Tıklayarak genişlet'}</em></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Silme butonu
                    if st.button(f"🗑️ Sil", key=f"delete_{i}"):
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

with sidebar_col:
    # Son eklenenler sidebar'ı
    st.markdown("### 📌 Son Eklenenler")
    st.markdown('<div class="recent-sidebar">', unsafe_allow_html=True)
    
    if st.session_state.contents:
        # Son 5 içeriği göster
        recent_contents = st.session_state.contents[-5:][::-1]  # En son eklenen en üstte
        for content in recent_contents:
            st.markdown(f"""
            <div class="recent-item" onclick="selectContent('{content['id']}')">
                <strong>{content['title']}</strong>
                <br>
                <small>📅 {content.get('date', '')}</small>
                <br>
                <small>🌍 {content.get('country', 'Türkiye')} - {content.get('region', 'Ankara')}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Henüz içerik yok")
    
    st.markdown('</div>', unsafe_allow_html=True)

# JavaScript fonksiyonları
st.markdown("""
<script>
function expandContent(contentId) {
    // Streamlit'e içeriği genişletme/daraltma bilgisini gönder
    fetch('/_stcore/streamlit-components/component-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: 'streamlit:setComponentValue',
            value: {action: 'toggle_expand', contentId: contentId}
        })
    });
}

function selectContent(contentId) {
    // Streamlit'e içerik seçme bilgisini gönder
    fetch('/_stcore/streamlit-components/component-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: 'streamlit:setComponentValue',
            value: {action: 'select_content', contentId: contentId}
        })
    });
}
</script>
""", unsafe_allow_html=True)

# JavaScript etkileşimleri için session state güncellemeleri
if st.session_state.get('component_value'):
    action_data = st.session_state.component_value
    if action_data.get('action') == 'toggle_expand':
        content_id = action_data.get('contentId')
        st.session_state.expanded_items[content_id] = not st.session_state.expanded_items.get(content_id, False)
        st.rerun()
    elif action_data.get('action') == 'select_content':
        content_id = action_data.get('contentId')
        selected_content = next((c for c in st.session_state.contents if c["id"] == content_id), None)
        if selected_content:
            st.session_state.selected_content = selected_content
            st.rerun()
