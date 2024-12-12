from abc import ABC, abstractmethod

from abc import ABC, abstractmethod

class InterfaceDeManipulacaoDoArquivo(ABC):
    dependencia = None  # Propriedade para armazenar dependências externas

    @abstractmethod
    def abrir_arquivo(self, caminho_pdf, dependencia):
        """Abre um arquivo PDF."""
        pass


    @abstractmethod
    def fechar_arquivo(self, pdf):
        """Fecha o arquivo PDF."""
        pass



class InterfaceDeLeituraDeArquivo(ABC):
    @abstractmethod
    def extrair_texto_pdf(self, PDF):
        """Extrai texto de um arquivo PDF."""
        pass


    


# Interface para escrita
class InterfaceDeEscrita(ABC):
    @abstractmethod
    def escrever_no_arquivo(self, caminho_do_novo_arquivo, conteudo):
        """Escreve conteúdo em um arquivo."""
        pass

    def salvar_arquivo_excel():
        pass

class InterfaceFormataçãoDosDados(ABC):
    @abstractmethod
    def limpar_conteudo(self, conteudo):
        """Limpa o conteúdo do arquivo para processar."""
        pass

    @abstractmethod
    def formatar_dados(self, PDF):
        """Formata os dados extraídos do arquivo."""
        pass