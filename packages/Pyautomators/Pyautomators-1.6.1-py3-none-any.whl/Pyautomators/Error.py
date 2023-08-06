# -*- coding: utf-8 -*-
'''
Created on 5 de jul de 2018

@author: koliveirab
'''
        
class Banco_erro(ConnectionError):
    ''''Gerador de erro para Banco de Dados, 
    Os erros são gerados para Detalhamento e Escrita Conexão com banco de dados'''

class Elemento_erro(InterruptedError):
    '''Gerador de erros para Elementos não encontrados''' 
    
class Ambiente_erro(TypeError):
    '''Gerardor de erros para Ambiente não encontrados'''
    
class Dado_erro(TypeError):
    '''Gerardor de erros para Dados com valores não encontrados'''
    
class Valida_erro(TypeError):
    '''Gerardor de erros para valores de validação não encontrados'''
    
class Driver_erro(TypeError):
    '''Gerardor de erros para valores de drivers errados'''