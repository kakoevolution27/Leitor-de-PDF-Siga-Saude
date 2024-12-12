
from classes import EscritorDeArquivosExcel, LeituraDeArquivoPDFAgenda, ManipuladorDeArquivos

path = [r"C:\Users\ADM\Desktop\agenda\12.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241211151037_2114138005062183.pdf",
        r"C:\Users\ADM\Desktop\agenda\12.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241211151049_2114149374269539.pdf",
        r"C:\Users\ADM\Desktop\agenda\12.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241211151109_2114169701419723.pdf",
        r"C:\Users\ADM\Desktop\agenda\12.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241211151142_2114202880167287.pdf",
        r"C:\Users\ADM\Desktop\agenda\12.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241211151158_2114218834057758.pdf",
        r"C:\Users\ADM\Desktop\agenda\12.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241211151216_2114236746437313.pdf",
        r"C:\Users\ADM\Desktop\agenda\12.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241211151346_2114326734490416.pdf"
]

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