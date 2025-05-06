import streamlit as st
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="Transportauftrag Extraktor", layout="centered")
st.title("Transportauftrag-Parser")

uploaded_file = st.file_uploader("PDF-Datei mit Transportauftrag hochladen", type="pdf")

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_fields(text):
    fields = {
        "Load latest": re.search(r"\d{1,2}-\d{1,2}-\d{4} \d{2}:\d{2}", text),
        "Loading place": re.search(r"Legmeerdijk.*?Aalsmeer", text),
        "Flightnumber / Shipment details": re.search(r"(43cc.*?)\n", text),
        "Specials": "Standaard koeler, keine ADR, HACCP-konform, Temperatur-Datalogger, Palettentausch",
        "Routing": "Aalsmeer → Geldern → Stutensee-Blankenloch",
        "Unloading latest": re.search(r"8-5-2025 00:00-03:59", text),
        "Unloading place": re.search(r"Linkenheimer Strasse.*?Stutensee-Blankenloch", text)
    }

    results = {}
    for key, match in fields.items():
        if match:
            results[key] = match.group(0).replace("\n", " ").strip()
        else:
            results[key] = "Nicht gefunden"
    return results

if uploaded_file:
    raw_text = extract_text_from_pdf(uploaded_file)
    data = extract_fields(raw_text)

    st.subheader("Ausgewertete Daten:")
    for key, value in data.items():
        st.write(f"**{key}:** {value}")
