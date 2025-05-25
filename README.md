# Local Deep Researcher - Flask Web Interface

AI Araştırma Asistanı - [Ollama](https://ollama.com/search) ile çalışan yerel LLM'ler kullanarak web araştırması yapabilen Flask tabanlı web arayüzü.

## 🌟 Özellikler

- **🌐 Web Arayüzü**: Kullanıcı dostu Flask tabanlı web interface
- **🔍 Otomatik Web Araştırması**: DuckDuckGo ile otomatik arama
- **🤖 Yerel LLM**: Ollama ile tamamen yerel AI desteği
- **🇹🇷 Türkçe Destek**: Türkçe araştırma konuları için optimize edilmiş
- **📊 Gerçek Zamanlı Takip**: Araştırma sürecini canlı izleme
- **📝 Markdown Çıktı**: Kaynaklarıyla birlikte detaylı rapor

![Flask Web Interface](https://via.placeholder.com/800x400/3498DB/ffffff?text=Flask+Web+Interface)

## 🚀 Hızlı Başlangıç

### 1. Projeyi İndir
```bash
git clone https://github.com/ahmetmnr/local-deep-researcher.git
cd local-deep-researcher
```

### 2. Ollama Kurulumu
1. [Ollama](https://ollama.com/download)'yı indir ve kur
2. Bir LLM modeli çek:
```bash
ollama pull llama3.2
```

### 3. Python Bağımlılıkları
```bash
# Sanal ortam oluştur (önerilen)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Bağımlılıkları yükle
pip install -e .
```

### 4. Flask Uygulamasını Çalıştır
```bash
python app.py
```

Tarayıcında şu adrese git: **http://localhost:5000**

## 🎯 Kullanım

1. **Araştırma Konusu Gir**: Web arayüzünde araştırmak istediğin konuyu yaz
   - Örnek: "Türkiye'de yapay zeka kullanımı"
   - Örnek: "2024 yılı teknoloji trendleri"

2. **Araştırma Başlat**: "Araştır" butonuna tıkla

3. **İlerlemeyi İzle**: Sistem hangi kaynakları incelediğini görebilirsin

4. **Sonuçları İncele**: Araştırma tamamlandığında detaylı raporu görebilirsin

## ⚙️ Yapılandırma

### Çevre Değişkenleri (.env)
```bash
cp .env.example .env
```

Önemli ayarlar:
```bash
LLM_PROVIDER=ollama
LOCAL_LLM=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
SEARCH_API=duckduckgo
MAX_WEB_RESEARCH_LOOPS=2
FETCH_FULL_PAGE=true
```

### Model Seçenekleri
- `llama3.2` (önerilen)
- `llama3.1`
- `qwen2.5`
- Diğer Ollama modelleri

## 🔧 Gelişmiş Özellikler

### LangGraph Studio ile Kullanım
Gelişmiş görselleştirme için:
```bash
pip install -U "langgraph-cli[inmem]"
langgraph dev
```

### Docker ile Çalıştırma
```bash
docker build -t local-deep-researcher .
docker run -p 5000:5000 local-deep-researcher
```

## 📁 Proje Yapısı

```
local-deep-researcher/
├── app.py                    # Flask web uygulaması
├── templates/
│   └── index.html           # Web arayüzü
├── ollama_deep_researcher/  # Ana araştırma modülü
├── pyproject.toml          # Python bağımlılıkları
├── .env.example           # Örnek yapılandırma
└── README.md             # Bu dosya
```

## 🛠️ Nasıl Çalışır

1. **Sorgu Oluşturma**: Kullanıcı konusundan web arama sorgusu üretir
2. **Web Arama**: DuckDuckGo ile ilgili kaynakları bulur
3. **İçerik Analizi**: Bulunan kaynakların içeriğini özetler
4. **Bilgi Boşlukları**: Eksik bilgileri tespit eder
5. **Tekrarlı Arama**: Eksiklikleri gidermek için yeni aramalar yapar
6. **Final Rapor**: Tüm bulguları markdown formatında sunar

## 🤝 Katkıda Bulunma

Bu proje açık kaynaklıdır ve katkılarınızı memnuniyetle karşılarız:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'i push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- [LangChain](https://www.langchain.com/) - AI framework
- [Ollama](https://ollama.com/) - Local LLM hosting
- [DuckDuckGo](https://duckduckgo.com/) - Privacy-focused search
- [Flask](https://flask.palletsprojects.com/) - Web framework
