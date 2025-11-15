<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enerji Veri Blog</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }
        
        body {
            background-color: #f5f5f5;
            color: #333;
        }
        
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .logo {
            font-size: 24px;
            font-weight: bold;
        }
        
        .nav-left {
            display: flex;
            gap: 15px;
        }
        
        .nav-right {
            display: flex;
            gap: 15px;
        }
        
        .nav-item {
            padding: 8px 15px;
            background-color: #34495e;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .nav-item:hover {
            background-color: #1abc9c;
        }
        
        .main-content {
            max-width: 1200px;
            margin: 20px auto;
            padding: 0 20px;
        }
        
        .featured-article {
            background-color: white;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .featured-article h1 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 28px;
        }
        
        .featured-article p {
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        .tabs-container {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 1px solid #ddd;
        }
        
        .tab {
            padding: 12px 20px;
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            border-bottom: none;
            border-radius: 5px 5px 0 0;
            margin-right: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .tab.active {
            background-color: white;
            border-bottom: 1px solid white;
            margin-bottom: -1px;
            font-weight: bold;
        }
        
        .tab-content {
            display: none;
            background-color: white;
            padding: 20px;
            border-radius: 0 0 5px 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .tab-content.active {
            display: block;
        }
        
        .content-section {
            margin-bottom: 25px;
        }
        
        .content-section h2 {
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }
        
        .news-item {
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .news-item:last-child {
            border-bottom: none;
        }
        
        .news-item h3 {
            color: #2c3e50;
            margin-bottom: 8px;
        }
        
        .news-item .date {
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 5px;
        }
        
        .news-item p {
            line-height: 1.5;
        }
        
        .highlight {
            background-color: #f8f9fa;
            padding: 15px;
            border-left: 4px solid #1abc9c;
            margin: 15px 0;
        }
        
        .author {
            font-style: italic;
            color: #7f8c8d;
            text-align: right;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="nav-left">
            <div class="nav-item" id="content-tab-header">İçerik</div>
            <div class="nav-item" id="image-tab-header">Görüntü</div>
        </div>
        <div class="logo">Enerji Veri Blog</div>
        <div class="nav-right">
            <div class="nav-item" id="logout-tab">Çıkış</div>
        </div>
    </div>
    
    <div class="main-content">
        <div class="featured-article">
            <h1>Spot Piyasada Elektrik ve Doğal Gaz Fiyatları</h1>
            <p>Enerji piyasalarında günlük olarak belirlenen spot elektrik ve doğal gaz fiyatları, enerji maliyetlerinin yönetimi açısından büyük önem taşıyor. 18 Mayıs 2023 tarihli verilere göre, Enerji Piyasaları İşletme A.Ş. (EPİAŞ) tarafından işletilen Enerji Borsası İstanbul'da (EXIST) elektrik piyasasında işlem hacmi 847 milyon Türk lirası olarak gerçekleşti.</p>
            
            <div class="highlight">
                <p><strong>Önemli Bilgi:</strong> 19 Mayıs Cuma günü için spot piyasada megavatsaat başına en yüksek elektrik fiyatı 2.600 Türk lirası olarak belirlendi. En düşük fiyat ise 1.424,34 lira ile sabah 06:00'da kaydedildi.</p>
            </div>
            
            <p>Doğal gaz piyasasında ise 17 Mayıs Çarşamba günü için spot piyasada 1.000 metreküp doğal gazın fiyatı 9.182,35 Türk lirası olarak belirlendi. Enerji fiyatlarındaki bu dalgalanmalar, hem üreticiler hem de tüketiciler için maliyet planlaması açısından kritik öneme sahip.</p>
            
            <p class="author">Yazar: Duvgu Aihan</p>
        </div>
        
        <div class="tabs-container">
            <div class="tab active" id="content-tab">İçerik</div>
            <div class="tab" id="image-tab">Görüntü</div>
        </div>
        
        <div class="tab-content active" id="content-tab-content">
            <div class="content-section">
                <h2>18 Mayıs 2023 14:24</h2>
                <div class="news-item">
                    <h3>Spot market electricity prices for Friday, May 19</h3>
                    <p class="date">18 May 2023 14:14</p>
                    <p>Energy Exchange Istanbul (EXIST) data shows electricity market trade amounts to 847 million Turkish liras</p>
                </div>
                
                <div class="news-item">
                    <h3>Türkiye - Ankara</h3>
                    <p class="date">18 May 2023 14:14</p>
                    <p>Spot market natural gas prices for Wednesday, May 17 - 1,000 cubic meters of natural gas on spot market costs 9,182.35 Turkish liras</p>
                </div>
                
                <div class="news-item">
                    <h3>Ekonomi</h3>
                    <p class="date">18 May 2023 14:14</p>
                    <p>Spot piyasada doğal gaz fiyatları</p>
                </div>
                
                <div class="news-item">
                    <h3>Ekonomi</h3>
                    <p class="date">18 May 2023 14:10</p>
                    <p>Spot piyasada elektrik fiyatları</p>
                </div>
                
                <div class="news-item">
                    <h3>Ekonomi</h3>
                    <p class="date">18 May 2023 11:25</p>
                    <p>Enerjisa Üretim Bilgi Teknolojileri ve Dijital İş Genel Müdür Yardımcısı Ali İnal, En İyi 10 CIO listesinde</p>
                </div>
            </div>
            
            <div class="content-section">
                <h2>Detaylı Haber İçeriği</h2>
                <div class="news-item">
                    <h3>Spot market electricity prices for Friday, May 19</h3>
                    <p>The highest electricity price rate for one megawatt-hour on Türkiye's day-ahead spotmarket for Friday will be 2,600 Turkish liras at 8 p.m. (1700 GMT), according to official figures on Thursday.</p>
                    <p>The lowest rate was set at 1,424.34 liras at 6 a.m. local time (0300 GMT), the data showed.</p>
                    <p>The Energy Exchange Istanbul (EXIST) data for the trade volume on Thursday's electricity market showed a decrease of 21.2% to 847 million liras compared to Wednesday.</p>
                    <p>The arithmetical and weighted average electricity prices on the day-ahead spot market are calculated as 1,893.76 liras and 1,899.899 liras, respectively.</p>
                    <p>The highest electricity price rate for one megawatt-hour for Thursday was set as 2,600 Turkish liras at 8 p.m. (1700 GMT), while the lowest rate was set at 1,349.99 liras at 7 a.m. local time (0400 GMT), according to official figures.</p>
                    <p>US$1 equals 19.79 liras at 2.23 p.m. local time (1123 GMT) on Thursday.</p>
                    <p class="author">By Duvgu Aihan</p>
                </div>
            </div>
        </div>
        
        <div class="tab-content" id="image-tab-content">
            <div class="content-section">
                <h2>Görsel İçerik</h2>
                <div class="news-item">
                    <h3>Enerji Fiyat Grafikleri</h3>
                    <p>Bu bölümde elektrik ve doğal gaz fiyatlarının günlük değişimini gösteren grafikler yer alacaktır.</p>
                    <div style="background-color: #f0f0f0; height: 300px; display: flex; justify-content: center; align-items: center; margin: 20px 0; border-radius: 5px;">
                        <p>Elektrik Fiyat Grafiği - Görsel İçeriği</p>
                    </div>
                </div>
                
                <div class="news-item">
                    <h3>Piyasa Verileri Görselleştirme</h3>
                    <p>Spot piyasa işlem hacimleri ve fiyat değişimlerini gösteren görsel veriler.</p>
                    <div style="background-color: #f0f0f0; height: 250px; display: flex; justify-content: center; align-items: center; margin: 20px 0; border-radius: 5px;">
                        <p>Doğal Gaz Fiyat Grafiği - Görsel İçeriği</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Sekme işlevselliği
        document.getElementById('content-tab').addEventListener('click', function() {
            document.getElementById('content-tab').classList.add('active');
            document.getElementById('image-tab').classList.remove('active');
            document.getElementById('content-tab-content').classList.add('active');
            document.getElementById('image-tab-content').classList.remove('active');
        });
        
        document.getElementById('image-tab').addEventListener('click', function() {
            document.getElementById('image-tab').classList.add('active');
            document.getElementById('content-tab').classList.remove('active');
            document.getElementById('image-tab-content').classList.add('active');
            document.getElementById('content-tab-content').classList.remove('active');
        });
        
        // Üst navigasyon için sekme işlevselliği
        document.getElementById('content-tab-header').addEventListener('click', function() {
            document.getElementById('content-tab').classList.add('active');
            document.getElementById('image-tab').classList.remove('active');
            document.getElementById('content-tab-content').classList.add('active');
            document.getElementById('image-tab-content').classList.remove('active');
        });
        
        document.getElementById('image-tab-header').addEventListener('click', function() {
            document.getElementById('image-tab').classList.add('active');
            document.getElementById('content-tab').classList.remove('active');
            document.getElementById('image-tab-content').classList.add('active');
            document.getElementById('content-tab-content').classList.remove('active');
        });
        
        // Çıkış sekmesi için basit uyarı
        document.getElementById('logout-tab').addEventListener('click', function() {
            alert('Çıkış yapılıyor...');
        });
    </script>
</body>
</html>
