import streamlit as st
import pandas as pd
from datetime import datetime
import os
from google.cloud import bigquery


# Set Google Cloud credentials environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

# Initialize BigQuery client
client = bigquery.Client()

# Function to initialize session state
def initialize_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = {}

# Function to save user data
def save_user_data(user_name, data):
    st.session_state.data[user_name] = data

# Function to display saved records as a table
def display_saved_records():
    st.title("Saved Records")
    df = pd.DataFrame.from_dict(st.session_state.data, orient='index')
    st.write(df)

    # Save records to BigQuery table
    if not df.empty:
        table_id = 'fynd-db.plan_maker.records'  # This is where the data is stored

        job_config = bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("Company_ID", "STRING"),
                bigquery.SchemaField("Company_Name", "STRING"),
                bigquery.SchemaField("Application_ID", "STRING"),
                bigquery.SchemaField("Fulfilling_Location", "STRING"),
                bigquery.SchemaField("Plan_Name", "STRING"),
                bigquery.SchemaField("Plan_Description", "STRING"),
                bigquery.SchemaField("Plan_Start_Date", "DATE"),
                bigquery.SchemaField("Ordering_Channels", "STRING"),
                bigquery.SchemaField("Fee_Type", "STRING"),
                bigquery.SchemaField("Fee_Nature", "STRING"),
                bigquery.SchemaField("Variable", "STRING"),
                bigquery.SchemaField("Plan_Validity", "STRING"),
                bigquery.SchemaField("Payment_Method", "STRING"),
            ],
            write_disposition="WRITE_APPEND",
        )

        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # Wait for the job to complete

        st.write("Records successfully exported to BigQuery.")

        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name="records.csv",
            mime="text/csv",
        )

# Initialize session state
initialize_session_state()

# User name & email id
user_name = st.sidebar.text_input("Enter your name:")

# Section 1: Plan Info
st.sidebar.title("Section 1: Plan Info")
plan_name = st.sidebar.text_input("Plan Name", help="Enter the name of the plan")
plan_description = st.sidebar.text_area("Plan Description", max_chars=250, help="Describe the plan")
plan_start_date = st.sidebar.date_input("Plan Start Date", value=datetime.now(), help="Select the start date of the plan")
a1 = ["GoFynd", "Uniket", "B2B", "Marketplaces", "StoreOS", "Website", "ONDC", "OMS", "TMS", "WMS", "GMC", "Catalog Cloud"]
ordering_channels = st.sidebar.selectbox("Product lines", ["--please select--"]+a1, help="Select the ordering channels")


# Section 2: Company Info
st.sidebar.title("Section 2: Company Info")
company_id = st.sidebar.text_input("Company ID", help="Enter the company ID")
company_name = st.sidebar.text_input("Company Name", help="Enter the company name")

# Layer 1: Mapping of Ordering channels with Fulfilling location
if "TMS" in ordering_channels or "GMC" in ordering_channels or "Catalog Cloud" in ordering_channels:
    fulfilling_location =  None
    application_id = None
else:
    abc = ["Store", "Warehouse"]
    fulfilling_location = st.sidebar.selectbox("Fulfilling Location", abc, help="Select the fulfilling location")
    application_id = st.sidebar.text_input("Application ID", key="application_id_input", help="Enter the application ID")


# Section 3: Defining products for each dropdown
product_options = ["B2B", "Marketplaces", "StoreOS", "Website", "ONDC", "OMS", "TMS", "WMS", "GMC", "Catalog Cloud"]
fee_type_options = ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee", "Logistics", "Packaging", "SLA", "Licensing"]
fee_nature_options = ["Fixed %", "Flat currency","Slab based"]
variable_options = ["Bag", "Order", "Shipment", "Application", "Extension", "Integration", "Store", "User"]
chargeable_on_options = ["Developed", "Installed", "Placed", "Invoiced", "Delivered", "Return window", "All", "Picked", "RTO", "DTO", "Packed"]
plan_validity_options = ["One time", "Monthly", "Quarterly", "Bi-Annually", "Annually"]
payment_method_options = ["Prepaid", "Postpaid"]


# Create a layout with two columns
col1, col2, col3 = st.columns([1, 3, 2])

# In the first column, display the image
with col1:
    st.image("Fynd copy.png", width=200)

st.title(":violet[Plan maker]")





fee_config = {

    'fee_type_mapping': {

        "ONDC": ["Development","Subscription", "Maintenance", "Transaction", "Minimum Guarantee", "Logistics", "Marketing", "SLA"],
        "GoFynd": ["Transaction","Logistics","Marketing", "Packaging", "SLA"],
        "B2B": ["Development","Subscription","Maintenance", "Transaction", "Minimum Guarantee", "Logistics", "Packaging"],
        "Marketplaces": ["Development","Subscription","Maintenance", "Transaction", "Minimum Guarantee"],
        "StoreOS": ["Development","Subscription","Maintenance", "Licensing", "Transaction", "Minimum Guarantee", "Logistics", "Packaging"],
        "Website": ["Development","Subscription","Maintenance", "Transaction", "Minimum Guarantee", "Logistics"],
        "TMS": ["Development","Subscription","Maintenance", "Licensing", "Logistics"],
        "WMS": ["Development","Subscription","Maintenance", "Licensing", "Transaction", "Minimum Guarantee", "Logistics", "Packaging"],
        "GMC": ["Development","Subscription","Maintenance"],
        "Catalog Cloud": ["Development","Subscription","Maintenance"],
        "Uniket": ["Transaction","Logistics","Marketing","Packaging","SLA"],
        "OMS": ["Development","Subscription","Maintenance", "Transaction", "Minimum Guarantee"]

}
}

var_config = { 

    'variable_type_mapping': {

    "Development": ["Application", "Extension", "Integration"],
    "Subscription": ["Application", "Extension", "Integration"],
    "Maintenance": ["Application", "Extension", "Integration"],
    "Licensing": ["Store", "User"],
    "Transaction": ["Bag", "Order", "Shipment"],
    "Minimum Guarantee": ["Bag", "Order", "Shipment"],
    "SLA": ["Bag", "Order", "Shipment"],
    "Logistics":["Shipment"],
    "Marketing":["Bag","Order"],
    "Packaging":["Shipment"]
}

}

char_config = {

    'chargeable_on_mapping' :{

    "Application": ["Developed", "Installed"],
    "Extension": ["Developed", "Installed"],
    "Integration": ["Developed", "Installed"],
    "Store": ["Added", "Active"],
    "User": ["Added", "Active"],
    "Bag": ["Placed", "Invoiced", "Delivered", "Return window", "Cancel", "RTO", "DTO"],
    "Order": ["Placed", "Invoiced", "Delivered", "Return window", "Cancel", "RTO", "DTO"],
    "Shipment":["Placed", "Invoiced", "Delivered", "Return window", "All", "Picked", "RTO", "DTO","Packed", "Cancel"]
}

}


# 2nd layer: Mapping of Ordering channels with fee types
fee_type_mapping = fee_config['fee_type_mapping']
selected_fee_type = st.selectbox("Fee Type", ["--please select--"] + fee_type_mapping.get(ordering_channels, []), help="Select the type of fee")


# 3rd layer mapping: Mapping of Fee type with variables 
variable_type_mapping = var_config["variable_type_mapping"]
selected_variable_type = st.selectbox("Variable Type", ["--please select--"] + variable_type_mapping.get(selected_fee_type, []), help="Select the type of variable")


# 4th layer mapping: Mapping of Fee type with variables 
chargeable_on_mapping = char_config["chargeable_on_mapping"]
selected_chargeable_on = st.selectbox("Chargeable on", ["--please select--"] + chargeable_on_mapping.get(selected_variable_type, []), help="Select the type of Chargeable")

# 5th layer: Mapping of fee types with variables and chargeable on
selected_fee_nature = st.selectbox("Fee Nature", ["--please select--"]+fee_nature_options, help="Select the fee nature")


if selected_fee_nature in ["Fixed %", "Flat currency"]:
    user_input = st.number_input("Please enter Commerical value:",  min_value=0.0, help="Enter a valid number")
elif selected_fee_nature == "Slab based":
    st.write("Please input values for the 3x3 table:")
    table_data = [[st.number_input(f"Row {i+1}, Column {j+1}", value=0, step=1) for j in range(3)] for i in range(3)]
    df = pd.DataFrame(table_data, columns=["Column 1", "Column 2", "Column 3"])
    st.write(df)    



# 6th layer: Expected Billing

Usage = st.number_input(f"Enter the usage limit for {selected_variable_type}", min_value=0.0, help="Enter the usage limit")
Capping_or_Minimum_Guarantee = st.number_input(f"Enter the Capping/Minimum Value for {selected_variable_type}", min_value = 0.0, help = "Enter the Capping/Minimum Gauarntee value")
Product = Usage*user_input if selected_fee_nature in ["Fixed %", "Flat currency"] else 0

abc = ['Capping value', 'Minimum Guarantee']
threshold = st.selectbox("Choose a threshold option:", ["--please select--"] + abc)

initial_expected_billing = Product

if threshold == 'Capping value':
    expected_billing = Product if Capping_or_Minimum_Guarantee > Product else Capping_or_Minimum_Guarantee
elif threshold == 'Minimum Guarantee':
    expected_billing = Product if Capping_or_Minimum_Guarantee < Product else Capping_or_Minimum_Guarantee
else:
    expected_billing = initial_expected_billing  # Default to initial Product value if no threshold selected

st.write(f"Expected Billing: {expected_billing}")


selected_plan_validity = st.selectbox("Plan Validity", ["--please select--"]+plan_validity_options, help="Select the plan validity")
selected_payment_method = st.selectbox("Payment Method",["--please select--"]+payment_method_options, help="Select the payment method")


# Submit button
if st.button("Submit"):
    # Save user data
    user_data = {
        "Company ID": company_id,
        "Company Name": company_name,
        "Application ID": application_id,
        "Fulfilling Location": fulfilling_location,
        "Plan Name": plan_name,
        "Plan Description": plan_description,
        "Plan Start Date": plan_start_date,
        "Ordering Channels": ordering_channels,
        "Fee Type": selected_fee_type,
        "Fee Nature": selected_fee_nature,
        "Variable": selected_variable_type,
        "Plan Validity": selected_plan_validity,
        "Payment Method": selected_payment_method,
    }
    save_user_data(user_name, user_data)


# Display saved records
display_saved_records()
