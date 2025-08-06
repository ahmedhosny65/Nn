
import import zipfile
import os

# Define project structure
project_name = "Customer_Sales_App"
base_path = f"/mnt/data/{project_name}"
os.makedirs(base_path, exist_ok=True)

# 1. Create app.py
app_py = """
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Sales Dashboard", layout="wide")

st.title("📊 تحليل مبيعات العملاء")

uploaded_file = st.file_uploader("ارفع ملف CSV يحتوي على بيانات المبيعات", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 البيانات الأصلية")
    st.dataframe(df)

    if "Customer" in df.columns and "Sales" in df.columns:
        grouped = df.groupby("Customer")["Sales"].sum().sort_values(ascending=False)
        st.subheader("💰 إجمالي المبيعات لكل عميل")
        st.dataframe(grouped)

        st.subheader("📈 رسم بياني لإجمالي المبيعات حسب العميل")
        fig, ax = plt.subplots()
        grouped.plot(kind="bar", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("⚠️ الملف لا يحتوي على الأعمدة المطلوبة: 'Customer' و 'Sales'")
else:
    st.info("👈 الرجاء رفع ملف CSV لبدء التحليل.")
"""

with open(f"{base_path}/app.py", "w", encoding="utf-8") as f:
    f.write(app_py)

# 2. Create sample CSV data
sample_data = """Customer,Sales
Ahmed,2000
Mohamed,1500
Sara,3000
Ali,1200
Laila,2500
"""

os.makedirs(f"{base_path}/data", exist_ok=True)
with open(f"{base_path}/data/sample_sales.csv", "w", encoding="utf-8") as f:
    f.write(sample_data)

# 3. Create requirements.txt
requirements = """streamlit
pandas
matplotlib
"""

with open(f"{base_path}/requirements.txt", "w") as f:
    f.write(requirements)

# 4. Zip the project
zip_path = f"/mnt/data/{project_name}.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, base_path)
            zipf.write(file_path, arcname)
            if product and amount > 0:
                new_id = f"S{len(st.session_state.sales) + 1:03}"
                new_sale = pd.DataFrame([[new_id, customer_id, date, product, amount]], columns=st.session_state.sales.columns)
                st.session_state.sales = pd.concat([st.session_state.sales, new_sale], ignore_index=True)
                st.success("Sale added successfully!")

    st.subheader("🧾 Sales List")
    st.dataframe(st.session_state.sales)

# Dashboard Page
elif page == "Dashboard":
    st.header("📊 Dashboard")

    if len(st.session_state.sales) == 0:
        st.info("No sales data to show.")
    else:
        st.subheader("🔝 Top Customers by Total Sales")
        merged = st.session_state.sales.merge(st.session_state.customers, on="Customer ID")
        top_customers = merged.groupby("Name")["Amount"].sum().sort_values(ascending=False).reset_index()
        st.bar_chart(top_customers.set_index("Name"))

        st.subheader("📅 Daily Sales")
        daily_sales = st.session_state.sales.groupby("Date")["Amount"].sum().reset_index()
        st.line_chart(daily_sales.set_index("Date"))

        st.subheader("⬇️ Download Reports")
        export_df = merged[["Date", "Name", "Product", "Amount", "City"]]
        towrite = io.BytesIO()
        export_df.to_excel(towrite, index=False, sheet_name="Sales_Report")
        st.download_button("Download Excel", data=towrite.getvalue(), file_name="sales_report.xlsx", mime="application/vnd.ms-excel")
