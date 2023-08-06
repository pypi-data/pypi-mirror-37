# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
'''

Este Modulo Trabalha ações do mouse e teclado

'''
import pyautogui
import lackey
class Teclado():
    ''' Esta classe tem o intuito de prover ações do Teclado'''
    
    ##################################################################################
    #                                  TECLAS                                        #
    ##################################################################################
    r"""'\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
     ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
     '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
     'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
     'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
     'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
     'browserback', 'browserfavorites', 'browserforward', 'browserhome',
     'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
     'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
     'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
     'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
     'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
     'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
     'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
     'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
     'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
     'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
     'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
     'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
     'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
     'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
     'command', 'option', 'optionleft', 'optionright'"""
    @staticmethod
    def digitos(*digito):
        r'''Este metodo trabalha com digitos do caracter e a repetição dos digitos atribuidos em uma tupla
        
        Exemplo:
        
        digitos("b","o",("m",10),'tab','d','i','a')
        >>>bommmmmmmmmm    dia
        
        '''
        #criando uma lista
        lista=[]
        #cerificando se os parametros estão de forma correta
        if(type(digito)==tuple):
            #fazendo a iteração dos itens
            for d in digito:
                #caso o item seja uma tupla com o valor e quantidade de vezes precionado
                if(type(d)==tuple):
                    #usando o laço for para colocar a quantidade de vezes na lista
                    for b in range(d[1]):
                        #adicionando na lista quantas vezes deve ser precionado uma unica tecla
                        lista.append(d[0])
                #caso nao seja uma tupla ele adiciona so coloca na fila de execução das teclas
                else:
                    lista.append(d)
        pyautogui.press(lista,interval=0.5)
        
    @staticmethod
    def mantenha_e_digite(mantenha,*digite):        
        r'''Este metodo mantem uma tecla pressionada enquanto digita uma lista de digitos
        
        Exemplo:
        
        mantenha_e_digite('capslock','a','b','c')
        >>>ABC
        
        '''
        #deixando a primeira tecla precionada
        pyautogui.keyDown(mantenha)
        #iteração das teclas
        for digito in digite:
            
            pyautogui.press(digito)
        #desprecionando a primeira tecla
        pyautogui.keyUp(mantenha)
        
    @staticmethod
    def combo_digitos(*teclas):
        r'''Este metodo falta digita diversas teclas ao mesmo tempo de acordo com a ordem
        
        Exemplo:
        
        combo_digitos('alt',"f4")
        
        '''
        #colocando todas as teclas que foram passadas para serem precionadas em conjunto
        pyautogui.hotkey(*teclas)
        
    @staticmethod    
    def escrever_direto(conteudo):
        r'''Este metodo escreve um texto com base no alfabeto
        
        Exemplo:
        
        escrever_direto('Bom dia pessoal')
        >>>Bom dia pessoal
        
        '''
        #Escrevendo texto passado
        pyautogui.typewrite(conteudo)
        
class Mouse():
    ''' Esta classe tem o intuito de prover ações do Mouse'''
    
    
    
    
    @staticmethod
    def clica_coordenada(x,y,cliques=1,botao='left'):
        r'''Este metodo clica em uma coordenada passada na tela
        
        Exemplo:
        
        clica_coordenada(216,114)
        clica_coordenada(216,114,1,'rigth')
        clica_coordenada(localizacao_imagem("teste.png",True),2)
        '''
        #clicando em uma coordenada passada
        pyautogui.click(x,y,clicks=cliques,button=botao)
    
    @staticmethod
    def arraste_coordenada(xi,yi,xf,yf,botao="left",duracao=0.0):
        r'''Este metodo arrasta algo de uma coordenada inicial para a final
         
        
        Exemplo:
        
        arraste_coordenada(216,114,1000,800)
        arraste_coordenada(216,114,1000,800,duracao=1.5)
        arraste_coordenada(localizacao_imagem("teste.png",True),localizacao_imagem("teste2.png",True))
        '''
        #movendo para o ponto inicial do arraste
        pyautogui.moveTo(x=xi,y=yi,duration=duracao)
        #arrastando ate o ponto final
        pyautogui.dragTo(x=xf,y=yf,button=botao,duration=duracao)
    
    @staticmethod
    def rolagemMouse(valor,x=None,y=None):
        r'''Este metodo arrasta algo de uma coordenada inicial para a final
         
        
        Exemplo:
        
        rolagemMouse(100)
        '''
        #movendo ate um ponto na tela
        pyautogui.moveTo(x, y)
        #decendo a tela
        pyautogui.scroll(valor)
        
    @staticmethod
    def clica_imagem(path_imagem,clicks=1,botao='left',similar=100):
        r'''Este metodo arrasta algo de uma coordenada inicial para a final
         
        
        Exemplo:
        
        clica_imagem("teste.png",2)
        clica_imagem("teste.png",similar=70)
        '''
        #criando um objeto pattern e verificar a similaridade
        imagem=lackey.Pattern(path_imagem).similar(similar/100)
        #Encontrando a imagem na tela e pegando o centro da tela
        valor=lackey.Screen().find(imagem).getCenter()
        x,y=valor.x,valor.y
        #clicando no centro da imagem
        pyautogui.click(x,y,clicks=clicks,button=botao)
    
    @staticmethod    
    def moverMouse(x,y,duracao=0.0):
        r'''Este metodo arrasta algo de uma coordenada inicial para a final
         
        
        Exemplo:
        
        arraste_coordenada(216,114)
        arraste_coordenada(216,114,1.5)
        arraste_coordenada(localizacao_imagem("teste.png",True))
        '''
        #movendo para o local passado
        pyautogui.moveTo(x,y,duration=duracao)    
        
        
class Teclas():
    EXCLAMACAO, ASPAS_DUPLAS, JOGO_DA_VELHA, CIFRAO, PORCENTAGEM, E_COMERCIAL, ASPAS_SIMPLES, ABERTURA_PARENTESES,\
    FECHAMENTO_PARENTESES, ASTERISCO, SOMA, VIRGULA, TRACO, PONTO, BARRA, NUM_0, NUM_1, NUM_2, NUM_3, NUM_4, NUM_5, NUM_6, NUM_7,\
    NUM_8, NUM_9, DOIS_PONTOS, PONTO_VIRGULA, SINAL_MENOR_QUE, IGUAL, SINAL_MAIOR_QUE, INTERROGACAO, ARROBA, ABERTURA_COLCHETE, BARRA_INTERTIDA, FECHAMENTO_COLCHETE, ACENTO_CIRCUNFLEXO, UNDERLINE, ACENTO_AGUDO,\
    A, B, C, D, E,F, G, H, I, J, K, L, M, N, O,\
    P, Q, R, S, T, U, V, W, X, Y, Z, ABERTURA_CHAVE, PIPE,FECHAMENTO_CHAVE, TI,\
    ACCEPT, ADD, ALT, ALTLEFT, ALTRIGHT, APPS, BACKSPACE,\
    BROWSERBACK, BROWSERFAVORITES, BROWSERFORWARD, BROWSERHOME,\
    BROWSERREFRESH, BROWSERSEARCH, BROWSERSTOP, CAPSLOCK, CLEAR,\
    CONVERT, CTRL, CTRLLEFT, CTRLRIGHT, DECIMAL, DEL, DELETE,\
    DIVIDE, DOWN, END, ENTER, ESC, ESCAPE, EXECUTE, F1, F10,\
    F11, F12, F13, F14, F15, F16, F17, F18, F19, F2, F20,\
    F21, F22, F23, F24, F3, F4, F5, F6, F7, F8, F9,\
    FINAL, FN, HANGUEL, HANGUL, HANJA, HELP, HOME, INSERT, JUNJA,\
    KANA, KANJI, LAUNCHAPP1, LAUNCHAPP2, LAUNCHMAIL,\
    LAUNCHMEDIASELECT, LEFT, MODECHANGE, MULTIPLY, NEXTTRACK,\
    NONCONVERT, NUMLOCK, PAGEDOWN, PAGEUP, PAUSE, PGDN,\
    PGUP, PLAYPAUSE, PREVTRACK, PRINT, PRINTSCREEN, PRNTSCRN,\
    PRTSC, PRTSCR, RETURN, RIGHT, SCROLLLOCK, SELECT, SEPARATOR,\
    SHIFT, SHIFTLEFT, SHIFTRIGHT, SLEEP, SPACE, STOP, SUBTRACT, TAB,\
    UP, VOLUMEDOWN, VOLUMEMUTE, VOLUMEUP, WIN, WINLEFT, WINRIGHT, YEN,\
    COMMAND, OPTION, OPTIONLEFT, OPTIONRIGTH=\
    '!', '"', '#', '$', '%', '&', "'", '(',\
    ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',\
    '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',\
    'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',\
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',\
    'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',\
    'browserback', 'browserfavorites', 'browserforward', 'browserhome',\
    'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',\
    'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',\
    'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',\
    'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',\
    'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',\
    'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',\
    'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',\
    'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',\
    'nonconvert','numlock', 'pagedown', 'pageup', 'pause', 'pgdn',\
    'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',\
    'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',\
    'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',\
    'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',\
    'command', 'option', 'optionleft', 'optionright'

