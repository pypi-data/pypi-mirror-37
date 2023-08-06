# -*- coding: utf-8 -*-
'''
@author: KaueBonfim
'''

'''

Este Modulo Trabalha com o processo automatizado de comunicação com outros programas e serviços

'''
import vsts
import testlink
    
class TestLink_API():
    ''' Esta classe gerar metodos melhorados para ser usado com a API do testlink em python'''
    def __init__(self,url_test_link,chave_usuario):
        '''No construtor temos dois parametros sendo um obrigatorio
        
        url_test_link(obrigatorio):Url do servidor jenkins de conexão com a API, sendo necessario passar o caminho ate o arquivo xmlrpc.php
        chave_usuario(obrigatorio): Qual a chave do usuario gerada dentro do Testlink para o usuario usar com a API
        
        Exemplo:
        
        TestLink_API("https://Server-testlink/lib/api/xmlrpc/v1/xmlrpc.php","1dbaee3220a7805fc501af94d084d04")
        '''
        self.__testlink = testlink.TestLinkHelper(url_test_link,chave_usuario).connect(testlink.TestlinkAPIClient)    
    
    def get_object(self):
        '''Este metodo retorna o objeto criado do testlink, tendo acesso as funções da API
        '''
        return self.__testlink
    
    def Criar_Feature(self,projeto_nome,plano_nome,suites_de_teste:list="Todas")->str:
        '''Este Metodo Cria apartir de suites de teste passadas os casos de teste e os steps em formato Gherkin
        recebendo como parametros:
        projeto_nome:Nome do projeto que esta locado no servidor e sera usado
        plano_nome:Nome do plano que esta locado no projeto e sera usado
        suites_de_teste: Pode se passar quais suites de teste deve ser feitas no servidor
        
        Exemplo:
        
        Criar_Feature("Projeto Energia e Luz", "Plano de teste de aplicações do tempo",["PES","Pis"])
        Criar_Feature("Projeto Energia e Luz", "Plano de teste de aplicações do tempo")
        '''
        def _replace(string:str):
            return string.replace("span","").replace('style="font-size:12px;"',"").replace('  style="font-family:arial,helvetica,sans-serif;"','')\
                .replace('- ','').replace("&ccedil;","ç").replace("&atilde;","ã").replace("&iacute;",'í').replace("\n\n","\n")\
                .replace('&quot;','"').replace('style="font-family: Arial, sans-serif; font-size: 13.3333px;"',"").replace('&eacute;',"é").replace('&aacute;',"á")\
                .replace('&oacute;',"ó").replace("&ordm;","°").replace("&gt;",">").replace("&otilde;","õ")\
                .replace('style="font-family: arial, helvetica, sans-serif; font-size: 12px;"',"").replace("//","").replace("./",".")\
                .replace('style="font-family:arial,helvetica,sans-serif;"',"").replace("&ecirc;","ê").replace("&#39;","'").replace("&uacute;","ú").replace("<br />","").replace("</p>","")\
                .replace("&Uacute;","Ú").replace("<p>","").replace("\n\t"," ",1).replace("\n ","And ").replace("\n\t","And ").replace("\n","").replace(",","").replace("&nbsp;"," ")\
                .replace("\t","").replace("And  ","").replace("&ldquo;",'"').replace("&rdquo;",'"').replace('< style="font-size: small;">< style="font-family: Arial;">',"")\
                .replace("</>","").replace("&Eacute;","-").replace("< >","").replace("<strong>","").replace("<em>","").replace("</em>","").replace("</strong>","")\
                .replace("<div>","").replace("</div>","").replace('< style="background-color: rgb(255 255 0);">',"").replace("<li>","").replace("</li>","")\
                .replace("<ul>","").replace("</ul>","").replace('< style="background-color:#ffff00;">',"")\
                .replace('''< style="font-size:12px;color:#000000;font-weight:400;text-decoration:none;font-family:'Arial';font-style:normal;">''',"").replace('< style="font-family: Arial;">',"")\
                .replace('< style="font-size: 12px;">< style="font-family: arial helvetica sans-serif;">',"").replace('<p style="margin-top: 0.49cm; margin-bottom: 0.49cm; line-height: 100%">','')\
                .replace('<font face="arial helvetica sans-serif">< style="font-size: 12px;">','').replace('</font>',"").replace('<p style="margin-bottom: 0cm; line-height: 150%;"> ',"")\
                .replace('<font face="Arial sans-serif">',"").replace('<font style="font-size: 11pt">',"").replace('<p style="margin-bottom: 0cm; line-height: 150%;">',"")\
                .replace('< style="font-size: 11pt; font-family: Arial sans-serif;">',"").replace('<p align="left" style="margin-bottom: 0cm; line-height: 150%;">','')\
                .replace('<font style="font-size: 12pt">','').replace('<font color="#000000">','')
                
        
        def tratar_step(step):
            return str(step).replace("And And ","And ").replace("Given And ","Given ").replace("And ","\nAnd ").replace("  "," ").replace('And \n',"")
        ##################################################################################
        #Separando o plano especifico que sera trabalhado para procurar os casos te teste#
        ##################################################################################
        
        
        plano=self.__testlink.getTestPlanByName(projeto_nome,plano_nome)
        
                
        #############################################################
        #Escolhendo quais Suites de Teste deve ser gerado o Gherkins#
        #############################################################
                
        suites=self.__testlink.getTestSuitesForTestPlan(plano[0]['id'])
        lista_suites=[]
        for suite in suites:
            if(suites_de_teste=="Todas"):
                lista_suites.append((suite['name'],suite['id']))
                
            else:
                for suitei in  suites_de_teste:
                    if(suitei==suite['name']):
                        lista_suites.append((suite['name'],suite['id']))
                        
        
        #############################################################
        #        Recebendo os casos de teste da suite de teste      #
        #############################################################
        
        lista_cenario=[]
        for suite in lista_suites:
            
            cenarios=self.__testlink.getTestCasesForTestSuite(suite[1],True,False)
            for cenario in cenarios:
                
                lista_cenario.append((suite[0],cenario['id'],cenario["name"]))
                
        #############################################################
        #  Encontrando as especificações do caso de teste           #
        #############################################################
        lista_especificando=[]
        for item_lista in lista_cenario:
            cenario=self.__testlink.getTestCase(item_lista[1])
            
            for especificacao in cenario:
                lista_especificando.append((item_lista[0],especificacao["name"],especificacao["preconditions"],especificacao["steps"]))
                
                
        ########################################################
        #  Colocando os steps em ordem do Gherkin              #
        ########################################################     
        Feature=[] 
        for especificacao in lista_especificando:
            Gherkin=[]
            for passos in especificacao[3]:
                Gherkin.append((str(passos["actions"]),str(passos["expected_results"])))
            

                Feature.append({"Feature:":especificacao[0],"Cenario: ":especificacao[1],"Given":str(especificacao[2]),"Passos: ":Gherkin})
        Arquivo={}
        ########################################################
        #  Construindo o arquivo .feature                      #
        ########################################################
        for especificacao in Feature:
            Feature={}
            Scenario="Scenario: "+especificacao["Cenario: "]
            Given="Given"+_replace(especificacao["Given"])
            Step=[]
            for steps in especificacao["Passos: "]:
                especificacao
                for step in range(len(steps)):
                    if(step==0):
                        passo=_replace(steps[step])
                        Step.append("When "+passo)
                    else:
                        passo=_replace(steps[step])
                        Step.append("Then "+passo)
            
            if(Arquivo.get(especificacao["Feature:"])):
                valor=Arquivo.get(especificacao["Feature:"])
                validador=True
                for v in valor:
                    if(v.get(Scenario)): 
                        validador=False
                        continue
                    
                if(validador==True):
                    valor.append({Scenario:Given+"\n"+"\n".join(Step)})        
                
                    
            else:
                Arquivo[especificacao["Feature:"]]=[{Scenario:Given+"\n"+"\n".join(Step)}]
            
        ########################################################
        #  Gravando o arquivo .feature                         #
        ########################################################
        
        for estrutura in Arquivo:
            feature=open(str(estrutura).replace("/", "-")+".feature","w")#gerando o arquivo
            feature.write("@"+estrutura.replace(" ","_")+"\n")#gerando a tag da feature
            feature.write("Feature: "+estrutura+"\n\n")#gerando o nome da feature
            
            for Cenarios in Arquivo[estrutura]:
                for Cenario in Cenarios:
                    feature.write("@"+Cenario.replace("Scenario: ","").replace(" ","_")+"\n")#gerando a tag do cenario
                    feature.write(str(Cenario)+"\n")#gerando o nome do cenario
                    feature.write(tratar_step(Cenarios[Cenario])+"\n\n")#Escrevendo os passos
            feature.close()#Fechando Arquivo