
# import requests
import random
import mysql.connector
from apiHandle import fetch_pokemons_data, fetch_single_pokemon_details
from dbConfig import connect_to_database


conn = connect_to_database()
    
def select_random_pokemon():

    pokemon_list = fetch_pokemons_data()

    # randomly select a Pokémon from the list
    random_pokemon = random.choice(pokemon_list)
    random_pokemon_name = random_pokemon['name']
    print('Random Pokemon was chosen.')

    # print(random_pokemon_name)
    return random_pokemon_name



def check_if_pokemon_in_database(random_pokemon_name):

    conn = connect_to_database()
    if conn is None:
        return
    
    cursor = conn.cursor(dictionary=True)


    # check if Pokémon name is already in database

    query = "SELECT * FROM pokemon_table WHERE name = %s"
    cursor.execute(query, (random_pokemon_name,))
    pokemon = cursor.fetchone()

    if pokemon:
        print('Found match!')
        print('-----------Pokemon details from database------')
        print(f"Pokémon: {pokemon['name']}\nID: {pokemon['id']}\nHeight: {pokemon['height']}\nWeight: {pokemon['weight']}")
    else:
        print('Error: Pokémon name is not found in the database. Fetching details...')
        pokemon_details = fetch_single_pokemon_details(random_pokemon_name)
        save_pokemon_to_mysql(pokemon_details)

    cursor.close()
    conn.close()



def save_pokemon_to_mysql(pokemon_details):
    conn = connect_to_database()
    if conn is None:
        return

    cursor = conn.cursor()

    # Create a table for storing Pokémon details if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS pokemon_table (
        id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        height INT NOT NULL,
        weight INT NOT NULL
    )
    """
    cursor.execute(create_table_query)

    # Insert Pokémon details into the MySQL table
    insert_query = """
    INSERT INTO pokemon_table (id, name, height, weight)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        height = VALUES(height),
        weight = VALUES(weight)
    """
    values = (pokemon_details['id'], pokemon_details['name'], pokemon_details['height'], pokemon_details['weight'])

    try:
        cursor.execute(insert_query, values)
        conn.commit()
        print(f'Success: Pokémon "{pokemon_details["name"]}" details saved to MySQL database!')
    except mysql.connector.Error as err:
        print(f"Error while inserting data: {err}")
    finally:
        cursor.close()
        conn.close()




def main():

    while True:
        userValue = input("Would you like to draw a Pokemon? yes/ no?: ").lower()
        if userValue == 'yes':
            random_pokemon_name = select_random_pokemon()
            check_if_pokemon_in_database(random_pokemon_name)
            break
        elif userValue == 'no':
            print('Goodbye, exiting...')
        
        else:
            print('Enter only yes or no')

main()