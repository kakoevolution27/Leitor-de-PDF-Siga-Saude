from classi import ManipuladorDePdf, LeituraDeArquivoPdfAgenda, FormatadorDeDados
import pandas as pd
path = [r"C:\Users\ADM\Desktop\agenda\13.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241212115031_756336592814342.pdf",
        r"C:\Users\ADM\Desktop\agenda\13.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241212115105_756370967981833.pdf",
        r"C:\Users\ADM\Desktop\agenda\13.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241212115127_756392523960357.pdf",
        r"C:\Users\ADM\Desktop\agenda\13.12.2024\REL_IMP_AGD_PROF_LOCAL_2787253_20241212115218_756443813841690.pdf"]

def main():
    for i , p in enumerate(path):
        manipuladorDeArquivos = ManipuladorDePdf()
        leitorDeArquivos = LeituraDeArquivoPdfAgenda()
        formatadorDeDados = FormatadorDeDados()
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
        df.to_csv(f"dados {i}.csv", index=False, sep=";")
        manipuladorDeArquivos.fechar_arquivo(pdf)
    




if __name__ == "__main__":
    main()