
import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Session state for storing data
if 'customers' not in st.session_state:
    st.session_state.customers = pd.DataFrame(columns=['Customer ID', 'Name', 'Phone', 'City'])
if 'sales' not in st.session_state:
    st.session_state.sales = pd.DataFrame(columns=['Sale ID', 'Customer ID', 'Date', 'Product', 'Amount'])

st.title("💼 Customer & Sales Management")

# Sidebar for navigation
page = st.sidebar.radio("Go to", ["Add Customer", "Add Sale", "Dashboard"])

# Add Customer Page
if page == "Add Customer":
    st.header("➕ Add New Customer")
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    city = st.text_input("City")

    if st.button("Add Customer"):
        if name and phone and city:
            new_id = f"C{len(st.session_state.customers) + 1:03}"
            new_customer = pd.DataFrame([[new_id, name, phone, city]], columns=st.session_state.customers.columns)
            st.session_state.customers = pd.concat([st.session_state.customers, new_customer], ignore_index=True)
            st.success("Customer added successfully!")

    st.subheader("📋 Customer List")
    st.dataframe(st.session_state.customers)

# Add Sale Page
elif page == "Add Sale":
    st.header("🛒 Add New Sale")
    if len(st.session_state.customers) == 0:
        st.warning("Please add customers first.")
    else:
        customer_id = st.selectbox("Select Customer", st.session_state.customers["Customer ID"])
        product = st.text_input("Product")
        amount = st.number_input("Amount", min_value=0)
        date = st.date_input("Date", value=datetime.today())

        if st.button("Add Sale"):
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
