from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_CONFIG = {
    'HOST': os.getenv('MYSQL_HOST'),
    'USER': os.getenv('MYSQL_USER'),
    'PASSWORD': os.getenv('MYSQL_PASSWORD'),
    'DATABASE': os.getenv('MYSQL_DATABASE')
}

CONNECT_MYSQL_STRING = (
    f"mysql+pymysql://"
    f"{MYSQL_CONFIG['USER']}:"  
    f"{MYSQL_CONFIG['PASSWORD']}@"  
    f"{MYSQL_CONFIG['HOST']}/" 
    f"{MYSQL_CONFIG['DATABASE']}"
)
