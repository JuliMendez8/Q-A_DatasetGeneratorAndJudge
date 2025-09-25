# Q&A_DatasetGeneratorAndJudge  

This project provides a pipeline for generating and evaluating synthetic **Question-Answer (Q&A)** datasets from PDF documents using local **Large Language Models (LLMs)** with **Ollama**.  

### **Generator**  
- **Extracts** text from PDFs.  
- **Splits** the text into chunks (paragraph-aware).  
- **Generates** synthetic Q&A pairs in JSON format.  

### **Judge**  
- **Evaluates** the generated Q&A pairs using another LLM acting as a "judge".  
- **Rates** each pair based on clarity, relevance, and faithfulness.  
- **Saves** the evaluation in JSONL format.  

### **📄 Workflow**  
**1 PDF → 1 Q&A dataset (.json) → 1 Evaluated dataset (.jsonl)**  

This tool is useful for creating useful and personaliced datasets to train chat LLMs.


### **Requeriments**  
- Download Ollama
- Enough resources in your PC based on which model are you using to be the generator and the judge
- Create the folders, "PDFs", "Outputs" and "Evaluated_Outputs" on the same level of the files "qa_judge.py" and "qa_pdf_local.py" 

