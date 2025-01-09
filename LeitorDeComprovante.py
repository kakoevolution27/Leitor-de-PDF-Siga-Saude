import pdfplumber
import unicodedata

path = r"C:\Users\ADM\Desktop\comprovantes\A.M - 968089809.pdf"
def main():
    texts = ""

    pdf = pdfplumber.open(path)

    for page in pdf.pages:
        text = page.extract_text()
        texts += text
    
    nome_paciente = encontrar_nome_paciente(texts)
    data = encontrar_data_hora(texts)
    profissional = encontrar_profissional_responsavel(texts)
    recomendacoes = encontrar_recomendacoes(texts)
    arr = encontrar_endereco_master(texts)
    

def encontrar_nome_paciente(string: str):
    index_inicial = string.find("Nome: ")
    index_final = string.find("Data nascimento: ")
    valor =  string[index_inicial + 6: index_final]
    if "\n" in valor:
        valor_modificado = valor.replace("\n", " ")
        return valor_modificado
    return valor
    
def encontrar_data_hora(string: str):
    index_inicial = string.find("Dados do Agendamento")
    data_hora_marcação = string[string.find("Data / Hora: ", index_inicial) + 13:string.find("(")]
    return data_hora_marcação

def encontrar_profissional_responsavel(string:str):
    index_inicial = string.find("Profissional resp.: ")
    index_final = string.find("Recomendações: ")
    valor = string[index_inicial+ 20:index_final]
    if "\n" in valor:
        valor_modificado = valor.replace("\n", " ")
        return valor_modificado
    return valor

def encontrar_recomendacoes(string:str):
    index_inicial = string.find("Recomendações: ")
    index_final = string.find("Profissional Marcador: ")
    valor = string[index_inicial + 15: index_final]

    if "\n" in valor: 
        valor_modificado = valor.replace("\n" , " ")
        return unicodedata.normalize('NFKD', valor_modificado)
    return unicodedata.normalize('NFKD', valor)

def encontrar_endereco_master(string:str):
    index_inicial = string.find("Unidade Executante: ")
    index_final = string.find("Procedimento: ")
    valor = string[index_inicial: index_final]
    nome_da_unidade_executante = encontrar_nome_unidade_executante(valor)
    endereco = encontrar_endereco_unidade_executante(valor)
    complemento = encontrar_complemento_unidade_executante(valor)
    bairro = encontrar_bairro_unidade_executante(valor)
    lista = [nome_da_unidade_executante,endereco,complemento,bairro]
    return lista

def encontrar_nome_unidade_executante(string:str):
    index_inicial = string.find("Unidade Executante: ")
    index_final = string.find("Endereço da Executante: ")
    valor = string[index_inicial + 19: index_final]
    return valor


def encontrar_endereco_unidade_executante(valor_Str: str):
    index_i = valor_Str.find("Endereço da Executante: ") 
    index_f = valor_Str.find("Complemento: ")
    endereco = valor_Str[index_i: index_f]
    if "\n" in endereco:
        valor_modificado = endereco.replace("\n", " ")
        return valor_modificado
    return endereco

def encontrar_complemento_unidade_executante(valor_Str:str):
    index_i = valor_Str.find("Complemento: ")
    index_f = valor_Str.find("Bairro: ")
    complemento = valor_Str[index_i: index_f]
    if "\n" in complemento:
        valor_modificado = complemento.replace("\n", " ")
        return valor_modificado
    return complemento

def encontrar_bairro_unidade_executante(valor_Str:str):
    index_i = valor_Str.find("Bairro: ")
    index_f = valor_Str.find("Telefone: ")
    bairro = valor_Str[index_i: index_f]
    return bairro
    




if __name__ == "__main__":
    main()