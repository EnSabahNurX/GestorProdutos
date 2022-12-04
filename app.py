import csv
import os
import sqlite3
from tkinter import *
from tkinter import ttk

cor_fundo = "#282a33"


class Produto:
    # Armazena a informação do PATH do projeto de acordo com o sistema utilizado
    diretorio_base = os.path.abspath(os.path.dirname(__file__))
    # Caminho para base de dados
    db = diretorio_base + '/database/produtos.db'

    def __init__(self, root):
        self.janela = root
        # Título da janela
        self.janela.title("App Gestor de Produtos")
        # Ativar a redimensionamento da janela. Para desativá - la: (0, 0)
        self.janela.resizable(1, 1)
        # Insere o caminho correto do ícone segundo o direório base e altera o ícone da janela
        # Usando um ícone PNG para que o programa seja multiplataforma, assim como o PATH
        # A depender onde o programa é executado, Windows, Linux, MAC, BSD, etc,
        # O PATH foi atribuído automático graças a biblioteca OS e o método path.abspath
        self.janela.iconphoto(False, PhotoImage(file=self.diretorio_base + '/recursos/icon.png'))
        # Criação do recipiente Frame principal
        frame = LabelFrame(self.janela, text="Registar um novo Produto", bg="#282a33", font="TkHeadingFont", fg="white")
        frame.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="")
        # Label Nome
        # Etiqueta de texto localizadano frame
        self.etiqueta_nome = Label(frame, text="Nome: ", bg="#282a33", font="TkMenuFont", fg="white")
        # Posicionamento através de grid
        self.etiqueta_nome.grid(row=1, column=0)
        # Entry Nome (caixa de texto que irá receber o nome)
        # Caixa de texto (input de texto) localizada no frame
        self.nome = Entry(frame, font="TkMenuFont")
        # Para que o foco do rato vá a esta Entry no início
        self.nome.focus()
        self.nome.grid(row=1, column=1)
        # Label Preço
        # Etiqueta de texto localizada no frame
        self.etiqueta_preço = Label(frame, text="Preço: ", bg="#282a33", font="TkMenuFont", fg="white")
        self.etiqueta_preço.grid(row=2, column=0)
        # Entry Preço (caixa de texto que irá receber o preço)
        # Caixa de texto (input de texto) localizada no frame
        self.preco = Entry(frame, font="TkMenuFont")
        self.preco.grid(row=2, column=1)
        # Botão Adicionar Produto
        self.botao_adicionar = ttk.Button(frame, text="Guardar Produto")
        self.botao_adicionar.grid(row=3, columnspan=2, sticky=W + E)
        # Tabela de Produtos
        # Estilo personalizado para a tabela
        style = ttk.Style()
        # Modifica-se a fonte da tabela
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('TkMenuFont', 11), background=cor_fundo,
                        foreground='white')
        # Modifica-se a fonte das cabeceiras
        style.configure("mystyle.Treeview.Heading", font=('TkMenuFont', 13, 'bold'), background=cor_fundo,
                        foreground='grey', relief="flat")
        # Eliminar as bordas
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
        # Estrutura da tabela
        self.tabela = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabela.grid(row=4, column=0, columnspan=2)
        # Cabeçalho 0
        self.tabela.heading('#0', text='Nome', anchor=CENTER)
        # Cabeçalho 1
        self.tabela.heading('#1', text='Preço', anchor=CENTER)
        # Criar tabela
        # Query para checar a existência da tabela produto
        verificar_tabela = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='produto'"
        # Testa se a tabela já existe para não tentar criar novamente, do contrário cria-se,
        if self.db_consulta(verificar_tabela).fetchone()[0] == 0:
            # Query para criar a tabela
            # criar_tabela_produto = 'CREATE table produto (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, preço REAL NOT NULL'
            criar_tabela_produto = 'CREATE TABLE "produto" ("id"	INTEGER NOT NULL,"nome"	TEXT NOT NULL,"preço"	REAL NOT NULL,PRIMARY KEY("id" AUTOINCREMENT))'
            self.db_consulta(criar_tabela_produto)
            # Popular a tabela com os dados do ficheiro CSV
            self.populate_produtos()

        # Chamada ao método get_produtos() para obter a listagem de produtos ao início da app
        self.get_produtos()

    def populate_produtos(self):
        with open(self.diretorio_base + "/database/produtos.csv", "r") as produtos:
            reader = csv.reader(produtos, delimiter=",")
            for index, row in enumerate(reader):
                # Query para inserir na tabela cada produto dentro do loop que percorre todos
                inserir_produto = "INSERT INTO produto VALUES (?,?,?)"
                parametros = [index + 1, row[0], float(row[1])]
                self.db_consulta(inserir_produto, parametros)
                print(row)
            produtos.close()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:  # Iniciamos uma conexão com a base de dados (alias con)
            cursor = con.cursor()  # Criamos um cursor da conexão para poder operar na base de dados
            resultado = cursor.execute(consulta, parametros)  # Preparar a consulta SQL (com parâmetros se os há)
            con.commit()  # Executar a consulta SQL preparada anteriormente
        return resultado  # Restituir o resultado da consulta SQL

    def get_produtos(self):
        query = 'SELECT * FROM produto ORDER BY nome DESC'
        # Faz-se a chamada ao método db_consultas
        registos = self.db_consulta(query)
        # Mostram-se os resultados


if __name__ == '__main__':
    # Instância da janela principal
    root = Tk()
    # Abrir a aplicação o mais próximo do centro possível
    root.eval("tk::PlaceWindow . center")
    # Define uma cor de fundo e tamanho inicial da janela
    root.configure(bg=cor_fundo)
    # Começamos o ciclo de aplicação, é como um while True
    # Envia-se para a classe Produto o controlo sobre a janela root
    app = Produto(root)
    root.mainloop()
