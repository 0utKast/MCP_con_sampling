# Implementation Plan - The Newsroom MCP

This project implements "The Newsroom" (La Sala de Redacción), an MCP server that uses **Sampling** to orchestrate a multi-persona editorial review of text drafts.

## Goal Description
Create a tool called `review_draft` that takes a user's text and passes it through a "mesa de redacción" (editorial board) composed of three specialized AI reviewers. A "Chief Editor" then synthesizes their feedback into a final, polished version.

> [!IMPORTANT]
> **Integración con Gemini**: Siguiendo tu petición, configuraremos el servidor para que use la API de Gemini mediante el archivo `.env`. Esto nos permite dos cosas:
> 1. Mostrar el flujo de "Muestreo" (Sampling) orquestado.
> 2. Asegurar que el servidor tenga "cerebro propio" usando tu clave, independientemente de si el cliente MCP soporta sampling nativo o no.

## Proposed Changes

### [Server Implementation]

#### [NEW] [the_newsroom.py](file:///c:/proyectos_python/muestreo/the_newsroom.py)
This will be the main entry point for the MCP server. It will use the `fastmcp` library.

**Key Features:**
- **Personas Definition**:
    - `SKEPTIC`: Focused on logic, risks, and accuracy.
    - `EMPATH`: Focused on tone, emotional impact, and audience reception.
    - `GRAMMARIAN`: Focused on grammar, syntax, and clarity.
    - `CHIEF_EDITOR`: The one who mediates and produces the final draft.
- **`review_draft` Tool**:
    - Uses `ctx.sampling.create_message` (or `ctx.sample`) to call the personas in parallel (or sequence depending on SDK nuances).
    - Aggregates the feedback.
    - Performs a final sampling call for the synthesis.

### [Environment Setup]

#### [NEW] [requirements.txt](file:///c:/proyectos_python/muestreo/requirements.txt)
- `fastmcp`
- `mcp`
- `google-generativeai`
- `python-dotenv`

## Verification Plan

### Manual Verification
1. Run the server using `mcp dev the_newsroom.py` and connect it to a client (like Cursor or Claude Desktop).
2. Invoke the `review_draft` tool with a sample text (e.g., a controversial tweet, a formal email, or a creative story).
3. Verify that the output contains:
    - The original text.
    - Insights from the three reviewers (internal or shared).
    - The final synthesized version.

### Automated Tests
- Since this relies heavily on Sampling (which involves a real LLM on the client side), automated tests will focus on the structure of the prompt generation and the handling of the tool call logic.

> [!NOTE]
> MCP Sampling is a relatively new feature. Success depends on the client (the AI app you are using) supporting the `sampling/create_message` capability.
