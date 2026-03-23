import streamlit as st
import pandas as pd


st.set_page_config(page_title="Construction Dashboard", layout="wide")
st.title("🏗 Construction Dashboard (No Progress Sheet)")


uploaded_file = st.file_uploader(
    "Upload your Construction Excel file",
    type=["xlsx"]
)

if not uploaded_file:
    st.info("Please upload your Excel file to continue.")
    st.stop()


@st.cache_data
def load_data(file):
    try:
        df_project = pd.read_excel(file, sheet_name="Төслийн мэдээлэл")
        df_schedule = pd.read_excel(file, sheet_name="Хугацаа")
        df_costs = pd.read_excel(file, sheet_name="Зардал")
        df_materials = pd.read_excel(file, sheet_name="Материал")
    except Exception as e:
        st.error("Excel sheet structure буруу байна!")
        st.stop()

    return df_project, df_schedule, df_costs, df_materials


df_project, df_schedule, df_costs, df_materials = load_data(uploaded_file)


df_costs['Budget'] = pd.to_numeric(df_costs['Budget'], errors='coerce')
df_costs['Actual'] = pd.to_numeric(df_costs['Actual'], errors='coerce')
df_materials['Qty_Planned'] = pd.to_numeric(df_materials['Qty_Planned'], errors='coerce')
df_materials['Qty_Used'] = pd.to_numeric(df_materials['Qty_Used'], errors='coerce')


budget_total = df_costs['Budget'].sum()
actual_total = df_costs['Actual'].sum()
budget_util = actual_total / budget_total if budget_total != 0 else 0

material_usage = (
    df_materials['Qty_Used'].sum() / df_materials['Qty_Planned'].sum()
    if df_materials['Qty_Planned'].sum() != 0 else 0
)


st.subheader("📊 Key Metrics")

col1, col2 = st.columns(2)
col1.metric("Budget Utilization", f"{budget_util*100:.2f}%")
col2.metric("Material Usage", f"{material_usage*100:.2f}%")



st.subheader("💰 Budget vs Actual")
if 'Cost_Type' in df_costs.columns:
    cost_summary = df_costs.groupby('Cost_Type')[['Budget', 'Actual']].sum()
    st.bar_chart(cost_summary)
else:
    st.warning("Cost_Type column олдсонгүй!")

st.subheader("🧱 Material Usage")
if 'Material_Name' in df_materials.columns:
    df_materials['Usage'] = df_materials['Qty_Used'] / df_materials['Qty_Planned']
    st.bar_chart(df_materials.set_index('Material_Name')['Usage'])
else:
    st.warning("Material_Name column олдсонгүй!")


with st.expander("View Raw Data"):
    st.write("Project Info", df_project)
    st.write("Schedule", df_schedule)
    st.write("Costs", df_costs)
    st.write("Materials", df_materials)