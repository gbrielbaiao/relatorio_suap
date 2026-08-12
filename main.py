from dotenv import load_dotenv
from os import getenv
import requests

from functions.boletim import coletarDadosBoletim
from functions.arquivo import salvarArquivo

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

def acessarPaginaBoletim(url, session) -> str | None:
    # Essa função deve coletar o conteúdo da página e retornar o 
    # conteudo no formato de String, ao invés de Bytes.

    res = session.get(url)
    if not res: return None
    if res.status_code != 200: return None
    return res.content.decode()

def main():
    session = fazer_login()
    if not session:
        return # Encerrando o código aqui, caso a sessão não seja criada.

    # Acessando as páginas para coletar os dados de cada periodo.
    periodos = ["2024_1", "2025_1", "2026_1"]
    boletimCompleto = {}
    for idx, periodo in enumerate(periodos):
        url_boletim = f"https://suap.ifmt.edu.br/edu/aluno/{getenv("MATRICULA")}/?tab=boletim&ano_periodo={periodo}"
        paginaBoletim = session.get(url_boletim).content.decode() # Código HTML da página.

        if not paginaBoletim:   
            return # Encerrando o código aqui, caso a página não seja carregada com sucesso.

        salvarArquivo(f"paginaboletin-{periodo}.html", paginaBoletim)

        # Coletando os dados de cada periodo.
        boletimPeriodo = coletarDadosBoletim(f"paginaboletin-{periodo}.html")
        boletimCompleto[idx] = boletimPeriodo
        
    # Salvando o boletim completo, com todos os periodos.
    salvarArquivo("dados.json", boletimCompleto)

if __name__ == "__main__":
    main()