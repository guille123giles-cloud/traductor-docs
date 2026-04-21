# 🌍 Traductor de Documentos e Imágenes

Aplicación web serverless construida con **Streamlit** que traduce documentos PDF, archivos Word e imágenes usando APIs gratuitas — sin servicios cloud de pago.

Originalmente construida con Azure Document Translation. Migrada completamente a un **stack 100% gratuito** usando Google Translate (via `deep-translator`), Google Gemini (para OCR), `pdfplumber`, `reportlab` y `python-docx`.

🔗 **Demo en vivo:** _https://traductor-docs-4gjrvwwnrazsdbj5y4fu37.streamlit.app/._

---

## ✨ Funcionalidades

- **Traducción de PDF** — Extrae texto de forma inteligente (reconstruye líneas cortadas por el layout del PDF), traduce y genera un nuevo PDF limpio descargable
- **Traducción de DOCX** — Lee documentos Word preservando los estilos de párrafo, traduce todo el texto y las tablas, devuelve un `.docx` listo para descargar
- **OCR + traducción de imágenes** — Usa Google Gemini 2.5 Flash para extraer texto de imágenes (PNG, JPG, JPEG) y lo traduce al instante
- **7 idiomas soportados** — Español, Inglés, Portugués, Francés, Italiano, Alemán (+ auto-detección)
- **Reintentos automáticos** — Lógica de retry ante fallos de traducción
- **Privacidad** — Ningún archivo se almacena; todo se procesa en memoria

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Frontend | Streamlit |
| Extracción de PDF | pdfplumber |
| Generación de PDF | ReportLab |
| Procesamiento DOCX | python-docx |
| Traducción | deep-translator (Google Translate, gratuito) |
| OCR de imágenes | Google Gemini 2.5 Flash API |
| Manejo de imágenes | Pillow |
| Deploy | Streamlit Cloud |

---

## 📁 Estructura del Proyecto

```
📦 traductor-documentos
├── app.py                  # App principal de Streamlit
├── requirements.txt        # Dependencias de Python
├── .streamlit/
│   ├── config.toml         # Configuración del tema visual
│   └── secrets.toml        # Claves API (NO se sube a git)
├── .gitignore
└── README.md
```

---

## 🚀 Correr en Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar los secrets

Crear el archivo `.streamlit/secrets.toml` con tu clave de API:

```toml
GEMINI_API_KEY = "tu_clave_de_gemini_acá"
```

> Podés obtener una clave gratuita de Gemini en [aistudio.google.com](https://aistudio.google.com)

### 4. Ejecutar la app
```bash
streamlit run app.py
```

---

## ☁️ Deploy en Streamlit Cloud

1. Subí este repositorio a GitHub
2. Entrá a [share.streamlit.io](https://share.streamlit.io) y conectá tu repo
3. En **Settings → Secrets**, agregá tu `GEMINI_API_KEY`
4. Desplegá — Streamlit Cloud instala las dependencias automáticamente desde `requirements.txt`

---

## ⚙️ Cómo Funciona

### Traducción de PDF
1. `pdfplumber` extrae las palabras agrupadas por su posición Y real (líneas reales del documento)
2. Las líneas cortadas por el margen derecho del PDF (x1 > 82% del ancho de página) se unen automáticamente con la siguiente — reconstruyendo oraciones completas
3. Los códigos `(cid:NNN)` (caracteres de fuentes no estándar, como bullets) se reemplazan por sus equivalentes Unicode (`•`)
4. El texto se traduce por página completa via Google Translate
5. `ReportLab` genera un PDF de salida limpio y bien formateado

### Traducción de DOCX
1. `python-docx` abre el documento y lee cada párrafo y celda de tabla
2. El texto se traduce preservando los estilos del run original (negrita, cursiva, fuente)
3. El documento traducido se guarda en un buffer y se devuelve para descarga

### OCR + Traducción de Imágenes
1. Google Gemini 2.5 Flash recibe la imagen y un prompt estricto de extracción
2. El modelo devuelve el texto respetando saltos de línea y orden de los mensajes
3. El texto extraído se traduce en una sola llamada para mayor velocidad

---

## 📄 Licencia

MIT License — libre para usar, modificar y distribuir.
