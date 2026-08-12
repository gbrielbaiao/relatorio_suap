import json

def salvarArquivo(arquivo_nome: str, conteudo: dict | str) -> dict:
    try:
        with open(arquivo_nome, 'w', encoding="utf-8") as arquivo:
            if type(conteudo) == dict:
                json.dump(conteudo, arquivo, indent=4, ensure_ascii=False) 
            else:
                arquivo.write(conteudo)

        return {"status": 200}
    except OSError as erro:
        print(f"Ocorreu um erro ao tentar salvar o arquivo ({arquivo_nome}):\n{erro}")
        return {"status": 500}

def lerArquivo(arquivo_nome: str) -> dict:
    try:
        with open(arquivo_nome, 'r', encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
            
        return {"status": 200, "conteudo": conteudo}
    except OSError as erro:
        print(f"Ocorreu um erro ao tentar ler o arquivo ({arquivo_nome}):\n{erro}")
        return {"status": 500}