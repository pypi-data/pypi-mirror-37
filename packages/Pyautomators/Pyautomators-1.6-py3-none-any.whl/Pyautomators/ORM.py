'''
Created on 9 de out de 2018

@author: koliveirab
'''
import sqlalchemy
from pandas.io import sql
from .Error import Banco_erro
class Alquimista():
    ''' Esta classe tem o intuito prover conexão e funções de CRUD em banco Relacional e fazer um link direto com DataFrame'''
    def __init__(self,url):   
        '''No construtor temos um parametro sendo um obrigatorio
        
        url= É a url de conexão do servidor de banco de dados. EXEMPLO.:'jdbc:sqlserver://localhost:1433' ou'postgresql://usr:pass@localhost:5432/sqlalchemy'
        
        USAR URL VALIDA
        '''
        try:
            self.__engine=sqlalchemy.create_engine(url)
        except:
            Erro='''
            Url Invalida!!
            Use o Exemplo:
            sqlserver://[serverName[\instanceName][:portNumber]][;property=value[;property=value]] 
            '''
            raise Banco_erro(Erro)
        
    def buscar(self,query,params=None):
        '''Este metodo busca valores em uma tabela, baseado em uma script/Query. Exemplo: 
            buscar("SELECT %(valor) FROM data_table group by dept",[(valor:valor)])
        
           , na qual temos os parametros
           
           query(obrigatorio): query no banco
           params(obrigatorio):uma tupla de valores para serem atualizados'''
        return sql.read_sql_query(sql=query.format(params), con=self.__engine)
    
    def DF_para_sql(self,DF,nome_tabela):
        '''Este metodo inseri um DataFrame em um banco. Exemplo: DF_para_sql(DF,"TabelaNova")
           , na qual temos os parametros
           
           DF(obrigatorio): DataFrame que sera inserido
           nome_tabela(obrigatorio):Nome da tabela'''
        DF.to_sql(nome_tabela,self.__engine)
    
    