
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Mepcrete Analytics Dashboard", layout="wide")

# Title
st.title("📊 Mepcrete Data Analytics Dashboard")
st.markdown("Analyze employee salaries, block measurements, and inventory trends with interactive visuals.")

# Load the data
@st.cache_data
def load_data():
    xls = pd.ExcelFile("mepcrete_data_trimmed_200.xlsx")
    df_salary = pd.read_excel(xls, sheet_name="Employee Salary Data")
    df_inventory = pd.read_excel(xls, sheet_name="Inventory Data")
    df_measurements = pd.read_excel(xls, sheet_name="AAC Measurements")
    return df_salary, df_inventory, df_measurements

df_salary, df_inventory, df_measurements = load_data()

# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Employee Salary", "Inventory", "AAC Measurements"])

# Employee Salary Section
if section == "Employee Salary":
    st.subheader("💼 Employee Salary Analysis")
    st.write("Explore employee data across job roles, education levels, and industries.")

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        sns.boxplot(data=df_salary, x="Education Level", y="Current Salary", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        sns.barplot(data=df_salary, x="Job Title", y="Current Salary", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    st.dataframe(df_salary)

# Inventory Section
elif section == "Inventory":
    st.subheader("🏗️ Inventory Trends")
    st.write("Analyze block production, sales, and waste over time.")

    df_inventory['Date'] = pd.to_datetime(df_inventory['Date'])

    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(df_inventory.set_index("Date")[["Blocks Made", "Blocks Sold"]])

    with col2:
        st.bar_chart(df_inventory.set_index("Date")["Waste (kg)"])

    st.dataframe(df_inventory)

# AAC Measurements Section
elif section == "AAC Measurements":
    st.subheader("📐 AAC Block Measurements")
    st.write("Inspect volume distribution and dimensions of AAC blocks.")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Volume (m³)", round(df_measurements["Volume (m3)"].mean(), 4))
        st.metric("Max Volume (m³)", round(df_measurements["Volume (m3)"].max(), 4))

    with col2:
        fig, ax = plt.subplots()
        sns.histplot(df_measurements["Volume (m3)"], bins=20, kde=True, ax=ax)
        st.pyplot(fig)

    st.dataframe(df_measurements)
