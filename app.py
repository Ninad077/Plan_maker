import streamlit as st
import pandas as pd
from datetime import datetime
import os
import configparser  # For activating the config

# Function to initialize session state
def initialize_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = {}

# Function to save user data
def save_user_data(user_name, user_data):
    st.session_state.data[user_name] = user_data

# Function to generate PM_id
def generate_pm_id(user_data):
    company_id = user_data.get('Company ID', '')
    ordering_channels = user_data.get('Ordering Channels', '')
    fulfilling_location = user_data.get('Fulfilling Location', '')
    application_id = user_data.get('Application ID', '')
    selected_fee_type = user_data.get('Fee Type', '')
    selected_variable_type = user_data.get('Variable', '')
    selected_chargeable_on = user_data.get('Chargeable on', '')
    selected_fee_nature = user_data.get('Fee Nature', '')
    threshold = user_data.get('Threshold option', '')

    # Extract first 2 characters from each field
    pm_id_parts = [
        company_id[:2],
        ordering_channels[:2],
        fulfilling_location[:2],
        application_id[:2],
        selected_fee_type[:2],
        selected_variable_type[:2],
        selected_chargeable_on[:2],
        selected_fee_nature[:2],
        threshold[:2]
    ]

    pm_id = '_'.join(pm_id_parts)  # Join parts with underscore
    return pm_id

# Function to display saved records as a table and save to CSV
def display_saved_records():
    st.write(":violet[Saved Records]")
    df = pd.DataFrame.from_dict(st.session_state.data, orient='index')
    df.reset_index(inplace=True)  # Reset index to convert index (user_name) to a regular column
    df.rename(columns={'index': 'User Name'}, inplace=True)  # Rename the index column to 'User Name'
    
    # Generate PM_id column
    df['PM_id'] = df.apply(generate_pm_id, axis=1)
    
    # Display DataFrame with increased height
    st.write(df.style.set_table_attributes('style="font-size: 14px; line-height: 18px; width: auto; height: auto;"'))

    # Save records to CSV
    if not df.empty:
        folder_path = "data"  # Folder name
        os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist
        file_path = os.path.join(folder_path, "records.csv")

        # Save DataFrame to CSV without index
        df.to_csv(file_path, index=False)

        st.download_button(
            label="Download CSV",
            data=open(file_path, 'rb').read(),
            file_name="records.csv",
            mime="text/csv",
        )

# Function to load theme configuration
def load_theme_config():
    config = configparser.ConfigParser()
    config.read('config.toml')

    # Extract theme settings
    theme_settings = config['theme']
    return theme_settings

# Initialize session state
initialize_session_state()

theme_settings = load_theme_config()


# Apply theme settings to Streamlit
st.set_page_config(
    page_title="Plan maker",
    page_icon="Fynd copy.png",  # Specify your own page icon
    layout="centered",  # "wide" or "centered"
    initial_sidebar_state="auto",  # "auto", "expanded", "collapsed"
)



# Section 1: Plan Info
st.sidebar.image('Fynd_logo2.png', width = 200)
user_name = st.sidebar.text_input("Enter your name:")
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
    fulfilling_location = None
    application_id = None
else:
    abc = ["Store", "Warehouse"]
    fulfilling_location = st.sidebar.selectbox("Fulfilling Location", abc, help="Select the fulfilling location")
    application_id = st.sidebar.text_input("Application ID", key="application_id_input", help="Enter the application ID")

# Section 3: Defining products for each dropdown
product_options = ["B2B", "Marketplaces", "StoreOS", "Website", "ONDC", "OMS", "TMS", "WMS", "GMC", "Catalog Cloud"]
fee_type_options = ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee", "Logistics", "Packaging", "SLA", "Licensing"]
fee_nature_options = ["Fixed %", "Flat currency", "Slab based"]
variable_options = ["Bag", "Order", "Shipment", "Application", "Extension", "Integration", "Store", "User"]
chargeable_on_options = ["Developed", "Installed", "Placed", "Invoiced", "Delivered", "Return window", "All", "Picked", "RTO", "DTO", "Packed"]
plan_validity_options = ["One time", "Monthly", "Quarterly", "Bi-Annually", "Annually"]
payment_method_options = ["Prepaid", "Postpaid"]

# In the first column, display the image
st.image("Fynd copy.png", width=300)

st.title(":violet[Plan maker]")

# Mapping index
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

# Create an empty DataFrame with the desired column names
slabs_df = pd.DataFrame(columns=["Slab", "Max_value", "Commercial_value", "Usage","Capping/Min_Guarantee_value", "Threshold"])

selected_fee_nature = st.selectbox("Fee Nature:", ["Fixed %", "Flat currency", "Slab based"], key="fee_nature_select")

if selected_fee_nature == "Slab based":
    st.write("Enter values for Slab based fee structure:")

    # Input fields for user data
    col1, col2 = st.columns([2, 2])

    with col1:
        slab = st.selectbox("Slab:", [1, 2, 3], key="slab_select")
    with col2:
        max_value = st.text_input("Max value:", key="max_value_input")
    with col1:
        user_input = st.text_input("Commercial Value:", key="user_input")
    with col2:
        Usage = st.text_input("Usage:", key="Usage_input")
    with col1:
        Capping_or_Minimum_Guarantee= st.text_input("Capping/Min_Guarantee:", key="Capping_or_Minimum_Guarantee_input")
    with col2:
        threshold = st.text_input("Threshold:", key="threshold_input")

    # Function to add data to DataFrame
    def add_data(slabs_df, slab, max_value, user_input, Usage, Capping_or_Minimum_Guarantee, threshold):

        max_value = int(max_value) if max_value else None
        user_input = int(user_input) if user_input else None
        Usage = int(Usage) if Usage else None
        Capping_or_Minimum_Guarantee = int(Capping_or_Minimum_Guarantee) if Capping_or_Minimum_Guarantee else None

        new_row = {
            "Slab": slab,
            "Max_value": max_value,
            "Commercial_value": user_input,
            "Usage": Usage,
            "Capping/Min_Guarantee_value": Capping_or_Minimum_Guarantee,
            "Threshold": threshold
        }
        new_row_df = pd.DataFrame([new_row])
        slabs_df = pd.concat([slabs_df, new_row_df], ignore_index=True)
        return slabs_df

    # Button to add data
    if st.button("Add Data", key="add_data_button"):
        slabs_df = add_data(slabs_df, slab, max_value, user_input, Usage, Capping_or_Minimum_Guarantee, threshold)

    # Display the updated DataFrame
    st.write("Updated Slab Data:")
    st.table(slabs_df)

    selected_plan_validity = st.selectbox("Plan Validity", ["--please select--"] + plan_validity_options, help="Select the plan validity")
    selected_payment_method = st.selectbox("Payment Method", ["--please select--"] + payment_method_options, help="Select the payment method")

# Submit button
    if st.button("Submit"):
    # Save user data
        user_data = {
        "Plan Name": plan_name,
        "Plan Description": plan_description,
        "Plan Start Date": plan_start_date,
        "Ordering Channels": ordering_channels,
        "Company ID": company_id,
        "Company Name": company_name,
        "Fulfilling Location": fulfilling_location,
        "Application ID": application_id,
        "Fee Type": selected_fee_type,
        "Variable": selected_variable_type,
        "Chargeable on": selected_chargeable_on,
        "Fee Nature": selected_fee_nature,
        "Commercial value": user_input,
        "Usage limit": Usage,
        "Minimum/Capping value": Capping_or_Minimum_Guarantee,
        "Threshold option": threshold,
        "Plan Validity": selected_plan_validity,
        "Payment Method": selected_payment_method,
        }

    # Generate PM_id and add it to user_data
        pm_id = generate_pm_id(user_data)
        user_data['PM_id'] = pm_id

        save_user_data(user_name, user_data)  # Save user data after submission

        # Display saved records
        display_saved_records()


elif selected_fee_nature in ["Fixed %", "Flat currency"]:
    user_input = st.number_input("Please enter Commercial value:", min_value=0.0, help="Enter a valid number")

    # 6th layer: Expected Billing
    Usage = st.number_input(f"Enter the usage limit for {selected_variable_type}", min_value=0.0, help="Enter the usage limit")
    Capping_or_Minimum_Guarantee = st.number_input(f"Enter the Capping/Minimum Value for {selected_variable_type}", min_value=0.0, help="Enter the Capping/Minimum Gauarntee value")
    Product = Usage * user_input if selected_fee_nature in ["Fixed %", "Flat currency"] else 0

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

    selected_plan_validity = st.selectbox("Plan Validity", ["--please select--"] + plan_validity_options, help="Select the plan validity")
    selected_payment_method = st.selectbox("Payment Method", ["--please select--"] + payment_method_options, help="Select the payment method")

# Submit button
    if st.button("Submit"):
    # Save user data
        user_data = {
        "Plan Name": plan_name,
        "Plan Description": plan_description,
        "Plan Start Date": plan_start_date,
        "Ordering Channels": ordering_channels,
        "Company ID": company_id,
        "Company Name": company_name,
        "Fulfilling Location": fulfilling_location,
        "Application ID": application_id,
        "Fee Type": selected_fee_type,
        "Variable": selected_variable_type,
        "Chargeable on": selected_chargeable_on,
        "Fee Nature": selected_fee_nature,
        "Commercial value": user_input,
        "Usage limit": Usage,
        "Minimum/Capping value": Capping_or_Minimum_Guarantee,
        "Threshold option": threshold,
        "Expected Billing": expected_billing,
        "Plan Validity": selected_plan_validity,
        "Payment Method": selected_payment_method,
        }

    # Generate PM_id and add it to user_data
        pm_id = generate_pm_id(user_data)
        user_data['PM_id'] = pm_id

        save_user_data(user_name, user_data)  # Save user data after submission

        # Display saved records
        display_saved_records()
