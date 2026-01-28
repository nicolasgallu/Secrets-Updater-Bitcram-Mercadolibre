import datetime
import requests
from logger import logger
from google.cloud import secretmanager
from notifications import enviar_mensaje_whapi
from settings import PROJECT_ID, SECRET_BITCRAM_ID, USER_BITCRAM, PASSWRD_BITCRAM, TOKEN_WHAPI, PHONE

def updating_bitcram_secrets():

    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{PROJECT_ID}/secrets/{SECRET_BITCRAM_ID}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        version = client.get_secret_version(request={"name": name})  

        #check vencimiento
        fecha_creacion = version.create_time 
        ahora = datetime.datetime.now(datetime.timezone.utc)
        antiguedad = ahora - fecha_creacion
        if antiguedad.days < 5:
            logger.info("Token still inside the time window of 5 days")
            return  None
        else:
            logger.info("Renovating Token")

            response = requests.post(
                "https://app.pos.bitcran.com/api/auth/",
                json={"username": USER_BITCRAM, "password": PASSWRD_BITCRAM}
            )

            response.raise_for_status()
            token = response.json()["token"]
            client.add_secret_version(
                parent=f"projects/{PROJECT_ID}/secrets/{SECRET_BITCRAM_ID}",
                payload={"data": token.encode("UTF-8")}
            )
            logger.info("Token Renovated Succesfully")
            
    except Exception as e:
        message = f"""Fallo en la renovacion del token de Bitcram el error fue: {e}"""
        enviar_mensaje_whapi(TOKEN_WHAPI, PHONE, message)