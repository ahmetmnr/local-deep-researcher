from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from ollama_deep_researcher.graph import graph
from ollama_deep_researcher.configuration import Configuration
import threading
import json
from ollama_deep_researcher.utils import duckduckgo_search

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)

# Global variables to store research results and status
research_results = {}
research_status = {}
research_sites = {}

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/research', methods=['POST'])
def start_research():
    """Start research process in background."""
    data = request.get_json()
    research_topic = data.get('topic', '')
    research_id = str(hash(research_topic))
    
    if not research_topic:
        return jsonify({"error": "Research topic is required"}), 400
    
    # Set initial status
    research_status[research_id] = "running"
    research_results[research_id] = ""
    research_sites[research_id] = []
    
    # Start research in background
    thread = threading.Thread(
        target=run_research, 
        args=(research_topic, research_id)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({"id": research_id, "status": "running"})

@app.route('/api/status/<research_id>', methods=['GET'])
def get_status(research_id):
    """Get the status of a research task."""
    status = research_status.get(research_id, "not_found")
    result = research_results.get(research_id, "")
    sites = research_sites.get(research_id, [])
    
    return jsonify({
        "id": research_id,
        "status": status,
        "result": result if status == "completed" else "",
        "sites": sites
    })

class SiteTracker:
    """Custom callback to track sites during research."""
    def __init__(self, research_id):
        self.research_id = research_id
        
    def on_new_site(self, site_info):
        if self.research_id in research_sites:
            research_sites[self.research_id].append(site_info)

def run_research(research_topic, research_id):
    """Run the research process."""
    try:
        # Configure the research assistant
        config = Configuration(
            max_web_research_loops=2,  # Number of research iterations
            local_llm="llama3.2",  # Using the llama3.2 model
            llm_provider="ollama",  # Use Ollama
            search_api="duckduckgo",  # Use DuckDuckGo for searching
            fetch_full_page=True,  # Fetch full page content
            ollama_base_url="http://localhost:11434/",  # Ollama API URL
            strip_thinking_tokens=True  # Remove thinking tokens from LLM responses
        )

        # Create a RunnableConfig with the configuration
        runnable_config = RunnableConfig(configurable=config.model_dump())

        # First get search results to display
        search_results = duckduckgo_search(research_topic, max_results=5)
        for result in search_results.get('results', []):
            site_info = {
                "title": result.get('title', 'Unknown Site'),
                "url": result.get('url', '#'),
            }
            research_sites[research_id].append(site_info)

        # Run the research workflow
        result = graph.invoke(
            {"research_topic": research_topic},
            config=runnable_config
        )
        
        # Store the result
        research_results[research_id] = result["running_summary"]
        research_status[research_id] = "completed"
    except Exception as e:
        # Handle errors
        research_results[research_id] = f"Error: {str(e)}"
        research_status[research_id] = "error"

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create index.html template with English interface
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Research Assistant</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3 {
            color: #2C3E50;
            margin-bottom: 20px;
        }
        h1 {
            text-align: center;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #2C3E50;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            background-color: #3498DB;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            display: block;
            margin: 0 auto;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #2980B9;
        }
        button:disabled {
            background-color: #95a5a6;
            cursor: not-allowed;
        }
        .result {
            margin-top: 30px;
            white-space: pre-wrap;
        }
        .loading {
            text-align: center;
            margin: 20px 0;
            color: #7f8c8d;
        }
        #status {
            text-align: center;
            margin-top: 10px;
            font-style: italic;
            color: #7f8c8d;
        }
        .markdown {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #3498DB;
        }
        .sites-container {
            margin-top: 20px;
            border: 1px solid #eee;
            border-radius: 4px;
            padding: 10px;
            background-color: #fafafa;
            max-height: 200px;
            overflow-y: auto;
        }
        .site-item {
            padding: 8px;
            border-bottom: 1px solid #eee;
        }
        .site-item:last-child {
            border-bottom: none;
        }
        .site-title {
            font-weight: bold;
            color: #2C3E50;
        }
        .site-url {
            color: #3498DB;
            font-size: 0.9em;
            text-decoration: none;
            word-break: break-all;
        }
        .site-url:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Research Assistant</h1>
        
        <div class="form-group">
            <label for="topic">Research Topic:</label>
            <input type="text" id="topic" placeholder="Example: The use of artificial intelligence in Turkish education">
        </div>
        
        <button id="submit">Research</button>
        
        <div id="status"></div>
        
        <div id="loading" class="loading" style="display: none;">
            <p>Research in progress, please wait...</p>
            <p>This process may take a few minutes.</p>
            
            <div>
                <h3>Sources being analyzed:</h3>
                <div id="sites" class="sites-container"></div>
            </div>
        </div>
        
        <div class="result" id="result" style="display: none;">
            <h2>Research Results</h2>
            <div class="markdown" id="resultContent"></div>
        </div>
    </div>

    <script>
        const submitBtn = document.getElementById('submit');
        const topicInput = document.getElementById('topic');
        const statusEl = document.getElementById('status');
        const loadingEl = document.getElementById('loading');
        const resultEl = document.getElementById('result');
        const resultContentEl = document.getElementById('resultContent');
        const sitesEl = document.getElementById('sites');
        
        let currentResearchId = null;
        let statusCheckInterval = null;
        let processedSites = new Set();
        
        submitBtn.addEventListener('click', async () => {
            const topic = topicInput.value.trim();
            
            if (!topic) {
                alert('Please enter a research topic.');
                return;
            }
            
            // Reset UI
            resultEl.style.display = 'none';
            loadingEl.style.display = 'block';
            submitBtn.disabled = true;
            statusEl.textContent = 'Starting research...';
            sitesEl.innerHTML = '';
            processedSites.clear();
            
            try {
                // Start research
                const response = await fetch('/api/research', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ topic })
                });
                
                if (!response.ok) {
                    throw new Error('Could not start research');
                }
                
                const data = await response.json();
                currentResearchId = data.id;
                
                // Start checking status
                checkStatus();
                statusCheckInterval = setInterval(checkStatus, 3000);
                
            } catch (error) {
                console.error('Error:', error);
                statusEl.textContent = `Error: ${error.message}`;
                loadingEl.style.display = 'none';
                submitBtn.disabled = false;
            }
        });
        
        function updateSitesList(sites) {
            if (!sites || !sites.length) return;
            
            sites.forEach(site => {
                const siteId = site.url;
                
                // Only add new sites
                if (!processedSites.has(siteId)) {
                    processedSites.add(siteId);
                    
                    const siteElement = document.createElement('div');
                    siteElement.className = 'site-item';
                    
                    const titleElement = document.createElement('div');
                    titleElement.className = 'site-title';
                    titleElement.textContent = site.title;
                    
                    const urlElement = document.createElement('a');
                    urlElement.className = 'site-url';
                    urlElement.href = site.url;
                    urlElement.textContent = site.url;
                    urlElement.target = '_blank';
                    
                    siteElement.appendChild(titleElement);
                    siteElement.appendChild(urlElement);
                    sitesEl.appendChild(siteElement);
                }
            });
        }
        
        async function checkStatus() {
            if (!currentResearchId) return;
            
            try {
                const response = await fetch(`/api/status/${currentResearchId}`);
                const data = await response.json();
                
                // Update sites list
                if (data.sites) {
                    updateSitesList(data.sites);
                }
                
                if (data.status === 'completed') {
                    // Research is complete
                    clearInterval(statusCheckInterval);
                    loadingEl.style.display = 'none';
                    resultEl.style.display = 'block';
                    resultContentEl.innerHTML = data.result.replace(/\\n/g, '<br>');
                    submitBtn.disabled = false;
                    statusEl.textContent = 'Research completed!';
                } else if (data.status === 'error') {
                    // Research encountered an error
                    clearInterval(statusCheckInterval);
                    loadingEl.style.display = 'none';
                    statusEl.textContent = `Error: ${data.result}`;
                    submitBtn.disabled = false;
                } else if (data.status === 'running') {
                    // Research is still running
                    statusEl.textContent = 'Research in progress...';
                } else {
                    // Unknown status
                    clearInterval(statusCheckInterval);
                    loadingEl.style.display = 'none';
                    statusEl.textContent = 'Unknown research status.';
                    submitBtn.disabled = false;
                }
                
            } catch (error) {
                console.error('Error checking status:', error);
                statusEl.textContent = `Status check error: ${error.message}`;
            }
        }
    </script>
</body>
</html>"""
    
    with open(os.path.join('templates', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000) 