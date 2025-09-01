import os
from dotenv import load_dotenv
import json
import textwrap
from pathlib import Path
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OUTPUT_DIR = Path("relatorios")
OUTPUT_DIR.mkdir(exist_ok=True)

CHUNK_SIZE = 3000  

def ler_codigo_python():
    """Lê todos os arquivos .py do projeto."""
    arquivos_codigo = []
    for root, _, files in os.walk("./testes"):
        if "venv" in root or ".github" in root or "scripts" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                caminho = os.path.join(root, file)
                with open(caminho, "r", encoding="utf-8") as f:
                    arquivos_codigo.append((caminho, f.read()))
    return arquivos_codigo

def dividir_em_chunks(texto, tamanho=CHUNK_SIZE):
    """Divide um texto em blocos menores."""
    return textwrap.wrap(texto, tamanho)

client = OpenAI(api_key=OPENAI_API_KEY)

def analisar_com_chatgpt(codigo):
    """Envia código para análise no ChatGPT."""
    prompt = f"""
Você é um especialista em segurança de software. 
Analise o código abaixo e identifique vulnerabilidades, 
classifique o tipo (ex: SQL Injection, XSS, etc.), 
explique o impacto e sugira uma correção:

{codigo}
"""
    try:
        resposta = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return resposta.choices[0].message.content
    except Exception as e:
        return f"Erro na análise com ChatGPT: {str(e)}"
    
def main():
    print("🔍 Iniciando análise com LLMs...")
    resultados = []

    for caminho, codigo in ler_codigo_python():
        for chunk in dividir_em_chunks(codigo):
            resultado_chatgpt = analisar_com_chatgpt(chunk)

            resultados.append({
                "arquivo": caminho,
                "codigo": chunk,
                "chatgpt": resultado_chatgpt,
            })

    with open(OUTPUT_DIR / "relatorio_llm.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    with open(OUTPUT_DIR / "relatorio_llm.txt", "w", encoding="utf-8") as f:
        for r in resultados:
            f.write(f"Arquivo: {r['arquivo']}\n")
            f.write(f"--- ChatGPT ---\n{r['chatgpt']}\n")
            f.write("\n" + "="*60 + "\n")

    print(f"✅ Análise concluída. Relatórios salvos em '{OUTPUT_DIR}'.")

if __name__ == "__main__":
    main()
