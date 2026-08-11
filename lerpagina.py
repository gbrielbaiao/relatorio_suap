from selectolax.parser import HTMLParser
import json

def pegar_texto(no): # Essa função está sendo usada para coletar o texto dos elementos HTML.
    return str(no.text(strip=True)) if no else None

def lerArquivo(arquivo_nome: str) -> str:
    try:
        with open(arquivo_nome, 'r', encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
        arquivo.close()
        return conteudo
    except:
        return None

def dadosBoletim(arquivo_nome: str) -> dict:
    # Essa função não está finalizada.
    # Ela ainda está sendo testada.

    pagina = lerArquivo(arquivo_nome)
    tree = HTMLParser(pagina)
    if not pagina:
        return None

    campoNotas = tree.css_first("tbody")
    materias = campoNotas.css("tr")

    objMaterias = {}

    for idx, materia in enumerate(materias):
        disciplina = pegar_texto(materia.css_first('td[headers="th_disciplina"]'))
        frequencia = pegar_texto(materia.css_first('td[headers="th_frequencia"]'))
        situacao = pegar_texto(materia.css_first('td[headers="th_situacao"]'))

        bimestres = {}
        for i in range(1,5):
            nota_prova = pegar_texto(materia.css_first(f'td[headers="th_n{i}p"]'))
            nota_atitudinal = pegar_texto(materia.css_first(f'td[headers="th_n{i}a"]'))
            nota_bimestre = pegar_texto(materia.css_first(f'td[headers="th_n{i}n"]'))

            bimestres[i] = {
                "nota_prova": nota_prova,
                "nota_atitudina": nota_atitudinal,
                "nota_bimestre": nota_bimestre
            }
        nota_final = pegar_texto(materia.css_first('td[headers="th_mfd"]'))

        objMaterias[idx] = {
            "disciplina": disciplina.split('-')[1].strip(),
            "frequencia": frequencia,
            "situacao": situacao,
            "bimestres": bimestres,
            "nota_final": nota_final
        }
        # Linhas de depuração:
        # print(pegar_texto(disciplina).split("-")[1].strip())
        # print(pegar_texto(frequencia))
        # print() 

    # Irei salvar o o Objeto em um arquivo json para conseguir vizualizar os dados de forma mais simples.
    with open('dados.json', 'w', encoding='utf-8') as arquivo:
        json.dump(objMaterias, arquivo, indent=4, ensure_ascii=False)

dadosBoletim("paginaboletin-2024_1.html") 
# A linha de código acima esta sendo usada apenas para testes.
# Quando a funcionalidade estivar pronta ela sera removida