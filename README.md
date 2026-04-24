# B2B Document Translator

Una aplicación web **serverless** y de alto rendimiento diseñada para la traducción inteligente de documentos y capturas de pantalla. Este proyecto elimina la dependencia de servicios premium costosos (como Azure Document Translator) utilizando un stack basado en modelos de IA de última generación y procesamiento local de archivos.

## Características Principales

* **Traducción de Word (.docx):** Extrae y traduce el contenido manteniendo la estructura de párrafos, estilos y tablas originales.
* **Procesamiento de PDF:** Implementa una lógica de extracción limpia mediante `pdfplumber`, reconstruyendo el flujo de lectura antes de generar un nuevo PDF con `reportlab`.
* **OCR con Gemini 2.5 Flash:** Utiliza la API de Google GenAI para leer texto en imágenes con alta precisión, ideal para traducir capturas de chats o documentos escaneados.
* **Optimización de Costos:** Arquitectura 100% gratuita que utiliza `deep-translator` (Google Translate Engine) y el nivel gratuito de Gemini.
* **Interfaz Fluida:** Construido con Streamlit para ofrecer una experiencia de usuario rápida con barras de progreso en tiempo real.

## Stack Tecnológico

* **Lenguaje:** Python.
* **Framework:** Streamlit (UI y despliegue).
* **IA & OCR:** Google Gemini 2.5 Flash (`google-genai`).
* **Traducción:** `deep-translator`.
* **Manejo de Documentos:** `python-docx`, `pdfplumber` y `reportlab`.

## Configuración Local

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/guille123giles-cloud/b2b-document-translator.git](https://github.com/guille123giles-cloud/b2b-document-translator.git)
    cd b2b-document-translator
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Variables de Entorno:**
    Añade tu API Key de Gemini en el archivo `.streamlit/secrets.toml`:
    ```toml
    GEMINI_API_KEY = "tu_clave_aqui"
    ```

4.  **Ejecutar:**
    ```bash
    streamlit run app.py
    ```

---
*Desarrollado como una solución de ingeniería para la automatización de flujos de trabajo multilingües.*
