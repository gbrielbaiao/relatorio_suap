from selectolax.parser import HTMLParser

from functions.arquivo import *

def pegarTexto(no): # Essa função está sendo usada para coletar o texto dos elementos HTML.
    return str(no.text(strip=True)) if no else None

def coletarDadosBoletim(arquivo_nome: str) -> dict:
    pagina = lerArquivo(arquivo_nome)
    if pagina["status"] != 200:
        return None
    tree = HTMLParser(pagina["conteudo"])

    campoNotas = tree.css_first("tbody")
    materias = campoNotas.css("tr")

    objMaterias = {}

    for idx, materia in enumerate(materias):
        disciplina = pegarTexto(materia.css_first('td[headers="th_disciplina"]'))
        frequencia = pegarTexto(materia.css_first('td[headers="th_frequencia"]'))
        situacao = pegarTexto(materia.css_first('td[headers="th_situacao"]'))

        bimestres = {}
        for i in range(1,5):
            nota_prova = pegarTexto(materia.css_first(f'td[headers="th_n{i}p"]'))
            nota_atitudinal = pegarTexto(materia.css_first(f'td[headers="th_n{i}a"]'))
            nota_bimestre = pegarTexto(materia.css_first(f'td[headers="th_n{i}n"]'))

            bimestres[i] = {
                "nota_prova": nota_prova,
                "nota_atitudina": nota_atitudinal,
                "nota_bimestre": nota_bimestre
            }
        nota_final = pegarTexto(materia.css_first('td[headers="th_mfd"]'))

        objMaterias[idx] = {
            "disciplina": disciplina.split('-')[1].strip(),
            "frequencia": frequencia,
            "situacao": situacao,
            "bimestres": bimestres,
            "nota_final": nota_final
        }
    return objMaterias

# coletarDadosBoletim("paginaboletin-2024_1.html") 
# A linha de código acima esta sendo usada apenas para testes.
# Quando a funcionalidade estivar pronta ela sera removida