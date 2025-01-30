import pdfplumber
from datetime import datetime
import re
import json
import pandas as pd
import tkinter as tk
import os
from tkinter import filedialog

def abrir_arquivo(caminho_pdf:str):
    arquivo = pdfplumber.open(caminho_pdf)
    try:
        return arquivo
    except Exception as e:
        print(f"o arquivo não foi aberto {e}")

def escolher_pasta():
    root = tk.Tk()
    root.withdraw()

    pasta_selecionada = filedialog.askdirectory(title="selecione a pasta de destino")

    if pasta_selecionada:
        return os.path.join(pasta_selecionada)
    else:
        return None    

def recuperar_caminho_do_arquivo(path_pasta):
    paths = []
    for root, dirs, files in os.walk(path_pasta):
        for file in files:
            if file.endswith('.pdf'):
                caminho_completo = os.path.join(root,file)
                paths.append(caminho_completo)
    return paths

def fechar_arquivo(pdf):
    pdf.close()
    print("arquivo fechado com sucesso")

def extrair_texto_pdf(pdf: pdfplumber.PDF):
    retorno = ""
    for pagina in pdf.pages:
        coluna_de_dados = (50.77,0,315.200,pagina.height)
        texto = pagina.within_bbox(coluna_de_dados).extract_text()
        retorno += texto
    return retorno


def gerar_profissional(conteudo, cabecalho):
        # Extrai a parte do nome do profissional da string 'cabecalho[1]'
        index_inicial = cabecalho[1].find("Profissional: ")
        index_final = cabecalho[1].find(" CNS:")

        # Se o índice final não for encontrado, pegamos o nome até o final da string
        if index_final == -1:
            profissional = cabecalho[1][index_inicial:]
        else: 
            profissional = cabecalho[1][index_inicial: index_final].strip()

        # Cria a lista de profissionais com o nome extraído, repetido para cada item no conteúdo
        profissionais = [profissional] * (len(conteudo) - 1)
        
        return profissionais

#string1 = "HEITOR VALENTIN DE ALBUQUERQUE\n17:30\nQUEIROZ\n898006261025489 Pront: 22997\nDN:16/10/2021 Idade: 3 R/C: PRETA\nTel Cel: 11 980206612 Tel Res: 11 983698237\nTel Com: NÃO INFORMADO Tel Cont: 11\n954807357\nMãe: FLAVIA ALBUQUERQUE DE ARAUJO\n"

def formatar_nomes(texto):
    s = ""
    lista = texto.split("\n")
    
    for index, item in enumerate(lista):
        if ":" in item:
            if _horario_valido(item):
                s += "Nome: " + lista[index - 1] + "\n"
            else:
                continue

    s_array = s.split("Nome: ")
    
    s_array = [item for item in s_array if ":" not in item and "Mãe: " not in item]
    return "".join(s_array)

def _horario_valido(texto):
    try:
        datetime.strptime(texto, "%H:%M").time()
        return True
    except ValueError:
        return False

def eliminar_horarios_invalidos(texto):
    s = ""
    lista = texto.split("\n")

    index = 0
    while index < len(lista):
        item = lista[index]
        if _horario_valido(item):
            if index >= 0 and "Mãe: " in lista[index - 1]:
                del lista[index]  # Deleta o item inválido
                # Não incrementa o index aqui, pois queremos reprocessar o próximo item
                continue
            else:
                if _horario_valido(lista[(index + 1)]):
                    del lista[(index - 1)]
                    del lista[index]
                    index -= 1
                else:
                    s += item + "\n"
                    index += 1  # Avança para o próximo item
        else:
            index += 1  # Avança para o próximo item
    return s

def extrair_cabecalho(PDF):
        try:
            primeira_pagina = PDF.pages[0]
            cabecalho =  primeira_pagina.extract_text().split('\n')[0:6]
            return cabecalho
        except Exception as e:
            print(f"erro ao extrair o cabeçalho {e}")

def extrair_telefone(texto):
    lista = texto.split("\n")
    tels = []
    for index, item in enumerate(lista):
        res = []
        index_tel_cel = item.find("Tel Cel: ")
        index_tel_Res = item.find("Tel Res: ")
        if index_tel_cel != -1:
            tel_cel = lista[index][index_tel_cel + 12: index_tel_cel + 8 + 13]
            res.append(tel_cel)
        if index_tel_Res != -1:
            tel_res = lista[index][index_tel_Res + 12: index_tel_Res + 8 + 13]
            res.append(tel_res)
        if len(res) != 0:
            tels.append(res)
    return tels

def _isnum(string):
    return string.isdigit()

def gerar_Data(conteudo, cabecalho):
    # Encontra a string "Agenda (LOCAL): " no cabeçalho
    index_inicial = cabecalho[4].find("Agenda (LOCAL): ")

    # Extrai a data, que está logo após "Agenda (LOCAL): "
    data = cabecalho[4][index_inicial:].split(" ")[2:]

     # Converte a data para uma string única e repete para o tamanho do conteúdo
    data_unificada = "".join(data)
    datas = [data_unificada] * (len(conteudo) - 1)
    return datas

def gerarsep(texto:str):
    arr = texto.split("\n")
    #é pra ser usada dentro de um loop for
    #encontra o numero do sus dentro de uma lista
    for i, linha in enumerate(arr):
        termos = linha.split()
        for termo in termos:
            # Verifica se o termo é um número
            if termo.isdigit():
                return i
    return None

def gerar_sus(texto:str):
        arr_de_sus = []
        conteudo = texto.split("\n")
        for cont in conteudo:
            # Verifica se a função 'gerarsep' retorna um índice válido
            index_sus = gerarsep(cont)
            if index_sus is not None:
                # Extraímos o SUS, que é a primeira palavra após o índice retornado
                sus = cont[index_sus].split(" ")[0]
                arr_de_sus.append(sus)
            else:
                # Se não encontrar o SUS, pode-se adicionar um valor default ou logar o erro
                print('SUS não encontrado na linha.')
                arr_de_sus.append('SUS não encontrado')

        return arr_de_sus

def filtrar_telefones(lista_de_listas):
    #filtra a lista de telefones para garantir que só havera numeros ou string vazias (caso o paciente não tenha numero)
    for index, lista in enumerate(lista_de_listas):   
        for index , item in enumerate(lista):
            if _isnum(item.strip()):
                continue
            else:
                del lista[index]
    return lista_de_listas

def limpar_cabecalho(conteudo:str):
    linhas = conteudo.split('\n')
    cabecalho = "\n".join(linhas[0:5])
    res = conteudo.replace(cabecalho, "")
    return res

#pasta_selecionada = escolher_pasta()
#paths = recuperar_caminho_do_arquivo(pasta_selecionada)

#PRIMEIRO TESTE COM "C:\Users\Kaio\Desktop\agenda\27.01.2025\REL_IMP_AGD_PROF_LOCAL_2787253_20250124144401_1555293423515468.pdf" / PASSOU COM ACURACIA DE 100%
#for index, path in enumerate(paths):
#
#    arquivo = abrir_arquivo(path)
#
#    string1 = extrair_texto_pdf(arquivo)
#    base = limpar_cabecalho(string1)
#    
#
#    nomes = formatar_nomes(base).split("\n")
#    horarios = eliminar_horarios_invalidos(base).split("\n")
#    tels = extrair_telefone(base)
#    tel_final = filtrar_telefones(tels)
#
#    dados = {
#        "nomes": pd.Series(nomes),
#        "horarios": pd.Series(horarios),
#        "tels": pd.Series(tels)
#    }
#
#   df = pd.DataFrame(dados)
    #escritor.escrever_texto()
#    df.to_csv(fr"C:\Users\Kaio\Desktop\RESIDUOS\agenda{index}.csv", index=False, sep=";")
#
#   fechar_arquivo(arquivo)
    

    