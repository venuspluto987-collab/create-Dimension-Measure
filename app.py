import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Auto Dimension & Measure Detection")

st.title("📊 CSV / Excel Dimension & Measure Detector")

# Folder path
DATA_FOLDER = "data"

# Get all csv/xlsx files
files = [
    f for f in os.listdir(DATA_FOLDER)
    if f.endswith(".csv") or f.endswith(".xlsx")
]

if not files:
    st.warning("No CSV or Excel files found in data folder.")
    st.stop()

# Select file
selected_file = st.selectbox("Select Dataset", files)

file_path = os.path.join(DATA_FOLDER, selected_file)

# Read file
if selected_file.endswith(".csv"):
    df = pd.read_csv(file_path)
else:
    df = pd.read_excel(file_path)

st.subheader("Dataset Preview")
st.dataframe(df.head())

# Detect Measures & Dimensions
measures = []
dimensions = []

for column in df.columns:

    # Numeric columns -> Measures
    if pd.api.types.is_numeric_dtype(df[column]):
        measures.append(column)

    # Everything else -> Dimensions
    else:
        dimensions.append(column)

# Display Results
col1, col2 = st.columns(2)

with col1:
    st.subheader("📏 Measures")
    for m in measures:
        st.success(m)

with col2:
    st.subheader("🧩 Dimensions")
    for d in dimensions:
        st.info(d)

# Extra Info
st.subheader("Column Data Types")

dtype_df = pd.DataFrame({
    "Column": df.columns,
    "Data Type": [str(df[col].dtype) for col in df.columns]
})

st.table(dtype_df)
