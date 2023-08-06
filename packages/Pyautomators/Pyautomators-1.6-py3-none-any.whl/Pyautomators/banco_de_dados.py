# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''
''' Este arquivo tem o intuito de promover conexão e funções com banco de dados'''
import pymysql
import cx_Oracle
import sqlite3

from pymongo import MongoClient
from .Error import Banco_erro

class Relacional():
    ''' Esta classe tem o intuito prover conexão e funções de CRUD em banco Relacional'''
    
    def __init__(self,servidor,user=None,senha=None,banco=None,endereco=None,porta=None):
        '''No construtor temos seis parametros sendo um obrigatorio
        
        Servidor(obrigatorio):Tipo de Servidor de banco de dados que vai trabalhar.EXP.: 'Oracle', 'SQLite' e 'MySQL'
        user: Usuario de conexão com o servidor
        senha: Senha de conexão com o servidor
        banco: O banco de dados na qual iremos no conectar no servidor
        endereco: É o endereço na qual vamos usar para nos conectar ao servidor.Exemplo: URL OU localhost OU 127.0.0.1...
        porta: É a porta de conexão para o endereço. Exemplo: 8080, 3601 ...
        '''
        #Verifica se o Servidor for valido ele escolhe um dos servidores do banco
        if (servidor=="MySQL"):
            #Verifica se os parametros foram preenchidos para o Mysql
            if(servidor is not None and user is not None and senha is not None and banco is not None and endereco is not None\
               and  porta is not None):
                self.__bank=pymysql.connect(user=user,passwd=senha,db=banco,host=endereco,port=porta,autocommit=True)
                
            else:
                Erro="""Não é um servidor valor valido para MySQL!
                        Valores obrigatorios são:
                        user=usuario que vai ser usado no banco,
                        senha=senha do usuario,
                        banco=banco de dados que sera usado,
                        endereco=endereco host do banco,
                        porta=porta do endereço de saida do banco
                        """
                raise Banco_erro(Erro)
        elif (servidor=="Oracle"):
            #Verifica se os parametros foram preenchidos para o Oracle
            if(servidor is not None and user is not None and senha is not None and endereco is not None\
               and  porta is not None):
                self.__bank=cx_Oracle.connect('{}/{}@{}{}'.format(user,senha,endereco,porta))
            else:
                Erro="""Não é um servidor valor valido para MySQL!
                        Valores obrigatorios são:
                        user=usuario que vai ser usado no banco,
                        senha=senha do usuario,
                        endereco=endereco host do banco,
                        porta=porta do endereço de saida do banco
                        
                        """
                raise Banco_erro(Erro)
            
            
        elif(servidor=="SQLite"):
            #Verifica se os parametros foram preenchidos para o SQLite

            if(banco is not None):
                self.__bank=sqlite3.connect(banco)
            else:
                Erro="""Não é um servidor valor valido para SQLite!
                        Valores obrigatorios são:
                       banco=Url ou Arquivo
                        """
                raise Banco_erro(Erro)
        else:
            Erro="\n\nNão é um servidor valido!\nOs servidores validos são: 'Oracle','MySQL' ou 'SQLite'\nInsira um valor correto!"
            raise Banco_erro(Erro)
            
        self.cursor=self.__bank.cursor()
        
    def buscar_tudo(self,query:str):
        '''Este metodo busca todos os valores de uma tabela, baseado em uma Query. Exemplo: buscar_tudo("SELECT {} FROM {}".format("*","table_name"))
           O retorno é uma lista com  dicionarios como colunas da tabela como chave
           , na qual temos os parametros
           
           query(obrigatorio): Select do banco
           '''
        Erro='Esta Query é invalida!'
        #verifica a query e retorna todos os dados na query
        if(str(query).upper().find('SELECT')!= -1):
            try:
                self.cursor.execute(query)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)
        return self.cursor.fetchall()
    
    def buscar_um(self,query:str):
        '''Este metodo busca o primeiro valor de uma tabela, baseado em uma Query. Exemplo: buscar_um("SELECT {} FROM {}".format("*","table_name"))
           O retorno é um dicionarios como colunas da tabela como chave
           , na qual temos os parametros
           
           query(obrigatorio): Select do banco'''
        Erro='Esta Query é invalida!'
        #Verifica a query e retorna somente o primeiro valor
        if(str(query).upper().find('SELECT')!= -1):
            try:
                self.cursor.execute(query)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)
        return self.cursor.fetchone()
    
        
    def inserir_lista(self,sql:str,valores:list):
        '''Este metodo inseri diversos valores em uma tabela, baseado em uma script sql. 
            Exemplo: 
            inserir_lista("INSERT INTO {} VALUES ({}, '{}');",[("a","b","c"),("a","b","c")...])
            
            
           , na qual temos os parametros
           
           sql(obrigatorio): SQL para inserir valor
           valores(obrigatorio):lista com tuplas de valores para serem inseridos
           inserir_lista('SELECT * FROM city;')'''
        
        Erro='Esta Query é invalida!'
        #Verifica a query Se é um Insert
        if(str(sql).upper().find('INSERT')!= -1):
            try:
                self.cursor.executemany(sql,valores)
            except:
                raise Banco_erro(Erro)
        else: 
            raise Banco_erro(Erro)
        self.__bank.commit() 
        
        
    def inserir(self,sql:str,valores:tuple):
        '''Este metodo inseri diversos valores em uma tabela, baseado em uma script. Exemplo: inserir("INSERT INTO {} VALUES ({}, '{}');",("a","b","c"))
           , na qual temos os parametros
           
           sql(obrigatorio): SQL para inserir valor
           valores(obrigatorio):uma tupla de valores para serem inseridos'''
        Erro='Esta Query é invalida!'
        #Verifica a query Se é um Insert
        if(str(sql).upper().find('INSERT')!= -1):
            try:
                self.cursor.execute(sql,valores)
            except:
                raise Banco_erro(Erro)
        else: 
            raise Banco_erro(Erro)
        self.__bank.commit()
    
    def deletar(self,sql:str,valores:tuple):
        '''Este metodo deleta valores em uma tabela, baseado em uma script. Exemplo: deletar("DELETE FROM {} WHERE id = {}",("TABELA","3"))
           , na qual temos os parametros
           
           sql(obrigatorio): SQL para deletar valores da tabela
           valores(obrigatorio):uma tupla de valores para serem deletados'''
        Erro='Esta Query é invalida!'
        #Verifica a query Se é um DELETE
        if(str(sql).upper().find('DELETE')!= -1):
            try:
                self.cursor.execute(sql,valores)
            except:
                raise Banco_erro(Erro)
        else: 
            raise Banco_erro(Erro)
        self.__bank.commit()
    
    def atualizar(self,sql:str,valores:tuple):
        '''Este metodo atualiza valores em uma tabela, baseado em uma script. Exemplo: atualizar("UPDATE {} SET title = {} WHERE id = {}",("TABELA","x","3"))
           , na qual temos os parametros
           
           sql(obrigatorio): SQL para atualizar valores da tabela
           valores(obrigatorio):uma tupla de valores para serem atualizados'''
        Erro='Esta Query é invalida!'
        #Verifica a query Se é um UPDATE
        result=None
        if(str(sql).upper().find('UPDATE')!= -1):
            try:
                result=self.cursor.execute(sql.format(*valores))
            except:
                raise Banco_erro(Erro) 
        else:
            raise Banco_erro(Erro)
        self.__bank.commit()
        return result
    def fechar_conexao(self):
        '''Este metodo fecha conexão com o driver. Exemplo: fechar()'''
        #fechando a comunicação com o cursor e com o banco
        self.cursor.close()
        self.__bank.close()
####################################################################################################        
class Nao_Relacional():
    ''' Esta classe tem o intuito prover conexão e funções de CRUD em banco Não Relacional'''
    def __init__(self,Servidor,banco=None,endereco=None,porta=None):       
        '''No construtor temos seis parametros sendo um obrigatorio
        
        Servidor(obrigatorio):Tipo de Servidor de banco de dados que vai trabalhar.EXP.: 'Mongo'
        banco: O banco de dados na qual iremos no conectar no servidor
        endereco: É o endereço na qual vamos usar para nos conectar ao servidor.Exemplo: URL OU localhost OU 127.0.0.1...
        porta: É a porta de conexão para o endereço. Exemplo: 8080, 3601 ...
        '''
        
        if(Servidor=='Mongo'):
            if(Servidor is not None and banco is not None and endereco is not None and porta is not None):
                self.__con=MongoClient(endereco,porta)
                self.__bank=self.__con[banco]
            else:
                
                Erro="""Não é um servidor valor valido para MongoDB!
                        Valores obrigatorios são:
                        banco=banco de dados que sera usado,
                        endereco=endereco host do banco,
                        porta=porta do endereço de saida do banco
                        """
                raise Banco_erro(Erro)
        else:
            Erro="\n\nNão é um servidor valido!\nOs servidores validos são: 'Mongo'\nInsira um valor correto!"
            raise Banco_erro(Erro)  
        
    def buscar(self,dicionario,colecao):
        '''Este metodo busca o primeiro valor de chaves no banco: 
            buscar({"nome": "Radioactive"})
            
           O retorno é um dicionario com as chave que foi procurada
           , na qual temos os parametros
           
           dicionario: dicionario com chave e valor que queremos procurar
           coleção: é como uma tabela de banco de dados que queremos procurar'''
        Erro='\nColecao ou dicionario invalido!!'
        #Verifica se os valores de entrada são nulos caso seja nulos
        result=None
        if(dicionario is not None and colecao is not None):
            try:
                #colecao e em qual base deve ser procurada e dicionario e o json/dicionario que vai procurar
                result=self.__bank[colecao].find(dicionario)
            except:
                raise Banco_erro(Erro) 
        else:
            raise Banco_erro(Erro)
        return result
    
    def buscar_tudo(self,colecao):
        '''Este metodo busca o todos os  valores de chaves no banco: 
            buscar_tudo({"nome": "Radioactive"})
            
           O retorno é um dicionario com as chave que foi procurada
           , na qual temos os parametros
           
           dicionario: dicionario com chave e valor que queremos procurar
           coleção: é como uma tabela de banco de dados que queremos procurar'''
        Erro='\nColecao ou dicionario invalido!!'
        #Verifica se os valores de entrada são nulos caso seja nulos
        result=None
        if( colecao is not None):
            try:
                #colecao e em qual base deve ser procurada e dicionario e o json/dicionario que vai procurar
                result=self.__bank[colecao].find()
            except:
                raise Banco_erro(Erro) 
        else:
            raise Banco_erro(Erro)
        return result
        
    
    def atualizar(self,colecao,anterior,atual):
        '''Este metodo atualiza o todos os  valores de chaves no banco: 
            atualizar({"_id": 2},{"$set",{"novo":"Novooooo"}})
            
           , na qual temos os parametros
           
           anterior: dicionario com chave e valor que queremos procurar para atualizar
           atual: e o valor que queremos atualizar'''
        Erro='\nAtualização com sintaxe incorreta!!'
        #Verifica se os valores de entrada são nulos caso seja nulos
        if(type(anterior) is dict and type(atual) is dict):
            
            try:
                type(atual['$set'])==dict
                #Set é uma sintaxe do MongoDB, para atualizar um valor os parametros são dicionarios
                self.__bank[colecao].update_one(anterior,atual)
            except:
                raise Banco_erro(Erro) 
        else:
            raise Banco_erro(Erro)
        
        
        
        
    def inserir(self,dicionario,colecao,ids=True):
        '''Este metodo inseri o todos os  valores de chaves no banco: 
            inserir({\
              "nome": "Nothing left to say",\
              "banda": "Imagine Dragons",\
              "categorias": ["indie", "rock"],\
              "lancamento": datetime.datetime.now()\
             },True)
            
           , na qual temos os parametros
           
           dicionario: dicionario com chave e valor que queremos inserir 
           ids: True, se vamos inserir um id e False, se o Id vir no dicionario'''
        Erro='\nInserção com sintaxe incorreta!!'
        #Verifica se os valores de entrada são nulos caso seja nulos
        if(ids==True and type(dicionario)==dict):
            try:
                #Inserindo um dicionario
                self.__bank[colecao].insert_one(dicionario).inserted_id
            except:
                raise Banco_erro(Erro)
        elif(ids==False and type(dicionario)==dict):
            try:
                #Inserindo um dicionario
                self.__bank[colecao].insert_one(dicionario)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)
        
    def inserir_lista(self,lista,ids=True):
        '''Este metodo inseri diversos valores chave no banco: 
            inserir_lista({\
              "nome": "Nothing left to say",\
              "banda": "Imagine Dragons",\
              "categorias": ["indie", "rock"],\
              "lancamento": datetime.datetime.now()\
             },True)
            
           , na qual temos os parametros
           
           lista: lista de dicionarios com chave e valor que queremos inserir 
           ids: True, se vamos inserir um id e False, se o Id vir no dicionario'''
        Erro='\nInserção com sintaxe incorreta!!'
        #Verifica se os valores de entrada são nulos caso seja nulos
        if(ids==True and type(lista)==dict):
            try:
                #Inserindo um dicionario
                self.__bank.insert_many(lista).inserted_id
            except:
                raise Banco_erro(Erro)
        elif(ids==False and type(lista)==dict):
            try:
                #Inserindo um dicionario
                self.__bank.insert_many(lista)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)
        
        
    def deletar(self,dicionario):
        '''Este metodo deletar um valore chave no banco: 
            deletar({"_id": 1})
            
           , na qual temos os parametros
           
           dicionario: dicionario de valor que queremos deletar'''
        Erro='\nDelete com sintaxe incorreta!!'
        #Verifica se os valores de entrada são nulos caso seja nulos
        if(type(dicionario)==dict):
            try:
                #Inserindo um dicionario
                self.__bank.delet_one(dicionario)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)
        
        
    def deletar_tudo(self,dicionario):
        '''Este metodo deletar diversos valores chave no banco: 
            deletar_tudo({"banda": "Imagine Dragons"})
            
           , na qual temos os vparametros
           
           dicionario: dicionario de valor que queremos deletar'''
        Erro='\nDelete com sintaxe incorreta!!'
        #Verifica se os valores de entrada são nulos caso seja nulos
        if(type(dicionario)==dict):
            try:
                #Removendo todos os dicionarios
                self.__bank.delete_many(dicionario)
            except:
                raise Banco_erro(Erro)
        else:
            raise Banco_erro(Erro)
        