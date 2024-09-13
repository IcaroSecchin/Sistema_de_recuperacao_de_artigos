import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
from dotenv import load_dotenv
import os
import random
import string
import requests
from classes import Usuario, Pesquisa
import sqlite3
import arxiv
from classes_DAO import salvar_artigos_CHDB, salvar_artigos_SQLITE
import csv

CHDB_path = "colecoes_artigos"

def criar_csv(file_path:str, id:list, titulo:list, resumo:list, link:list):
    
    with open(file_path, 'w', newline='') as csvfile:
        
        spamwriter = csv.writer(csvfile, delimiter=';')
        spamwriter.writerow(["identificador"]+["titulo"]+["resumo"]+["link"])
        
        for i, t, r, l in zip(id, titulo, resumo, link):
            spamwriter.writerow([i]+[t]+[r]+[l])
    
    return 0
    
        

def buscar_arxiv(consulta, total_artigos, cpf, bd_path):
    
    client = arxiv.Client()

    pesquisa = arxiv.Search(
    query = consulta,
    max_results = int(total_artigos),
    sort_by = arxiv.SortCriterion.Relevance
    )
    
    identificador_lista = []
    titulo_lista = []
    resumo_lista = []
    link_lista = []
    
    for r in client.results(pesquisa):
        identificador = r.get_short_id()
        titulo = r.title
        resumo = r.summary
        link = r.entry_id
        
        identificador_lista.append(identificador)
        titulo_lista.append(titulo)
        resumo_lista.append(resumo)
        link_lista.append(link)
    
    if identificador_lista == []:
        return 0
    
    pesquisa = Pesquisa(identificador=identificador_lista, titulo= titulo_lista, resumo= resumo_lista, link= link_lista, consulta= consulta, cpf= cpf)
    
    salvar_artigos_SQLITE(pesquisa, bd_path)
    salvar_artigos_CHDB(pesquisa, CHDB_path)
    
    return 1

def login(cpf, senha, bd_path):
    
    banco = sqlite3.connect(bd_path)
    cursor = banco.cursor()
    

    cursor.execute("""SELECT nome FROM Usuario WHERE cpf = ? AND senha = ?""", [cpf, senha])

    usuario = cursor.fetchone()
    
    
    if usuario != None:    
        #login sucesso
        banco.commit()
        banco.close()
        return True
        
    banco.commit()
    banco.close()
    #login errado
    return False

def email_existe(email, bd_path):
    
    banco = sqlite3.connect(bd_path)
    cursor = banco.cursor()
    

    cursor.execute("""SELECT nome FROM Usuario WHERE e_mail = ?""", [email])

    usuario = cursor.fetchone()
    
    
    if usuario == None:    
        #e_mail não existente
        banco.commit()
        banco.close()
        return False
        
    banco.commit()
    banco.close()
    return True

def mudar_senha_bd(nova_senha, e_mail, bd_path):
    
    banco = sqlite3.connect(bd_path)
    cursor = banco.cursor()
    
    cursor.execute("""UPDATE Usuario SET senha = ? WHERE e_mail = ?""", (nova_senha, e_mail))
    
    banco.commit()
    banco.close()

    
def recuperar_senha(e_mail, bd_path):
    
    '''
    conteudo do arquivo .env ja que tal não será enviado pelo ava:
    enviador=sistemaderecuperacaodeconta.poo@gmail.com
    senhaapp=gjsz ucpq hqax akbi
    '''
    
    banco = sqlite3.connect(bd_path)
    cursor = banco.cursor()
    

    cursor.execute("""SELECT nome FROM Usuario WHERE e_mail = ?""", [e_mail])

    usuario = cursor.fetchall()
    
    if usuario == None:    
        #e_mail não existente
        banco.commit()
        banco.close()
        return False
    
    usuario = usuario[0][0]
        
    banco.commit()
    banco.close()

    characteres = ['!','@','#','$']
    senhalist = []

    while len(senhalist) < 5:

        j = random.randrange(3)

        if j == 0:
            
            letra = random.choice(string.ascii_letters)

            senhalist.append(letra)
        
        elif j == 1:

            num = random.randrange(10)

            senhalist.append(str(num))

        elif j == 2:

            char = random.choice(characteres)
            senhalist.append(char)

    novasenha = ''.join(senhalist)

    load_dotenv()
    
    enviador = os.getenv('enviador')
    senhaapp = os.getenv('senhaapp')
    
    recebedor = e_mail

    assunto = "Recuperação de Senha" 
    body = f"Olá {usuario}, sua nova senha é ({novasenha})."

    mensagem = MIMEMultipart()
    mensagem["From"] = enviador
    mensagem["To"] = recebedor
    mensagem["Subject"] = assunto

    mensagem.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(enviador, senhaapp)
            server.sendmail(enviador, recebedor, mensagem.as_string())
        mudar_senha_bd(novasenha, e_mail, bd_path)
        return True

    except Exception as e:
        return False
    
def achar_cep(usuario:Usuario):

    link = f'https://viacep.com.br/ws/{usuario.endereco}/json/'

    requisicao = requests.get(link)

    if requisicao.status_code == 200:

        endereco = requisicao.json()

        logradouro = endereco['logradouro']
        cidade = endereco['localidade']
        bairro = endereco['bairro']
        estado = endereco['uf']
        
        endereco_completo = f'{logradouro},{cidade},{bairro},{estado}'
        
        return endereco_completo

    else:
        #Falhou

        return False