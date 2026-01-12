# 📰 The Newsroom MCP (Model Context Protocol)

**Versión:** 0.1.0-alpha

Este proyecto implementa un servidor **MCP (Model Context Protocol)** avanzado llamado **"The Newsroom"** (La Sala de Redacción). Utiliza la técnica de **MCP Sampling (Muestreo)** e **Inversión de Control** para orquestar un flujo de revisión editorial multi-persona utilizando IA.

## 🚀 Características

- **Orquestación Multi-Persona**: Un borrador de texto es analizado simultáneamente por tres expertos virtuales:
    - 😈 **El Escéptico**: Busca fallos lógicos, riesgos y debilidades.
    - 🤝 **El Empatizador**: Analiza el tono y el impacto emocional en la audiencia.
    - 📝 **El Corrector de Estilo**: Busca mejorar la gramática, claridad y fluidez.
- **Síntesis del Editor Jefe**: Un cuarto proceso actúa como Editor Jefe, recibiendo las tres críticas y el texto original para generar una versión final pulida y equilibrada.
- **Arquitectura Híbrida**: Diseñado para soportar **MCP Sampling** (usando el cerebro del cliente) con un fallback automático a la **API de Gemini 2.0 Flash** (usando el cerebro del servidor).
- **Herramientas de Diagnóstico**: Incluye herramientas `ping` y `ping_ai` para verificar la conectividad y el estado de la IA.

## 🛠️ Instalación y Uso

### 1. Requisitos
- Python 3.10 o superior.
- Una clave de API de **Google Gemini**.

### 2. Configuración
1. Clona este repositorio.
2. Crea un archivo `.env` en la raíz del proyecto con tu clave:
   ```env
   GOOGLE_API_KEY=tu_clave_aqui
   ```
3. Crea un entorno virtual e instala las dependencias:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

### 3. Ejecución
Para probar el servidor con el **MCP Inspector**:
```powershell
mcp dev the_newsroom.py
```
Copia la URL con el Token que aparecerá en la terminal y pégala en tu navegador.

## 🧠 El Concepto de Sampling

Este servidor demuestra la potencialidad de que las herramientas de IA no solo devuelvan datos, sino que **orquesten pensamientos**. En lugar de requerir una infraestructura compleja de agentes, "The Newsroom" utiliza al propio Cliente (como Cursor o Claude Desktop) para realizar las llamadas cognitivas, permitiendo una escalabilidad inteligente y económica.

## 📚 Recursos Educativos (Documentación del Proceso)

Para ayudar a entender mejor el desarrollo de este servidor MCP, hemos incluido los documentos de planificación y depuración generados durante su creación:

*   [**Informe de Sampling**](Sampling_Report_Debugging_MCP_Server_Launch.md): Explicación detallada del concepto de Muestreo e Inversión de Control.
*   [**Guía de Uso (Walkthrough)**](Walkthrough_Debugging_MCP_Server_Launch.md): Cómo probar y verificar las herramientas paso a paso.
*   [**Plan de Implementación**](Implementation_Plan_Debugging_MCP_Server_Launch.md): El diseño técnico original y los retos superados.
*   [**Registro de Tareas**](Task_Debugging_MCP_Server_Launch.md): El checklist del proceso de construcción.

## 📄 Licencia
MIT

---
*Desarrollado para explorar los límites de la orquestación cognitiva con MCP y Gemini.*
