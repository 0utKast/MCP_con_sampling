import sys
import os
import asyncio
import warnings
from typing import Dict, List, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
import google.generativeai as genai

# Silenciar avisos de deprecación para una consola limpia
warnings.filterwarnings("ignore", category=FutureWarning)

def log(msg: str):
    """Escribe en stderr para que aparezca en la terminal sin romper el protocolo MCP"""
    sys.stderr.write(f"LOG: {msg}\n")
    sys.stderr.flush()

# Cargar variables de entorno
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(env_path)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    log("Configurando Gemini API...")
    genai.configure(api_key=GOOGLE_API_KEY)
    MODEL_NAME = 'gemini-2.0-flash'
    model = genai.GenerativeModel(MODEL_NAME)
    log(f"✅ Gemini configurado correctamente con: {MODEL_NAME}")
else:
    log(f"❌ ERROR: No se encontró la API KEY en: {env_path}")

# Inicializar FastMCP
app = FastMCP("The Newsroom")

@app.tool()
async def ping() -> str:
    """Herramienta de prueba rápida."""
    log("Recibido 'ping'")
    return "¡PONG! El servidor está vivo."

@app.tool()
async def review_draft(text: str, ctx: Context) -> str:
    """Revisión editorial profunda optimizada para evitar timeouts."""
    log(f"--- INICIO REVISIÓN (Modo Concilio): {text[:30]}... ---")
    
    # Optimizamos a una sola llamada potente para evitar el timeout del Inspector
    system_prompt = """
    Actúa como un Consejo Editorial de élite compuesto por:
    1. EL ESCÉPTICO: Identifica riesgos, grietas lógicas y fallos de credibilidad.
    2. EL EMPÁTICO: Analiza el tono, la conexión con la audiencia y el impacto emocional.
    3. EL LINGÜISTA: Asegura la claridad radical, elegancia léxica y gramática perfecta.
    
    Tu tarea:
    - Analiza el texto desde estas 3 perspectivas.
    - Como EDITOR JEFE, genera una VERSIÓN FINAL pulida que integre todas las mejoras.
    
    Formato de respuesta:
    # 📰 INFORME DE REDACCIÓN
    ## 🧐 Visión del Escéptico
    ...
    ## 🎭 Visión del Empático
    ...
    ## ✍️ Visión del Lingüista
    ...
    ## 🚀 VERSIÓN FINAL MEJORADA
    ...
    """
    
    log("Consultando al Concilio de Expertos (Llamada única para velocidad)...")
    
    try:
        # Usamos threading para no bloquear el transporte mientras esperamos a Gemini
        full_prompt = f"TEXTO A REVISAR:\n\"{text}\""
        
        # Primero intentamos Sampling si está disponible (solo por si el cliente lo soporta)
        if ctx and hasattr(ctx, "sampling") and ctx.sampling:
            try:
                log("Intentando Sampling...")
                result = await ctx.sampling.create_message(
                    messages=[{"role": "user", "content": full_prompt}],
                    system_prompt=system_prompt,
                    max_tokens=1000
                )
                log("--- FIN REVISIÓN (SAMPLING) OK ---")
                return result.content.text
            except Exception:
                log("Sampling no disponible. Usando Gemini directo...")

        # Fallback: Llamada directa rápida
        response = await asyncio.to_thread(
            model.generate_content, 
            f"SYSTEM: {system_prompt}\n\nUSER: {full_prompt}"
        )
        
        log("--- FIN REVISIÓN OK ---")
        return response.text

    except Exception as e:
        log(f"❌ Error en la revisión: {e}")
        return f"Lo siento, hubo un error procesando la revisión: {e}"

if __name__ == "__main__":
    app.run()
