# **mnemonic adaptor**
![image](https://github.com/user-attachments/assets/3dcdb657-d1c0-490a-b385-269abbff7286)

A Python-based utility for advanced memory segmentation and extraction using large language models (LLMs) via the Ollama API. This script processes user inputs (files or raw text), segments them into meaningful "core memories," and generates structured memory objects in JSON format, ready for use in AI-driven workflows.

## **Features**:
- **Configurable and Modular**: Centralized configuration for API endpoints, model parameters, and processing options.
- **Prompt Management**: Load and customize system and user prompts dynamically from external files.
- **Chunked Processing**: Automatically handles large inputs by splitting them into manageable chunks for processing.
- **Memory Segmentation**: Extracts key information from text, with support for structured JSON output.
- **Error Handling**: Robust error management for file operations, API calls, and JSON parsing.
- **Output Management**: Saves extracted memories as uniquely named JSON files in an organized directory.

## **Why Use This Tool?**
This tool is ideal for developers, researchers, and enthusiasts working with LLMs to:
- Extract structured data from unstructured text.
- Implement memory augmentation or knowledge persistence in AI systems.
- Simplify API-based workflows with streamlined automation.

## **Requirements**:
- Python 3.7+
- `requests` library for API communication.
- Access to an Ollama server for model interactions.

## **Getting Started**:
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/ollama-memory-agent.git
   cd ollama-memory-agent
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure settings in the `CONFIG` dictionary in `main.py`.
4. Run the script with your input:
   ```bash
   python main.py "Your text here"
   python main.py /path/to/text_file.txt
   ```

## **Customization**:
Easily modify the system and user prompts by editing the corresponding `.txt` files:
- `segmentation_agent_system_prompt.txt`
- `memory_extraction_agent_system_prompt.txt`

## **Contributing**:
Contributions are welcome! Feel free to submit issues or pull requests to help improve this project.
