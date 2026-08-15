import json

def salvarArquivo(arquivo_nome: str, conteudo: dict | list | str) -> bool:
    try:
        with open(arquivo_nome, 'w', encoding="utf-8") as arquivo:
            if type(conteudo) in (dict, list):
                json.dump(conteudo, arquivo, indent=1, ensure_ascii=False) 
            else:
                arquivo.write(conteudo)

        return True
    except OSError as erro:
        print(f"Ocorreu um erro ao tentar salvar o arquivo ({arquivo_nome}):\n{erro}")
        return False

def lerArquivo(arquivo_nome: str) -> str | None:
    try:
        with open(arquivo_nome, 'r', encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            
        return conteudo
    except OSError as erro:
        print(f"Ocorreu um erro ao tentar ler o arquivo ({arquivo_nome}):\n{erro}")
        return