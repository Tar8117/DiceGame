from os import getenv

from dotenv import load_dotenv

load_dotenv()

bot_token = getenv('BOT_TOKEN')
if not bot_token:
    exit('Error: no token provided')
