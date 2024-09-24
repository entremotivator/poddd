import streamlit as st
import pandas as pd

# Title and Description
st.title("VIDeMI Services - Cleaning Schedule & Services")
st.markdown("""
### Welcome to the VIDeMI Services Dashboard
This app helps you manage and visualize the cleaning schedule for various villas. You can interact with the data, update service requirements, and select additional amenities as needed.
""")

# Data Setup (Replicating the table from the image)
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

# Display the table
st.subheader("Cleaning Schedule")
st.dataframe(df)

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
    'Conditioner', 'Welcome groceries Package'
]
selected_package_items = st.multiselect('Select items for the Welcome Package:', welcome_package_options)

# Display selected items for Welcome Package
if selected_package_items:
    st.write(f"Selected Welcome Package items: {', '.join(selected_package_items)}")

# Conditional display based on inputs
st.markdown("### Summary of Selected Services")

if amenities:
    st.write("- **Amenities will be provided**")
else:
    st.write("- **No amenities will be provided**")

if laundry_services:
    st.write("- **Laundry services will be provided**")
else:
    st.write("- **No laundry services**")

if keys:
    st.write("- **Keys are available**")
else:
    st.write("- **No keys available**")

st.write(f"- **Cleaning Type:** {selected_cleaning}")
if selected_package_items:
    st.write(f"- **Welcome Package Items:** {', '.join(selected_package_items)}")
else:
    st.write("- **No welcome package items selected**")

st.markdown("### Additional Information")
st.text_area("Comments/Requests", "Please add any additional information here...")

# Display the final message
st.success("Thank you! Your schedule and preferences have been saved.")
