import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
# --- CONFIGURACIÓN TÉCNICA GROQ ---
API_KEY = os.getenv("API_KEY")
MODELO = "meta-llama/llama-4-scout-17b-16e-instruct"
URL = "https://api.groq.com/openai/v1/chat/completions"

def ejecutar_analisis():
    try:
        # Cargar datos brutos
        with open("datos_brutos.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        texto_videos = "\n".join([f"- {v.get('descripcion', '')}" for v in datos])

        # Prompt Existencialista (Mantenemos la esencia literaria solicitado inicialmente)
        prompt_sistema = (
            "Eres un Analista Existencialista experto con un tono literario inspirado en Dostoievski y Alejandra Pizarnik. "
            "Tu misión es transformar datos mundanos de TikTok en un perfil psicológico profundo y crudo."
        )

        prompt_intereses = (
            "Analiza las siguientes descripciones de videos de TikTok y genera un RESUMEN ESTRUCTURADO de los intereses de este usuario. "
            "El formato debe ser obligatoriamente:\n"
            "1. TOP 5 CATEGORÍAS\n"
            "2. TEMAS RECURRENTES\n"
            "3. NIVEL DE AFINIDAD (Porcentaje estimado)\n"
            "4. CONCLUSIÓN TÉCNICA (Análisis existencialista en 3 líneas)\n"
            "5. OPORTUNIDADES COMERCIALES (Qué ofrecerle según su psique)\n\n"
            "DATOS A ANALIZAR:\n" + texto_videos
        )

        # Payload para Groq (Formato OpenAI)
        payload = {
            "model": MODELO,
            "messages": [
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_intereses}
            ],
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        print(f"Enviando datos al motor Groq...")
        
        response = requests.post(URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            res_json = response.json()
            informe = res_json['choices'][0]['message']['content']
            
            with open("informe_final.txt", "w", encoding="utf-8") as f:
                f.write(informe)
            
            print("\nEXITO. Informe generado en 'informe_final.txt'.")
            print("-" * 30)
            print("Fragmento del análisis de Groq:")
            print(informe[:500] + "...")
        else:
            print(f"❌ Error {response.status_code}")
            print("Detalle técnico de Groq:")
            print(response.text)

    except Exception as e:
        print(f"❌ Error de ejecución: {e}")

if __name__ == "__main__":
    ejecutar_analisis()
