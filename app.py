import streamlit as st
from jinja2 import Environment, FileSystemLoader
import os

# ✅ Configuración de la página (va aquí)
st.set_page_config(page_title="Informe Técnico ASEI", layout="centered")

# 🧾 Título visual dentro de la app
st.title("📋 Generador de Informes Técnicos - ASEI")

# Datos del informe
st.header("🛠️ Datos generales")
proyecto = st.text_input("Nombre del proyecto")
cliente = st.text_input("Cliente")
fecha = st.date_input("Fecha de inspección")
inspector = st.text_input("Inspector")

# Datos por junta
st.header("📌 Información de la inspección")
tipo_ensayo = st.selectbox("Tipo de inspección", ["Visual", "Líquidos penetrantes", "Partículas magnéticas"])
junta = st.text_input("Número de junta")
resultado = st.radio("Resultado", ["OK", "NO OK"])
observaciones = st.text_area("Observaciones", height=100)

# Botón para generar vista previa
if st.button("🔍 Generar vista previa del informe"):
    # Cargar plantilla HTML
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("informe_impresion.html")

    datos_visual = [{
        "junta": junta,
        "resultado": resultado,
        "observaciones": observaciones
    }]

    html = template.render(
        proyecto=proyecto,
        cliente=cliente,
        fecha=fecha.strftime("%d/%m/%Y"),
        inspector=inspector,
        datos_visual=datos_visual,
        datos_particulas=[],
        datos_liquidos=[],
        anexos=[]
    )

    # Mostrar vista previa en la app
    st.markdown("---")
    st.subheader("Vista previa del informe generado:")
    st.components.v1.html(html, height=400, scrolling=True)

    # Guardar el HTML como archivo temporal
    output_path = os.path.join("output", f"informe_{junta}_{tipo_ensayo}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Convertir HTML a PDF
    #try:
     #   from weasyprint import HTML
      #  pdf_path = os.path.join("output", f"informe_{junta}_{tipo_ensayo}.pdf")
       # HTML(output_path).write_pdf(pdf_path)
        #st.success("✅ PDF generado con éxito.")
        #with open(pdf_path, "rb") as f:
         #   st.download_button("📥 Descargar PDF", f, file_name=os.path.basename(pdf_path))
    #except Exception as e:
     #   st.error(f"❌ Error al generar PDF: {e}")

st.components.v1.html(html, height=800, scrolling=True)
st.info("🖨️ Usa Ctrl + P o 'Imprimir' para guardar este informe como PDF.")
