# Pipeline de Análisis Existencialista: TikTok Profile Insights

### Objetivo del Proyecto
Desarrollar un sistema automatizado de extracción y análisis de datos que transforme el historial de consumo de TikTok (descripciones de videos) en un perfil psicológico profundo. El proyecto busca identificar patrones subyacentes, evasiones y anhelos del usuario mediante Inteligencia Artificial Generativa, aplicando un tono literario existencialista (inspirado en Dostoievski y Pizarnik).

### Flujo del Sistema
1. **Extracción (Scraping):** Uso de Selenium en Python para conectar con una instancia de Brave/Chrome abierta en modo depuración.
2. **Procesamiento de Datos:** Limpieza y estructuración de las descripciones extraídas en un archivo `datos_brutos.json`.
3. **Análisis de IA:** Envío del JSON a la API de **Gemini 2.5 Flash** mediante peticiones REST (POST).
4. **Generación de Informe:** Producción de un archivo de texto final con las conclusiones del análisis.
5. **Orquestación:** Comando unificado `run.py` que encadena todo el proceso.

### Uso del Pipeline Unificado
Para ejecutar todo el flujo (Extracción + Análisis) con un solo comando:
```bash
python run.py
```

### Configuración del Entorno de Navegación
Para evitar bloqueos de login y usar las cookies activas (Extension: **Cookie-Editor**), se utiliza el modo de depuración remota:

**Comando de apertura (Windows + R):**
- **Brave:** `brave.exe --remote-debugging-port=9222`
- **Chrome:** `chrome.exe --remote-debugging-port=9222`
con la cuenta de trabajo

### Estado de la Infraestructura (API Testing)

#### Curl Exitoso (Validación de Conexión):
Este comando confirmó que la API Key y el modelo Gemini 2.5 Flash están operativos:
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=AIzaSyC7cMVXFjB7aHaDyJdJWukeRAYJlLwMzYo" -H "Content-Type: application/json" -X POST -d "{\"contents\": [{\"parts\":[{\"text\": \"Hola, responde solo con la palabra CONECTADO\"}]}]}"