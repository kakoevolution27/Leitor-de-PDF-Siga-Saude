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
            try:
                int(s)
                return True
            except ValueError:
                return False

    def limpar_nomes(self, conteudo: list):
                arr_de_nomes = []
                narr_de_nomes = []
                nnarr_nomes = []
    
                for cont in conteudo:
                    arr_de_nomes.append(cont[0:2])

                for nome in arr_de_nomes:
                    sep = nome[1].split(" ") 
                    if len(sep) > 1:
                        if self.isnum(sep[0]):
                            narr_de_nomes.append(nome[0])
                        else:
                            narr_de_nomes.append(nome[1])
                    else:
                        narr_de_nomes.append(nome[0])


                for nome in narr_de_nomes:
                    if " " in nome:
                        nnarr_nomes.append(nome)
                    else: 
                        continue

                return nnarr_nomes

    def gerarsep(self, arr:list):
    #é pra ser usada dentro de um loop for
    #encontra o numero do sus dentro de uma lista
        for i, linha in enumerate(arr):
            termos = linha.split(" ")
            for j, ter in enumerate(termos):
                try:
                    int(ter)
                    return i
                except ValueError:
                    pass
        return None

    def gerar_telefones(self, conteudo:list):
        lista = []
        lista2 = []
        for conte in conteudo:
            for cont in conte:
                index_tel_cel = cont.find("Tel Cel: ") 
                index_tel_com = cont.find("Tel Com: ")

                if index_tel_com != -1:
                    index = index_tel_com + 9
                    telefones = cont[index:].split("Tel Cont: ")
                    if len(telefones) >= 1:
                        lista2.append(telefones)

                if index_tel_cel != -1:
                    index = index_tel_cel + 9
                    telefones = cont[index:].split("Tel Res: ")
                    if len(telefones) >= 1:
                        lista.append(telefones)

        return lista, lista2
                
    def gerar_profissional(self, conteudo, cabecalho):
        tamanho_do_conteudo = len(conteudo)
        lista = [0] * tamanho_do_conteudo
        index_inicial = cabecalho[1].find("Profissional: ")
        index_final = cabecalho[1].find(" CNS:")
        if index_final == -1:
            profissional = cabecalho[1][index_inicial:]
        else: 
            profissional = cabecalho[1][index_inicial: index_final + 1]
        
        
        profissionais = []
        
        for i in lista:
            profissionais.append(profissional)
        
        return profissionais

    def gerar_Data(self, conteudo, cabecalho):
        tamanho_do_conteudo = len(conteudo)
        lista = [0] * tamanho_do_conteudo
        index_inicial = cabecalho[4].find("Agenda (LOCAL): ")
        data = cabecalho[4][index_inicial:].split(" ")[2:]
        print(data)
        datas = []

        for i in lista:
            datas.append("".join(data))
        return datas

    def limparHora(self, conteudo:str):
        cont = conteudo.replace("end Hora", "").split(";")
        lista_filtrada = [elemento for elemento in cont if elemento]
        return lista_filtrada
        

    def gerar_sus(self, conteudo:list):
        arr_de_sus = []
        for cont in conteudo:
            try:
                arr_de_sus.append(cont[self.gerarsep(cont)].split(" ")[0])
            except ValueError:
                print('erro')
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

 
    

    
        
    