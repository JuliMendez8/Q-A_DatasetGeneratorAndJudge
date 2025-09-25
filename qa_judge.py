import ollama
import json
import os

# Carpetas
OUTPUT_FOLDER = "Outputs"
EVALUATED_FOLDER = "Evaluated_Outputs"
os.makedirs(EVALUATED_FOLDER, exist_ok=True)

## 1. Llamada al modelo local (llama3 en este caso) con Ollama y se le da un rol de "Juez"
def evaluate_qa(question, answer, model="llama3"):
    """
    Evalúa un par Pregunta-Respuesta usando un modelo LLM como 'juez'.
    Retorna un dict con claridad, relevancia, fidelidad, puntaje y comentarios.
    """
    prompt = f"""
Eres un evaluador experto.
Evalúa la calidad del siguiente par Pregunta-Respuesta.

Devuelve SOLO un JSON válido en este formato:

{{
  "question": "{question}",
  "answer": "{answer}",
  "evaluation": {{
    "clarity": "good|bad",
    "relevance": "good|bad",
    "faithfulness": "good|bad",
    "overall_score": 1-5,
    "comments": "explicación breve"
  }}
}}
"""
    try:
        Answ = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        output = Answ["message"]["content"].strip()
        return json.loads(output)
    except json.JSONDecodeError:
        return {
            "raw": output
        }
    except Exception as e:
        return {
            "error": str(e)
        }

# 2. Se procesan todos los JSONs de la carpeta Outputs
if __name__ == "__main__":
    json_files = [f for f in os.listdir(OUTPUT_FOLDER) if f.lower().endswith(".json")]

    if not json_files:
        print("No se encontraron archivos JSON en la carpeta 'Outputs'.")
    else:
        for json_file in json_files:
            input_path = os.path.join(OUTPUT_FOLDER, json_file)
            output_name = os.path.splitext(json_file)[0] + "_evaluated.jsonl"
            output_path = os.path.join(EVALUATED_FOLDER, output_name)

            if os.path.exists(output_path):
                print(f"{json_file} ya evaluado. Se omite.")
                continue

            # Leer dataset de Q&A
            with open(input_path, "r", encoding="utf-8") as f:
                qa_dataset = json.load(f)

            with open(output_path, "w", encoding="utf-8") as f_out:
                for i, item in enumerate(qa_dataset, 1):
                    print(f"Evaluando {json_file} → Q&A {i}/{len(qa_dataset)}...")
                    result = evaluate_qa(item["question"], item["answer"], model="llama3")
                    # Se guarda cada resultado inmediatamente en formato JSON Lines
                    f_out.write(json.dumps(result, ensure_ascii=False) + "\n")
                    f_out.flush()

            print(f"Evaluación completada.")