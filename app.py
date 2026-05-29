import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Dimension & Measure Detector",
    layout="wide"
)

# Load CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Title
st.title("📊 Auto Dimension & Measure Detector")

# File Upload
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Read File
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

    # Dataset Preview
    st.markdown(
        '<div class="section-title">📄 Dataset Preview</div>',
        unsafe_allow_html=True
    )

    st.dataframe(df.head(), use_container_width=True)

    # Lists
    measures = []
    dimensions = []

    # Auto Detect
    for col in df.columns:

        if (
            pd.api.types.is_numeric_dtype(df[col])
            and "id" not in col.lower()
        ):
            measures.append(col)

        else:
            dimensions.append(col)

    # Display Columns
    col1, col2 = st.columns(2)

    # Measures
    with col1:

        st.markdown(
            '<div class="section-title">📏 Measures</div>',
            unsafe_allow_html=True
        )

        if measures:

            for m in measures:
                st.markdown(
                    f'<div class="measure-card">{m}</div>',
                    unsafe_allow_html=True
                )

        else:
            st.warning("No Measures Found")

    # Dimensions
    with col2:

        st.markdown(
            '<div class="section-title">🧩 Dimensions</div>',
            unsafe_allow_html=True
        )

        if dimensions:

            for d in dimensions:
                st.markdown(
                    f'<div class="dimension-card">{d}</div>',
                    unsafe_allow_html=True
                )

        else:
            st.warning("No Dimensions Found")

    # Data Types
    st.markdown(
        '<div class="section-title">🔍 Column Data Types</div>',
        unsafe_allow_html=True
    )

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": [str(df[col].dtype) for col in df.columns]
    })

    st.dataframe(dtype_df, use_container_width=True)

    # Chart Section
    if measures:

        st.markdown(
            '<div class="section-title">📈 Measure Visualization</div>',
            unsafe_allow_html=True
        )

        selected_measure = st.selectbox(
            "Select Measure",
            measures
        )

        st.bar_chart(df[selected_measure])

else:
    st.info("⬆️ Upload a CSV or Excel file to begin.")
