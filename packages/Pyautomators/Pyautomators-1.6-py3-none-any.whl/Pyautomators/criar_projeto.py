# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
'''Este Modulo tem como função gerar apartir de linha de comando um projeto no Padrão de Pyautomators'''
import argparse
from .pyautomator import Project

if('__main__'==__name__):

    ARG=argparse.ArgumentParser()
    ARG.add_argument("-n",'--nome_projeto',required=True,help="Criar um projeto")
    ARG.add_argument("-d",'--diretorio',required=False,help="diretorio")
    
    projeto=vars(ARG.parse_args())
    Project().Criar_Projeto(projeto["nome_projeto"], projeto["diretorio"])