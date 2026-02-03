import streamlit as st
from fpdf import FPDF
import os
 
def gerar_pdf(descricao, observacao, imagem_path=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Relatório de Envio", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"Descrição:\n{descricao}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"Observação:\n{observacao}")
    if imagem_path:
        pdf.ln(10)
        pdf.cell(200, 10, txt="Anexo abaixo:", ln=True)
        pdf.image(imagem_path, x=10, y=None, w=150)
    return pdf.output(dest='S').encode('latin1')  # Retorna bytes
 
st.title("Formulário com Geração de PDF")
 
# Campos
descricao = st.text_area("Descrição")
anexo = st.file_uploader("Anexo (Imagens funcionam melhor no PDF)", type=["png", "jpg", "jpeg"])
observacao = st.text_input("Observação")
 
if st.button("Gerar PDF"):
    if descricao and observacao:
        temp_path = None
        if anexo is not None:
            temp_path = f"temp_{anexo.name}"
            with open(temp_path, "wb") as f:
                f.write(anexo.getbuffer())
        pdf_bytes = gerar_pdf(descricao, observacao, temp_path)
        st.success("PDF gerado com sucesso! Clique no botão abaixo para baixar:")
        st.download_button(
            label="Baixar PDF",
            data=pdf_bytes,
            file_name="formulario_completo.pdf",
            mime="application/pdf"
        )
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
    else:
        st.error("Por favor, preencha a descrição e a observação.")
