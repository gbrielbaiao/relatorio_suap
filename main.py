from os import getenv

from functions.dados import coletarDadosBoletim
from functions.arquivo import salvarArquivo 
from functions.pagina import fazer_login, acessarPaginaBoletim

def main():
    session = fazer_login()
    if not session:
        return # Encerrando o código aqui, caso a sessão não seja criada.

    # Acessando as páginas para coletar os dados de cada periodo.
    periodos = ["2024_1", "2025_1", "2026_1"]
    boletimCompleto = []
    for periodo in periodos:
        url_boletim = f"https://suap.ifmt.edu.br/edu/aluno/{getenv("MATRICULA")}/?tab=boletim&ano_periodo={periodo}"
        paginaBoletim = acessarPaginaBoletim(url_boletim, session) # Código HTML da página.

        if not paginaBoletim:   
            print("A página do boletim pode não ter sido carregada.")
            return # Encerrando o código aqui, caso a página não seja carregada com sucesso.

        # Coletando os dados de cada periodo.
        boletimPeriodo = coletarDadosBoletim(paginaBoletim)
        boletimCompleto.append(boletimPeriodo)

    # Salvando o boletim completo, com todos os periodos.
    salvarArquivo("dados.json", boletimCompleto)

if __name__ == "__main__":
    main()