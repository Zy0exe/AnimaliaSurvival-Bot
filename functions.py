from functions import *
from import_lib import *

animals = {
    "Lion": {
        "price": 30000,
        "image": "",
        "slot": "1",
        "quantity": 0,
        "gender": "",
        #"kind": "carn"
    },
    "Crocodille": {
        "price": 25000,
        "image": "",
        "slot": "2",
        "quantity": 0,
        "gender": "",
        #"kind": "carn"
    },
    "Elephant": {
        "price": 25000, 
        "image": "", 
        "slot": "3", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "Giraffe": {
        "price": 20000, 
        "image": "", 
        "slot": "4", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "Hippopotamus": {
        "price": 20000, 
        "image": "", 
        "slot": "5", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "Hyena": {
        "price": 15000, 
        "image": "", 
        "slot": "6", 
        "quantity": 0, 
        "gender": "",
        #"kind": "carn"
    },
    "Leopard": {
        "price": 20000, 
        "image": "", 
        "slot": "7", 
        "quantity": 0, 
        "gender": "",
        #"kind": "carn"
    },
    "Meerkat": {
        "price": 3000, 
        "image": "", 
        "slot": "8", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "Rhinoceros": {
        "price": 20000, 
        "image": "", 
        "slot": "9", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "Wildebeest": {
        "price": 15000, 
        "image": "",  #<:wildbeest:1188049123165868042>
        "slot": "10", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
    "WildDog": {
        "price": 20000, 
        "image": "", 
        "slot": "11", 
        "quantity": 0, 
        "gender": "",
        #"kind": "carn"
    },
    "Zebra": {
        "price": 15000, 
        "image": "", 
        "slot": "12", 
        "quantity": 0, 
        "gender": "",
        #"kind": "herb"
    },
}

# Connect to the database
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="animalia_bot"
)

# Where the bot can be used
def in_animal_shop(ctx):
    return ctx.channel.name == os.getenv("BOT_CHANNEL")

# Where the bot can be used
def in_og_chan(ctx):
    return ctx.channel.name == os.getenv("VIP_CHANNEL")

# object hook
def object_hook(d):
    for key, value in d.items():
        if isinstance(value, list):
            d[key] = tuple(value)
    return d

def get_player_data(discord_id):
    db = mysql.connector.connect(
        host=os.getenv("DATABASE_HOST"), user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PW"), database=os.getenv("DATABASE_NAME")
    )
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM players WHERE discord_id = %s", (discord_id,))
        result = cursor.fetchone()
        cursor.close()
        db.close()

        if result is None:
            return None

        last_work_time = result.get("last_work_time", datetime.min)
        voice_start_time = result.get("voice_start_time", datetime.min)
        last_voice_time = result.get("last_voice_time", datetime.min)

        player_data = {
            "steam_id": result["steam_id"],
            "discord_id": result["discord_id"],
            "coins": result["coins"],
            "animals": result["animals"],
            "last_work_time": last_work_time,
            "voice_start_time": voice_start_time,
            "last_voice_time": last_voice_time,
        }

        print(f"DEBUG: {discord_id} has {player_data['coins']} coins.")
        return player_data

    except mysql.connector.Error as e:
        print(f"DEBUG: Error during database query: {e}")
        return None


def save_player_data(discord_id, player_data):
    db = mysql.connector.connect(
        host=os.getenv("DATABASE_HOST"), user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PW"), database=os.getenv("DATABASE_NAME")
    )
    cursor = db.cursor()

    # Update the user data in the database
    cursor.execute(
        "UPDATE players SET coins = %s, animals = %s, last_work_time = %s, voice_start_time = %s, last_voice_time = %s WHERE discord_id = %s",
        (
            player_data["coins"],
            player_data["animals"],
            player_data["last_work_time"],
            player_data.get("voice_start_time", None),
            player_data.get("last_voice_time", None),
            discord_id,
        ),
    )

    db.commit()
    cursor.close()
    db.close()

    print(f"DEBUG: User {discord_id} data saved to the database")


# Function to clear the players cage
def clear_player_animals(discord_id):
    # Retrieve player data from the database
    player_data = get_player_data(discord_id)
    if not player_data:
        return False

    # Clear the player's animal inventory in the database
    db = mysql.connector.connect(
        host=os.getenv("DATABASE_HOST"), user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PW"), database=os.getenv("DATABASE_NAME")
    )
    cursor = db.cursor()
    cursor.execute("UPDATE players SET animals = NULL WHERE discord_id = %s", (discord_id,))
    db.commit()

    return True

# Function to retrieve animals data from the database
def get_player_animals(discord_id):
    db = mysql.connector.connect(
        host=os.getenv("DATABASE_HOST"), user=os.getenv("DATABASE_USER"), password=os.getenv("DATABASE_PW"), database=os.getenv("DATABASE_NAME")
    )
    cursor = db.cursor()
    cursor.execute("SELECT animals FROM players WHERE discord_id = %s", (discord_id,))
    player_data = cursor.fetchone()
    if player_data is None:
        return {}

    if player_data[0] is not None:
        try:
            player_animals = json.loads(player_data[0], object_hook=object_hook)
        except json.decoder.JSONDecodeError as e:
            traceback.print_exc()
            player_animals = {}
    else:
        player_animals = {}

    return player_animals

cursor = db.cursor()