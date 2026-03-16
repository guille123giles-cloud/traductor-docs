# 🌍 B2B Document Translator: Traducción Inteligente & OCR

Una plataforma web de grado profesional diseñada para la traducción asíncrona de documentos técnicos/legales y la extracción de texto complejo en imágenes. Esta herramienta supera las limitaciones de las librerías de procesamiento local delegando la carga computacional a arquitecturas de Inteligencia Artificial en la nube.

## 🚀 Características Principales

* **Procesamiento de Documentos (PDF/DOCX):** Integración con **Microsoft Azure AI Document Translation** y **Azure Blob Storage**. Traduce documentos completos manteniendo exactamente la misma maquetación, gráficos, tablas y estilos originales.
* **Visión Artificial Avanzada (OCR):** Implementación del modelo **Google Gemini 2.5 Flash** para extraer texto de capturas de pantalla, recibos y fotos con precisión absoluta (incluso con fondos complejos o emojis), superando a los motores tradicionales como Tesseract.
* **Arquitectura Segura (Stateless):** Privacidad garantizada. Los archivos se suben a la nube mediante tokens de seguridad temporales (SAS) e inmediatamente se ejecutan rutinas de limpieza (`delete_blob`) para no dejar rastros de los documentos de los clientes en los servidores.
* **Traducción Optimizada:** Procesamiento en bloque para reducir la latencia de red y evitar la saturación de peticiones a la API.

## 🛠️ Tecnologías Utilizadas

* **Frontend & Framework:** Python 3.9+, [Streamlit](https://streamlit.io/)
* **Cloud Storage:** Azure Blob Storage (Contenedores seguros origen/destino)
* **Cloud AI:** Azure Cognitive Services (Traductor), Google GenAI SDK (Gemini)
* **Procesamiento de Texto:** Deep Translator

## ⚙️ Instalación y Uso Local

Si querés correr este proyecto en tu propia computadora, seguí estos pasos:

1. **Clonar el repositorio:**
```bash
git clone [https://github.com/tu-usuario/b2b-document-translator.git](https://github.com/tu-usuario/b2b-document-translator.git)
cd b2b-document-translator
```

2. **Instalar las dependencias:**
Se recomienda usar un entorno virtual (venv).
```bash
pip install -r requirements.txt
```

3. **Configurar las variables de entorno (Secretos):**
Creá una carpeta llamada `.streamlit` en la raíz del proyecto y adentro un archivo `secrets.toml`. Agregá tus claves de esta forma (¡Nunca subas este archivo a GitHub!):
```toml
TRANSLATOR_KEY = "tu_clave_de_azure_translation"
TRANSLATOR_ENDPOINT = "tu_endpoint_de_azure"
STORAGE_CONNECTION_STRING = "tu_cadena_de_conexion_de_blob_storage"
GEMINI_API_KEY = "tu_clave_de_google_aistudio"
```

4. **Ejecutar la aplicación:**
```bash
streamlit run app.py
```

## ☁️ Despliegue en Producción

Este proyecto está optimizado para ser desplegado de forma gratuita en **Streamlit Community Cloud**. Solo necesitás conectar tu repositorio, configurar los secretos desde el panel de "Advanced settings" y darle a Deploy.
