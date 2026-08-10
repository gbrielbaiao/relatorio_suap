from dotenv import load_dotenv
from os import getenv
import json

load_dotenv()
ARQUIVO_COOKIES = getenv("ARQUIVO_COOKIES")

def salvarCookies(cookies):
    cookiesJson = {
        "csrftoken": cookies["__Host-csrftoken"],
        "sessionid": cookies["__Host-sessionid"],
        "BIGipServerPOOL": cookies["BIGipServerPOOL-SUAP"],
        "TS01b01e68": cookies["TS01b01e68"]
    }

    with open(ARQUIVO_COOKIES, "w", encoding="utf-8") as arquivo:
        json.dump(cookiesJson, arquivo, ensure_ascii=False, indent=4)
    arquivo.close()

def carregarCookies() -> dict | None:
    try:
        with open(ARQUIVO_COOKIES, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
        arquivo.close()
        return dados
    except:
        return None