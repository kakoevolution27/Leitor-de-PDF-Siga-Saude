from openpyxl import Workbook
import pdfplumber
from Interfaces import InterfaceDeEscrita, InterfaceDeLeituraDeArquivo, InterfaceDeManipulacaoDoArquivo

class ManipuladorDePdf(InterfaceDeManipulacaoDoArquivo):
    dependencia = pdfplumber
    def abrir_arquivo(self, caminho_pdf):
        try:
            arquivo = self.dependencia.open(caminho_pdf)
            print("arquivo aberto com sucesso")
            return arquivo
        except Exception as e:
            print(f"Erro ao abrir o arquivo {caminho_pdf}: {e}")

    def fechar_arquivo(self, pdf:Workbook):
        try:
            pdf.close()
            print("arquivo fechado")
        except Exception as e:
            print("Erro ao fechar aqruivo {e}")
        

class LeituraDeArquivoPdfAgenda(InterfaceDeLeituraDeArquivo):
    def extrair_texto_segunda_coluna(self,PDF):
        retorno = []
        try:
            for pagina in PDF.pages:
                segunda_coluna_documento = (101.77,0,318.22,pagina.height)
                texto_extraido = pagina.within_bbox(segunda_coluna_documento).extract_text()
                texto_da_segunda_coluna_formatado = texto_extraido.replace('\n', ';')
                if texto_da_segunda_coluna_formatado: 
                     retorno.append(texto_da_segunda_coluna_formatado)
            return "".join(retorno)
        except Exception as e:
            print(f"Erro ao extrair segunda coluna: {e}")

    def extrair_texto_primeira_coluna(self, PDF):
        retorno = []
        try:
            for pagina in PDF.pages:
                primeira_coluna_documento = (50.77,0,110, pagina.height)
                texto__extraido = pagina.within_bbox(primeira_coluna_documento).extract_text()
                texto_da_primeira_coluna_formatado = texto__extraido.replace('\n', ';')
                if texto_da_primeira_coluna_formatado:
                    retorno.append(texto_da_primeira_coluna_formatado)
            return "".join(retorno)
        except Exception as e:
            print(f"Erro ao extrair primeira coluna {e}")
        

    def extrair_cabecalho(self, PDF):
        try:
            primeira_pagina = PDF.pages[0]
            cabecalho =  primeira_pagina.extract_text().split('\n')[0:6]
            return cabecalho
        except Exception as e:
            print(f"erro ao extrair o cabeçalho {e}")

    def extrair_texto_pdf(self, PDF):
        pass


class FormatadorDeDados():
    import pandas as pd
    dependencia = pd
    def limpar_conteudo(self, conteudo:str):

        pass

    def limpar_cabecalho(self, conteudo:str):
        linhas = conteudo.split(';')
        cabecalho = ";".join(linhas[0:5])
        return conteudo.replace(cabecalho, "")

    def limpar_telefone(self, conteudo:str):
        substituicoes = {
                "NÃO": "",
                "INFORMADO": "",
                "RESPONDEU": "",
                "(": "",
        }

        for chave, valor in substituicoes.items():
            conteudo = conteudo.replace(chave, valor)

        return conteudo
    def verificar_tamanho_das_listas(self, lista_de_listas):
        verificados = []
        for lista in lista_de_listas:
            verificados.append(len(lista))
        
        print(verificados)

    def isnum(self, s):
        return s.isdigit()

    def limpar_nomes(self, conteudo: list):
            nnarr_nomes = []
            for cont in conteudo:
                # Extrai os primeiros dois caracteres
                nome = cont[0:2]
                sep = nome[1].split()

                # Verifica se há mais de um item após o split
                if len(sep) > 1:
                    # Verifica se o primeiro item é um número
                    if self.isnum(sep[0]):
                        nome_final = nome[0]
                    else:
                        nome_final = nome[1]
                else:
                    nome_final = nome[0]

                # Adiciona ao resultado se o nome contiver um espaço
                if " " in nome_final:
                    nnarr_nomes.append(nome_final)

            return nnarr_nomes

    def gerarsep(self, arr:list):
    #é pra ser usada dentro de um loop for
    #encontra o numero do sus dentro de uma lista
        for i, linha in enumerate(arr):
            termos = linha.split()
            for termo in termos:
                # Verifica se o termo é um número
                if termo.isdigit():
                    return i
        return None

    def gerar_telefones(self, conteudo: list):
        lista = []
        lista2 = []
        for conte in conteudo:
            for cont in conte:
                # Verifica e processa os telefones de "Tel Com" e "Tel Cel"
                self._processar_telefone(cont, "Tel Com: ", lista2)
                self._processar_telefone(cont, "Tel Cel: ", lista)

        return lista, lista2

    def _processar_telefone(self, cont: str, tipo_tel: str, lista_destino: list):
    # Encontra o índice do telefone e processa
        index = cont.find(tipo_tel)
        if index != -1:
            index += len(tipo_tel)
            telefones = cont[index:].split("Tel Cont: ")[0]  # Pega a parte relevante antes de "Tel Cont"
            if telefones:
                lista_destino.append(telefones)
                
    def gerar_profissional(self, conteudo, cabecalho):
        # Extrai a parte do nome do profissional da string 'cabecalho[1]'
        index_inicial = cabecalho[1].find("Profissional: ")
        index_final = cabecalho[1].find(" CNS:")

        # Se o índice final não for encontrado, pegamos o nome até o final da string
        if index_final == -1:
            profissional = cabecalho[1][index_inicial:]
        else: 
            profissional = cabecalho[1][index_inicial: index_final].strip()

        # Cria a lista de profissionais com o nome extraído, repetido para cada item no conteúdo
        profissionais = [profissional] * len(conteudo)
        
        return profissionais

    def gerar_Data(self, conteudo, cabecalho):
        # Encontra a string "Agenda (LOCAL): " no cabeçalho
        index_inicial = cabecalho[4].find("Agenda (LOCAL): ")

        # Extrai a data, que está logo após "Agenda (LOCAL): "
        data = cabecalho[4][index_inicial:].split(" ")[2:]

        # Converte a data para uma string única e repete para o tamanho do conteúdo
        data_unificada = "".join(data)
        datas = [data_unificada] * len(conteudo)
        return datas

    def limparHora(self, conteudo:str):
        cont = conteudo.replace("end Hora", "").split(";")
        lista_filtrada = [elemento for elemento in cont if elemento]
        return lista_filtrada
        

    def gerar_sus(self, conteudo:list):
        arr_de_sus = []

        for cont in conteudo:
            # Verifica se a função 'gerarsep' retorna um índice válido
            index_sus = self.gerarsep(cont)
            if index_sus is not None:
                # Extraímos o SUS, que é a primeira palavra após o índice retornado
                sus = cont[index_sus].split(" ")[0]
                arr_de_sus.append(sus)
            else:
                # Se não encontrar o SUS, pode-se adicionar um valor default ou logar o erro
                print('SUS não encontrado na linha.')
                arr_de_sus.append('SUS não encontrado')

        return arr_de_sus

    def gerar_prontuario(self, conteudo:list):
        arr_de_prontuario = []
        for conte in conteudo:
            for cont in conte:
                index_prontuario = cont.find("Pront: ")
                if index_prontuario != -1:
                    prontuario = cont[index_prontuario:].split(" ")
                    arr_de_prontuario.append(prontuario[1])
        return arr_de_prontuario

    def gerar_data_nascimento(self, conteudo:list):
        arr_de_Dn = []
        for conte in conteudo:
            for cont in conte:
                index_Dn = cont.find("DN:")
                if index_Dn != -1:
                    dn = cont[index_Dn:13].split(":")
                    arr_de_Dn.append(dn[1])
        return arr_de_Dn


    def formatar_dados(self, conteudo:str):
       #deve ser executada primeiro
       #transforma os dados em uma lista de dados base para as outras funções
       linhas = conteudo.split(";")
       narr = []
       array = []

       for linha in linhas:
            array.append(linha)
            if "Mãe: " in linha:
                narr.append(array)
                array = []
                continue
       return narr

class EscritorDeTexto():
    def escrever_texto(self, data):
        #texto = f"Olá, *{data["nome"]}* Somos da AMA/UBSi JARDIM CASTRO ALVES \n \nViemos por esse meio relembrar que sua consulta com *{}*, será em: *{}* às *{}*. \n\nOBS: A falta prejudica os demais pacientes que estão em fila aguardando o atendimento.\n\n*OBRIGATORIO chegar com antecedência de 30 min.*\n*Atrasos serão tolerados até 5 minutos. após o período de tolerância o atendimento não é garantido*\n*Obrigatório trazer cartão do SUS, documento com foto* \nWa.me/5511«TEL_1» \nWa.me/5511«TEL_2»"
        pass
 
    

    
        
    