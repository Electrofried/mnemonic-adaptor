# **Mnemonic Adaptor**

<div align="center">
<img src="https://github.com/user-attachments/assets/b7252e05-a9ab-4474-ab3c-eb6a9227a725" width="600">
</div>


A sophisticated Python utility for advanced memory segmentation and extraction, leveraging large language models (LLMs) through the Ollama API. This tool distinguishes itself with its modular architecture, seamless customization via external prompt files, and its capability to efficiently process extensive input data by dynamically segmenting text into coherent "core memories." These outputs are structured as JSON objects, enabling their direct integration into AI-driven systems and workflows.&#x20;

---

## **Key Features**

- **Configurable and Modular Design** 🛠️: Centralized configuration for API endpoints, model parameters, and operational settings ensures flexibility and scalability.
- **Dynamic Prompt Management** ✏️: Load and customize system and user prompts via external files, tailoring workflows to diverse applications.
- **Advanced Memory Segmentation** 🧠: Extract and organize critical information from text, generating structured JSON outputs for downstream processing.
- **Chunked Input Processing** 🔄: Handle large text inputs by dividing them into manageable segments without losing coherence or context.
- **Robust Error Handling** 🛡️: Comprehensive error management addresses potential issues with file operations, API communication, and JSON parsing.
- **Efficient Output Management** 📁: Save extracted memory objects as uniquely named JSON files, systematically organized within a designated output directory. 

---

## **Why Use This Tool?**

This utility is particularly suited for researchers, developers, and AI practitioners working with LLMs who aim to:

- Extract structured insights from unstructured data, such as synthesizing information from extensive reports or summarizing collaborative meeting transcripts. 
- Implement persistent memory modules within AI systems to support applications like personal knowledge management, context-aware assistance, or decision-making frameworks. 
- Streamline API workflows, automating complex tasks such as customer sentiment analysis, content classification, and thematic research synthesis. 

---

## **Requirements**

- Python 3.7+ 🐍
- `requests` library for API interactions 🌐
- Access to a functional Ollama server for model communication 

---

## **Getting Started**

1. **Clone the repository** 🛠️:

   ```bash
   git clone https://github.com/<your-username>/ollama-memory-agent.git
   cd ollama-memory-agent
   ```

2. **Install dependencies** 📦:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings** ⚙️:
   Adjust the `CONFIG` dictionary within `main.py` to align with your specific requirements.

4. **Run the script** ▶️:

   ```bash
   python main.py "Your text here"
   python main.py /path/to/text_file.txt
   ```

---

## **Customization**

System and user prompts can be tailored to specific use cases by modifying the respective `.txt` files. For example, you can adjust the tone, level of detail, or domain specificity to align with tasks such as generating concise technical summaries or simplifying content for general audiences. These adjustments directly influence the tool's output, ensuring it is adaptable and purpose-driven.&#x20;

Editable prompt files include:

- `segmentation_agent_system_prompt.txt` ✏️
- `memory_extraction_agent_system_prompt.txt` 🗒️

---

## **Contributing**

We welcome contributions from the community! Whether it’s submitting issues, proposing enhancements, or providing pull requests, your input is invaluable to the continuous improvement of this project.&#x20;

