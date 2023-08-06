# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''

''' Este modulo tem o intuito de trabalhar com a descoberta de elementos dinamicos ou de imagens dinamicas, 
inpeção de tela e de HTML'''
import pyautogui
from  urllib import request
from bs4 import BeautifulSoup
import re
from .Error import Elemento_erro,Valida_erro
import lackey

def tamanhoTela():
    '''Esta função retorna o tamanho da tela grafica
        Exemplo:
        VALOR=tamanhoTela()
        print(VALOR)
        >>>1225,1600'''
    #retorna o tamanho da tela que ets usando
    return pyautogui.size()
 

def localizacao_imagem(imagem,centro=False):
    '''Esta função retorna o valor real na localicação da imagem passada       
        
        Exemplo:
        VALOR=localizacao_imagem("imagem.png")
        print(VALOR)
        >>>1000,200,1225,1600
        VALOR=localizacao_imagem("imagem.png",True)
        print(VALOR)
        >>>1000,200,1225,1600,'''
    #localiza as coordenadas de uma imagem baseando na tela atual
    valor=None
    Erro='Imagem nao encontrada'
    try:
        valor=pyautogui.locateOnScreen(imagem)
    except:
        raise Valida_erro(Erro)
    #caso o parametro centro for verdadeiro ele retorna somente os pontos do centro da imagem
    if(centro):
        valor=centralizar_pontos(valor)
    return valor

def localiza_todas_imagens(imagem,centro:bool=False):
    '''Esta função retorna o valor real na localicação de todas as imagens encontradas pela imagem passada        
        Exemplo:
        VALOR=localiza_todas_imagens("imagem.png")
        print(VALOR)
        >>>[(77, 601, 71, 52), (527, 601, 71, 52)]
        VALOR=localiza_todas_imagens("imagem.png",True)
        print(VALOR)
        >>>[(112, 627), (562, 627)]'''
    #localiza todas os pontos que tiverem esta imagem na tela
    valor=list(pyautogui.locateAllOnScreen(imagem))
    #centralizacao da imagem caso for veridadeiro 
    if(centro):
        novo=[]
        #passa por todas as imagens
        for v in valor:
            v=centralizar_pontos(v)
            novo.append(v)
        valor=novo
        #retorna todos os pontos achados como uma lista
    return valor

def centralizar_pontos(localizacao:tuple):
    '''Esta função gera o centro de pontos passados dentro de uma tupla       
        Exemplo:
        VALOR=localiza_todas_imagens("imagem.png")
        print(VALOR)
        >>>[(77, 601, 71, 52), (527, 601, 71, 52)]
        VALOR=localiza_todas_imagens("imagem.png",True)
        print(VALOR)
        >>>[(112, 627), (562, 627)]'''
    #centraliza o meio do de uma foto com base dos pontos iniciais e finais da imagem
    #verifica se os pontos da imagem tem todos os pontos como uma tupla
    if(type(localizacao)==tuple):
        x,y=pyautogui.center(localizacao)
    else:
        Erro=r'''
        Para usar a centralicação use em forma de tupla
        Exemplo:
        
        centralizar_pontos((1416, 562, 50, 41))
        centraliar_pontos(localizacao_imagem("imagem.png"))'''
        raise Elemento_erro(Erro)
    #Retorna o ponto do meio da imagem
    return x,y
    
def get_html(url):
    '''Esta retorna o html de uma pagina especificada       
        Exemplo:
        
        get_html("http://pyautogui.readthedocs.io/en/latest/cheatsheet.html")
        '''
    #tras o conteudo da requisicao do html
    response=request.urlopen(url)
    #retira o html do objeto
    valor=response.read()
    #passa o html para ser direcionado BeatifulSoup
    soup=BeautifulSoup(valor,'html.parser')
    return soup

def valor_tag(url,tag,atributo):
    '''Esta retorna o uma tag de uma pagina html com o valor de um atributo da tag
        Exemplo:
        
        valor_tag("http://pyautogui.readthedocs.io/en/latest/cheatsheet.html","input","value")
        '''
    #cria uma lista para poder ser retornada
    dicionario=[]
    #verifica o tamanho da palavra atributo
    tamanho=len(atributo)    
    #passa o html para ser direcionado BeatifulSoup
    soup=get_html(url)
    #intera em todas as linhas do html
    for line in soup.find_all(tag):
        #tenta encontrar o atributo na linha
        if(re.search(str(atributo)+'="', str(line)) is not None):
            #pega o valor do atributo do html
            comeco=tamanho+2+int(str(line).find(str(atributo)+'="'))
            fim=int(str(line).find('"',comeco))
            #adiciona na lista o valor do atributo, mais a tag que ele representa
            dicionario.append((str(line)[comeco:fim],line))
    #retorna a lista
    return dicionario     

def localliza_com_precisao(imagem,similaridade=100):
    #cria um objeto pattern para char na tela, similaridade em porcentagem
    imagem=lackey.Pattern(imagem).similar(similaridade/100)
    #encontra a imagem na tela
    valor=lackey.Screen().find(imagem).getTuple()
    #retorna os pontos do centro do objeto
    return valor