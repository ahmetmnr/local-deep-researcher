import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from ollama_deep_researcher.graph import graph
from ollama_deep_researcher.configuration import Configuration

# Load environment variables from .env file if it exists
load_dotenv()

# Configure the research assistant
config = Configuration(
    max_web_research_loops=2,  # Number of research iterations
    local_llm="llama3.2", # Using the llama3.2 model that's available
    llm_provider="ollama",  # Use Ollama (alternatives: "lmstudio")
    search_api="duckduckgo",  # Use DuckDuckGo for searching (alternatives: "perplexity", "tavily", "searxng")
    fetch_full_page=True,  # Fetch full page content for better research
    ollama_base_url="http://localhost:11434/",  # Ollama API URL
    strip_thinking_tokens=True  # Remove thinking tokens from LLM responses
)

# Create a RunnableConfig with the configuration
runnable_config = RunnableConfig(configurable=config.model_dump())

# Define a more specific research topic in Turkish about educational AI implementations
research_topic = "Türkiye'deki okullarda yapay zeka destekli eğitim uygulamaları ve başarı oranları"

# Run the research workflow
result = graph.invoke(
    {"research_topic": research_topic},
    config=runnable_config
)

# Print the research result
print("\n\n=== RESEARCH SUMMARY ===\n\n")
print(result["running_summary"]) 