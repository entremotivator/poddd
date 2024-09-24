import streamlit as st
import pandas as pd

# Title and Description
st.title("VIDeMI Services - Cleaning Schedule & Services")
st.markdown("""
### Welcome to the VIDeMI Services Dashboard
This app helps you manage and visualize the cleaning schedule for various villas. You can interact with the data, update service requirements, and select additional amenities as needed.
""")

# Data Setup
data = {
    'Date': ["Saturday 5/10", "Saturday 5/10", "Friday 11/10", "Saturday 12/10", "Monday 14/10", 
             "Thursday 17/10", "Friday 18/10", "Friday 18/10", "Saturday 19/10", "Saturday 26/10", 
             "Sunday 27/10", "Thursday 31/10"],
    'Type of Cleaning': ["CI", "CI", "CO/CI 11am-3pm", "CI", "CO/CI 11am-3pm", 
                         "CI", "CI", "CI", "CI", "CI", "CI", "CI"],
    'Villa Number': [2, 32, 2, 32, 36, 47, 2, 45, 32, 2, 32, 7],
    '#pax': ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    'Laundry': ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    'Comments/ Requests': ["Whole day possible", "Whole day possible", "OUT/IN 11am-3pm", 
                           "Whole day possible", "OUT/IN 11am-3pm", "Whole day possible", 
                           "Whole day possible", "Whole day possible", "After 11am!", 
                           "After 11am!", "After 11am!", "Whole day possible"]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Editable DataFrame using input fields
st.subheader("Editable Cleaning Schedule")
cleaning_schedule = []

# Create input fields for each row in the original DataFrame
for index, row in df.iterrows():
    st.write(f"### Entry {index + 1}")
    date = st.text_input(f"Date:", value=row['Date'], key=f"date_{index}")
    cleaning_type = st.selectbox(f"Type of Cleaning:", options=["CI", "CO/CI 11am-3pm", "FU", "DC"], index=["CI", "CO/CI 11am-3pm", "FU", "DC"].index(row['Type of Cleaning']), key=f"type_{index}")
    villa_number = st.number_input(f"Villa Number:", value=row['Villa Number'], key=f"villa_{index}")
    pax = st.text_input(f"#pax:", value=row['#pax'], key=f"pax_{index}")
    laundry = st.text_input(f"Laundry:", value=row['Laundry'], key=f"laundry_{index}")
    comments = st.text_area(f"Comments/ Requests:", value=row['Comments/ Requests'], key=f"comments_{index}")
    
    cleaning_schedule.append({
        "Date": date,
        "Type of Cleaning": cleaning_type,
        "Villa Number": villa_number,
        "#pax": pax,
        "Laundry": laundry,
        "Comments/ Requests": comments
    })

# Section for Additional Inputs
st.markdown("### Service Options")
col1, col2, col3 = st.columns(3)

with col1:
    amenities = st.checkbox("Amenities Provided?", value=False)
    st.text("Includes items like coffee, tea, sugar, etc.")

with col2:
    laundry_services = st.checkbox("Laundry Services?", value=False)
    st.text("Laundry services available for extra cost.")

with col3:
    keys = st.checkbox("Keys Available?", value=False)
    st.text("Confirm if keys are accessible.")

# Dropdown for Type of Cleaning
st.markdown("### Select the Type of Cleaning Required")
cleaning_options = ["Check-out/in (CO/CI)", "Fresh-up (FU)", "Deep Cleaning (DC)"]
selected_cleaning = st.selectbox("Choose Cleaning Type:", cleaning_options)
st.write(f"You selected: **{selected_cleaning}**")

# Multiselect for Welcome Package Options
st.markdown("### Welcome Package Options")
welcome_package_options = [
    'Coffee', 'Tea', 'Sugar', 'Hand soap', 'Shower Gel', 
    'Conditioner', 'Welcome groceries Package', 'Toilet Paper', 'Garbage Bags'
]
selected_package_items = st.multiselect('Select items for the Welcome Package:', welcome_package_options)

# Display selected items for Welcome Package
if selected_package_items:
    st.write(f"Selected Welcome Package items: {', '.join(selected_package_items)}")

# Summary of Selected Services
st.markdown("### Summary of Selected Services")
summary_data = {
    "Amenities Provided": ["Yes" if amenities else "No"],
    "Laundry Services": ["Yes" if laundry_services else "No"],
    "Keys Available": ["Yes" if keys else "No"],
    "Cleaning Type": [selected_cleaning],
    "Welcome Package Items": [', '.join(selected_package_items) if selected_package_items else "None"]
}

summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df)

# Text area for additional comments
st.markdown("### Additional Information")
additional_comments = st.text_area("Comments/Requests", "Please add any additional information here...")

# Button to download CSV file
if st.button("Export to CSV"):
    # Combine the editable schedule with summary data into one exportable DataFrame
    export_data = {
        "Date": [entry['Date'] for entry in cleaning_schedule],
        "Type of Cleaning": [entry['Type of Cleaning'] for entry in cleaning_schedule],
        "Villa Number": [entry['Villa Number'] for entry in cleaning_schedule],
        "Amenities Provided": ["Yes" if amenities else "No"] * len(cleaning_schedule),
        "Laundry Services": ["Yes" if laundry_services else "No"] * len(cleaning_schedule),
        "Keys Available": ["Yes" if keys else "No"] * len(cleaning_schedule),
        "Cleaning Type": [selected_cleaning] * len(cleaning_schedule),
        "Welcome Package Items": [', '.join(selected_package_items) if selected_package_items else "None"] * len(cleaning_schedule),
        "Additional Comments": [additional_comments] * len(cleaning_schedule)
    }
    
    export_df = pd.DataFrame(export_data)
    csv = export_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "videmi_services_schedule.csv", "text/csv")

# Display the final message
st.success("Thank you! Your schedule and preferences have been saved.")
