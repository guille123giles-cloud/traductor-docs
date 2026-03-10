import streamlit as st
import docx
from pdf2docx import Converter
from deep_translator import GoogleTranslator
import tempfile
import os
import concurrent.futures
import time
import pytesseract
from PIL import Image

st.set_page_config(page_title="Traductor de documentos", page_icon="🌍", layout="wide")

def traducir_bloque(texto, origen, destino):
    """Traduce un bloque de texto con reintentos automáticos en caso de fallas de conexión."""
    if not texto.strip() or len(texto.strip()) < 2: 
        return texto
    for intento in range(3):
        try:
            return GoogleTranslator(source=origen, target=destino).translate(texto)
        except Exception:
            time.sleep(1.5)
    return texto 

def procesar_documento(archivo_subido, origen, destino, barra, estado):
    """Procesa y traduce archivos PDF y DOCX manteniendo la estructura básica."""
    extension = os.path.splitext(archivo_subido.name)[1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
        tmp_file.write(archivo_subido.getvalue())
        ruta_original = tmp_file.name
        
    ruta_docx_out = ruta_original.replace(extension, "_traducido.docx")

    try:
        if extension == ".pdf":
            estado.info("⚙️ Paso 1/3: Convirtiendo PDF a Word y extrayendo estructura...")
            ruta_docx = ruta_original.replace(".pdf", ".docx")
            cv = Converter(ruta_original)
            cv.convert(ruta_docx, start=0, end=None)
            cv.close()
        elif extension == ".docx":
            estado.info("⚙️ Paso 1/3: Analizando la estructura del documento Word...")
            ruta_docx = ruta_original 
        else:
            return None

        doc = docx.Document(ruta_docx)
        
        textos_a_traducir = []
        for parrafo in doc.paragraphs:
            if parrafo.text.strip(): textos_a_traducir.append(parrafo)
            
        for tabla in doc.tables:
            for fila in tabla.rows:
                for celda in fila.cells:
                    for parrafo in celda.paragraphs:
                        if parrafo.text.strip(): textos_a_traducir.append(parrafo)

        total = len(textos_a_traducir)
        if total == 0:
            estado.warning("⚠️ No se encontró texto legible en el documento.")
            return None

        estado.info(f"🚀 Paso 2/3: Traduciendo {total} fragmentos de texto...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futuros = [executor.submit(traducir_bloque, p.text, origen, destino) for p in textos_a_traducir]
            for i, futuro in enumerate(futuros):
                textos_a_traducir[i].text = futuro.result()
                barra.progress((i + 1) / total)

        estado.info("💾 Paso 3/3: Ensamblando el documento final traducido...")
        doc.save(ruta_docx_out)
        
        with open(ruta_docx_out, "rb") as f:
            datos = f.read()
            
        estado.success("✅ ¡Traducción de documento completada!")
        return datos

    except Exception as e:
        estado.error(f"❌ Ocurrió un error al procesar el documento: {e}")
        return None
    finally:
        archivos_a_borrar = set()
        if 'ruta_original' in locals(): archivos_a_borrar.add(ruta_original)
        if 'ruta_docx' in locals() and ruta_docx != ruta_original: archivos_a_borrar.add(ruta_docx)
        if 'ruta_docx_out' in locals(): archivos_a_borrar.add(ruta_docx_out)
        for f in archivos_a_borrar:
            if os.path.exists(f): os.remove(f)

def procesar_imagen(imagen_subida, origen, destino, barra, estado):
    """Extrae texto de una imagen con OCR y lo traduce línea por línea."""
    estado.info("⚙️ Paso 1/2: Leyendo el texto de la imagen...")
    img = Image.open(imagen_subida)
    
    texto_extraido = pytesseract.image_to_string(img)
    
    if not texto_extraido.strip():
        return None, "⚠️ No se detectó texto legible en la imagen."
        
    lineas = texto_extraido.split('\n')
    lineas_validas = [l for l in lineas if l.strip()]
    total = len(lineas_validas)
    
    if total == 0:
        return None, "⚠️ No se detectó texto legible en la imagen."

    estado.info(f"🚀 Paso 2/2: Traduciendo {total} líneas de texto...")
    lineas_traducidas = []
    procesadas = 0
    
    for linea in lineas:
        if linea.strip():
            lineas_traducidas.append(traducir_bloque(linea, origen, destino))
            procesadas += 1
            barra.progress(procesadas / total)
        else:
            lineas_traducidas.append("") 
            
    texto_final = "\n".join(lineas_traducidas)
    estado.success("✅ ¡Lectura y traducción de imagen completada!")
    return texto_extraido, texto_final


st.title("🌍 Traductor de Documentos e Imágenes")
st.divider()

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("1. Subir Archivo")
    archivo = st.file_uploader("Soporta: PDF, DOCX, PNG, JPG, JPEG", type=["pdf", "docx", "png", "jpg", "jpeg"])

with col2:
    st.subheader("2. Opciones de Idioma")
    with st.container(border=True):
        idiomas = {"Auto-detectar": "auto", "Español": "es", "Inglés": "en", "Portugués": "pt", "Francés": "fr", "Italiano": "it", "Alemán": "de"}
        ori_nombre = st.selectbox("Idioma de origen:", list(idiomas.keys()))
        des_nombre = st.selectbox("Traducir al:", [k for k in idiomas.keys() if k != "Auto-detectar"], index=0)
        
        idioma_ori = idiomas[ori_nombre]
        idioma_des = idiomas[des_nombre]

st.divider()

_, col_btn, _ = st.columns([1, 2, 1])

with col_btn:
    if archivo:
        if archivo.size > 5 * 1024 * 1024:
            st.warning("⚠️ El archivo supera los 5MB. El proceso puede demorar más de lo habitual.")
            
        if st.button("🚀 COMENZAR TRADUCCIÓN", use_container_width=True):
            estado = st.empty()
            barra = st.progress(0)
            
            extension = os.path.splitext(archivo.name)[1].lower()
            nombre_base = os.path.splitext(archivo.name)[0]
            
            if extension in [".pdf", ".docx"]:
                resultado = procesar_documento(archivo, idioma_ori, idioma_des, barra, estado)
                
                if resultado:
                    st.download_button(
                        label="⬇️ DESCARGAR DOCUMENTO TRADUCIDO (.DOCX)", 
                        data=resultado, 
                        file_name=f"TRADUCIDO_{nombre_base}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
            
            elif extension in [".png", ".jpg", ".jpeg"]:
                texto_original, texto_traducido = procesar_imagen(archivo, idioma_ori, idioma_des, barra, estado)
                
                if texto_original:
                    st.markdown("### 📝 Resultados")
                    col_res1, col_res2 = st.columns(2)
                    with col_res1:
                        st.text_area("Texto Original", value=texto_original, height=350)
                    with col_res2:
                        st.text_area(f"Traducción al {des_nombre}", value=texto_traducido, height=350)
                else:
                    estado.error(texto_traducido)

