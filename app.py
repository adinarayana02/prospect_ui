import streamlit as st
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Connect to PostgreSQL database
def connect_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

# Rest of the code remains unchanged
# Search for company names based on query
def search_users(query):
    conn = connect_db()
    cur = conn.cursor()

    search_query = """
    SELECT company_name
    FROM users
    WHERE company_name ILIKE %s
    """
    
    cur.execute(search_query, (f"%{query}%",))
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return [row[0] for row in results]

# Get detailed information for a selected company
def get_company_details(company_name):
    conn = connect_db()
    cur = conn.cursor()

    details_query = """
    SELECT company_name, requirements, date, status, notes, next_steps, contact_person, contact_information
    FROM users
    WHERE company_name = %s
    """
    
    cur.execute(details_query, (company_name,))
    details = cur.fetchone()
    cur.close()
    conn.close()
    
    return details

# Streamlit UI
st.title("User Management")

# Search bar
search_query = st.text_input("Search for a company", placeholder="Enter company name...", max_chars=100)

if search_query:
    # Fetch matching company names
    company_names = search_users(search_query)
    
    if company_names:
        # Display suggestions in a selectbox
        selected_company = st.selectbox("Select a company:", company_names)
        
        if selected_company:
            # Fetch and display details of the selected company
            details = get_company_details(selected_company)
            if details:
                st.subheader("Company Details")
                st.write(f"**Company Name:** {details[0]}")
                st.write(f"**Requirements:** {details[1]}")
                st.write(f"**Date:** {details[2]}")
                st.write(f"**Status:** {details[3]}")
                st.write(f"**Notes:** {details[4]}")
                st.write(f"**Next Steps:** {details[5]}")
                st.write(f"**Contact Person:** {details[6]}")
                st.write(f"**Contact Information:** {details[7]}")
            else:
                st.write("No details found for the selected company.")
    else:
        st.write("No companies found matching your query.")

# Form for adding a new user
st.header("Add a New User")
with st.form("user_form"):
    company_name = st.text_input("Company Name", max_chars=255)
    requirements = st.text_area("Requirements", height=100)
    date = st.date_input("Date", value=datetime.today())
    status = st.text_input("Status", max_chars=50)
    notes = st.text_area("Notes", height=100)
    next_steps = st.text_area("Next Steps", height=100)
    contact_person = st.text_input("Contact Person", max_chars=100)
    contact_information = st.text_input("Contact Information (Email/Phone)", max_chars=255)

    # Form submission button
    submitted = st.form_submit_button("Add User")

    if submitted:
        if company_name and contact_person and contact_information:
            insert_user(
                company_name, requirements, date, status, notes, next_steps, contact_person, contact_information
            )
        else:
            st.error("Please fill in all required fields (Company Name, Contact Person, Contact Information).")
