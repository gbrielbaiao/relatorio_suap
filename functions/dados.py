from selectolax.parser import HTMLParser
import json

from functions.arquivo import lerArquivo

def pegarTexto(no) -> str | None: # Essa função está sendo usada para coletar o texto dos elementos HTML.
    return str(no.text(strip=True)) if no else None

def coletarDadosBoletim(conteudo: str) -> dict | None:
    if not conteudo:
        return
    tree = HTMLParser(conteudo)

    campoNotas = tree.css_first("tbody")
    materias = campoNotas.css("tr")

    objMaterias = {}

    for idx, materia in enumerate(materias):
        disciplina = pegarTexto(materia.css_first('td[headers="th_disciplina"]'))
        frequencia = pegarTexto(materia.css_first('td[headers="th_frequencia"]'))
        situacao = pegarTexto(materia.css_first('td[headers="th_situacao"]'))

        bimestres = {}
        for i in range(1,5):
            nota_prova = pegarTexto(materia.css_first(f'td[headers="th_n{i}p"]')).replace('-','')
            nota_atitudinal = pegarTexto(materia.css_first(f'td[headers="th_n{i}a"]')).replace('-','')
            nota_bimestre = pegarTexto(materia.css_first(f'td[headers="th_n{i}n"]')).replace('-','')

            bimestres[i] = {
                "nota_prova": nota_prova.replace('-',''),
                "nota_atitudinal": nota_atitudinal.replace('-',''),
                "nota_bimestre": nota_bimestre.replace('-','')
            }
            
        nota_final = pegarTexto(materia.css_first('td[headers="th_mfd"]'))

        objMaterias[idx] = {
            "disciplina": disciplina.split('-')[1].strip(),
            "frequencia": frequencia.replace('-',''),
            "situacao": situacao.replace('-',''),
            "bimestres": bimestres,
            "nota_final": nota_final.replace('-','')
        }
    return objMaterias

def tratarDados() -> list:
    conteudoArquivo = lerArquivo("dados/bruto/dados.json")
    dadosBruto: list[dict] = json.loads(conteudoArquivo)
    colunas = ["disciplina","frequencia","situacao","n1p","n1a","n1f","n2p","n2a","n2f","n3p","n3a","n3f","n4p","n4a","n4f","nf"]
    linhas = []

    for disciplinas in dadosBruto:
        for _, disciplina in disciplinas.items():
            linha = [
                disciplina["disciplina"],
                disciplina["frequencia"],
                disciplina["situacao"]
            ]

            for numero in range(1, 5):
                bimestre = disciplina["bimestres"][str(numero)]

                linha.extend([
                    bimestre["nota_prova"],
                    bimestre["nota_atitudinal"],
                    bimestre["nota_bimestre"]
                ])

            linha.append(disciplina["nota_final"])

            linhas.append(linha)

    return [colunas, linhas]
    