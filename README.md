# Food Wastage Management System (Streamlit + MySQL)

1. Project Overview
This project is a web-based Food Wastage Management System designed to reduce food waste by connecting food providers (restaurants, stores) with receivers in need. It enables efficient food donation tracking, management, and analysis.

---

2. Objective
- Reduce food wastage
- Connect providers with receivers
- Track donations and claims efficiently
- Provide insights for better food distribution

---

3. Features

# Food Listing Management
- Add new food items
- Auto-link with providers
- Location-based tracking

# Provider Management
- Add new providers dynamically
- Store contact and city details

# Claim System
- Track food claims by receivers
- Monitor claim status (Pending, Completed)

# Delete Functionality
- Delete food items safely
- Handles foreign key constraints (claims)

# Dashboard & Insights
- Total food items, providers, claims (KPIs)
- Food type distribution
- Meal type analysis
- Expiry alerts

# Advanced SQL Analysis
- Providers per city
- Top providers
- Claim statistics
- Donation patterns
- Expiring food alerts

---

4. Tech Stack
- Python (Streamlit) – Frontend & App Logic  
- MySQL – Database  
- Pandas – Data handling  
- SQL – Querying & analysis  

---

5. Database Structure
Main tables used:
- `providers`
- `food_listings`
- `claims`
- `receivers`

---

6. Key Insights
- Certain cities have higher food donation activity  
- Meal type distribution shows peak donation times  
- Some providers contribute significantly more food  
- Expiry tracking helps reduce waste effectively  

---

7. Business Impact
- Helps reduce food wastage in urban areas  
- Improves food distribution efficiency  
- Enables data-driven decisions for NGOs and providers  
- Supports sustainability initiatives  

---

8. How to Run

 Install dependencies
```bash
pip install streamlit pandas mysql-connector-python python-dotenv
