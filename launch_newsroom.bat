@echo off
SETLOCAL EnableDelayedExpansion

echo 📰 Iniciando The Newsroom MCP...
cd /d "%~dp0"

:: 1. Activar entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Error: No se encuentra el entorno virtual. Ejecuta primero la instalacion.
    pause
    exit /b
)

echo 🚀 Levantando servidor e Inspector MCP...
:: Iniciar el servidor con mcp dev (esta vez sin minimizar para que se vea la URL y el Token)
start cmd /k ".\venv\Scripts\activate.bat && mcp dev the_newsroom.py"

echo ⏳ El Inspector MCP se abrira en una nueva ventana.
echo 💡 Busca la linea que dice "MCP Inspector is up and running at http://..." 
echo 💡 Copia y pega esa URL en tu navegador si no se abre automaticamente.

echo ✅ El sistema esta arrancando...
timeout /t 10 > nul
exit
