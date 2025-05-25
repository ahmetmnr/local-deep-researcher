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

## How it works

Local Deep Researcher is inspired by [IterDRAG](https://arxiv.org/html/2410.04343v1#:~:text=To%20tackle%20this%20issue%2C%20we,used%20to%20generate%20intermediate%20answers.). This approach will decompose a query into sub-queries, retrieve documents for each one, answer the sub-query, and then build on the answer by retrieving docs for the second sub-query. Here, we do similar:
- Given a user-provided topic, use a local LLM (via [Ollama](https://ollama.com/search) or [LMStudio](https://lmstudio.ai/)) to generate a web search query
- Uses a search engine / tool to find relevant sources
- Uses LLM to summarize the findings from web search related to the user-provided research topic
- Then, it uses the LLM to reflect on the summary, identifying knowledge gaps
- It generates a new search query to address the knowledge gaps
- The process repeats, with the summary being iteratively updated with new information from web search
- Runs for a configurable number of iterations (see `configuration` tab)

## Outputs

The output of the graph is a markdown file containing the research summary, with citations to the sources used. All sources gathered during research are saved to the graph state. You can visualize them in the graph state, which is visible in LangGraph Studio:

![Screenshot 2024-12-05 at 4 08 59 PM](https://github.com/user-attachments/assets/e8ac1c0b-9acb-4a75-8c15-4e677e92f6cb)

The final summary is saved to the graph state as well:

![Screenshot 2024-12-05 at 4 10 11 PM](https://github.com/user-attachments/assets/f6d997d5-9de5-495f-8556-7d3891f6bc96)

## Deployment Options

There are [various ways](https://langchain-ai.github.io/langgraph/concepts/#deployment-options) to deploy this graph. See [Module 6](https://github.com/langchain-ai/langchain-academy/tree/main/module-6) of LangChain Academy for a detailed walkthrough of deployment options with LangGraph.

## TypeScript Implementation

A TypeScript port of this project (without Perplexity search) is available at:
https://github.com/PacoVK/ollama-deep-researcher-ts

## Running as a Docker container

The included `Dockerfile` only runs LangChain Studio with local-deep-researcher as a service, but does not include Ollama as a dependant service. You must run Ollama separately and configure the `OLLAMA_BASE_URL` environment variable. Optionally you can also specify the Ollama model to use by providing the `LOCAL_LLM` environment variable.

Clone the repo and build an image:
```
$ docker build -t local-deep-researcher .
```

Run the container:
```
$ docker run --rm -it -p 2024:2024 \
  -e SEARCH_API="tavily" \ 
  -e TAVILY_API_KEY="tvly-***YOUR_KEY_HERE***" \
  -e LLM_PROVIDER=ollama
  -e OLLAMA_BASE_URL="http://host.docker.internal:11434/" \
  -e LOCAL_LLM="llama3.2" \  
  local-deep-researcher
```

NOTE: You will see log message:
```
2025-02-10T13:45:04.784915Z [info     ] 🎨 Opening Studio in your browser... [browser_opener] api_variant=local_dev message=🎨 Opening Studio in your browser...
URL: https://smith.langchain.com/studio/?baseUrl=http://0.0.0.0:2024
```
...but the browser will not launch from the container.

Instead, visit this link with the correct baseUrl IP address: [`https://smith.langchain.com/studio/thread?baseUrl=http://127.0.0.1:2024`](https://smith.langchain.com/studio/thread?baseUrl=http://127.0.0.1:2024)
