from dotenv import load_dotenv
from os import getenv
import requests
import json

from functions.cookies import carregarCookies, salvarCookies

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


cookies = carregarCookies()
if cookies:
    print(cookies)
else:
    cookies = fazer_login()
    salvarCookies(cookies)
