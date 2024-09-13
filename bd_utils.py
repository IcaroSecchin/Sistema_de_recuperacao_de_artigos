import sqlite3

def criar_banco_dados_Usuario(bd_path):
    
    conexao = sqlite3.connect(bd_path)
    
    cursor = conexao.cursor()
    
    cursor.execute(
        """            
        CREATE TABLE Usuario (
            nome TEXT NOT NULL,
            cpf VARCHAR(14) NOT NULL,
            idade TEXT NOT NULL,
            e_mail TEXT NOT NULL,
            endereco TEXT NOT NULL,
            senha TEXT         
        );
    """
    )
    
    conexao.close()

def criar_banco_dados_Artigo(bd_path):
    
    conexao = sqlite3.connect(bd_path)
    
    cursor = conexao.cursor()
    
    cursor.execute(
        """            
        CREATE TABLE Artigo (
            id_artigo TEXT NOT NULL,
            titulo TEXT NOT NULL,
            resumo TEXT NOT NULL,
            link TEXT NOT NULL,
            CPF_do_usuario TEXT NOT NULL,
            consulta TEXT NOT NULL        
        );
    """
    )
    
    conexao.close()