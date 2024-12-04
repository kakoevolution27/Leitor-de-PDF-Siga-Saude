
from func import abrir_arquivo, escrever_Planilha, ext_teste,extrair_numero_de_paginas, extrair_texto_pdf, extrair_cabecalho, fechar_arquivo, limpar_cabecalho, limpar_paginas


arquivos = {"Escrever_txt": False,
            "Escrever_Excel": True,
            "Escrever_Docx": False}

caminhos = [r"C:/Users/kakoe/Desktop/REL_IMP_AGD_PROF_LOCAL_2787253_20241113145451_202654987541760.pdf"]


    

for index_dos_caminhos, caminho in enumerate(caminhos):
    pdf = abrir_arquivo(caminho)
    num_de_paginas = extrair_numero_de_paginas(pdf)
    texto = extrair_texto_pdf(pdf)
    texto2 = ext_teste(pdf)
    cabecalho = extrair_cabecalho(pdf)
    texto_sem_cabecalhos = limpar_cabecalho("\n".join(cabecalho), texto) 
    #tornar funções de limpeza em apenas uma
    texto_final = limpar_paginas(num_de_paginas, texto_sem_cabecalhos) 
    texto2_final = limpar_paginas(num_de_paginas, texto2)
    print(ext_teste(pdf))
    #if arquivos.get("Escrever_txt") == True:
        #escrever_arquivo_txt(index_dos_caminhos, "Agenda", texto_final)
    #"""
    if arquivos.get("Escrever_Excel") == True:
        escrever_Planilha(texto2_final,cabecalho,index_dos_caminhos)
    #"""
    fechar_arquivo(pdf)



