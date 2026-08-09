from dotenv import load_dotenv
from os import getenv
import requests

load_dotenv()

def fazer_login():
    url_login = "https://suap.ifmt.edu.br/accounts/login/?next=/"
    EMAIL = getenv("EMAIL")
    SENHA = getenv("SENHA")

    parametros = {
        "username": EMAIL,
        "password": SENHA
    }

    return requests.get(url_login, parametros)
