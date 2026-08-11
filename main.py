from dotenv import load_dotenv
from os import getenv
import requests

from lerpagina import dadosBoletim

load_dotenv()

def fazer_login():
    url_login = "https://suap.ifmt.edu.br/accounts/login/?next=/"
    MATRICULA = getenv("MATRICULA")
    SENHA = getenv("SENHA")

    session = requests.Session()

    session.get(url_login)
    csrftoken = session.cookies.get("__Host-csrftoken")

    if not csrftoken:
        print("Não consegui obter o csrftoken.") 
        return None

    payload = {
        "username": MATRICULA,
        "password": SENHA,
        "csrfmiddlewaretoken": csrftoken,
    }
    headers = {
        "Referer": url_login,
    }
    session.post(url_login, data=payload, headers=headers)

    print("Login realizado com sucesso!")
    return session

def acessarBoletim(url, session) -> str | None:
    res = session.get(url)
    if not res: return None
    if res.status_code != 200: return None
    return res.content.decode()

def main():
    session = fazer_login()
    if not session:
        return # Encerrando a função aqui caso a sessão não seja iniciada.

    periodos = ["2024_1", "2025_1", "2026_1"]
    for periodo in periodos:
        url_boletim = f"https://suap.ifmt.edu.br/edu/aluno/{getenv("MATRICULA")}/?tab=boletim&ano_periodo={periodo}"
        paginaBoletim = session.get(url_boletim).content.decode() # Código HTML da página.w

        if not paginaBoletim:   
            return

        with open(f'paginaboletin-{periodo}.html', 'w', encoding="utf-8") as arquivo:
            arquivo.write(paginaBoletim)
        arquivo.close()

    dadosBoletim("paginaboletin-2024_1.html")

if __name__ == "__main__":
    main()