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

# Editable DataFrame using st.experimental_data_editor (new feature in Streamlit)
st.subheader("Editable Cleaning Schedule")
editable_df = st.experimental_data_editor(df, num_rows="dynamic")

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
    # Combine the editable DataFrame and the summary into one exportable DataFrame
    export_data = {
        "Date": editable_df['Date'],
        "Type of Cleaning": editable_df['Type of Cleaning'],
        "Villa Number": editable_df['Villa Number'],
        "Amenities Provided": ["Yes" if amenities else "No"] * len(editable_df),
        "Laundry Services": ["Yes" if laundry_services else "No"] * len(editable_df),
        "Keys Available": ["Yes" if keys else "No"] * len(editable_df),
        "Cleaning Type": [selected_cleaning] * len(editable_df),
        "Welcome Package Items": [', '.join(selected_package_items) if selected_package_items else "None"] * len(editable_df),
        "Additional Comments": [additional_comments] * len(editable_df)
    }
    
    export_df = pd.DataFrame(export_data)
    csv = export_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "videmi_services_schedule.csv", "text/csv")

# Display the final message
st.success("Thank you! Your schedule and preferences have been saved.")
