import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="SAC Table Layout",
    layout="wide"
)

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown(
    """
    <div class="top-header">
        New_Analytic_Model_3
    </div>
    """,
    unsafe_allow_html=True
)

# Upload
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

    # Detect dimensions & measures
    dimensions = []
    measures = []

    for col in df.columns:

        if (
            pd.api.types.is_numeric_dtype(df[col])
            and "id" not in col.lower()
        ):
            measures.append(col)

        else:
            dimensions.append(col)

    # Arrange order
    ordered_cols = dimensions + measures

    # Create HTML Table
    html = """
    <div class="table-wrapper">

    <table>

    <thead>
    """

    # First Header Row
    html += "<tr>"

    # Empty headers for dimensions
    for d in dimensions:
        html += '<th class="blank-head"></th>'

    # Measures group header
    html += f'''
        <th class="measure-group" colspan="{len(measures)}">
            Measures
        </th>
    '''

    html += "</tr>"

    # Column Names Row
    html += "<tr>"

    for col in ordered_cols:

        if col in measures:
            html += f'<th class="measure-col">{col}</th>'

        else:
            html += f'<th class="dimension-col">{col}</th>'

    html += "</tr></thead>"

    # Body
    html += "<tbody>"

    for _, row in df.iterrows():

        html += "<tr>"

        for col in ordered_cols:
            html += f"<td>{row[col]}</td>"

        html += "</tr>"

    html += "</tbody></table></div>"

    # Render
    st.markdown(html, unsafe_allow_html=True)

else:
    st.info("Upload CSV or Excel File")
