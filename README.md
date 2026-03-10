# B2B Document Translator: Traducción Inteligente & OCR

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Concurrency](https://img.shields.io/badge/Concurrency-Multi--Threading-blue?style=for-the-badge)

**B2B Document Translator** es una plataforma robusta diseñada para la traducción masiva de documentos técnicos y legales. A diferencia de los traductores simples, este motor mantiene la estructura original del archivo, procesa tablas y utiliza ejecución concurrente para reducir los tiempos de espera en documentos extensos.

---

## Características Principales

* **Traducción Estructural:** Convierte archivos PDF a DOCX de forma interna para traducir párrafos y tablas manteniendo el formato original.
* **Motor OCR para Imágenes:** Extrae y traduce texto de archivos visuales (`.png`, `.jpg`, `.jpeg`) línea por línea.
* **Alta Performance:** Implementa `ThreadPoolExecutor` con 8 workers en paralelo, lo que permite traducir documentos largos hasta un 500% más rápido que un proceso secuencial.
* **Resiliencia:** Sistema de reintentos automáticos ante fallas de conexión con la API de traducción.
* **Multilenguaje:** Soporte para detección automática y traducción entre los principales idiomas globales (Español, Inglés, Portugués, Francés, etc.).

---

## Stack Tecnológico

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Conversión PDF/Word:** [pdf2docx](https://dothinking.github.io/pdf2docx/) & [python-docx](https://python-docx.readthedocs.io/)
* **Traducción Engine:** [deep-translator](https://github.com/nidhaloff/deep-translator) (Google Translator API)
* **OCR:** [PyTesseract](https://github.com/madmaze/pytesseract)
* **Optimización:** Python Concurrency (Concurrent Futures)

---

## Instalación y Configuración

1.  **Cloná el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/b2b-document-translator.git](https://github.com/tu-usuario/b2b-document-translator.git)
    cd b2b-document-translator
    ```

2.  **Instalá las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Dependencias Externas (Tesseract OCR):**
    * Este proyecto requiere que el motor **Tesseract** esté instalado en el sistema.
    * **Windows:** Instalar en la ruta por defecto o configurar el path en `app.py`.
    * **Linux:** `sudo apt install tesseract-ocr tesseract-ocr-spa`

4.  **Ejecutá la plataforma:**
    ```bash
    streamlit run app.py
    ```

---

## Flujo de Trabajo

1.  **Carga:** Subí un archivo PDF, DOCX o una imagen técnica.
2.  **Configuración:** Seleccioná el idioma de destino (puedes dejar el origen en "Auto-detectar").
3.  **Traducción:** El sistema dividirá el documento en fragmentos y los procesará en paralelo. Podrás ver el avance en tiempo real con la barra de progreso.
4.  **Descarga:** Para documentos, obtené un archivo `.docx` listo para usar. Para imágenes, obtené una comparativa visual de los textos.

---
*Optimizado para flujos de trabajo B2B y procesamiento eficiente de documentos.*
