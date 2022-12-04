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
        self.etiqueta_preco = Label(frame, text="Preço: ", bg="#282a33", font="TkMenuFont", fg="white")
        self.etiqueta_preco.grid(row=2, column=0)
        # Entry Preço (caixa de texto que irá receber o preço)
        # Caixa de texto (input de texto) localizada no frame
        self.preco = Entry(frame, font="TkMenuFont")
        self.preco.grid(row=2, column=1)
        # Botão Adicionar Produto
        self.botao_adicionar = ttk.Button(frame, text="Guardar Produto", command=self.add_produto)
        self.botao_adicionar.grid(row=3, columnspan=2, sticky=W + E)

        # Mensagem informativa para o utilizador
        self.mensagem = Label(text='A espera de inserir novos produtos', fg='red')
        self.mensagem.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Tabela de Produtos
        # Estilo personalizado para a tabela
        style = ttk.Style()
        # Modifica-se a fonte da tabela
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('TkMenuFont', 11), background=cor_fundo,
                        foreground='white')
        # Modifica-se a fonte das cabeceiras
        style.configure("mystyle.Treeview.Heading", font=('TkMenuFont', 13, 'bold'), background=cor_fundo,
                        foreground='grey')
        # Eliminar as bordas
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
        # Estrutura da tabela
        self.tabela = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabela.grid(row=4, column=0, columnspan=2)
        # Cabeçalho 0
        self.tabela.heading('#0', text='Nome', anchor=CENTER)
        # Cabeçalho 1
        self.tabela.heading('#1', text='Preço', anchor=CENTER)

        # Botões de Eliminar e Editar
        botão_eliminar = ttk.Button(text='ELIMINAR', command=self.del_produto)
        botão_eliminar.grid(row=5, column=0, sticky=W + E)
        botão_editar = ttk.Button(text='EDITAR', command=self.edit_produto)
        botão_editar.grid(row=5, column=1, sticky=W + E)

        # Criar tabela
        # Query para checar a existência da tabela produto
        verificar_tabela = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='produto'"
        # Testa se a tabela já existe para não tentar criar novamente, caso não exista é criada,
        if self.db_consulta(verificar_tabela).fetchone()[0] == 0:
            # Query para criar a tabela
            criar_tabela_produto = 'CREATE TABLE "produto" ("id"	INTEGER NOT NULL,"nome"	TEXT NOT NULL,"preço"	REAL NOT NULL,PRIMARY KEY("id" AUTOINCREMENT))'
            self.db_consulta(criar_tabela_produto)
            # Popular a tabela com os dados do ficheiro CSV
            self.popular_tabela()

        # Chamada ao método get_produtos() para obter a listagem de produtos ao início da app
        self.get_produtos()

    def popular_tabela(self):
        with open(self.diretorio_base + "/database/produtos.csv", "r") as produtos:
            reader = csv.reader(produtos, delimiter=",")
            for index, row in enumerate(reader):
                # Query para inserir na tabela cada produto dentro do loop que percorre todos
                inserir_produto = "INSERT INTO produto VALUES (?,?,?)"
                parametros = [index + 1, row[0], float(row[1])]
                self.db_consulta(inserir_produto, parametros)
            produtos.close()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:  # Iniciamos uma conexão com a base de dados (alias con)
            cursor = con.cursor()  # Criamos um cursor da conexão para poder operar na base de dados
            resultado = cursor.execute(consulta, parametros)  # Preparar a consulta SQL (com parâmetros se os há)
            con.commit()  # Executar a consulta SQL preparada anteriormente
        return resultado  # Restituir o resultado da consulta SQL

    def get_produtos(self):
        # O primeiro, ao iniciar a app, vamos limpar a tabela se tiver dados residuais ou antigos
        # Obter todos os dados da tabela
        registos_tabela = self.tabela.get_children()
        for linha in registos_tabela:
            self.tabela.delete(linha)

        # Consulta SQL
        query = 'SELECT * FROM produto ORDER BY nome DESC'
        # Faz-se a chamada ao método db_consultas
        registos_db = self.db_consulta(query)

        # Escrever os dados no ecrã
        for linha in registos_db:
            # print para verificar por consola os dados
            # print(linha)
            self.tabela.insert('', 0, text=linha[1], values=linha[2])

    def validacao_nome(self):
        nome_introduzido_por_utilizador = self.nome.get()
        return len(nome_introduzido_por_utilizador) != 0

    def validacao_preco(self):
        preco_introduzido_por_utilizador = self.preco.get()
        return len(preco_introduzido_por_utilizador) != 0

    def add_produto(self):
        if self.validacao_nome() and self.validacao_preco():
            # Consulta SQL (sem os dados)
            query = 'INSERT INTO produto VALUES(NULL, ?, ?)'
            # Parâmetros da consulta SQL
            parametros = (self.nome.get(), float(self.preco.get().replace(",", ".")))
            self.db_consulta(query, parametros)

            # Label localizada entre o botão e a tabela
            self.mensagem['text'] = f'Produto {self.nome.get()} adicionado com êxito'

            # Para debug
            # print(self.nome.get())
            # print(self.preco.get())

            # Limpa os campos de nome e preço após serem adicionados com sucesso à tabela
            self.nome.delete(0, END)
            self.preco.delete(0, END)
        elif self.validacao_nome() and self.validacao_preco() == False:
            self.mensagem['text'] = 'O preço é obrigatório'
        elif self.validacao_nome() == False and self.validacao_preco():
            self.mensagem['text'] = 'O nome é obrigatório'
        else:
            self.mensagem['text'] = 'O nome e o preço são obrigatórios'

        # Quando se finalizar a inserção de dados voltamos a invocar este método para atualizar o conteúdo e ver as alterações
        self.get_produtos()

    def del_produto(self):
        # Debug
        print(self.tabela.item(self.tabela.selection()))
        # print(self.tabela.item(self.tabela.selection())['text'])
        # print(self.tabela.item(self.tabela.selection())['values'])
        # print(self.tabela.item(self.tabela.selection())['values'][0])

        # Mensagem inicialmente vazio
        self.mensagem['text'] = ''
        # Comprovação de que se selecione um produto para poder eliminá-lo
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return
        self.mensagem['text'] = ''
        # Armazena o nome do produto que se deseja eliminar
        nome = self.tabela.item(self.tabela.selection())['text']
        # Consulta SQL
        query = 'DELETE FROM produto WHERE nome = ?'
        # Executar a consulta
        self.db_consulta(query, (nome,))
        self.mensagem['text'] = 'Produto {} eliminado com êxito'.format(nome)
        # Atualizar a tabela de produtos
        self.get_produtos()

    def edit_produto(self):
        # Mensagem inicialmente vazia
        self.mensagem['text'] = ''
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return
        nome = self.tabela.item(self.tabela.selection())['text']
        # O preço encontra-se dentro de uma lista
        old_preco = self.tabela.item(self.tabela.selection())['values'][0]

        # Criar uma janela à frente da principal
        self.janela_editar = Toplevel()
        # Titulo da janela
        self.janela_editar.title = "Editar Produto"
        # Ativar a redimensão da janela. Para desativá-la: (0,0)
        self.janela_editar.resizable(1, 1)
        # Define uma cor de fundo e tamanho inicial da janela
        self.janela_editar.configure(bg=cor_fundo)
        # Ícone da janela
        self.janela_editar.iconphoto(False, PhotoImage(file=self.diretorio_base + '/recursos/icon.png'))

        título = Label(self.janela_editar, text='Edição de Produtos', font=('TkHeadingFont', 30, 'bold'),
                       background=cor_fundo, foreground='white')
        título.grid(column=0, row=0)

        # Criação do recipiente Frame da janela de Editar Produto
        frame_ep = LabelFrame(self.janela_editar, text="Editar o seguinte Produto", background=cor_fundo,
                              foreground='white')  # frame_ep: Frame Editar Produto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nome antigo
        # Etiqueta de texto localizada no frame
        self.etiqueta_nome_antigo = Label(frame_ep, text="Nome antigo: ", background=cor_fundo, foreground='white')
        # Posicionamento através de grid
        self.etiqueta_nome_antigo.grid(row=2, column=0)
        # Entry Nome antigo (texto que não se poderá modificar)
        self.input_nome_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=nome),
                                       state='readonly')
        self.input_nome_antigo.grid(row=2, column=1)

        # Label Nome novo
        self.etiqueta_nome_novo = Label(frame_ep, text="Nome novo: ", background=cor_fundo, foreground='white')
        self.etiqueta_nome_novo.grid(row=3, column=0)
        # Entry Nome novo (texto que se poderá modificar)
        self.input_nome_novo = Entry(frame_ep)
        self.input_nome_novo.grid(row=3, column=1)
        # Para que a seta do rato vá a esta Entry ao início
        self.input_nome_novo.focus()

        # Label Preço antigo
        # Etiqueta de texto localizada no frame
        self.etiqueta_preco_antigo = Label(frame_ep, text="Preço antigo: ", background=cor_fundo, foreground='white')
        # Posicionamento através de grid
        self.etiqueta_preco_antigo.grid(row=4, column=0)
        # Entry Preço antigo (texto que não se poderá modificar)
        self.input_preco_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=old_preco),
                                        state='readonly')
        self.input_preco_antigo.grid(row=4, column=1)

        # Label Preço novo
        self.etiqueta_preco_novo = Label(frame_ep, text="Preço novo: ", background=cor_fundo, foreground='white')
        self.etiqueta_preco_novo.grid(row=5, column=0)
        # Entry Preço novo (texto que se poderá modificar)
        self.input_preco_novo = Entry(frame_ep)
        self.input_preco_novo.grid(row=5, column=1)

        # Botão Atualizar Produto
        self.botao_atualizar = ttk.Button(frame_ep, text="Atualizar Produto",
                                          command=lambda: self.atualizar_produtos(self.input_nome_novo.get(),
                                                                                  self.input_nome_antigo.get(),
                                                                                  self.input_preco_novo.get(),
                                                                                  self.input_preco_antigo.get()))

        self.botao_atualizar.grid(row=6, columnspan=2, sticky=W + E)
        self.etiqueta_preco_novo.grid(row=5, column=0)
        # Entry Preço novo (texto que se poderá modificar)
        self.input_preco_novo = Entry(frame_ep)
        self.input_preco_novo.grid(row=5, column=1)

        # Botão Atualizar Produto
        self.botão_atualizar = ttk.Button(frame_ep, text="Atualizar Produto",
                                          command=lambda: self.atualizar_produtos(self.input_nome_novo.get(),
                                                                                  self.input_nome_antigo.get(),
                                                                                  self.input_preco_novo.get(),
                                                                                  self.input_preco_antigo.get()))

        self.botao_atualizar.grid(row=6, columnspan=2, sticky=W + E)

    def atualizar_produtos(self, novo_nome, antigo_nome, novo_preco, antigo_preco):
        produto_modificado = False
        novo_preco = novo_preco.replace(',', '.')
        query = 'UPDATE produto SET nome = ?, preço = ? WHERE nome = ? AND preço = ?'
        if novo_nome != '' and novo_preco != '':
            # Se o utilizador escreve novo nome e novo preço, mudam-se ambos
            parametros = (novo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome != '' and novo_preco == '':
            # Se o utilizador deixa vazio o novo preço, mantém-se o preço anterior
            parametros = (novo_nome, antigo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome == '' and novo_preco != '':
            # Se o utilizador deixa vazio o novo nome, mantém-se o nome anterior
            parametros = (antigo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        if (produto_modificado):
            # Executar a consulta
            self.db_consulta(query, parametros)
            # Fechar a janela de edição de produtos
            self.janela_editar.destroy()
            # Mostrar mensagem para o utilizador
            self.mensagem['text'] = f'O produto {antigo_nome} foi atualizado com êxito'
            # Atualizar a tabela de produtos
            self.get_produtos()
        else:
            # Fechar a janela de edição de produtos
            self.janela_editar.destroy()
            # Mostrar mensagem para o utilizador
            self.mensagem['text'] = f'O produto {antigo_nome} NÃO foi atualizado'
            self.get_produtos()


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
