import os
from dotenv import load_dotenv
load_dotenv()

PROJECT_ID=os.getenv("PROJECT_ID")
SECRET_BITCRAM_ID=os.getenv("SECRET_BITCRAM_ID")
SECRET_MELI_ID=os.getenv("SECRET_MELI_ID")

CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")
REDIRECT_URI=os.getenv("REDIRECT_URI")
FIRST_CODE=os.getenv("FIRST_CODE")

USER_BITCRAM=os.getenv("USER_BITCRAM")
PASSWRD_BITCRAM=os.getenv("PASSWRD_BITCRAM")

TOKEN_WHAPI=os.getenv("TOKEN_WHAPI")
PHONE=os.getenv("PHONE")

RUN_BITCRAM=os.getenv("RUN_BITCRAM")