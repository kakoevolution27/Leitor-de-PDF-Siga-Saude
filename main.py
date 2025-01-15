from classi import ManipuladorDePdf, LeituraDeArquivoPdfAgenda, FormatadorDeDados, EscritorDeTexto
import pandas as pd

caminho_do_txt = fr""

path = []
caminhos = open(caminho_do_txt).readlines()

for texto in caminhos:
    path.append(fr"{texto.replace("\n", "")}")


def main():
    for i , p in enumerate(path):
        caminho_destino = fr""
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
                "tel inut": pd.Series(tel1),
                "profissional": pd.Series(profissional),
                "data": pd.Series(data),
                "hora": pd.Series(hora)
            }
        df = pd.DataFrame(dados)
        #escritor.escrever_texto()
        df.to_csv(caminho_destino, index=False, sep=";")
        manipuladorDeArquivos.fechar_arquivo(pdf)
    

if __name__ == "__main__":
    main()