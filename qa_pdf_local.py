import json
from pypdf import PdfReader
import subprocess
import os

# Carpetas
PDF_FOLDER = "PDFs"
OUTPUT_FOLDER = "Outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 1. Leectura PDF
def extract_pdfs_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for pagina in reader.pages:
        text += pagina.extract_text() + "\n"
    return text

# 2. División de texto de los PDF en chunks
def split_text(text, max_chars=2000):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

# 3. Llamada al modelo local con Ollama
def generate_qa(chunk, n_questions=5, model="mistral"):
    prompt = f"""
    Genera {n_questions} preguntas y respuestas en español
    basadas en el siguiente texto. Devuelve solo un JSON válido:

    [
      {{"question": "...", "answer": "..."}}
    ]

    Texto:
    {chunk}
    """
    
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    
    output = result.stdout.decode("utf-8").strip()
    
    try:
        return json.loads(output)
    except:
        print("No se pudo parsear como JSON. Texto devuelto:")
        print(output)
        return []

# 4. Función principal que llama demás funciones para generar las preguntas Q&A
def process_pdf(pdf_path, output_json, questions_per_chunk=5):
    text = extract_pdfs_text(pdf_path)
    chunks = split_text(text)

    qa_total = []
    for i, chunk in enumerate(chunks, 1):
        print(f"Procesando chunk {i}/{len(chunks)}...")
        qa = generate_qa(chunk, questions_per_chunk)
        qa_total.extend(qa)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(qa_total, f, indent=2, ensure_ascii=False)

    print(f"Q&A guardados")


# 5. Se procesan todos los PDFs de la carpeta PDFs
if __name__ == "__main__":
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No se encontraron PDFs en la carpeta 'PDFs'.")
    else:
        for pdf_file in pdf_files:
            pdf_path = os.path.join(PDF_FOLDER, pdf_file)
            output_name = os.path.splitext(pdf_file)[0] + "_qa.json"
            output_path = os.path.join(OUTPUT_FOLDER, output_name)

            if os.path.exists(output_path): #Se ignora algún PDF que ya se haya procesado con anterioridad, eliminar archivo o cambiar noche si se quiere volver a procesar
                print(f"PDF {pdf_file} ya procesado.")
                continue

            try: #Si algun archivo genera un error, se salta el archivo y se sigue con el siguiente
                process_pdf(pdf_path, output_path, questions_per_chunk=3)
                print(f"Procesado: {pdf_file}")
            except Exception as e:
                print(f"Error {pdf_file}: {e}")