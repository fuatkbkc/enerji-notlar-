import streamlit as st
import json
import pandas as pd
from datetime import datetime
import uuid

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
    
    .featured-article {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #3498db;
    }
    
    .content-item {
        background: white;
        padding: 20px;
        margin: 10px 0;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #3498db;
    }
    
    .delete-btn {
        background-color: #e74c3c;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
        margin-left: 10px;
    }
    
    .edit-btn {
        background-color: #f39c12;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
        margin-left: 10px;
    }
    
    .highlight {
        background-color: #e8f4fd;
        padding: 20px;
        border-left: 4px solid #1abc9c;
        margin: 20px 0;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if 'contents' not in st.session_state:
    st.session_state.contents = [
        {
            "id": str(uuid.uuid4()),
            "type": "featured",
            "title": "Spot Piyasada Elektrik ve Doğal Gaz Fiyatları",
            "content": "Enerji piyasalarında günlük olarak belirlenen spot elektrik ve doğal gaz fiyatları, enerji maliyetlerinin yönetimi açısından büyük önem taşıyor.",
            "highlight": "19 Mayıs Cuma günü için spot piyasada megavatsaat başına en yüksek elektrik fiyatı 2.600 Türk lirası olarak belirlendi.",
            "author": "Duvgu Aihan",
            "date": "18 Mayıs 2023"
        },
        {
            "id": str(uuid.uuid4()),
            "type": "news",
            "title": "Spot market electricity prices for Friday, May 19",
            "content": "Energy Exchange Istanbul (EXIST) data shows electricity market trade amounts to 847 million Turkish liras.",
            "date": "18 Mayıs 2023 14:24",
            "category": "Elektrik"
        },
        {
            "id": str(uuid.uuid4()),
            "type": "news",
            "title": "Spot market natural gas prices",
            "content": "1,000 cubic meters of natural gas on spot market costs 9,182.35 Turkish liras.",
            "date": "18 Mayıs 2023 14:14",
            "category": "Doğal Gaz"
        }
    ]

if 'editing_id' not in st.session_state:
    st.session_state.editing_id = None

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "content"

# Header
st.markdown("""
<div class="header">
    <div class="nav-container">
        <div class="nav-item">İçerik Yönetimi</div>
    </div>
    <div class="logo">⚡ Enerji Veri Blog</div>
    <div class="nav-container">
        <div class="nav-item">Çıkış</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Yönetim butonları
col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

with col1:
    if st.button("📝 Yeni İçerik Ekle", use_container_width=True):
        st.session_state.active_tab = "add_content"

with col2:
    if st.button("🗑️ Tümünü Temizle", use_container_width=True):
        if st.session_state.contents:
            st.session_state.contents = []
            st.rerun()

with col3:
    if st.button("📊 İçerik Görüntüle", use_container_width=True):
        st.session_state.active_tab = "content"

with col4:
    if st.button("⚙️ Ayarlar", use_container_width=True):
        st.session_state.active_tab = "settings"

# İçerik görüntüleme sekmesi
if st.session_state.active_tab == "content":
    st.markdown("## 📋 Mevcut İçerikler")
    
    if not st.session_state.contents:
        st.info("Henüz içerik eklenmemiş.")
    else:
        for i, content in enumerate(st.session_state.contents):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    if content["type"] == "featured":
                        st.markdown(f"""
                        <div class="featured-article">
                            <h2>{content['title']}</h2>
                            <p>{content['content']}</p>
                            <div class="highlight">
                                <p><strong>Önemli Bilgi:</strong> {content['highlight']}</p>
                            </div>
                            <p class="author">Yazar: {content['author']} | {content['date']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="content-item">
                            <h3>{content['title']}</h3>
                            <p><strong>Tarih:</strong> {content['date']}</p>
                            <p><strong>Kategori:</strong> {content.get('category', 'Genel')}</p>
                            <p>{content['content']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    col2_1, col2_2 = st.columns(2)
                    with col2_1:
                        if st.button("✏️", key=f"edit_{i}", use_container_width=True):
                            st.session_state.editing_id = content["id"]
                            st.session_state.active_tab = "edit_content"
                            st.rerun()
                    with col2_2:
                        if st.button("🗑️", key=f"delete_{i}", use_container_width=True):
                            st.session_state.contents = [c for c in st.session_state.contents if c["id"] != content["id"]]
                            st.rerun()

# İçerik ekleme sekmesi
elif st.session_state.active_tab == "add_content":
    st.markdown("## ➕ Yeni İçerik Ekle")
    
    with st.form("add_content_form"):
        content_type = st.selectbox("İçerik Türü", ["featured", "news", "general"])
        
        title = st.text_input("Başlık")
        content = st.text_area("İçerik")
        date = st.text_input("Tarih", value=datetime.now().strftime("%d %B %Y %H:%M"))
        
        if content_type == "featured":
            highlight = st.text_area("Önemli Bilgi (Highlight)")
            author = st.text_input("Yazar")
        elif content_type == "news":
            category = st.selectbox("Kategori", ["Elektrik", "Doğal Gaz", "Enerji", "Ekonomi", "Diğer"])
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("✅ İçeriği Ekle", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ İptal", use_container_width=True)
        
        if submitted and title and content:
            new_content = {
                "id": str(uuid.uuid4()),
                "type": content_type,
                "title": title,
                "content": content,
                "date": date
            }
            
            if content_type == "featured":
                new_content["highlight"] = highlight
                new_content["author"] = author
            elif content_type == "news":
                new_content["category"] = category
            
            st.session_state.contents.append(new_content)
            st.success("İçerik başarıyla eklendi!")
            st.session_state.active_tab = "content"
            st.rerun()
        
        if cancel:
            st.session_state.active_tab = "content"
            st.rerun()

# İçerik düzenleme sekmesi
elif st.session_state.active_tab == "edit_content" and st.session_state.editing_id:
    st.markdown("## ✏️ İçerik Düzenle")
    
    content_to_edit = next((c for c in st.session_state.contents if c["id"] == st.session_state.editing_id), None)
    
    if content_to_edit:
        with st.form("edit_content_form"):
            content_type = st.selectbox("İçerik Türü", ["featured", "news", "general"], 
                                      index=["featured", "news", "general"].index(content_to_edit["type"]))
            
            title = st.text_input("Başlık", value=content_to_edit["title"])
            content = st.text_area("İçerik", value=content_to_edit["content"])
            date = st.text_input("Tarih", value=content_to_edit["date"])
            
            if content_type == "featured":
                highlight = st.text_area("Önemli Bilgi (Highlight)", 
                                       value=content_to_edit.get("highlight", ""))
                author = st.text_input("Yazar", value=content_to_edit.get("author", ""))
            elif content_type == "news":
                category = st.selectbox("Kategori", ["Elektrik", "Doğal Gaz", "Enerji", "Ekonomi", "Diğer"],
                                      index=["Elektrik", "Doğal Gaz", "Enerji", "Ekonomi", "Diğer"].index(
                                          content_to_edit.get("category", "Elektrik")))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                save = st.form_submit_button("💾 Kaydet", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("❌ İptal", use_container_width=True)
            with col3:
                delete = st.form_submit_button("🗑️ Sil", use_container_width=True)
            
            if save and title and content:
                content_to_edit.update({
                    "type": content_type,
                    "title": title,
                    "content": content,
                    "date": date
                })
                
                if content_type == "featured":
                    content_to_edit["highlight"] = highlight
                    content_to_edit["author"] = author
                    content_to_edit.pop("category", None)
                elif content_type == "news":
                    content_to_edit["category"] = category
                    content_to_edit.pop("highlight", None)
                    content_to_edit.pop("author", None)
                
                st.success("İçerik başarıyla güncellendi!")
                st.session_state.editing_id = None
                st.session_state.active_tab = "content"
                st.rerun()
            
            if cancel:
                st.session_state.editing_id = None
                st.session_state.active_tab = "content"
                st.rerun()
            
            if delete:
                st.session_state.contents = [c for c in st.session_state.contents if c["id"] != content_to_edit["id"]]
                st.session_state.editing_id = None
                st.session_state.active_tab = "content"
                st.rerun()
    else:
        st.error("Düzenlenecek içerik bulunamadı!")
        st.session_state.editing_id = None
        st.session_state.active_tab = "content"
        st.rerun()

# Ayarlar sekmesi
elif st.session_state.active_tab == "settings":
    st.markdown("## ⚙️ Ayarlar")
    
    st.markdown("### Veri Yönetimi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 İçeriği Dışa Aktar", use_container_width=True):
            if st.session_state.contents:
                json_data = json.dumps(st.session_state.contents, indent=2, ensure_ascii=False)
                st.download_button(
                    label="JSON olarak indir",
                    data=json_data,
                    file_name="enerji_icerikleri.json",
                    mime="application/json"
                )
            else:
                st.warning("Dışa aktarılacak içerik yok.")
    
    with col2:
        uploaded_file = st.file_uploader("İçeriği İçe Aktar", type="json")
        if uploaded_file:
            try:
                imported_data = json.load(uploaded_file)
                if st.button("İçeri Aktar", use_container_width=True):
                    st.session_state.contents = imported_data
                    st.success("İçerik başarıyla içe aktarıldı!")
                    st.rerun()
            except:
                st.error("Geçersiz JSON dosyası!")

# İstatistikler
st.markdown("---")
st.markdown("### 📊 İstatistikler")

if st.session_state.contents:
    featured_count = len([c for c in st.session_state.contents if c["type"] == "featured"])
    news_count = len([c for c in st.session_state.contents if c["type"] == "news"])
    general_count = len([c for c in st.session_state.contents if c["type"] == "general"])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Toplam İçerik", len(st.session_state.contents))
    col2.metric("Öne Çıkan", featured_count)
    col3.metric("Haber", news_count)
    col4.metric("Genel", general_count)
else:
    st.info("Henüz içerik eklenmemiş. İstatistikler burada görünecek.")
