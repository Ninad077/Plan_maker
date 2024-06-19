

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
        "Uniket": ["Transaction","Logistics","Marketing","Packaging","SLA"]

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






