# **Mnemonic Adaptor**

<div align="center">

<img src="https://github.com/user-attachments/assets/b7252e05-a9ab-4474-ab3c-eb6a9227a725" width="600">

</div>

A simple yet powerful example of LLM-based computation for creating mnemonic devices from universal text input sources. This project focuses on local hosting and on-demand functionality, emphasizing simplicity while producing memory JSON objects that can serve diverse applications—from chatbot memory systems to dynamic database generation based on user inputs.

---

## **Key Features**

- **Configurable and Modular Design** 🛠️: Centralized configuration for API endpoints, model parameters, and operational settings ensures flexibility and scalability.
- **Dynamic Prompt Management** ✏️: Easily load and customize system and user prompts via external files, enabling tailored workflows for varied use cases.
- **Advanced Memory Segmentation** 🧠: Extract and organize critical information from text, generating structured JSON outputs suitable for downstream processing.
- **Chunked Input Processing** 🔄: Handles large text inputs by dividing them into manageable segments while preserving coherence for inputs up to **20,000 characters**.
- **Robust Error Handling** 🛡️: Implements comprehensive error management to address issues with file operations, API communication, and JSON parsing.
- **Efficient Output Management** 📁: Saves extracted memory objects as uniquely named JSON files, systematically organized within a designated output directory.

---

## **Why Use This Tool?**

This utility is designed for researchers, developers, and AI practitioners who need to:

- Extract structured insights from unstructured data, such as synthesizing information from extensive reports or summarizing collaborative meeting transcripts. 📋🧾📊
- Implement persistent memory modules within AI systems to support applications like personal knowledge management, context-aware assistance, or decision-making frameworks. 🧠🤖🔍
- Streamline API workflows, automating complex tasks such as customer sentiment analysis, content classification, and thematic research synthesis. 💻🌐🔧

---

## **Requirements**

- Python 3.7+ 🐍
- `requests` library for API interactions 🌐
- Access to a functional **DeepSeek API** for model communication 📡💾🔌

---

## **Getting Started**

1. **Clone the repository** 🛠️:

   ```bash
   git clone https://github.com/<your-username>/mnemonic-adaptor.git
   cd mnemonic-adaptor
   ```

2. **Install dependencies** 📦:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings** ⚙️:
   Adjust the `CONFIG` dictionary within `config.py` to align with your specific requirements. Ensure you have your DeepSeek API key in the `api.txt` file.

4. **Run the script** ▶️:

   ```bash
   python main.py "Your text here"
   python main.py /path/to/text_file.txt
   ```

---

## **Customization**

Tailor system and user prompts to specific use cases by modifying the respective `.json` files. For example, you can adjust tone, level of detail, or domain specificity to align with tasks such as generating concise technical summaries or simplifying content for general audiences. These adjustments directly influence the tool's output, ensuring it remains adaptable and purpose-driven.

Editable prompt files include:

- `prompts.json` ✏️: Contains system and user prompts for memory extraction and segmentation.

---

## **Contributing**

We welcome contributions from the community! Whether it’s submitting issues, proposing enhancements, or providing pull requests, your input is invaluable to the continuous improvement of this project. 🙌🌍🤝

For detailed contribution guidelines, refer to the `CONTRIBUTING.md` file in the repository. 💡🎉✨

---

## **Changelog**

### **Latest Changes**
- **Increased Chunk Size**: The system now supports processing text chunks of up to **20,000 characters**, allowing for more efficient handling of large inputs.
- **DeepSeek Integration**: The project can now use DeepSeek's advanced chat model for improved memory extraction and segmentation.

---


