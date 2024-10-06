import requests
import mysql.connector
from dbConfig import connect_to_database

base_url =  'https://pokeapi.co/api/v2/pokemon'
limit = 200
url=f"{base_url}?limit={limit}"


def fetch_pokemons_data():

    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
    else:
        print(f'Error: fetching data failed! {res.status_code}')

    pokemon_list = data['results']
    return pokemon_list



def fetch_single_pokemon_details(random_pokemon_name):

    res = requests.get(f'{base_url}/{random_pokemon_name}')
    if res.status_code == 200:
        data = res.json()
    else:
        print(f'Error: fetching data failed! {res.status_code}')
   
    pokemon_details_data = data

    # Pokemon types values 
    pokemon_type_names  = []
    for type in pokemon_details_data['types']:
        pokemon_type_names.append(type['type']['name'])

    
    # extract pokemon another values 
    # object to be appended
    pokemon_details = {
        "id": pokemon_details_data['id'],
        "name": pokemon_details_data['name'],
        "height": pokemon_details_data['height'],
        "weight": pokemon_details_data['weight'],
        "types": pokemon_type_names
    }

    return pokemon_details




def save_pokemon_to_mysql():
    pokemon_details = fetch_single_pokemon_details()
    conn = connect_to_database()

    # try:
    #     conn = mysql.connector.connect(**DB_CONFIG)
    
    # except mysql.connector.Error as err:
    #     print(f"Error: {err}")
    #     return
    


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
        # Commit the transaction
        conn.commit()
        
        # print('success, Pokemon details saved to database!')
        # print('---------Pokemon details:-------------------')
        # print(f"Pokémon: {name}\nID: {id}\nHeight: {height}\nWeight: {weight} \nTypes: {pokemon_type_names}")

        print('success, Pokemon details saved to MySQL database!')
        print('---------Pokemon details:-------------------')
        print(f'Pokémon "{pokemon_details["name"]}"')
    except mysql.connector.Error as err:
        print(f"Error while inserting data: {err}")
    finally:
        # Close the connection
        cursor.close()
        conn.close()