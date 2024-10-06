
import mysql.connector


DB_CONFIG = {
    'host':'54.213.19.160',  # Replace with your EC2 public IP
    'user':'root',    # Replace with your MySQL username
    'password':'Djavivovgen',  # Replace with your MySQL password
    'database':'pokemons_db'      # Replace with your database name
}


def connect_to_database():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
