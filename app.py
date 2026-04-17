from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import pandas as pd
from db_config import get_connection

# ---------------- DB CONNECTION ----------------
conn = get_connection()

# ---------------- CUSTOM CSS ----------------
st.markdown("""<style>
/* keep your full CSS unchanged */
</style>""", unsafe_allow_html=True)

st.set_page_config(page_title="Food Wastage System", layout="wide")

# ---------------- TITLE ----------------
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <h1>🍱 Food Wastage Management System</h1>
    <p>Reducing waste, feeding communities</p>
</div>
""", unsafe_allow_html=True)

# ---------------- LOAD FUNCTION ----------------
@st.cache_data(ttl=10)
def load_data(query):
    return pd.read_sql(query, conn)

# ---------------- KPIs ----------------
col1, col2, col3 = st.columns(3)

col1.metric("🍽️ Total Food Items",
            load_data("SELECT COUNT(*) c FROM food_listings")['c'][0])

col2.metric("🏪 Total Providers",
            load_data("SELECT COUNT(*) c FROM providers")['c'][0])

col3.metric("📦 Total Claims",
            load_data("SELECT COUNT(*) c FROM claims")['c'][0])

st.divider()

# ---------------- SIDEBAR FILTERS ----------------
with st.sidebar:
    st.header("🔍 Filters")

    city = st.selectbox(
        "City",
        ["All"] + list(load_data("SELECT DISTINCT City FROM providers")['City'])
    )

    food_type = st.selectbox(
        "Food Type",
        ["All"] + list(load_data("SELECT DISTINCT Food_Type FROM food_listings")['Food_Type'])
    )

    meal_type = st.selectbox(
        "Meal Type",
        ["All"] + list(load_data("SELECT DISTINCT Meal_Type FROM food_listings")['Meal_Type'])
    )

# ---------------- MAIN DATA ----------------
query = """
SELECT f.*, p.Name AS Provider_Name, p.Contact
FROM food_listings f
JOIN providers p ON f.Provider_ID = p.Provider_ID
WHERE 1=1
"""

if city != "All":
    query += f" AND p.City = '{city}'"

if food_type != "All":
    query += f" AND f.Food_Type = '{food_type}'"

if meal_type != "All":
    query += f" AND f.Meal_Type = '{meal_type}'"

data = load_data(query)

st.subheader("📋 Available Food Listings")
st.dataframe(data, use_container_width=True)

# ---------------- ADD FOOD (FIXED FOR MYSQL) ----------------
st.divider()
st.subheader("➕ Add New Food Listing")

# Fetch providers
providers_df = load_data("SELECT Provider_ID, Name FROM providers")

provider_names = list(providers_df['Name'])
provider_names.append("➕ Add New Provider")

provider_dict = dict(zip(providers_df['Name'], providers_df['Provider_ID']))

with st.form("add_food", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:
        food_name = st.text_input("🍲 Food Name *")
        qty = st.number_input("📦 Quantity", min_value=1)
        provider_name = st.selectbox("🏪 Select Provider", provider_names)

    with col2:
        meal = st.selectbox("🕐 Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
        food_type_input = st.selectbox("🥗 Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        location = st.text_input("📍 Location *")

    # 👇 SHOW NEW PROVIDER FIELDS IF SELECTED
    if provider_name == "➕ Add New Provider":
        st.markdown("### ➕ Add New Provider Details")

        new_name = st.text_input("Provider Name *")
        new_type = st.selectbox("Provider Type", ["Restaurant", "Grocery", "Supermarket"])
        new_city = st.text_input("City *")
        new_contact = st.text_input("Contact")

    submit = st.form_submit_button("✨ Add Food", use_container_width=True)

    if submit:

        # VALIDATION
        if not food_name or not location:
            st.error("❌ Food Name and Location are required!")

        else:
            cursor = conn.cursor()

            # 👉 CASE 1: EXISTING PROVIDER
            if provider_name != "➕ Add New Provider":
                provider_id = provider_dict[provider_name]

            # 👉 CASE 2: NEW PROVIDER
            else:
                if not new_name or not new_city:
                    st.error("❌ Provider Name and City are required!")
                    st.stop()

                cursor.execute("""
                INSERT INTO providers (Name, Type, City, Contact)
                VALUES (%s, %s, %s, %s)
                """, (new_name, new_type, new_city, new_contact))

                conn.commit()

                # GET NEW PROVIDER ID
                provider_id = cursor.lastrowid

                st.success(f"✅ New provider '{new_name}' added!")

            # 👉 INSERT FOOD
            cursor.execute("""
            INSERT INTO food_listings 
            (Food_Name, Quantity, Provider_ID, Meal_Type, Food_Type, Location)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (food_name, qty, provider_id, meal, food_type_input, location))

            conn.commit()

            st.success("✅ Food added successfully!")
            st.rerun()
# ---------------- DELETE ----------------
st.subheader("❌ Delete Food")

delete_id = st.number_input("Enter Food ID", min_value=1, step=1)

if st.button("Delete"):
    cursor = conn.cursor()

    # CHECK IF FOOD EXISTS
    cursor.execute("SELECT Food_Name FROM food_listings WHERE Food_ID=%s", (delete_id,))
    result = cursor.fetchone()

    if result:
        food_name = result[0]

        # STEP 1: delete dependent claims first (fix FK error)
        cursor.execute("DELETE FROM claims WHERE Food_ID=%s", (delete_id,))

        # STEP 2: delete food item
        cursor.execute("DELETE FROM food_listings WHERE Food_ID=%s", (delete_id,))

        conn.commit()

        st.success(f"✅ Deleted Food ID {delete_id} ({food_name}) and related claims")
        st.rerun()

    else:
        st.error("❌ Food ID not found")
# ---------------- INSIGHTS ----------------
st.divider()
st.subheader("📊 Insights")

col1, col2 = st.columns(2)

with col1:
    df1 = load_data("SELECT Food_Type, COUNT(*) count FROM food_listings GROUP BY Food_Type")
    st.bar_chart(df1.set_index("Food_Type"))

with col2:
    df2 = load_data("SELECT Meal_Type, COUNT(*) count FROM food_listings GROUP BY Meal_Type")
    st.bar_chart(df2.set_index("Meal_Type"))

# ---------------- SQL QUERY SELECTOR ----------------
st.divider()
st.subheader("🧠 SQL Analysis")

option = st.selectbox("Choose Query", [
    "Providers per City",
    "Top Provider Type",
    "Top Receivers",
    "Total Food",
    "Top City",
    "Food Types",
    "Claims per Food",
    "Top Provider (Claims)",
    "Claim Status %",
    "Avg Food per Receiver",
    "Top Meal Type",
    "Donation per Provider",
    "Provider Contacts",
    "Expiring Soon",
    "Pending Claims"
])

if option == "Providers per City":
    st.dataframe(load_data("SELECT City, COUNT(*) FROM providers GROUP BY City"))

elif option == "Top Provider Type":
    st.dataframe(load_data("SELECT Provider_Type, SUM(Quantity) FROM food_listings GROUP BY Provider_Type"))

elif option == "Top Receivers":
    st.dataframe(load_data("""
        SELECT r.Name, COUNT(*) 
        FROM claims c JOIN receivers r 
        ON c.Receiver_ID = r.Receiver_ID 
        GROUP BY r.Name ORDER BY COUNT(*) DESC
    """))

elif option == "Total Food":
    st.dataframe(load_data("SELECT SUM(Quantity) FROM food_listings"))

elif option == "Top City":
    st.dataframe(load_data("SELECT Location, COUNT(*) FROM food_listings GROUP BY Location"))

elif option == "Food Types":
    st.dataframe(load_data("SELECT Food_Type, COUNT(*) FROM food_listings GROUP BY Food_Type"))

elif option == "Claims per Food":
    st.dataframe(load_data("SELECT Food_ID, COUNT(*) FROM claims GROUP BY Food_ID"))

elif option == "Top Provider (Claims)":
    st.dataframe(load_data("""
        SELECT p.Name, COUNT(*) 
        FROM claims c 
        JOIN food_listings f ON c.Food_ID=f.Food_ID
        JOIN providers p ON f.Provider_ID=p.Provider_ID
        GROUP BY p.Name ORDER BY COUNT(*) DESC
    """))

elif option == "Claim Status %":
    st.dataframe(load_data("""
        SELECT Status, COUNT(*)*100/(SELECT COUNT(*) FROM claims)
        FROM claims GROUP BY Status
    """))

elif option == "Avg Food per Receiver":
    st.dataframe(load_data("""
        SELECT Receiver_ID, COUNT(*) 
        FROM claims GROUP BY Receiver_ID
    """))

elif option == "Top Meal Type":
    st.dataframe(load_data("SELECT Meal_Type, COUNT(*) FROM food_listings GROUP BY Meal_Type"))

elif option == "Donation per Provider":
    st.dataframe(load_data("""
        SELECT p.Name, SUM(f.Quantity)
        FROM food_listings f JOIN providers p
        ON f.Provider_ID=p.Provider_ID
        GROUP BY p.Name
    """))

elif option == "Provider Contacts":
    st.dataframe(load_data("SELECT Name, City, Contact FROM providers"))

elif option == "Expiring Soon":
    st.dataframe(load_data("""
        SELECT * FROM food_listings
        WHERE Expiry_Date <= CURDATE() + INTERVAL 2 DAY
    """))

elif option == "Pending Claims":
    st.dataframe(load_data("SELECT * FROM claims WHERE Status='Pending'"))

# ---------------- EXPIRY ALERT ----------------
st.divider()
st.subheader("⏰ Expiring Soon Food")

expiring = load_data("""
SELECT * FROM food_listings
WHERE Expiry_Date <= CURDATE() + INTERVAL 2 DAY
""")

if not expiring.empty:
    st.dataframe(expiring)
else:
    st.success("No food expiring soon 🎉")