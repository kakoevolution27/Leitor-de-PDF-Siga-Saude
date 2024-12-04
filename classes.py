from openpyxl import Workbook
import pdfplumber
from Interfaces import InterfaceDeEscrita, InterfaceDeLeituraDeArquivo, InterfaceDeManipulacaoDoArquivo



class ManipuladorDeArquivos(InterfaceDeManipulacaoDoArquivo):
    dependencia = pdfplumber
    def abrir_arquivo(self, caminho_pdf):
        """
        Abre um arquivo PDF usando a dependência fornecida.

        Args:
            caminho_pdf (str): Caminho do arquivo PDF a ser aberto.
            dependencia (module): Dependência que será usada para abrir o PDF (ex.: pdfplumber).

        Returns:
            arquivo (obj): Objeto do arquivo PDF aberto, se bem-sucedido.
            Exception: Exceção capturada, se ocorrer um erro.
        """
        try:
            arquivo = self.dependencia.open(caminho_pdf)
            print("arquivo aberto com sucesso")
            return arquivo
        except Exception as e:
            print(f"Erro ao abrir o arquivo {caminho_pdf}: {e}")
            return e
        
    def fechar_arquivo(self, pdf:Workbook):
        pdf.close()
        print("arquivo fechado")

class LeituraDeArquivoPDFAgenda(InterfaceDeLeituraDeArquivo):
    def extrair_texto_pdf(self, PDF):
        """
        Extrai o texto da segunda coluna do PDF de Agendas.

        Args:
            pdf (pdfplumber.PDF): Objeto PDF aberto com pdfplumber.

        Returns:
            str: Texto concatenado extraído da segunda coluna do PDF.
        """
        texto_extraido_segunda_coluna = []  
    

        try:
            for pagina in PDF.pages:
                segunda_coluna_documento = (101.77,0,318.22,pagina.height)
                texto_da_segunda_coluna = pagina.within_bbox(segunda_coluna_documento).extract_text()
                if texto_da_segunda_coluna: 
                     texto_extraido_segunda_coluna.append(texto_da_segunda_coluna)
            return "\n".join(texto_extraido_segunda_coluna)
        except Exception as e:
            print(f"Erro ao extrair paginas do arquivo: {e}")
        

    def extrair_texto_primeira_coluna(self, PDF):
        retorno = []
        
        try:
            for pagina in PDF.pages:
                primeira_coluna_documento = (50.77,0,110, pagina.height)
                texto_da_primeira_coluna = pagina.within_bbox(primeira_coluna_documento).extract_text().split("\n")

                for item in texto_da_primeira_coluna:
                    retorno.append(item)
            return retorno
        except Exception as e:
            print(f"Erro ao extrair primeira coluna")


    def extrair_cabecalho(self, PDF):
        """
        Extrai o cabeçalho padrão do documento a partir da primeira página.

        Args:
            pdf (pdfplumber.PDF): Objeto PDF aberto com pdfplumber.

        Returns:
            list: Uma lista de strings representando as linhas do cabeçalho.
        """
        try:
            primeira_pagina = PDF.pages[0]
            cabecalho =  primeira_pagina.extract_text().split('\n')[0:6]
            return cabecalho
        except Exception as e:
            return f"erro ao extrair o cabeçalho {e}"

    def limpar_conteudo(self, conteudo:str):
        try:
            cabecalho = conteudo[:60]
            novoconteudo = conteudo.replace(cabecalho,"")
            return novoconteudo
        except Exception as e:
            return {f"erro ao extrair cabecalho {e}"}


    #def zipar_listas(self, lista1, lista2):
    #    lista = [list(par) for par in zip(lista1, lista2)]
    #    return lista





    
    def formatar_dados(self, conteudo:str,pdf):
            try:
                linhas = conteudo.split("\n")
                horarios = self.extrair_texto_primeira_coluna(pdf) #retorno é uma lista
                horarios_filtrados = []
                lista = [] #lista de listas
                sublista = []
                nlist = []

                for hor in horarios:
                    if "end Hora" in hor:
                        continue
                    else:
                        horarios_filtrados.append(hor)

                for linha in linhas:
                    if linha == "" or linha == "\n":
                        continue
                    if "Mãe:" in linha:
                        lista.append(sublista)
                        sublista = []
                    else:
                        linha = linha.replace("Tel Cel: ", "")
                        linha = linha.replace("Tel Res: ", "")
                        linha = linha.replace("Tel Com: ", "")
                        linha = linha.replace("Tel Cont: ", "")
                        linha = linha.replace("NÃO", "")
                        linha = linha.replace("INFORMADO", "")
                        linha = linha.replace("RESPONDEU", "")
                        linha = linha.replace("e", "")
                        linha = linha.replace("te", "")
                        linha = linha.replace("nte", "")
                        linha = linha.replace("nt", "")
                        linha = linha.replace("t", "")
                        sublista.append(linha)

                    
                for index, registro in enumerate(lista):
                    if "end Hora" in horarios_filtrados[index]:
                        continue
                    else:
                        print(horarios_filtrados[index])
                        r = registro.append(horarios_filtrados[index])
                        nlist.append(r)

                print(lista)
                return lista
            except Exception as e:
                return f"erro ao formatar os dados {e}"
    
    def formatar_dict(self, conteudo: list): 
        valor_para_remover = '' 
        lista_formatada = [] # Remover todas as ocorrências de valores vazios nas sublistas 
        for sublista in conteudo: 
            sublista_filtrada = [item for item in sublista if item != valor_para_remover and item != ' '] 
            if sublista_filtrada: # Adicionar somente sublistas não vazias 
                lista_formatada.append(sublista_filtrada) # Mostrar o resultado formatado 
        print("Lista formatada:", lista_formatada) 
        return lista_formatada
    

    #def formatar_dict(conteudo: list): valor_para_remover = '' lista_formatada = [] # Remover todas as ocorrências de valores vazios e "11" nas sublistas for sublista in conteudo: sublista_filtrada = [item.replace('11 ', '') for item in sublista if item != valor_para_remover and item != " "] if sublista_filtrada: # Adicionar somente sublistas não vazias lista_formatada.append(sublista_filtrada) # Mostrar o resultado formatado print("Lista formatada:", lista_formatada) return lista_formatada


class EscritorDeArquivosExcel(InterfaceDeEscrita):
    def __init__(self): 
        self.dependencia = Workbook() 
        self.sheet = self.dependencia.active

    def escrever_no_arquivo(self, conteudo):
        for cont in conteudo:
            self.sheet.append(cont)

    def salvar_arquivo_excel(self, numero_da_iteracao ):
        self.dependencia.save(f"AGENDA {numero_da_iteracao + 1}.xlsx")
        
            
            