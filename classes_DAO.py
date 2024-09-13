import sqlite3
from classes import Usuario, Pesquisa
import chromadb

def modificar_senha(cpf, senha_antiga, nova_senha, bd_path):
    
    banco = sqlite3.connect(bd_path)
    cursor = banco.cursor()
    
    cursor.execute("""SELECT senha FROM Usuario WHERE cpf = ?""", [cpf])
    
    senha_antiga_bd = cursor.fetchone()
    
    senha_antiga_bd = senha_antiga_bd[0]
    
    if senha_antiga_bd != senha_antiga:
        
        banco.commit()
        banco.close()
        
        return False
    
    cursor.execute("""UPDATE Usuario SET senha=? WHERE cpf=?""", [nova_senha, cpf])
    
    banco.commit()
    banco.close()
    
    return True
    
def salvar_usuario(usuario : Usuario, bd_path):
    
    banco = sqlite3.connect(bd_path)
    cursor = banco.cursor()
    
    cursor.execute("INSERT INTO Usuario (nome, cpf, idade, e_mail, endereco, senha) VALUES (?,?,?,?,?,?)", (usuario.nome, usuario.cpf, usuario.idade, usuario.e_mail, usuario.endereco, usuario.senha))
                
    banco.commit()
    banco.close()
    
    #Sucesso
    return 0

def verificar_CPF_duplicado(usuario: Usuario, bd_path):
    
    banco = sqlite3.connect(bd_path)
    cursor = banco.cursor()
    
    cursor.execute("""SELECT * FROM Usuario WHERE cpf = ?""", [usuario.cpf])

    if cursor.fetchone():    
        #Caso CPF tenha sido cadastrado
        banco.commit()
        banco.close()
        return 1
    
    banco.commit()
    banco.close()
    
    return 0

def salvar_artigos_SQLITE(pesquisa: Pesquisa, bd_path):
    banco = sqlite3.connect(bd_path)
    cursor = banco.cursor()
    
    for ide, tit, res, lin in zip(pesquisa.identificador, pesquisa.titulo, pesquisa.resumo, pesquisa.link):
    
        cursor.execute("INSERT INTO Artigo (id_artigo, titulo, resumo, link, CPF_do_usuario, consulta) VALUES (?,?,?,?,?,?)", (ide, tit, res, lin, pesquisa.cpf, pesquisa.consulta))
                
    banco.commit()
    banco.close()
    
    #Sucesso
    return 0

def salvar_artigos_CHDB(pesquisa: Pesquisa, path_chromadb):
    client = chromadb.PersistentClient(path = path_chromadb)
    
    collection = client.get_or_create_collection(name=str(pesquisa.cpf))
    
    collection.upsert(
    documents = pesquisa.resumo,
    ids =  pesquisa.identificador
    )

def consultar_BD(consulta: str, cpf, path_chromadb,bd_path):
    
    client = chromadb.PersistentClient(path= path_chromadb)
    
    collection = client.get_or_create_collection(name=str(cpf))
    
    resultado = collection.get(
    where_document= {"$contains": consulta}
    )
    
    if resultado["ids"] == []:
        return 1
    
    banco = sqlite3.connect(bd_path)
    cursor = banco.cursor()
    
    
    titulos = []
    resumos = []
    links = []
    
    for i in resultado["ids"]:
        
        cursor.execute("""SELECT titulo FROM Artigo WHERE id_artigo = ?""", [i])
        titulo = cursor.fetchone()
        titulo = list(titulo)
        titulo = titulo[0]
        titulos.append(titulo)
        
        cursor.execute("""SELECT resumo FROM Artigo WHERE id_artigo = ?""", [i])
        resumo = cursor.fetchone()
        resumo = list(resumo)
        resumo = resumo[0]
        resumos.append(resumo)
        
        cursor.execute("""SELECT link FROM Artigo WHERE id_artigo = ?""", [i])
        link = cursor.fetchone()
        link = list(link)
        link = link[0]
        links.append(link)
    
    banco.commit()
    banco.close()
    
    return resultado["ids"], titulos, resumos, links

def consultar_toda_colecao(cpf, path_chromadb,bd_path):
    
    client = chromadb.PersistentClient(path= path_chromadb)
    
    collection = client.get_or_create_collection(name=str(cpf))
    
    resultado = collection.get()
    
    titulos = []
    resumos = []
    links = []
    
    if resultado["ids"] == []:
        return resultado["ids"], titulos, resumos, links
    
    banco = sqlite3.connect(bd_path)
    cursor = banco.cursor()
    
    
    for i in resultado["ids"]:
        
        cursor.execute("""SELECT titulo FROM Artigo WHERE id_artigo = ?""", [i])
        titulo = cursor.fetchone()
        titulo = list(titulo)
        titulo = titulo[0]
        titulos.append(titulo)
        
        cursor.execute("""SELECT resumo FROM Artigo WHERE id_artigo = ?""", [i])
        resumo = cursor.fetchone()
        resumo = list(resumo)
        resumo = resumo[0]
        resumos.append(resumo)
        
        cursor.execute("""SELECT link FROM Artigo WHERE id_artigo = ?""", [i])
        link = cursor.fetchone()
        link = list(link)
        link = link[0]
        links.append(link)
    
    banco.commit()
    banco.close()
    
    return resultado["ids"], titulos, resumos, links