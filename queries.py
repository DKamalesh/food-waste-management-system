queries = {

    # 1️ Providers per city
    "providers_per_city": """
        SELECT City, COUNT(*) AS Providers_Count
        FROM providers
        GROUP BY City
    """,

    # 2️ Receivers per city
    "receivers_per_city": """
        SELECT City, COUNT(*) AS Receivers_Count
        FROM receivers
        GROUP BY City
    """,

    # 3️ Provider type contributing most food
    "top_provider_type": """
        SELECT Provider_Type, SUM(Quantity) AS Total_Food
        FROM food_listings
        GROUP BY Provider_Type
        ORDER BY Total_Food DESC
    """,

    # 4️ Contact info of providers in a city
    "provider_contacts_city": """
        SELECT Name, City, Contact
        FROM providers
    """,

    # 5️ Receivers with most claims
    "top_receivers": """
        SELECT r.Name, COUNT(c.Claim_ID) AS Total_Claims
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY r.Name
        ORDER BY Total_Claims DESC
    """,

    # 6️ Total food available
    "total_food": """
        SELECT SUM(Quantity) AS Total_Food
        FROM food_listings
    """,

    # 7️ City with highest listings
    "top_city": """
        SELECT Location, COUNT(*) AS Listings
        FROM food_listings
        GROUP BY Location
        ORDER BY Listings DESC
    """,

    # 8️ Most common food type
    "food_types": """
        SELECT Food_Type, COUNT(*) AS Count
        FROM food_listings
        GROUP BY Food_Type
        ORDER BY Count DESC
    """,

    # 9️ Claims per food item
    "claims_per_food": """
        SELECT Food_ID, COUNT(*) AS Claims_Count
        FROM claims
        GROUP BY Food_ID
    """,

    # 10 Provider with most successful claims
    "top_successful_provider": """
        SELECT p.Name, COUNT(*) AS Successful_Claims
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Name
        ORDER BY Successful_Claims DESC
    """,

    # 11 Claim status percentage
    "claim_status_percentage": """
        SELECT 
            Status,
            COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS Percentage
        FROM claims
        GROUP BY Status
    """,

    # 12 Avg quantity claimed per receiver
    "avg_quantity_per_receiver": """
        SELECT c.Receiver_ID, AVG(f.Quantity) AS Avg_Quantity
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY c.Receiver_ID
    """,

    # 13 Most claimed meal type
    "meal_type": """
        SELECT f.Meal_Type, COUNT(*) AS Count
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Meal_Type
        ORDER BY Count DESC
    """,

    # 14 Total food donated per provider
    "food_per_provider": """
        SELECT p.Name, SUM(f.Quantity) AS Total_Donated
        FROM food_listings f
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY p.Name
        ORDER BY Total_Donated DESC
    """,

    # 15 Expiring soon (important insight 🔥)
    "expiring_soon": """
        SELECT Food_Name, Expiry_Date, Location
        FROM food_listings
        WHERE Expiry_Date <= CURDATE() + INTERVAL 2 DAY
    """,

    # BONUS (extra for safety)
    "pending_claims": """
        SELECT *
        FROM claims
        WHERE Status = 'Pending'
    """
}