from Func import *

def main():
    pasta_selecionada = escolher_pasta()
    paths = recuperar_caminho_do_arquivo(pasta_selecionada)

    for index, path in enumerate(paths):

        arquivo = abrir_arquivo(path)

        string1 = extrair_texto_pdf(arquivo)
        base = limpar_cabecalho(string1)
    

        nomes = formatar_nomes(base).split("\n")
        horarios = eliminar_horarios_invalidos(base).split("\n")
        tels = extrair_telefone(base)
        tel_final = filtrar_telefones(tels)

        dados = {
            "nomes": pd.Series(nomes),
            "horarios": pd.Series(horarios),
            "tels": pd.Series(tels)
        }

        df = pd.DataFrame(dados)
        #escritor.escrever_texto()
        df.to_csv(fr"C:\Users\Kaio\Desktop\RESIDUOS\agenda{index}.csv", index=False, sep=";")

        fechar_arquivo(arquivo)


if __name__ == "__main__":
    main()