# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
import pyautogui
from time import sleep
from .Error import Valida_erro
''' Este modulo trabalha com o conjunto de validações,
    pode conter valor valores e imagens para ser verificadas'''
import lackey
class Valida():
    ''' Esta classe tem o intuito de gerar um conjunto de validações que auxiliem testes'''
    
    @staticmethod
    def verifica_tela(imagem,tentativa=1,tempo=0.1,valida=False,acao=None,valor:tuple=None,similaridade=100):
        '''Verifica em tela se uma imagem esta , caso não estiver ela pode gerar um erro ou fazer alguma ação
            e retorna o valor das coordenadas para uso
        parametros:
        imagem(obrigatorio):Verifica se a imagem esta visivel
        tentativa:fala quantos ciclos de tentativa ele tentara achar a foto
        tempo:intervalo entre um ciclo e outro
        valida:se True, caso o ciclo passe e a imagem não for achada, levanta um erro
        acao: acao que sera feita durante o ciclo, sendo passada um valor de um metodo para o argumento
        valor:caso a açao tenha valores passados por parametros, colocar os parametros dentro de uma tupla
        Exemplo:
        verifica_tela("Capturar.PNG", 3, 2, acao=Teclado.digitos,valor=("tab","tab"))
        verifica_tela("Capturar.PNG", 3, 2, true,Teclado.clica,(120,1200))
        verifica_tela('Capturar.PNG',10,1,acao=self.app.clica,('elemento'))
        '''
        #vai iniciar o validador como falso
        validador=False
        #vai iterar com o numero de tentativas
        for ponto in range(tentativa):
            #criando a imagem com a similaridade
            image=lackey.Pattern(imagem).similar(similaridade/100)
            
            
            
            #encontra a imagem na tela
            result=lackey.Screen().exists(image, 3)
            #verificando se foi encontrado
            if(result  is not None):
                #torna o validador como True
                validador=True
                #pega as referencias da imagem na tela
                #para a execução
                break
            #vai verificar se existe alguma ação para ser feita entre as tentativas        
            if(acao is not None):
                #verifica se existe uma tupla para ser levada com parametros
                if(valor is not None):
                    #executa a ação com os parametros
                    acao(*valor)
                #verifica se o valor esta vazio
                elif(valor is None):
                    #executa a ação sem parametros
                    acao()
            #aguarda pelo parametro tempo para executar a proxima tentativa     
            sleep(tempo)
        #executa a validaçãp caso o parametro valida e verdadeiro
        if(valida):
            #se o validador achou ele para e retorna os resultados
            if(validador):
                pass
            #caso não achou a imagem na tela durante o cliclo ele quebra o teste
            else:
                
                Erro='\n\n\tImagem não foi encontrada!!'
                raise Valida_erro(Erro)
        result=result.getCenter()
        return result.x,result.y