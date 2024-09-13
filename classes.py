class Usuario:
    def __init__ (self, nome, cpf, idade, e_mail, endereco, senha):

        self.nome = nome
        self.cpf = cpf
        self.idade = idade
        self.e_mail = e_mail
        self.endereco = endereco
        self.senha = senha

class Pesquisa:
    def __init__(self, identificador, titulo, resumo, link, consulta, cpf):
        
        self.identificador = identificador
        self.titulo = titulo
        self.resumo = resumo
        self.link = link
        self.consulta = consulta
        self.cpf = cpf