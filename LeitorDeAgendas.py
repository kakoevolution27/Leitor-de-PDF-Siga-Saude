from Func import *

def main():
    teste = False
    paths = []
    if teste:
        paths.append(fr"C:\Users\Kaio\Desktop\agenda\janeiro\31.01.2025\REL_IMP_AGD_PROF_LOCAL_2787253_20250130103218_239632288983044.pdf")
    else:
        pasta_selecionada = escolher_pasta()
        paths = recuperar_caminho_do_arquivo(pasta_selecionada)

    for index, path in enumerate(paths):

        try:
            arquivo = abrir_arquivo(path)
            string1 = extrair_texto_pdf(arquivo)
            cabecalho = extrair_cabecalho(arquivo)
            base = limpar_cabecalho(string1)
            nomes = formatar_nomes(base).split("\n")
            horarios = eliminar_horarios_invalidos(base).split("\n")
            profissionais = gerar_profissional(nomes, cabecalho)
            data = gerar_Data(nomes, cabecalho)
            tels = extrair_telefone(base)
        except ValueError as e:
            print(f"erro {e} no arquivo {path}")

        dados = {
            "nomes": pd.Series(nomes),
            "tels": pd.Series(tels),
            "profissionais": pd.Series(profissionais),
            "horarios": pd.Series(horarios),
            "Data": pd.Series(data)
        }

        df = pd.DataFrame(dados)
        #escritor.escrever_texto()
        df.to_csv(fr"C:\Users\Kaio\Desktop\RESIDUOS\agenda{index}.csv", index=False, sep=";")

        fechar_arquivo(arquivo)


if __name__ == "__main__":
    main()