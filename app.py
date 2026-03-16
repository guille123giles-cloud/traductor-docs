import streamlit as st
import tempfile
import os
import time
from PIL import Image
from deep_translator import GoogleTranslator
import datetime

# --- NUEVA LIBRERÍA DE GOOGLE ---
from google import genai

# Librerías de Azure
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.document import DocumentTranslationClient, DocumentTranslationInput, TranslationTarget
from azure.storage.blob import BlobServiceClient, generate_container_sas, ContainerSasPermissions

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Traductor de documentos", page_icon="🌍", layout="wide")

def traducir_bloque(texto, origen, destino):
    """Traduce un bloque de texto entero. Súper rápido y con reintentos."""
    if not texto.strip() or len(texto.strip()) < 2: 
        return texto
    for intento in range(3):
        try:
            return GoogleTranslator(source=origen, target=destino).translate(texto)
        except Exception:
            time.sleep(1.5)
    return texto 

def procesar_documento(archivo_subido, origen, destino, barra, estado):
    """Procesa y traduce archivos PDF y DOCX en la nube conservando 100% el layout original."""
    try:
        endpoint = st.secrets["TRANSLATOR_ENDPOINT"]
        key = st.secrets["TRANSLATOR_KEY"]
        conn_str = st.secrets["STORAGE_CONNECTION_STRING"]
        
        nombre_archivo = archivo_subido.name
        
        estado.info("⚙️ Paso 1/4: Conectando con Azure y subiendo documento seguro...")
        barra.progress(25)
        
        # Conectar al Storage y subir a 'origen'
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        account_name = blob_service_client.account_name
        account_key = blob_service_client.credential.account_key
        
        blob_client_origen = blob_service_client.get_blob_client(container="origen", blob=nombre_archivo)
        blob_client_origen.upload_blob(archivo_subido.getvalue(), overwrite=True)
        
        estado.info("🔐 Paso 2/4: Generando permisos temporales de lectura y escritura...")
        barra.progress(50)
        
        ahora = datetime.datetime.now(datetime.timezone.utc)
        inicio = ahora - datetime.timedelta(minutes=15)
        fin = ahora + datetime.timedelta(hours=1)
        
        sas_origen = generate_container_sas(
            account_name=account_name,
            container_name="origen",
            account_key=account_key,
            permission=ContainerSasPermissions(read=True, list=True),
            start=inicio,
            expiry=fin
        )
        url_origen = f"https://{account_name}.blob.core.windows.net/origen?{sas_origen}"
        
        sas_destino = generate_container_sas(
            account_name=account_name,
            container_name="destino",
            account_key=account_key,
            permission=ContainerSasPermissions(read=True, write=True, list=True),
            start=inicio,
            expiry=fin
        )
        url_destino = f"https://{account_name}.blob.core.windows.net/destino?{sas_destino}"
        
        estado.info("🚀 Paso 3/4: Azure está renderizando y traduciendo tu documento (puede demorar)...")
        barra.progress(75)
        
        # Enviar a Azure Document Translation
        client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))
        inputs = [
            DocumentTranslationInput(
                source_url=url_origen,
                targets=[TranslationTarget(target_url=url_destino, language=destino)]
            )
        ]
        
        poller = client.begin_translation(inputs)
        poller.result() # Espera a que termine el proceso asíncrono
        
        estado.info("💾 Paso 4/4: Descargando el documento final maquetado...")
        barra.progress(90)
        
        # Descargar el archivo traducido
        blob_client_destino = blob_service_client.get_blob_client(container="destino", blob=nombre_archivo)
        datos_traducidos = blob_client_destino.download_blob().readall()
        
        # Limpieza en la nube (Privacidad)
        blob_client_origen.delete_blob()
        try:
            blob_client_destino.delete_blob()
        except:
            pass 
            
        estado.success("✅ ¡Traducción profesional completada con éxito!")
        barra.progress(100)
        return datos_traducidos

    except Exception as e:
        estado.error(f"❌ Ocurrió un error con la API de Azure: {e}")
        return None

def procesar_imagen(imagen_subida, origen, destino, barra, estado):
    """Extrae texto de una imagen usando Google Gemini y lo traduce en bloque."""
    estado.info("⚙️ Paso 1/2: Leyendo la imagen con Inteligencia Artificial...")
    img = Image.open(imagen_subida)
    
    try:
        # Usar el nuevo cliente de Google GenAI
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        prompt_ocr = "Extrae todo el texto de esta imagen con precisión absoluta. Respeta los saltos de línea y el orden de los mensajes. No agregues introducciones, ni comentarios, solo devuelve el texto exacto que ves."
        
        respuesta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt_ocr, img]
        )
        
        texto_extraido = respuesta.text
        
    except Exception as e:
        return None, f"⚠️ Error al leer la imagen con Gemini: {e}"
    
    if not texto_extraido or not texto_extraido.strip():
        return None, "⚠️ No se detectó texto legible en la captura."

    estado.info("🚀 Paso 2/2: Traduciendo texto de forma optimizada...")
    barra.progress(50)
    
    # TRADUCCIÓN EN UN SOLO VIAJE (Muchísimo más rápido)
    texto_final = traducir_bloque(texto_extraido, origen, destino)
            
    barra.progress(100)
    estado.success("✅ ¡Lectura y traducción de imagen completada al instante!")
    return texto_extraido, texto_final


# --- INTERFAZ PARA EL CLIENTE ---
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

# --- PROCESAMIENTO ---
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
            
            # --- RUTA 1: DOCUMENTOS (PDF / DOCX) ---
            if extension in [".pdf", ".docx"]:
                resultado = procesar_documento(archivo, idioma_ori, idioma_des, barra, estado)
                
                if resultado:
                    tipo_mime = "application/pdf" if extension == ".pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    
                    st.download_button(
                        label=f"⬇️ DESCARGAR DOCUMENTO TRADUCIDO ({extension.upper()})", 
                        data=resultado, 
                        file_name=f"TRADUCIDO_{nombre_base}{extension}",
                        mime=tipo_mime,
                        use_container_width=True
                    )
            
            # --- RUTA 2: IMÁGENES (PNG / JPG / JPEG) ---
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
                    if texto_traducido:
                        estado.error(texto_traducido)
