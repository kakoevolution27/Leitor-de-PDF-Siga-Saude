
from classes import EscritorDeArquivosExcel, LeituraDeArquivoPDFAgenda, ManipuladorDeArquivos

path = []

def main():
    manipulador_de_arquivos = ManipuladorDeArquivos()
    leitor_de_arquivo = LeituraDeArquivoPDFAgenda()
    
  
    #implementar o sistema que concatena o profissional corretamente
    #implementar o sistema que concatena a data corretamente
    #implementar a função limpar conteudo deve limpar as grafias de Não informado dos telefones


    for numero_da_iteracao, caminho in enumerate(path):
        escritor_excel = EscritorDeArquivosExcel()
        Pdf = manipulador_de_arquivos.abrir_arquivo(caminho)
        texto_extraido = leitor_de_arquivo.extrair_texto_pdf(Pdf)
        texto_segunda_coluna_limpo = leitor_de_arquivo.limpar_conteudo(texto_extraido)
        dados_finais_coluna_2 = leitor_de_arquivo.formatar_dados(texto_segunda_coluna_limpo, Pdf)
        dados = leitor_de_arquivo.formatar_dict(dados_finais_coluna_2)
        escritor_excel.escrever_no_arquivo(dados)
        escritor_excel.salvar_arquivo_excel(numero_da_iteracao)
        manipulador_de_arquivos.fechar_arquivo(Pdf)

if __name__ == "__main__":
    main()