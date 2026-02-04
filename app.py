import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from ocr.ocr_engine import extract_text
from nlp.nlp_processor import process_ingredients
from report.report_generator import generate_report
from analysis.safety_analyzer import analyze_safety

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="ChemCheck",
    page_icon="🧪",
    layout="centered"
)

# -----------------------------
# Header
# -----------------------------
st.title("ChemCheck 🧪")
st.markdown(
    "Analyze **cosmetic and product ingredients** for potential safety risks.\n"
    "Upload a label image *or* paste an ingredient list to get a simple safety report."
)

st.markdown("---")

# -----------------------------
# Input section
# -----------------------------
st.header("1. Provide Product Information")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Option A: Upload Label Image")
    image = st.file_uploader(
        "Upload Product Label Image",
        type=["jpg", "jpeg", "png"],
        help="Clear, readable photos work best for text extraction."
    )

with col2:
    st.subheader("Option B: Paste Ingredient List")
    text_input = st.text_area(
        "Enter ingredients separated by commas",
        placeholder="e.g. Aqua, Glycerin, Methylparaben, Fragrance",
        height=150
    )

st.caption("You can use either option. If both are provided, the **image** will be used.")

# -----------------------------
# Analyze button + basic validation
# -----------------------------
st.markdown("---")
st.header("2. Run Safety Analysis")

analyze_clicked = st.button("Analyze Ingredients")

if analyze_clicked:
    if not image and not text_input.strip():
        st.warning("Please upload an image **or** enter an ingredient list before analyzing.")
    else:
        with st.spinner("Analyzing ingredients. This may take a few seconds..."):
            # Step 1: Get raw text
            if image:
                raw_text = extract_text(image)
            else:
                raw_text = text_input

            # Step 2: NLP processing
            ingredients = process_ingredients(raw_text)

            if not ingredients:
                st.error("No valid ingredients were detected. Please check the input and try again.")
            else:
                # Step 3: Safety analysis + report generation
                results = analyze_safety(ingredients)
                report = generate_report(results)

                # -----------------------------
                # Output section
                # -----------------------------
                st.markdown("---")
                st.header("3. Safety Report")

                st.markdown("Below is a simplified safety summary based on the detected ingredients:")
                st.text(report)

                # Optional: show detected ingredient list for transparency
                with st.expander("Show detected ingredients"):
                    st.write(ingredients)

