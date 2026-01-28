import requests
import json
from google.cloud import secretmanager
from logger import logger
from notifications import enviar_mensaje_whapi
from settings import PROJECT_ID, SECRET_MELI_ID, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, FIRST_CODE, TOKEN_WHAPI, PHONE

#JSON STRUCTURE TO SECRET MANAGER.
MELI_SECRETS = {
    'questions':{
        'CLIENT_ID':CLIENT_ID,
        'CLIENT_SECRET':CLIENT_SECRET,
        'CODE':None,
        'REDIRECT_URI':REDIRECT_URI,
        'TOKEN':None,
        'UPDATED_AT':None}}


def create_secrets(grant_type, code):
    payload = {
        "grant_type": grant_type,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }
    if grant_type == "authorization_code":
        payload["code"]= code
    else:
        payload["refresh_token"]= code
    logger.info("Making petition to Meradolibre.")
    response = requests.post("https://api.mercadolibre.com/oauth/token", data=payload).json()
    token = response['access_token']
    code = response['refresh_token']
    return token,code


def norm_secret(client, name):
    "normalizar response del secret manager"
    logger.info("Searching for Secrets in Secret Manager.")
    response = client.access_secret_version(request={"name": name})
    #decodificamos repsuesta y guardamos en formato json.
    response = response.payload.data.decode("UTF-8")
    try:
        response = json.loads(response)
        return response
    except:
        return response
    

def updating_meli_secrets():
    #searching token existence.
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{SECRET_MELI_ID}/versions/latest"
    
    try:
        response = norm_secret(client, name)
        if  'questions' not in response: #questions ya tiene los permisos necesarios para utilizar todas las operaciones de la API de Meli.
            logger.info("Creating token for the first time.")
            token,code = create_secrets(grant_type='authorization_code',code=FIRST_CODE)
            MELI_SECRETS['questions']['TOKEN'] = token
            MELI_SECRETS['questions']['CODE'] = code
            logger.info("Credentials Succesfully created.")
        else:
            #renovating token
            logger.info("Renovating token and refresh code.")
            code = response['questions']['CODE']
            token, code = create_secrets(grant_type='refresh_token',code=code)
            MELI_SECRETS['questions']['TOKEN'] = token
            MELI_SECRETS['questions']['CODE'] = code
            logger.info("Credentials Succesfully renovated.")


        logger.info("Saving creds in secret manager.")
        meli_secrets = json.dumps(MELI_SECRETS, indent=2).encode("UTF-8")
        client.add_secret_version(
            parent=f"projects/{PROJECT_ID}/secrets/{SECRET_MELI_ID}",
            payload= {"data":meli_secrets})
        
    except Exception as e:
        logger.info("token renovation failed")
        message = f"""Fallo en la renovacion del token de Mercadolibre el error fue: {e}"""
        enviar_mensaje_whapi(TOKEN_WHAPI, PHONE, message)

