from os import getenv, remove as removerArquivo
from dotenv import load_dotenv

import requests
load_dotenv()

def fazer_login():
    # Essa função ira criar uma sessão para que proximas interassões com o site (SUAP) 
    # sejam feitas mais facilmente.

    url_login = "https://suap.ifmt.edu.br/accounts/login/?next=/"
    MATRICULA = getenv("MATRICULA")
    SENHA = getenv("SENHA")

    session = requests.Session()

    session.get(url_login)
    csrftoken = session.cookies.get("__Host-csrftoken")

    if not csrftoken:
        print("Não consegui obter o csrftoken.") 
        return 

    payload = {
        "username": MATRICULA,
        "password": SENHA,
        "csrfmiddlewaretoken": csrftoken,
    }
    headers = {
        "Referer": url_login,
    }
    res = session.post(url_login, data=payload, headers=headers)

    if not res.url == "https://suap.ifmt.edu.br/":
        print("Erro ao fazer login.")
        return  

    print("Login realizado com sucesso!")
    return session

def acessarPaginaBoletim(url, session) -> str | None:
    # Essa função deve coletar o conteúdo da página e retornar o 
    # conteudo no formato de String, ao invés de Bytes.

    res = session.get(url)
    if not res.ok: return 
    if res.status_code != 200: return 
    return res.content.decode()