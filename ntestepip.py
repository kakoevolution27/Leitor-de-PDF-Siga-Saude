from classi import ManipuladorDePdf, LeituraDeArquivoPdfAgenda, FormatadorDeDados, EscritorDeTexto
import pandas as pd
path = [r"C:\Users\ADM\Desktop\agenda\18.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241217103442_3457838298716656.pdf",
        r"C:\Users\ADM\Desktop\agenda\18.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241217103606_3457922476371479.pdf",
        r"C:\Users\ADM\Desktop\agenda\18.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241217103725_3458001486007737.pdf",
        r"C:\Users\ADM\Desktop\agenda\18.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241217104622_3458539129125078.pdf",
        r"C:\Users\ADM\Desktop\agenda\18.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241217104812_3458648893630119.pdf",
        r"C:\Users\ADM\Desktop\agenda\18.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241217104840_3458677105706570.pdf",
        r"C:\Users\ADM\Desktop\agenda\18.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241217104909_3458705460513385.pdf",
        r"C:\Users\ADM\Desktop\agenda\18.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241217104934_3458730914801434.pdf",
        r"C:\Users\ADM\Desktop\agenda\18.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241217104958_3458755052029141.pdf",
        r"C:\Users\ADM\Desktop\agenda\18.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241217105023_3458779424511313.pdf",
        r"C:\Users\ADM\Desktop\agenda\18.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241217105042_3458799155548522.pdf",
]

def main():
    for i , p in enumerate(path):
        manipuladorDeArquivos = ManipuladorDePdf()
        leitorDeArquivos = LeituraDeArquivoPdfAgenda()
        formatadorDeDados = FormatadorDeDados()
        escritor = EscritorDeTexto()
        pdf = manipuladorDeArquivos.abrir_arquivo(p)
        texto = leitorDeArquivos.extrair_texto_segunda_coluna(pdf)
        texto1 = leitorDeArquivos.extrair_texto_primeira_coluna(pdf)
        hora = formatadorDeDados.limparHora(texto1)
        cabecalho = leitorDeArquivos.extrair_cabecalho(pdf)
        texto2 = formatadorDeDados.limpar_telefone(texto)
        texto3 = formatadorDeDados.limpar_cabecalho(texto2)
        array = formatadorDeDados.formatar_dados(texto3)
        nomes = formatadorDeDados.limpar_nomes(array)
        sus = formatadorDeDados.gerar_sus(array)
        prontuarios = formatadorDeDados.gerar_prontuario(array)
        dn = formatadorDeDados.gerar_data_nascimento(array)
        tel1 = formatadorDeDados.gerar_telefones(array)[0]
        tel2 = formatadorDeDados.gerar_telefones(array)[1]
        profissional = formatadorDeDados.gerar_profissional(array, cabecalho)
        data = formatadorDeDados.gerar_Data(array, cabecalho)
        
      
        dados = {"nome": pd.Series(nomes),
                "sus": pd.Series(sus),
                "prontuarios": pd.Series(prontuarios),
                "dn": pd.Series(dn),
                "tel": pd.Series(tel1),
                "profissional": pd.Series(profissional),
                "data": pd.Series(data),
                "hora": pd.Series(hora)
            }
        df = pd.DataFrame(dados)
        #escritor.escrever_texto()
        df.to_csv(f"./residuos/dados {i}.csv", index=False, sep=";")
        manipuladorDeArquivos.fechar_arquivo(pdf)
    

if __name__ == "__main__":
    main()