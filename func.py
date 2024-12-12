import pdfplumber
from openpyxl import Workbook
import re

def abrir_arquivo(caminho_pdf):
    print("arquivo aberto")
    return pdfplumber.open(caminho_pdf)

def extrair_numero_de_paginas(pdf):
    numero_de_paginas = len(pdf.pages)
    return numero_de_paginas

def extrair_texto_pdf(pdf):
    texto = "" 
    for pagina in pdf.pages: 
        texto += pagina.extract_text()
    return texto


def ext_teste(pdf):
    txt = []
    str = ""
    for pagina in pdf.pages:
        segunda_coluna_documento = (101.77,0,318.22,pagina.height)
        texto_da_segunda_coluna = pagina.within_bbox(segunda_coluna_documento).extract_text()
        txt.append(texto_da_segunda_coluna)
    return str.join(txt)
    

def extrair_cabecalho(pdf):
    primeira_pagina = pdf.pages[0]
    cabecalho =  primeira_pagina.extract_text().split('\n')[0:6]
    return cabecalho

def fechar_arquivo(pdf):
      pdf.close()
      print("arquivo fechado com sucesso")

def limpar_cabecalho(cabecalho, texto):
    texto_limpo = texto.replace(cabecalho, "")
    return texto_limpo

def limpar_paginas(num_de_paginas, texto_sem_cabecalho:str):
    #limpa a grafia "Pagina (n) de(n)" no texto
    texto_limpo = texto_sem_cabecalho 
    for num in range(num_de_paginas): 
        grafia = f"Pagina {num + 1} de{num_de_paginas}" 
        texto_limpo = texto_limpo.replace(grafia, "") 
    return texto_limpo


def escrever_arquivo_txt(numero_do_caminho, nome_do_arquivo, conteudo_do_arquivo):
     conteudo_do_arquivo_str = "".join(conteudo_do_arquivo)
     with open(f"{nome_do_arquivo}{numero_do_caminho}.txt", "w") as arquivo:
        arquivo.write(conteudo_do_arquivo_str)

def encontrar_profissional(cabecalho):
    indice = cabecalho[1].find("CNS:")
    if indice != -1:
        profissional = cabecalho[1][14:indice]
    else: 
        profissional = cabecalho[1][14:]
    return profissional
def encontrar_data(cabecalho):
    data = cabecalho[4][16:]

def criar_arquivo_excel():
    workbook = Workbook() 
    return workbook

def criar_sheet(workbook: Workbook, cabecalho):
    sheet = workbook.active
    sheet.title = f"Agendas {encontrar_data(cabecalho)}"
    return sheet
    
def salvar_arquivo_excel(numero_da_iteracao, workbook):
    workbook.save(f"AGENDAS{numero_da_iteracao}.xlsx")

def escrever_arquivo_Excel(conteudo, sheet):
        for linha in conteudo:
            sheet.append(linha)
        #sheet.append(conteudo)

def formatar_dados(dados):
    padrao = re.compile( r"(.*?(?:030101011-0\s?-.*?\n.*?)?Mãe:.*?)(?=\n(?:.*?(?:030101011-0|030101006-4|030101950-9|030101007-2).*)|\Z)", re.DOTALL)
    registros = padrao.findall(dados) 
    retorno = []
    for registro in registros:
        lista = registro.split("\n")
        retorno.append(lista)
    return retorno

def escrever_Planilha(texto_final, cabecalho, index_dos_caminhos):
        conteudo = formatar_dados(texto_final)
        workbook = criar_arquivo_excel()
        sheet = criar_sheet(workbook, cabecalho)
        escrever_arquivo_Excel(conteudo, sheet)
        salvar_arquivo_excel(index_dos_caminhos,workbook)
