import sys
import os
import asyncio
import warnings
from typing import Dict, List, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
import google.generativeai as genai

# Silenciar avisos de deprecación
warnings.filterwarnings("ignore", category=FutureWarning)

def log(msg: str):
    """Escribe en stderr para que aparezca en la terminal sin romper el protocolo MCP"""
    sys.stderr.write(f"LOG: {msg}\n")
    sys.stderr.flush()

# Cargar variables de entorno con ruta absoluta
# Esto es vital para que el Inspector encuentre la clave
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    log("Configurando Gemini API...")
    genai.configure(api_key=GOOGLE_API_KEY)
    MODEL_NAME = 'gemini-2.0-flash'
    model = genai.GenerativeModel(MODEL_NAME)
    log(f"✅ Gemini configurado correctamente con el modelo: {MODEL_NAME}")
else:
    log(f"❌ ERROR: No se encontró la API KEY en: {env_path}")
    log("Por favor, verifica que el archivo .env existe en esa carpeta.")

# Inicializar FastMCP
app = FastMCP("The Newsroom")

@app.tool()
async def ping() -> str:
    """Herramienta de prueba rápida."""
    log("Recibido 'ping'")
    return "¡PONG! El servidor está vivo."

@app.tool()
async def ping_ai(mensaje: str) -> str:
    """Prueba si Gemini responde a una sola pregunta."""
    log(f"Recibido 'ping_ai' con: {mensaje}")
    try:
        response = await asyncio.to_thread(model.generate_content, mensaje)
        log("✅ Gemini respondió en ping_ai")
        return f"Gemini dice: {response.text}"
    except Exception as e:
        log(f"❌ Error en ping_ai: {e}")
        return f"Error: {e}"

# Personas
PERSONAS = {
    "skeptic": "Eres el 'Abogado del Diablo'. Busca fallos lógicos y riesgos.",
    "empath": "Eres experto en empatía. Analiza el tono y el impacto emocional.",
    "grammar": "Eres experto en estilo. Busca errores gramaticales y falta de claridad.",
    "chief_editor": "Eres el Editor Jefe. Synthetiza las críticas y crea la versión final."
}

async def get_ai_response(prompt: str, system_prompt: str, ctx: Optional[Context] = None) -> str:
    persona_short = system_prompt.split(".")[0][:20]
    
    # Intento de Sampling
    if ctx and hasattr(ctx, "sampling") and ctx.sampling:
        try:
            log(f"-> [SAMPLING] {persona_short}...")
            result = await ctx.sampling.create_message(
                messages=[{"role": "user", "content": prompt}],
                system_prompt=system_prompt,
                max_tokens=500
            )
            log(f"<- [SAMPLING] OK")
            return result.content.text
        except Exception as e:
            log(f"Sampling falló ({e}). Usando fallback...")

    # Fallback Directo
    log(f"-> [GEMINI] {persona_short}...")
    full_prompt = f"SYSTEM: {system_prompt}\n\nUSER: {prompt}"
    response = await asyncio.to_thread(model.generate_content, full_prompt)
    log(f"<- [GEMINI] OK")
    return response.text

@app.tool()
async def review_draft(text: str, ctx: Context) -> str:
    """Revisión editorial profunda con 4 llamadas a Gemini."""
    log(f"--- INICIO REVISIÓN: {text[:30]}... ---")
    
    tasks = [
        get_ai_response(text, PERSONAS["skeptic"], ctx),
        get_ai_response(text, PERSONAS["empath"], ctx),
        get_ai_response(text, PERSONAS["grammar"], ctx)
    ]
    
    log("Esperando las 3 revisiones paralelas...")
    results = await asyncio.gather(*tasks)
    skeptic_res, empath_res, grammar_res = results
    
    log("Revisiones recibidas. Generando síntesis final...")
    
    synthesis_prompt = f"ORIGINAL: {text}\n\nSKEPTIC: {skeptic_res}\n\nEMPATH: {empath_res}\n\nGRAMMAR: {grammar_res}\n\nGenera la versión final pulida."
    final = await get_ai_response(synthesis_prompt, PERSONAS["chief_editor"], ctx)
    
    log("--- FIN REVISIÓN OK ---")
    
    return f"# 📰 REPORTE\n\n## SUGERENCIA\n{final}\n\n---\n## EXPERTOS\n- **Escéptico:** {skeptic_res}\n- **Empatía:** {empath_res}\n- **Estilo:** {grammar_res}"

if __name__ == "__main__":
    app.run()
