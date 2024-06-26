import streamlit as st
import pandas as pd
from datetime import datetime
import os
import configparser  # For activating the config
from PIL import Image, ImageFilter 
import io

global_user_data = []  # For appending user_data


# Function to initialize session state
def initialize_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = []
    if 'alphabet_counter' not in st.session_state:
        st.session_state.alphabet_counter = 0
    if 'serial_counter' not in st.session_state:
        st.session_state.serial_counter = -1


# Function to save user data
def save_user_data(user_data):
    st.session_state.data.append(user_data)


# Function to save Slab data
def save_slab_data(new_row):
    st.session_state.data.append(new_row)


# Function to generate PM_id
def generate_rule_id(user_data):
    company_id = user_data.get('Company ID', '')
    ordering_channels = user_data.get('Ordering Channels', '')
    fulfilling_location = user_data.get('Fulfilling Location', '')
    application_id = user_data.get('Application ID', '')
    selected_fee_type = str(user_data.get('Fee type', ''))
    selected_variable_type = user_data.get('Variable', '')
    selected_chargeable_on = user_data.get('Chargeable on', '')
    selected_fee_nature = user_data.get('Fee Nature', '')
    threshold = user_data.get('Threshold option', '')

  # Ensure all fields are strings
    company_id = str(company_id) if company_id is not None else ''
    ordering_channels = str(ordering_channels) if ordering_channels is not None else ''
    fulfilling_location = str(fulfilling_location) if fulfilling_location is not None else ''
    application_id = str(application_id) if application_id is not None else ''
    selected_variable_type = str(selected_variable_type) if selected_variable_type is not None else ''
    selected_chargeable_on = str(selected_chargeable_on) if selected_chargeable_on is not None else ''
    selected_fee_nature = str(selected_fee_nature) if selected_fee_nature is not None else ''
    threshold = str(threshold) if threshold is not None else ''


    company_id = company_id.zfill(5)[:5]

    # Extract first 2 characters from each field
    rule_id_parts = [
        company_id[:5],
        ordering_channels[:2],
        fulfilling_location[:2],
        application_id[:2],
        selected_fee_type[:2],
        selected_variable_type[:2],
        selected_chargeable_on[:2],
        selected_fee_nature[:2],
        threshold[:2]
    ]

    rule_id = '_'.join(rule_id_parts)  # Join parts with underscore
    return rule_id


# Function to generate Plan ID
def generate_plan_id(user_data):
    initialize_session_state()  # Ensure session state is initialized

    alphabet_counter = st.session_state.alphabet_counter
    serial_counter = st.session_state.serial_counter

    company_id = user_data.get('Company ID', '')  # Get company_id from user_data

    # Increment serial counter and reset if it reaches 999999
    serial_counter += 1
    if serial_counter > 999999:
        serial_counter = 0
        alphabet_counter += 1

    # Save updated counters back to session state
    st.session_state['alphabet_counter'] = alphabet_counter
    st.session_state['serial_counter'] = serial_counter

    # Calculate alphabet ('a' to 'z')
    current_alphabet = chr(alphabet_counter % 26 + ord('a'))

    # Format serial counter as six-digit number
    serial_number = str(serial_counter).zfill(6)

    # Get the first 5 characters of company_id and pad it with zeros
    company_id_part = company_id[:5].zfill(5)

    # Generate the plan_id
    plan_id = f"{company_id_part}_{current_alphabet}_{serial_number}"

    return plan_id


# Function to display saved records as a table and save to CSV
def display_saved_records():
    st.subheader(":violet[Saved Records]")
    df = pd.DataFrame(st.session_state.data)

    if not df.empty:
        # Apply generate_rule_id function to each row to generate rule_id
        df['rule_id'] = df.apply(lambda row: generate_rule_id(row), axis=1)

        # Display DataFrame with increased height
        st.write(df.style.set_table_attributes('style="font-size: 14px; line-height: 18px; width: auto; height: auto;"'))

        # Save records to CSV
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


# Background image 

def set_bg_hack_url(image_url, width='100%', height='100vh'):
    '''
    A function to set a background image from a URL with custom dimensions and shift it to the right.
    Parameters
    ----------
    image_url : str
        The URL of the image.
    width : str, optional
        Width of the background image. Defaults to '30%'.
    height : str, optional
        Height of the background image. Defaults to '20vh' (20% of viewport height).
    '''
    st.markdown(
         f"""
         <style>
         :root {{
             --bg-width: {width};
             --bg-height: {height};
         }}
         .stApp {{
             background: url("{image_url}");
             background-size: cover;
             background-position: center; /* Shifts the image to the right */
             width: var(--bg-width);
             height: var(--bg-height);
             position: fixed;
             top: 0;
             left: 0;
             z-index: -1;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# Example usage with a demo URL and custom dimensions
demo_image_url = "https://cdn.pixelbin.io/v2/falling-surf-7c8bb8/fyprod/wrkr/platform/pictures/free-logo/original/oanADZQ9B-platform-meta-image.jpeg"
set_bg_hack_url(demo_image_url, width='100%', height='100vh')





# Section 1: Plan Info
st.sidebar.image('Fynd_logo2.png', width=300)
st.sidebar.title(":blue[Plan maker]")
user_name = st.sidebar.text_input("Enter your name:")
st.sidebar.title("Section 1: Plan Info")
v1 = ["Commerce India", "Reliance", "Commerce Global", "Government Projects", "Individual BH"]
business_head = st.sidebar.selectbox("Business Head", [""] + v1, help="Enter the name of Business head")
company_id = st.sidebar.text_input("Company ID", help="Enter the company ID")
company_name = st.sidebar.text_input("Company Name", help="Enter the company name")
currency = st.sidebar.radio("Select the currency type", options= ["INR", "USD"], help= "Select the type of currency", index =None)
bundle_by = st.sidebar.radio(options=["Single value", "Feature specific"], label="Bundle by", help = "Select the bundle", index=None)

if bundle_by == "Feature specific":

    plan_name = st.sidebar.text_input("Plan Name", help="Enter the name of the plan")
    plan_description = st.sidebar.text_area("Plan Description", max_chars=250, help="Describe the plan")
    plan_start_date = st.sidebar.date_input("Plan Start Date", value=datetime.now(), help="Select the start date of the plan")


# Section 2: Company Info
    st.sidebar.title("Section 2: Rule Info")
    a1 = ["GoFynd", "Uniket", "B2B", "Marketplaces", "StoreOS", "Storefronts", "ONDC", "Fynd OMS", "Fynd TMS", "Fynd WMS",
      "GMC", "Catalog Cloud", "Fynd Commerce Platform", "Logistics", "PixelBin", "Boltic", "CoPilot"]
    ordering_channels = st.sidebar.selectbox("Product lines", [""] + a1, help="Select the ordering channels")

# Layer 1: Mapping of Ordering channels with Fulfilling location
    if "Fynd TMS" in ordering_channels or "GMC" in ordering_channels or "Catalog Cloud" in ordering_channels:
        fulfilling_location = None
        application_id = None
    else:
        abc = ["Store", "Warehouse"]
        fulfilling_location = st.sidebar.selectbox("Fulfilling Location", [""] + abc, help="Select the fulfilling location")
        application_id = st.sidebar.text_input("Application ID", key="application_id_input", help="Enter the application ID")

# Section 3: Defining products for each dropdown
    product_options = ["B2B", "Marketplaces", "StoreOS", "Storefronts", "ONDC", "Fynd OMS", "Fynd TMS", "Fynd WMS", "GMC",
                   "Catalog Cloud", "Fynd Commerce Platform", "Logistics", "Logistics", "PixelBin", "Boltic",
                   "CoPilot"]
    fee_type_options = ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee", "Logistics",
                    "Packaging", "SLA", "Licensing"]
    fee_nature_options = ["Fixed %", "Flat currency", "Slab based", "As per rate card"]
    variable_options = ["Bag", "Shipment", "Application", "Extension", "Integration", "Store", "User"]
    chargeable_on_options = ["Developed", "Installed", "Placed", "Invoiced", "Delivered", "Return window", "All", "Picked",
                         "RTO", "DTO", "Packed"]
    plan_validity_options = ["One time", "Monthly", "Quarterly", "Bi-Annually", "Annually"]
    payment_method_options = ["Prepaid", "Postpaid"]

# Mapping index
    fee_config = {
        'fee_type_mapping': {
        "ONDC": ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee", "Logistics",
                 "Marketing", "SLA"],
        "GoFynd": ["Transaction", "Logistics", "Marketing", "Packaging", "SLA"],
        "B2B": ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee", "Logistics",
                "Packaging"],
        "Marketplaces": ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee"],
        "StoreOS": ["Development", "Subscription", "Maintenance", "Licensing", "Transaction", "Minimum Guarantee",
                    "Logistics", "Packaging"],
        "Storefronts": ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee", "Logistics"],
        "Fynd TMS": ["Development", "Subscription", "Maintenance", "Licensing", "Logistics"],
        "Fynd WMS": ["Development", "Subscription", "Maintenance", "Licensing", "Transaction", "Minimum Guarantee",
                     "Logistics", "Packaging"],
        "GMC": ["Development", "Subscription", "Maintenance"],
        "Catalog Cloud": ["Development", "Subscription", "Maintenance"],
        "Uniket": ["Transaction", "Logistics", "Marketing", "Packaging", "SLA"],
        "Fynd OMS": ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee"],
        "Fynd Commerce Platform": ["Subscription"],
        "Logistics": ["Logistics"],
        "PixelBin": ["Subscription"],
        "Boltic": ["Subscription"],
        "CoPilot": ["Subscription"],

        }
    }

    var_config = {
        'variable_type_mapping': {
        "Development": ["Application", "Extension", "Integration"],
        "Subscription": ["Application", "Extension", "Integration", "Platform"],
        "Maintenance": ["Application", "Extension", "Integration"],
        "Licensing": ["Store", "User"],
        "Transaction": ["Bag", "Shipment"],
        "Minimum Guarantee": ["Bag", "Shipment"],
        "SLA": ["Bag", "Shipment"],
        "Logistics": ["Shipment"],
        "Marketing": ["Bag"],
        "Packaging": ["Shipment"]
        }
    }

    char_config = {
        'chargeable_on_mapping': {
        "Application": ["Developed", "Installed"],
        "Extension": ["Developed", "Installed", "Subscribed"],
        "Integration": ["Developed", "Installed"],
        "Store": ["Added", "Active"],
        "User": ["Added", "Active"],
        "Bag": ["Placed", "Invoiced", "Delivered", "Return window", "Cancel", "RTO", "DTO"],
        "Shipment": ["Placed", "Invoiced", "Delivered", "Return window", "All", "Picked", "RTO", "DTO", "Packed",
                     "Cancel"],
        "Platform": ["Subscribed"],
        }
    }


# 2nd layer: Mapping of Ordering channels with fee types
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    
    fee_type_mapping = fee_config['fee_type_mapping']
    selected_fee_type = st.selectbox("Fee Type", [""] + fee_type_mapping.get(ordering_channels, []),
                                 help="Select the type of fee")

# 3rd layer mapping: Mapping of Fee type with variables
    variable_type_mapping = var_config["variable_type_mapping"]
    selected_variable_type = st.selectbox("Variable Type", [""] + variable_type_mapping.get(selected_fee_type, []),
                                      help="Select the type of variable")

# 4th layer mapping: Mapping of Fee type with variables
    chargeable_on_mapping = char_config["chargeable_on_mapping"]
    selected_chargeable_on = st.selectbox("Chargeable on", [""] + chargeable_on_mapping.get(selected_variable_type, []),
                                       help="Select the type of Chargeable")

# Create an empty DataFrame with the desired column names
    slabs_df = pd.DataFrame(columns=["Slab", "Max_value", "Commercial_value", "Usage", "Capping/Min_Guarantee_value", "Threshold"])

    ttt = ["Fixed %", "Flat currency", "Slab based"]
    selected_fee_nature = st.selectbox("Fee Nature:", [""] + ttt, key="fee_nature_select")

    if selected_fee_nature == "Slab based":
        st.write("Enter values for Slab based fee structure:")

    # Initialize an empty list to store data rows
        # Global list to store slab data rows
        global_data_rows = []

        def add_data(slab, max_value, user_input, Usage, Capping_or_Minimum_Guarantee, threshold):
    # Convert values to int if not None
            max_value = int(max_value.strip()) if max_value else None
            user_input = int(user_input.strip()) if user_input else None
            Usage = int(Usage.strip()) if Usage else None
            Capping_or_Minimum_Guarantee = int(Capping_or_Minimum_Guarantee.strip()) if Capping_or_Minimum_Guarantee else None
    
    # Create a new row dictionary
            new_row = {
                "Slab": slab,
                "Max_value": max_value,
                "Commercial_value": user_input,
                "Usage": Usage,
                "Capping/Min_Guarantee_value": Capping_or_Minimum_Guarantee,
                "Threshold": threshold
            }
    
    # Append new_row to global list of rows
            global_data_rows.append(new_row)
            save_slab_data(new_row) 

    # Display all rows in a table
            st.subheader("Added Slabs")
            for i, row in enumerate(global_data_rows):
                st.write(f"Entry {i + 1}:")
                st.table([row])

# Streamlit UI code
        def main():
            st.title("Slab Data Management")
    
    # Inputs for adding data
            col1, col2 = st.columns([2, 2])
            with col1:
                slab = st.selectbox("Slab:", [1, 2, 3], key="slab_select")
                user_input = st.text_input("Commercial Value:", key="user_input")
                Capping_or_Minimum_Guarantee = st.text_input("Capping/Min_Guarantee:", key="Capping_or_Minimum_Guarantee_input")
            with col2:
                max_value = st.text_input("Max value:", key="max_value_input")
                Usage = st.text_input("Usage:", key="Usage_input")
                threshold = st.text_input("Threshold:", key="threshold_input")
    
    # Button to add data
            if st.button("Add Data", key="add_data_button"):
                if not (slab and user_input and Capping_or_Minimum_Guarantee):
                    st.warning("Please fill in all required fields.")
                else:
                    add_data(slab, max_value, user_input, Usage, Capping_or_Minimum_Guarantee, threshold)
                    st.success(f"Data for Slab '{slab}' added successfully!")

                

        if __name__ == "__main__":
            main()


    elif selected_fee_nature in ["Fixed %", "Flat currency"]:
        user_input = st.number_input("Commercial value:", min_value=0.0, help="Enter a valid number")

    # 6th layer: Expected Billing
        fee_reversal_options = ["RTO", "DTO", "Cancel"]
        fee_reversal = st.multiselect("Fee Reversal", fee_reversal_options) if selected_fee_type == "Transaction" and selected_variable_type == "Bag" else None
        reversal_per = st.number_input("Reversal %", min_value= 0.0, help = "Enter the reversal percentage") if selected_fee_type == "Transaction" and selected_variable_type == "Bag" else None
        Usage = st.number_input(f"Usage limit for {selected_variable_type}", min_value=0.0, help="Enter the usage limit")
        Capping_or_Minimum_Guarantee = st.number_input(f"Capping/Minimum Guarantee for {selected_variable_type}", min_value=0.0,
                                                    help="Enter the Capping/Minimum Gauarntee value")
        Product = Usage * user_input if selected_fee_nature in ["Fixed %", "Flat currency"] else 0

        abc = ['Capping value', 'Minimum Guarantee']
        threshold = st.selectbox("Threshold option:", [""] + abc)

        initial_expected_billing = Product

        if threshold == 'Capping value':
            expected_billing = Product if Capping_or_Minimum_Guarantee > Product else Capping_or_Minimum_Guarantee
        elif threshold == 'Minimum Guarantee':
            expected_billing = Product if Capping_or_Minimum_Guarantee < Product else Capping_or_Minimum_Guarantee
        else:
            expected_billing = initial_expected_billing  # Default to initial Product value if no threshold selected

        st.write(f"Expected Billing (excluding GST): {expected_billing}")

    selected_plan_validity = st.selectbox("Plan Validity", [""] + plan_validity_options, help="Select the plan validity", key="plan_vd_2")
    selected_payment_method = st.selectbox("Payment Method", [""] + payment_method_options, help="Select the payment method", key="py_vd_2")

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
        "Currency type": currency,
        "Bundle by": bundle_by,
        "Fulfilling Location": fulfilling_location,
        "Application ID": application_id,
        "Fee Type": selected_fee_type,
        "Variable": selected_variable_type,
        "Chargeable on": selected_chargeable_on,
        "Fee Nature": selected_fee_nature,
        "Commercial value": user_input,
        "Fee reversal": fee_reversal,
        "Reversal %": reversal_per,
        "Usage limit": Usage,
        "Minimum/Capping value": Capping_or_Minimum_Guarantee,
        "Threshold option": threshold,
        "Expected Billing": expected_billing,
        "Plan Validity": selected_plan_validity,
        "Payment Method": selected_payment_method,
        }

        global_user_data.append((user_name, user_data))

    # Generate PM_id and add it to user_data
        rule_id = generate_rule_id(user_data)
        user_data['rule_id'] = rule_id

    # Generate Plan ID and add it to user_data
        plan_id = generate_plan_id(user_data)
        user_data['plan_id'] = plan_id

        save_user_data(user_data)  # Save user data after submission

    # Display saved records
        display_saved_records()



elif bundle_by == "Single value":
    user_input_1 = st.sidebar.text_input("Enter Single values:")

    plan_name = st.sidebar.text_input("Plan Name", help="Enter the name of the plan")
    plan_description = st.sidebar.text_area("Plan Description", max_chars=250, help="Describe the plan")
    plan_start_date = st.sidebar.date_input("Plan Start Date", value=datetime.now(), help="Select the start date of the plan")


# Section 2: Company Info
    st.sidebar.title("Section 2: Rule Info")
    a1 = ["GoFynd", "Uniket", "B2B", "Marketplaces", "StoreOS", "Storefronts", "ONDC", "Fynd OMS", "Fynd TMS", "Fynd WMS",
      "GMC", "Catalog Cloud", "Fynd Commerce Platform", "Logistics", "PixelBin", "Boltic", "CoPilot"]
    ordering_channels = st.sidebar.selectbox("Product lines", [""] + a1, help="Select the ordering channels")

# Layer 1: Mapping of Ordering channels with Fulfilling location
    if "Fynd TMS" in ordering_channels or "GMC" in ordering_channels or "Catalog Cloud" in ordering_channels:
        fulfilling_location = None
        application_id = None
    else:
        abc = ["Store", "Warehouse"]
        fulfilling_location = st.sidebar.selectbox("Fulfilling Location", [""] + abc, help="Select the fulfilling location")
        application_id = st.sidebar.text_input("Application ID", key="application_id_input", help="Enter the application ID")

# Section 3: Defining products for each dropdown
    product_options = ["B2B", "Marketplaces", "StoreOS", "Storefronts", "ONDC", "Fynd OMS", "Fynd TMS", "Fynd WMS", "GMC",
                   "Catalog Cloud", "Fynd Commerce Platform", "Logistics", "Logistics", "PixelBin", "Boltic",
                   "CoPilot"]
    fee_type_options = ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee", "Logistics",
                    "Packaging", "SLA", "Licensing"]
    fee_nature_options = ["Fixed %", "Flat currency", "Slab based", "As per rate card"]
    variable_options = ["Bag", "Shipment", "Application", "Extension", "Integration", "Store", "User"]
    chargeable_on_options = ["Developed", "Installed", "Placed", "Invoiced", "Delivered", "Return window", "All", "Picked",
                         "RTO", "DTO", "Packed"]
    plan_validity_options = ["One time", "Monthly", "Quarterly", "Bi-Annually", "Annually"]
    payment_method_options = ["Prepaid", "Postpaid"]

# Mapping index
    fee_config = {
        'fee_type_mapping': {
        "ONDC": ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee", "Logistics",
                 "Marketing", "SLA"],
        "GoFynd": ["Transaction", "Logistics", "Marketing", "Packaging", "SLA"],
        "B2B": ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee", "Logistics",
                "Packaging"],
        "Marketplaces": ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee"],
        "StoreOS": ["Development", "Subscription", "Maintenance", "Licensing", "Transaction", "Minimum Guarantee",
                    "Logistics", "Packaging"],
        "Storefronts": ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee", "Logistics"],
        "Fynd TMS": ["Development", "Subscription", "Maintenance", "Licensing", "Logistics"],
        "Fynd WMS": ["Development", "Subscription", "Maintenance", "Licensing", "Transaction", "Minimum Guarantee",
                     "Logistics", "Packaging"],
        "GMC": ["Development", "Subscription", "Maintenance"],
        "Catalog Cloud": ["Development", "Subscription", "Maintenance"],
        "Uniket": ["Transaction", "Logistics", "Marketing", "Packaging", "SLA"],
        "Fynd OMS": ["Development", "Subscription", "Maintenance", "Transaction", "Minimum Guarantee"],
        "Fynd Commerce Platform": ["Subscription"],
        "Logistics": ["Logistics"],
        "PixelBin": ["Subscription"],
        "Boltic": ["Subscription"],
        "CoPilot": ["Subscription"],

        }
    }

    var_config = {
        'variable_type_mapping': {
        "Development": ["Application", "Extension", "Integration"],
        "Subscription": ["Application", "Extension", "Integration", "Platform"],
        "Maintenance": ["Application", "Extension", "Integration"],
        "Licensing": ["Store", "User"],
        "Transaction": ["Bag", "Shipment"],
        "Minimum Guarantee": ["Bag", "Shipment"],
        "SLA": ["Bag", "Shipment"],
        "Logistics": ["Shipment"],
        "Marketing": ["Bag"],
        "Packaging": ["Shipment"]
        }
    }

    char_config = {
        'chargeable_on_mapping': {
        "Application": ["Developed", "Installed"],
        "Extension": ["Developed", "Installed", "Subscribed"],
        "Integration": ["Developed", "Installed"],
        "Store": ["Added", "Active"],
        "User": ["Added", "Active"],
        "Bag": ["Placed", "Invoiced", "Delivered", "Return window", "Cancel", "RTO", "DTO"],
        "Shipment": ["Placed", "Invoiced", "Delivered", "Return window", "All", "Picked", "RTO", "DTO", "Packed",
                     "Cancel"],
        "Platform": ["Subscribed"],
        }
    }


# 2nd layer: Mapping of Ordering channels with fee types
    st.write("")
    st.write("")
    st.write("")
    st.write("")



    fee_type_mapping = fee_config['fee_type_mapping']
    selected_fee_type = st.selectbox("Fee Type", [""] + fee_type_mapping.get(ordering_channels, []),
                                 help="Select the type of fee")

# 3rd layer mapping: Mapping of Fee type with variables
    variable_type_mapping = var_config["variable_type_mapping"]
    selected_variable_type = st.selectbox("Variable Type", [""] + variable_type_mapping.get(selected_fee_type, []),
                                      help="Select the type of variable")

# 4th layer mapping: Mapping of Fee type with variables
    chargeable_on_mapping = char_config["chargeable_on_mapping"]
    selected_chargeable_on = st.selectbox("Chargeable on", [""] + chargeable_on_mapping.get(selected_variable_type, []),
                                       help="Select the type of Chargeable")

    Usage = st.number_input(f"Usage limit for {selected_variable_type}", min_value=0.0, help="Enter the usage limit")
    selected_plan_validity = st.selectbox("Plan Validity", [""] + plan_validity_options, help="Select the plan validity", key="plan_vd_2")
    selected_payment_method = st.selectbox("Payment Method", [""] + payment_method_options, help="Select the payment method", key="py_vd_2")

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
        
        "Plan Validity": selected_plan_validity,
        "Payment Method": selected_payment_method,
        }

        global_user_data.append((user_name, user_data))

    # Generate PM_id and add it to user_data
        rule_id = generate_rule_id(user_data)
        user_data['rule_id'] = rule_id

    # Generate Plan ID and add it to user_data
        plan_id = generate_plan_id(user_data)
        user_data['plan_id'] = plan_id

        save_user_data(user_data)  # Save user data after submission

    # Display saved records
        display_saved_records()

