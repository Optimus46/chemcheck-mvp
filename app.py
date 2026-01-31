import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))





import streamlit as st
from ocr.ocr_engine import extract_text
from nlp.nlp_processor import process_ingredients
from ml.toxicity_model import predict_toxicity
from report.report_generator import generate_report
from analysis.safety_analyzer import analyze_safety

st.title("ChemCheck 🧪")
st.write("Analyze product ingredients for safety")

image = st.file_uploader("Upload Product Label Image", type=["jpg", "png"])
text_input = st.text_area("OR Enter Ingredient List")

if st.button("Analyze"):
    if image:
        raw_text = extract_text(image)
    else:
        raw_text = text_input

    ingredients = process_ingredients(raw_text)
    results = analyze_safety(ingredients)
    report = generate_report(results)

    st.subheader("Safety Report")
    st.write(report)

