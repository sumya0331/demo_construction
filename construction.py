import streamlit as st
import pandas as pd

st.set_page_config(page_title="Construction Dashboard", layout="wide")
st.title("🏗 Construction Dashboard (Excel Upload Demo)")


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
        st.error(f"Excel sheet structure буруу байна! Алдаа: {e}")
        st.stop()


    df_project.columns = df_project.columns.str.strip().str.lower()
    df_schedule.columns = df_schedule.columns.str.strip().str.lower()
    df_costs.columns = df_costs.columns.str.strip().str.lower()
    df_materials.columns = df_materials.columns.str.strip().str.lower()

    return df_project, df_schedule, df_costs, df_materials

df_project, df_schedule, df_costs, df_materials = load_data(uploaded_file)


df_costs['budget'] = pd.to_numeric(df_costs.get('budget', pd.Series([0]*len(df_costs))), errors='coerce')
df_costs['actual'] = pd.to_numeric(df_costs.get('actual', pd.Series([0]*len(df_costs))), errors='coerce')
df_materials['qty_planned'] = pd.to_numeric(df_materials.get('qty_planned', pd.Series([0]*len(df_materials))), errors='coerce')
df_materials['qty_used'] = pd.to_numeric(df_materials.get('qty_used', pd.Series([0]*len(df_materials))), errors='coerce')


budget_total = df_costs['budget'].sum()
actual_total = df_costs['actual'].sum()
budget_util = actual_total / budget_total if budget_total != 0 else 0

material_usage = (
    df_materials['qty_used'].sum() / df_materials['qty_planned'].sum()
    if df_materials['qty_planned'].sum() != 0 else 0
)


st.subheader("📊 Key Metrics")
col1, col2 = st.columns(2)
col1.metric("Budget Utilization", f"{budget_util*100:.2f}%")
col2.metric("Material Usage", f"{material_usage*100:.2f}%")


st.subheader("💰 Budget vs Actual")
if 'cost_type' in df_costs.columns:
    cost_summary = df_costs.groupby('cost_type')[['budget', 'actual']].sum()
    st.bar_chart(cost_summary)
else:
    st.warning("Cost_Type column олдсонгүй!")

st.subheader("🧱 Material Usage")
if 'material_name' in df_materials.columns:
    df_materials['usage'] = df_materials['qty_used'] / df_materials['qty_planned']
    st.bar_chart(df_materials.set_index('material_name')['usage'])
else:
    st.warning("Material_Name column олдсонгүй!")


with st.expander("View Raw Data"):
    st.write("Project Info", df_project)
    st.write("Schedule", df_schedule)
    st.write("Costs", df_costs)
    st.write("Materials", df_materials)