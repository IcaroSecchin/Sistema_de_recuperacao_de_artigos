import functions
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QInputDialog,
    QMessageBox,
    QWidget,
    QLineEdit,
    QFormLayout,
    QScrollArea,
    QLabel,
    QFrame,
    QFileDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
import os
import bd_utils
import functions
import classes_DAO
from classes import Usuario

bd_path = 'Banco_de_dados/banco_dados.bd'
chromabd_path = 'colecoes_artigos'

class Janela_Inicial(QWidget):
    def __init__(self):

        botao_cadastro = QPushButton("Cadastrar Novo Usuário")
        botao_recuperarsenha = QPushButton("Recuperar Senha")
        botao_login = QPushButton("Login")

        super().__init__()
        
        self.setWindowTitle("SISTEMA RECUPERAÇÃO DE ARTIGOS CIENTÍFICOS")
        self.setFixedSize(500,300)
        
        layout = QVBoxLayout()
        
        layout.addWidget(botao_cadastro)
        botao_cadastro.clicked.connect(self.abrir_janela_cadastro)
        botao_cadastro.setFixedHeight(60)

        layout.addWidget(botao_recuperarsenha)
        botao_recuperarsenha.clicked.connect(self.abrir_janela_recuperar_senha)
        botao_recuperarsenha.setFixedHeight(60)

        layout.addWidget(botao_login)
        botao_login.clicked.connect(self.abrir_janela_login)
        botao_login.setFixedHeight(60)
        
        self.setLayout(layout)
        
    def abrir_janela_cadastro(self):
        self.janela_cadastro = Janela_Cadastro()
        self.janela_cadastro.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.janela_cadastro.show()
    
    def abrir_janela_recuperar_senha(self):
        self.janela_recuperar_senha = Janela_recuperar_senha()
        self.janela_recuperar_senha.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.janela_recuperar_senha.show()
    
    def abrir_janela_login(self):
        self.janela_login = Janela_login(self)
        self.janela_login.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.janela_login.show()

class Janela_Cadastro(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("CADASTRO")
        self.setFixedWidth(300)
        
        layout = QVBoxLayout()
        formlayout = QFormLayout()
        
        self.caixa_nome = QLineEdit(self)
        text_nome = 'Nome:'
        
        self.caixa_idade = QLineEdit(self)
        text_idade = 'Idade:'
        
        self.caixa_cpf = QLineEdit(self)
        text_cpf = 'CPF:'
        
        self.caixa_email = QLineEdit(self)
        text_email = 'Email'
        
        self.caixa_senha = QLineEdit(self)
        text_senha = 'Senha:'
        
        self.caixa_endereco = QLineEdit(self)
        text_endereco = 'CEP:'
        
        formlayout.addRow(text_nome, self.caixa_nome)
        formlayout.addRow(text_idade, self.caixa_idade)
        formlayout.addRow(text_cpf, self.caixa_cpf)
        formlayout.addRow(text_email, self.caixa_email)
        formlayout.addRow(text_senha, self.caixa_senha)
        formlayout.addRow(text_endereco, self.caixa_endereco)
        
        
        botao_confirmar = QPushButton('Confirmar')
        
        botao_confirmar.clicked.connect(self.salvar_dados)
        layout.addLayout(formlayout)
        layout.addWidget(botao_confirmar)
        self.setLayout(layout)
        
    def keyPressEvent(self, event):
        # Capturar evento de tecla Enter
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.salvar_dados()
            
    def salvar_dados(self):
        
        nome = self.caixa_nome.text()
        cpf = self.caixa_cpf.text()
        idade = self.caixa_idade.text()
        e_mail = self.caixa_email.text()
        senha = self.caixa_senha.text()
        cep = self.caixa_endereco.text()
        
        usuario = Usuario(nome, cpf, idade, e_mail, cep, senha) 
        
        if (nome or cpf or idade or e_mail or senha or cep) == '':
            self.erro_campos_nao_preenchidos()
            return 0
        
        if not os.path.exists(bd_path): 
            bd_utils.criar_banco_dados_Usuario(bd_path)
            bd_utils.criar_banco_dados_Artigo(bd_path)
            
        if classes_DAO.verificar_CPF_duplicado(usuario, bd_path) == 1:
            self.erro_CPF_ja_registrado()
        else:
            if functions.achar_cep(usuario) == False:
                self.erro_CEP_nao_achado()
                endereco_completo = self.caixa_endereco.text()
                usuario.endereco = endereco_completo
            else:
                usuario.endereco = functions.achar_cep(usuario)
                
            classes_DAO.salvar_usuario(usuario, bd_path)
            self.cadastro_sucesso()
              

    def erro_CPF_ja_registrado(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('ERRO!')
        
        self.mensagem.setText('CPF Já Cadastrado.\nCaso não lembre a senha,\nfaça o procedimeto de recuperação.')
        self.close()
        self.mensagem.exec()
        
    def erro_campos_nao_preenchidos(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('ERRO!')
        self.mensagem.setText('Há campos obrigatorios não preenchidos')
        self.close()
        self.mensagem.exec()
    
    def erro_CEP_nao_achado(self):
    
        novo_endereco, ok = QInputDialog.getText(self, 'ERRO!', 'CEP não encontrado, digite o endereço completo:')
        
        if ok and novo_endereco:
            self.caixa_endereco.setText(novo_endereco)
            return 0
            
        elif novo_endereco == '' and ok:
            self.erro_CEP_nao_achado()
            
        else:
            self.close()
    
    def cadastro_sucesso(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('SUCESSO!')
        
        self.mensagem.setText('Cadastro realizado com Sucesso!')
        self.close()
        self.mensagem.exec()
    
class Janela_recuperar_senha(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("RECUPERAR SENHA")
        
        layout = QVBoxLayout()
        formlayout = QFormLayout()
        
        self.caixa_email = QLineEdit(self)
        text_email = 'Email de recuperação:'
        
        formlayout.addRow(text_email, self.caixa_email)
        
        botao_confirmar = QPushButton('Confirmar')
        
        botao_confirmar.clicked.connect(self.funcao_de_envio)
        
        layout.addLayout(formlayout)
        layout.addWidget(botao_confirmar)
        self.setLayout(layout)
    
    def keyPressEvent(self, event):
        # Capturar evento de tecla Enter
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.funcao_de_envio()
    
    def erro_email_nao_achado(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('ERRO!')
        self.mensagem.setText('Email não cadastrado, tente novamente ou faça o seu registro.')
        self.close()
        self.mensagem.exec()
    
    def email_recupercao_enviado(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('EMAIL ENVIADO')
        self.mensagem.setText('Email de recuperação de senha enviado com sucesso.')
        self.close()
        self.mensagem.exec()
    
    def funcao_de_envio(self):
        email = self.caixa_email.text()
        
        if functions.email_existe(email, bd_path) == False:
            self.erro_email_nao_achado()
            
        else:
            functions.recuperar_senha(email, bd_path)
            self.email_recupercao_enviado()
            
    
class Janela_login(QWidget):
    def __init__(self, janela_inicial):
        super().__init__()
        
        self.janela_inicial = janela_inicial
        
        self.setWindowTitle("LOGIN")
        self.setFixedSize(250,100)
        
        layout = QVBoxLayout()
        formlayout = QFormLayout()
        
        self.caixa_cpf = QLineEdit(self)
        text_cpf = 'CPF:'
        
        self.caixa_senha = QLineEdit(self)
        text_senha = 'Senha:'
        
        formlayout.addRow(text_cpf, self.caixa_cpf)
        formlayout.addRow(text_senha, self.caixa_senha)
        
        botao_confirmar = QPushButton('Confirmar')
        
        botao_confirmar.clicked.connect(self.enviar_login)
        
        layout.addLayout(formlayout)
        layout.addWidget(botao_confirmar)
        self.setLayout(layout)
    
    def keyPressEvent(self, event):
        # Capturar evento de tecla Enter
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.enviar_login()
    
    def enviar_login(self):
        cpf = self.caixa_cpf.text()
        senha = self.caixa_senha.text()
        
        if functions.login(cpf, senha, bd_path) == True:
            self.abrir_menu_principal()
            
        else:
            self.erro_usuario_nao_cadastrado()
    
    def erro_usuario_nao_cadastrado(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('ERRO!')
        self.mensagem.setText('CPF ou senha errado, tente novamente ou faça registro caso não tenha.')
        self.close()
        self.mensagem.exec()
    
    def abrir_menu_principal(self):
        self.menu_principal = Menu_Principal(self.caixa_cpf.text())
        self.menu_principal.show()
        self.janela_inicial.close()
        self.close() 

class Menu_Principal(QWidget):
    def __init__(self, cpf):
        
        self.cpf_do_pesquisador = cpf
        
        botao_buscar_arxiv = QPushButton("REALIZAR BUSCA ARXIV")
        botao_buscar_artigos = QPushButton("REALIZAR BUSCA COLEÇÃO ARTIGOS")
        botao_listar_artigos = QPushButton("LISTAR ARTIGOS")
        botao_mudar_senha = QPushButton("MUDAR SENHA")
        botao_voltar = QPushButton("VOLTAR AO MENU PRINCIPAL")

        super().__init__()
        
        self.setWindowTitle("MENU PRINCIPAL")
        self.setFixedSize(600,400)
        
        layout = QVBoxLayout()
        
        layout.addWidget(botao_buscar_arxiv)
        botao_buscar_arxiv.clicked.connect(self.buscar_arxiv)
        botao_buscar_arxiv.setFixedHeight(60)

        layout.addWidget(botao_buscar_artigos)
        botao_buscar_artigos.clicked.connect(self.colecao_artigos)
        botao_buscar_artigos.setFixedHeight(60)

        layout.addWidget(botao_listar_artigos)
        botao_listar_artigos.clicked.connect(self.lsitar_artigos)
        botao_listar_artigos.setFixedHeight(60)
        
        layout.addWidget(botao_mudar_senha)
        botao_mudar_senha.clicked.connect(self.mudar_senha)
        botao_mudar_senha.setFixedHeight(60)
        
        layout.addWidget(botao_voltar)
        botao_voltar.clicked.connect(self.voltar_ao_inicio)
        botao_voltar.setFixedHeight(60)
        
        self.setLayout(layout)

    def buscar_arxiv(self):
        self.janela_de_busca = Janela_buscar_arxiv(self.cpf_do_pesquisador)
        self.janela_de_busca.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.janela_de_busca.show()
        
    def colecao_artigos(self):
        self.janela_de_colecao = Janela_colecao_de_artigos(self.cpf_do_pesquisador)
        self.janela_de_colecao.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.janela_de_colecao.show()
        
    def lsitar_artigos(self):
        
        ids, titulos, resumos, links = classes_DAO.consultar_toda_colecao(self.cpf_do_pesquisador, chromabd_path, bd_path)
        
        self.janela_listar_artigos = Janela_mostrar_colecao(ids, titulos, resumos, links, self.cpf_do_pesquisador)
        
        self.janela_listar_artigos.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.janela_listar_artigos.show()
    
    def mudar_senha(self):
        self.janela_mudar_senha = Janela_mudar_senha(self.cpf_do_pesquisador)
        self.janela_mudar_senha.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.janela_mudar_senha.show()
        
    def voltar_ao_inicio(self):
        self.janela_inicial = Janela_Inicial()
        self.janela_inicial.show()
        self.close()

class Janela_buscar_arxiv(QWidget):
    def __init__(self, cpf):
        super().__init__()
        
        self.cpf_do_pesquisador = cpf
        
        self.setWindowTitle("BUSCAR ARQUIVOS")
        self.setFixedSize(250,100)
        
        layout = QVBoxLayout()
        formlayout = QFormLayout()
        
        self.caixa_consulta = QLineEdit(self)
        text_consulta = 'Consulta:'
        
        self.caixa_quant_artigos = QLineEdit(self)
        text_quant_artigos = 'Quantidade de Artigos:'
        
        formlayout.addRow(text_consulta, self.caixa_consulta)
        formlayout.addRow(text_quant_artigos, self.caixa_quant_artigos)
        
        botao_confirmar = QPushButton('Confirmar')
        
        botao_confirmar.clicked.connect(self.buscar_e_salvar)
        
        layout.addLayout(formlayout)
        layout.addWidget(botao_confirmar)
        self.setLayout(layout)
    
    def keyPressEvent(self, event):
        # Capturar evento de tecla Enter
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.buscar_e_salvar()
    
    def buscar_e_salvar(self):
        total_artigos = self.caixa_quant_artigos.text()
        consulta = self.caixa_consulta.text()
        
        if (total_artigos or consulta) == '':
            self.campos_vazios()
        else:
            resposta = functions.buscar_arxiv(consulta, total_artigos, self.cpf_do_pesquisador, bd_path)
            
            if resposta == 0:
                self.erro_nada_achado()
            else: 
                self.busca_realizada()
    
    def busca_realizada(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('SUCESSO!')
        self.mensagem.setText('Busca realizada com sucesso e já armazenada no banco de dados.')
        self.close()
        self.mensagem.exec()
    
    def campos_vazios(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('ERRO!')
        self.mensagem.setText('Há campos obrigatórios não preenchidos.')
        self.close()
        self.show()
        self.mensagem.exec()
    
    def erro_nada_achado(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('ERRO!')
        self.mensagem.setText('Nenhum artigo foi encontrado com base na sua pesquisa.')
        self.close()
        self.mensagem.exec()
        
class Janela_colecao_de_artigos(QWidget):
    def __init__(self, cpf):
        super().__init__()
        
        self.cpf_do_pesquisador = cpf
        
        self.setWindowTitle("COLEÇÃO DE ARTIGOS")
        self.setFixedSize(300,100)
        
        layout = QVBoxLayout()
        formlayout = QFormLayout()
        
        self.caixa_consulta = QLineEdit(self)
        text_consulta = 'Consulta:'
        
        formlayout.addRow(text_consulta, self.caixa_consulta)
        
        botao_confirmar = QPushButton('Confirmar')
        
        botao_confirmar.clicked.connect(self.buscar_colecoes)
        
        layout.addLayout(formlayout)
        layout.addWidget(botao_confirmar)
        self.setLayout(layout)
    
    def keyPressEvent(self, event):
        # Capturar evento de tecla Enter
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.buscar_colecoes()
    
    def buscar_colecoes(self):
     
        consulta = self.caixa_consulta.text()
        
        if consulta == '':
            self.erro_nada_achado()
        else:
            if classes_DAO.consultar_BD(consulta, self.cpf_do_pesquisador, chromabd_path, bd_path) == 1:
                self.erro_nada_achado()
            else:
                ids, titulos, resumos, links = classes_DAO.consultar_BD(consulta, self.cpf_do_pesquisador, chromabd_path, bd_path)
                
                self.Janela_mostrar_colecao = Janela_mostrar_pesquisa(ids, titulos, resumos, links, self.cpf_do_pesquisador)
                
                self.Janela_mostrar_colecao.setWindowModality(Qt.WindowModality.ApplicationModal) 
                self.Janela_mostrar_colecao.show()   
                self.close()
    
    def erro_nada_achado(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('ERRO!')
        self.mensagem.setText('Nenhum artigo foi achado.')
        self.mensagem.exec()
        
        
class Janela_mostrar_pesquisa(QWidget):
    def __init__(self, ids, titulos, resumos, links, cpf):
        
        self.ids = ids
        self.titulos = titulos
        self.resumos = resumos
        self.links = links
        self.cpf_do_pesquisador = cpf
        
        super().__init__()
        self.setWindowTitle('COLEÇÃO DE ARTIGOS')
        self.setFixedSize(600, 600)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Área de rolagem para os textos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Permitir que o widget dentro da área de rolagem seja redimensionado
        main_layout.addWidget(scroll_area)

        # Widget para conter os rótulos
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        # Layout para os rótulos
        scroll_layout = QVBoxLayout(scroll_widget)
        
        texto_quant = QLabel(f'\nForam achados {len(ids)} textos para a pesquisa feita\n')
        texto_quant.setWordWrap(True)
        texto_quant.setStyleSheet("font-size: 14px;")
        texto_quant.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(texto_quant)
        
        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setFrameShadow(QFrame.Shadow.Sunken)
        scroll_layout.addWidget(separador)
        
        for i, t, r, l in zip(ids, titulos, resumos, links):
            
        
            texto = QLabel(f'ID: {i}\n\nTítulo: {t}\n\nResumo:')
            texto.setWordWrap(True)
            texto.setStyleSheet("font-size: 14px;")
            texto.setAlignment(Qt.AlignmentFlag.AlignJustify)
            scroll_layout.addWidget(texto)
            
            resumo = QLabel(f'{r}')
            resumo.setWordWrap(True)
            resumo.setStyleSheet("font-size: 14px;")
            resumo.setAlignment(Qt.AlignmentFlag.AlignJustify)
            scroll_layout.addWidget(resumo)
            
            link = QLabel(f'\n<a href={l}>Clique aqui para acessar o site com este artigo!</a>\n\n')
            link.setOpenExternalLinks(True)
            link.setStyleSheet("font-size: 14px;")
            link.setAlignment(Qt.AlignmentFlag.AlignJustify)
            scroll_layout.addWidget(link)
            
            separador = QFrame()
            separador.setFrameShape(QFrame.Shape.HLine)
            separador.setFrameShadow(QFrame.Shadow.Sunken)
            scroll_layout.addWidget(separador)
        
        botao = QPushButton("Exportar CSV")
        
        botao.clicked.connect(self.salvar_arq_csv)
        
        main_layout.addWidget(botao)
        scroll_widget.setLayout(scroll_layout)
        self.setLayout(main_layout)
    
    def salvar_arq_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", f"{self.cpf_do_pesquisador}_pesquisa", "Arquivos CSV (*.csv);;Arquivo texto (*.txt);;Todos os Arquivos (*)")
        if file_path:
            functions.criar_csv(file_path, self.ids, self.titulos, self.resumos, self.links)
            self.csv_salvo_sucesso()
            
    def csv_salvo_sucesso(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('SALVO COM SUCESSO!')
        self.mensagem.setText('Arquivo salvo com sucesso.')
        self.mensagem.exec()

class Janela_mostrar_colecao(QWidget):
    def __init__(self, ids, titulos, resumos, links, cpf):
        
        self.ids = ids
        self.titulos = titulos
        self.resumos = resumos
        self.links = links
        self.cpf_do_pesquisador = cpf
        
        super().__init__()
        self.setWindowTitle('TODA COLEÇÃO DE ARTIGOS')
        self.setFixedSize(600, 600)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Área de rolagem para os textos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Permitir que o widget dentro da área de rolagem seja redimensionado
        main_layout.addWidget(scroll_area)

        # Widget para conter os rótulos
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        # Layout para os rótulos
        scroll_layout = QVBoxLayout(scroll_widget)
        
        texto_quant = QLabel(f'\nVocê pussui {len(ids)} artigos registrados\n')
        texto_quant.setWordWrap(True)
        texto_quant.setStyleSheet("font-size: 14px;")
        texto_quant.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(texto_quant)
        
        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setFrameShadow(QFrame.Shadow.Sunken)
        scroll_layout.addWidget(separador)
        
        for i, t, r, l in zip(ids, titulos, resumos, links):
            
        
            texto = QLabel(f'ID: {i}\n\nTítulo: {t}\n\nResumo:')
            texto.setWordWrap(True)
            texto.setStyleSheet("font-size: 14px;")
            texto.setAlignment(Qt.AlignmentFlag.AlignJustify)
            scroll_layout.addWidget(texto)
            
            resumo = QLabel(f'{r}')
            resumo.setWordWrap(True)
            resumo.setStyleSheet("font-size: 14px;")
            resumo.setAlignment(Qt.AlignmentFlag.AlignJustify)
            scroll_layout.addWidget(resumo)
            
            link = QLabel(f'\n<a href={l}>Clique aqui para acessar o site com este artigo!</a>\n\n')
            link.setOpenExternalLinks(True)
            link.setStyleSheet("font-size: 14px;")
            link.setAlignment(Qt.AlignmentFlag.AlignJustify)
            scroll_layout.addWidget(link)
            
            separador = QFrame()
            separador.setFrameShape(QFrame.Shape.HLine)
            separador.setFrameShadow(QFrame.Shadow.Sunken)
            scroll_layout.addWidget(separador)
        
        botao = QPushButton("Exportar CSV")
        
        botao.clicked.connect(self.salvar_arq_csv)
        
        main_layout.addWidget(botao)
        scroll_widget.setLayout(scroll_layout)
        self.setLayout(main_layout)
        
    def salvar_arq_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Arquivo", f"{self.cpf_do_pesquisador}_colecao", "Arquivos CSV (*.csv);;Arquivo texto (*.txt);;Todos os Arquivos (*)")
        if file_path:
            functions.criar_csv(file_path, self.ids, self.titulos, self.resumos, self.links)
            self.csv_salvo_sucesso()
            
    def csv_salvo_sucesso(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('SALVO COM SUCESSO!')
        self.mensagem.setText('Arquivo salvo com sucesso.')
        self.mensagem.exec()
        
class Janela_mudar_senha(QWidget):
    def __init__(self, cpf):
        
        self.cpf_do_pesquisador = cpf
        
        super().__init__()
        self.setWindowTitle('MUDAR SENHA')
        self.setFixedSize(250,100)
        
        layout = QVBoxLayout()
        formlayout = QFormLayout()
        
        self.caixa_senha_antiga = QLineEdit(self)
        text_senha_antiga = 'Senha atual:'
        
        self.caixa_senha_nova = QLineEdit(self)
        text_senha_nova = 'Senha nova:'
        
        formlayout.addRow(text_senha_antiga, self.caixa_senha_antiga)
        formlayout.addRow(text_senha_nova, self.caixa_senha_nova)
        
        botao_confirmar = QPushButton('Confirmar')
        
        botao_confirmar.clicked.connect(self.mudar_senha)
        
        layout.addLayout(formlayout)
        layout.addWidget(botao_confirmar)
        self.setLayout(layout)
    
    def keyPressEvent(self, event):
        # Capturar evento de tecla Enter
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.mudar_senha()
        
    def mudar_senha(self):
        
        senha_antiga = self.caixa_senha_antiga.text()
        senha_nova = self.caixa_senha_nova.text()
        
        teste = classes_DAO.modificar_senha(self.cpf_do_pesquisador, senha_antiga, senha_nova, bd_path)
        
        if senha_antiga == '' or senha_nova == '':
            self.campos_nao_preenchidos()
        else:
            if teste == False:
                self.erro_mudanca()
            else:
                self.sucesso_mudanca()
    
    def sucesso_mudanca(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('SUCESSO!')
        self.mensagem.setText('Mudança realizada com sucesso.')
        self.close()
        self.mensagem.exec()
    
    def erro_mudanca(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('ERRO!')
        self.mensagem.setText('Senha atual digitada errada.')
        self.close()
        self.show()
        self.mensagem.exec()
    
    def campos_nao_preenchidos(self):
        self.mensagem = QMessageBox()
        self.mensagem.setWindowTitle('ERRO!')
        self.mensagem.setText('Há campos obrigatorios não preenchidos.')
        self.close()
        self.show()
        self.mensagem.exec()     