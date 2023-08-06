# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
import yaml
import json
import pytesseract as ocr
from PIL import Image
import pyautogui
import pandas
import os
from .Error import Dado_erro
''' Este modulo tem o intuito de trabalhar com dados de entrada para teste, 
trabalhando com a entrada dos dados para o teste'''

def tela_texto(xi:int, yi:int, xf:int, yf:int,renderizacao=False,x=-1,y=-1,limpar=True,language="eng")->str:
    '''Esta função retira de um ponto expecifico da tela um valor apartir dos pontos inicias xi:yi, traçado um contorno ate xf:yf
    em uma tela, 
    a mesma retira um print podendo renderizar o tamanho da informação para melhorar a captura do dado
    
    parametros:
    xi,yi,xf,yf(obrigatorio):pontos para retangular o local que sera retirado a informação
    renderizacao:Se o valor for True e pode renderizar a imagem para um tamannho de leitura melhor do Tesseract
    x:y:Tamanho da foto Renderizada
    limpar:Exclui a imagem apos utilização
    language:Lingua para tradução, sendo 
    Exemplo:
    tela_texto(1,100,50,200,True,200,300,False)'''
    
    #formando a função lambda de subtração
    result=lambda a,b:b-a 
    #gerano a subtração dos pontos, para achar a largura e altura
    xd=result(xi,xf)
    yd=result(yi,yf)
    #verifica se os pontos são inteiros e se não são negativos 
    if((type(xd) is float) or (type(yd) is float) or xd<=0 or yd<=0):
        Erro="""
                Os Valores de xi:yi e xf:yf estão errados
                tente seguir este padrão e contruir com valores inteiros:
                xf>xi
                Yf>yi"""
        raise Dado_erro(Erro)
    #cria o arquivo temporario para retirar o valor da imagem
    nome="teste.png"
    #retirando o print da tela e guardando no arquivo temporario
    pyautogui.screenshot(nome,region=(xi,yi,xd,yd))
    #caso renderização seja true ele começa o processo de ajuste da imagem
    if(renderizacao==True ):
        #verifica se os valores de x e y são menores que 0
        if(y<=0 or x<=0):
            Erro="""
                    Os Valores de x:y estão errados
                    tente seguir e contruir com valores positivos
                    """
            raise Dado_erro(Erro)
        else:
            #abre a imagem e renderiza e salva novamente
            im = Image.open(nome)
            ims=im.resize((x, y),Image.ANTIALIAS)
            ims.save(nome,'png')
    #Abre a imagem 
    im=Image.open(nome)    
    #Retira a string da imagem
    valor=ocr.image_to_string(im,lang=language)
    #Caso o parametro limpar sejá True, a imagem e descartada
    if(limpar):
        #remove a imagem
        os.remove(nome)
    return valor
    
def pegarConteudoJson(NomeArquivo):
    '''Esta função retira o conteudo de um json e retorna um Dicionario
    
    parametros:
    NomeArquivo(obrigatorio):Nome do arquivo Json
    
    Exemplo:
    pegarConteudoJson("valor.json")'''
    #Vai Abrir o conteudo e vai retornar o json como dicionario
    arquivo = open(NomeArquivo.replace("\\","/"), 'r')
    lista = arquivo.read()
    arquivo.close()    
    #Carregando conteudo para dicionarios
    jso=json.loads(lista)  
    return dict(jso)


def pegarConteudoCSV(NomeArquivo:str):
    '''Esta função retira o conteudo de um CSV e retorna um DataFrame
    
    parametros:
    NomeArquivo(obrigatorio):Nome do arquivo CSV
    
    Exemplo:
    pegarConteudoCSV("valor.csv")'''
    #Vai abrir o conteudo e vai retornar um dataframe
    valor=pandas.read_csv(NomeArquivo)
    valor=pandas.DataFrame(valor)
    return valor
    
def pegarConteudoXLS(NomeArquivo:str,Planilha:str):
    '''Esta função retira o conteudo de um Excel e retorna um DataFrame
    
    parametros:
    NomeArquivo(obrigatorio):Nome do arquivo XLS
    Planilha: Qual planilha deve ser retirado o conteudo
    
    Exemplo:
    pegarConteudoXLS("valor.xls","Planilha1")'''
    #Vai abrir o conteudo e vai retornar um dataframe
    valor=pandas.read_excel(NomeArquivo,sheet_name=Planilha)
    valor=pandas.DataFrame(valor)
    return valor

def pegarConteudoYAML(NomeArquivo):
    '''Esta funcao retira o conteudo de um yaml e retorna um dict
    
    parametros:
    NomeArquivo(obrigatorio):Nome do arquivo YAML
    
    Exemplo:
    pegarConteudoYAML('teste.yaml')
    '''
    #Vai Abrir o conteudo e vai retornar o json como dicionario
    arquivo=open(NomeArquivo,"r")
    
    return yaml.load(arquivo)
    