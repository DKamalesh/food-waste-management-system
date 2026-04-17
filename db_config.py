import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Kamal@3008",
        database="food_waste"
    )

# 👇 THIS PART IS VERY IMPORTANT
if __name__ == "__main__":
    try:
        print("Connecting...")
        conn = get_connection()
        print("✅ Connected to MySQL successfully!")
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)