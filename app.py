import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="SAC Style Table",
    layout="wide"
)

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title
st.title("New_Analytic_Model")

# Upload File
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

    # Auto Detect
    measures = []
    dimensions = []

    for col in df.columns:

        if (
            pd.api.types.is_numeric_dtype(df[col])
            and "id" not in col.lower()
        ):
            measures.append(col)

        else:
            dimensions.append(col)

    # SAC Layout Header
    st.markdown(
        f"""
        <div class="measure-header">
            <div class="left-space"></div>
            <div class="measure-title">
                Measures
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Arrange Columns
    ordered_columns = dimensions + measures

    # Display Table
    st.dataframe(
        df[ordered_columns],
        use_container_width=True,
        height=500
    )

    # Bottom Info
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Dimensions")
        st.write(dimensions)

    with col2:
        st.subheader("Measures")
        st.write(measures)

else:
    st.info("Upload CSV or Excel File")
