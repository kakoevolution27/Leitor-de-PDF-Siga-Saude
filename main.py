from classi import ManipuladorDePdf, LeituraDeArquivoPdfAgenda, FormatadorDeDados, EscritorDeTexto
import pandas as pd
import os 
import tkinter as tk
from tkinter import filedialog

def recuperar_caminho_do_arquivo(path_pasta):
    paths = []
    for root, dirs, files in os.walk(path_pasta):
        for file in files:
            if file.endswith('.pdf'):
                caminho_completo = os.path.join(root,file)
                paths.append(caminho_completo)
    return paths

def escolher_pasta():
    root = tk.Tk()
    root.withdraw()

    pasta_selecionada = filedialog.askdirectory(title="selecione a pasta de destino")

    if pasta_selecionada:
        return os.path.join(pasta_selecionada)
    else:
        return None    

pasta_selecionada = escolher_pasta()
path = recuperar_caminho_do_arquivo(pasta_selecionada)


def main() -> None:
    for i , p in enumerate(path):
        caminho_destino = fr"C:\Users\Kaio\Desktop\RESIDUOS\dados {i}.csv"
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
    return None
    

if __name__ == "__main__":
    main()