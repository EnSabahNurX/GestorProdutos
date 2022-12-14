import csv
import os
from tkinter import *
from tkinter import ttk

import sqlalchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# Terceira versão do app, que herda tudo da versão beta, com adição de mais uma categoria na tabela de produtos

# Cor de fundo padrão para o app
cor_fundo = "#282a33"
# Armazenar a informação do PATH do projeto de acordo com o sistema utilizado
# independente se for MAC, Windows, Linux, BSD, etc
diretorio_base = os.path.abspath(os.path.dirname(__file__))
# Caminho para base de dados
db = diretorio_base + '/database/produtos.db'

# Criar ligações para conectar a base dados posteriormente
engine = sqlalchemy.create_engine('sqlite:///' + db)
Base = declarative_base()


# Modelar a tabela com uma classe específica
class Produtos(Base):
    __tablename__ = 'produtos'
    id = Column(Integer(), primary_key=True, nullable=False)
    nome = Column(String(), nullable=False)
    preço = Column(Float(), nullable=False)
    categoria = Column(String(), nullable=False)


# Criar tabela no banco de dados
Base.metadata.create_all(engine, checkfirst=True)

# Sessão para acessar o banco de dados e enviar comandos
Session = sessionmaker(bind=engine)
session = Session()

# Popular a tabela com uma carga inicial, em caso de estar vazia, com dados contidos num arquivo CSV
if not session.query(Produtos).first():
    with open(diretorio_base + "/database/produtos.csv", "r") as produtos:
        reader = csv.reader(produtos, delimiter=",")
        for row in reader:
            # Query para inserir na tabela cada produto dentro do loop que percorre todos
            session.add(Produtos(nome=row[0], preço=float(row[1]), categoria=row[2]))
            session.commit()
        produtos.close()


# Classe para controlar a janela root
class Produto:
    def __init__(self, window):
        self.janela = window
        # Título da janela
        self.janela.title("App Gestor de Produtos")
        # Ativar a redimensionamento da janela. Para desativá - la: (0, 0)
        self.janela.resizable(1, 1)
        # Insere o caminho correto do ícone segundo o direório base e altera o ícone da janela
        # Usando um ícone PNG para que o programa seja multiplataforma, assim como o PATH
        # A depender onde o programa é executado, Windows, Linux, MAC, BSD, etc,
        # O PATH foi atribuído automático graças a biblioteca OS e o método path.abspath
        self.janela.iconphoto(False, PhotoImage(file=diretorio_base + '/recursos/icon.png'))

        # Criação do recipiente Frame principal
        frame = LabelFrame(self.janela, text="Registar um novo Produto", bg="#282a33", fg="white",
                           font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="")
        # Label Nome
        # Etiqueta de texto localizada no frame
        self.etiqueta_nome = Label(frame, text="Nome: *", bg="#282a33", fg="white", font=('Calibri', 13))
        # Posicionamento através de grid
        self.etiqueta_nome.grid(row=1, column=0)
        # Entry Nome (caixa de texto que irá receber o nome)
        # Caixa de texto (input de texto) localizada no frame
        self.nome = Entry(frame, font=('Calibri', 13))
        # Para que o foco do rato vá a esta Entry no início
        self.nome.focus()
        self.nome.grid(row=1, column=1, sticky=NSEW, columnspan=2)
        # Label Preço
        # Etiqueta de texto localizada no frame
        self.etiqueta_preco = Label(frame, text="Preço: *", bg="#282a33", fg="white", font=('Calibri', 13))
        self.etiqueta_preco.grid(row=2, column=0)
        # Entry Preço (caixa de texto que irá receber o preço)
        # Caixa de texto (input de texto) localizada no frame
        self.preco = Entry(frame, font=('Calibri', 13))
        self.preco.grid(row=2, column=1, sticky=NSEW, columnspan=2)
        # Label Categoria
        # Etiqueta de texto localizada no frame
        self.etiqueta_categoria = Label(frame, text="Categoria: *", bg="#282a33", fg="white", font=('Calibri', 13))
        # Posicionamento através de grid
        self.etiqueta_categoria.grid(row=3, column=0)
        # Entry Nome (caixa de texto que irá receber o nome)
        # Caixa de texto (input de texto) localizada no frame
        self.categoria = Entry(frame, font=('Calibri', 13))
        self.categoria.grid(row=3, column=1, sticky=NSEW, columnspan=2)

        # Botão Adicionar Produto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_adicionar = ttk.Button(frame, text="GUARDAR", command=self.add_produto, style='my.TButton')
        self.botao_adicionar.grid(row=4, column=0, sticky=NSEW, columnspan=1, padx=10, pady=10)

        # Mensagem informativa para o utilizador
        self.mensagem = Label(text='A espera de inserir novos produtos', fg='red', font='Calibri')
        self.mensagem.grid(row=5, column=0, columnspan=2, sticky=NSEW)

        # Tabela de Produtos
        # Estilo personalizado para a tabela
        style = ttk.Style()
        # Modifica-se a fonte da tabela
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11), background=cor_fundo,
                        foreground='white')
        # Modifica-se a fonte das cabeceiras
        style.configure("mystyle.Treeview.Heading", font=('TkMenuFont', 13, 'bold'), background=cor_fundo,
                        foreground='grey')
        # Eliminar as bordas
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
        # Estrutura da tabela
        colunas = ['id', 'Nome', 'Preço', 'Categoria']
        self.tabela = ttk.Treeview(height=20, columns=colunas, style="mystyle.Treeview", show='headings')
        self.tabela.grid(row=6, column=0)

        for col in colunas:
            self.tabela.heading(col, text=col.title(), anchor=CENTER)
            if col == 'id':
                self.tabela.column(col, width=0, anchor='center')
            else:
                self.tabela.column(col, anchor='center')

        # Definir quais colunas serão visíveis na tabela ou não
        colunas_nao_visiveis = ['id']
        colunas_visiveis = []
        for col in self.tabela['columns']:
            if not f'{col}' in colunas_nao_visiveis:
                colunas_visiveis.append(col)
        self.tabela['displaycolumns'] = colunas_visiveis

        # Botões de Eliminar e Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botão_eliminar = ttk.Button(frame, text='ELIMINAR', command=self.del_produto, style='my.TButton')
        self.botão_eliminar.grid(row=4, column=2, sticky=NSEW, columnspan=1, padx=10, pady=10)
        self.botão_editar = ttk.Button(frame, text='EDITAR', command=self.edit_produto, style='my.TButton')
        self.botão_editar.grid(row=4, column=1, sticky=W + E, columnspan=1, padx=10, pady=10)

        # Chamada ao método get_produtos() para obter a listagem de produtos ao início da app
        self.get_produtos()
        # Flag para identificar se está em processo de edição do registo na tabela
        # e não permitir que seja interrompida a edição por outro comando
        self.editando = False

    def get_produtos(self):
        # O primeiro, ao iniciar a app, vamos limpar a tabela se tiver dados residuais ou antigos
        # Obter todos os dados da tabela
        registos_tabela = self.tabela.get_children()
        for linha in registos_tabela:
            self.tabela.delete(linha)

        # Armazenar todos os produtos da tabela numa variável
        registos_db = session.query(Produtos).order_by(Produtos.nome.desc())

        # Escrever os dados no ecrã a percorrer todas as linhas da tabela
        for linha in registos_db:
            items = [linha.id, linha.nome, linha.preço, linha.categoria]
            self.tabela.insert("", 0, values=items)

    def validacao_nome(self):
        nome_introduzido_por_utilizador = self.nome.get()
        return len(nome_introduzido_por_utilizador) != 0

    def validacao_preco(self):
        preco_introduzido_por_utilizador = self.preco.get()
        return len(preco_introduzido_por_utilizador) != 0

    def validacao_categoria(self):
        categoria_introduzida_por_utilizador = self.categoria.get()
        return len(categoria_introduzida_por_utilizador) != 0

    def add_produto(self):
        if self.editando:
            self.mensagem['text'] = 'Em processo de edição de produto, primeiro conclua a edição antes de prosseguir.'
            return
        if self.validacao_nome() and self.validacao_preco() and self.validacao_categoria():
            # Parâmetros da query
            parametros = (self.nome.get(), float(self.preco.get().replace(",", ".")), self.categoria.get())
            session.add(Produtos(nome=parametros[0], preço=parametros[1], categoria=parametros[2]))
            session.commit()
            # Label localizada entre o botão e a tabela
            self.mensagem['text'] = f'Produto {self.nome.get()} adicionado com êxito'

            # Limpa os campos de nome,preço e categoria após serem adicionados com sucesso à tabela
            self.nome.delete(0, END)
            self.preco.delete(0, END)
            self.categoria.delete(0, END)

        else:
            self.mensagem['text'] = 'Há campos que são obrigatórios sem preencher.'

        # Quando se finalizar a inserção de dados voltamos a invocar este
        # método para atualizar o conteúdo e ver as alterações
        self.get_produtos()

    def del_produto(self):
        if self.editando:
            self.mensagem['text'] = 'Em processo de edição de produto, primeiro conclua a edição antes de prosseguir.'
            return
        # Debug
        # print(self.tabela.item(self.tabela.selection()))
        # print(self.tabela.item(self.tabela.selection())['text'])
        # print(self.tabela.item(self.tabela.selection())['values'])
        # print(self.tabela.item(self.tabela.selection())['values'][0])

        # Mensagem inicialmente vazio
        self.mensagem['text'] = ''
        # Comprovação de que se selecione um produto para poder eliminá-lo
        try:
            self.tabela.item(self.tabela.selection())['values'][0]

        except IndexError:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return
        self.mensagem['text'] = ''

        # Armazena o nome do produto que se deseja eliminar
        valor_id = self.tabela.item(self.tabela.selection())['values'][0]
        nome = self.tabela.item(self.tabela.selection())['values'][1]

        # Filtra pela linha selecionada e elimina da tabela e do banco de dados segundo o ID
        delete_produto = session.query(Produtos).filter_by(id=valor_id).first()
        session.delete(delete_produto)
        session.commit()
        # Exibir mensagem ao utilizador
        self.mensagem['text'] = f'Produto {nome} eliminado com êxito'
        # Atualizar a tabela de produtos
        self.get_produtos()

    def edit_produto(self):

        # Mensagem inicialmente vazia
        self.mensagem['text'] = ''
        try:
            self.tabela.item(self.tabela.selection())['values'][0]
        except IndexError:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return
        self.mensagem['text'] = 'A editar o produto selecionado.'

        valor_id = self.tabela.item(self.tabela.selection())['values'][0]
        nome = self.tabela.item(self.tabela.selection())['values'][1]
        preço = self.tabela.item(self.tabela.selection())['values'][2]
        categoria = self.tabela.item(self.tabela.selection())['values'][3]

        parametros = [valor_id, nome, preço, categoria]
        if not self.editando:
            # Limpa os campos de nome, preço e categoria antes de serem editados
            self.nome.delete(0, END)
            self.preco.delete(0, END)
            self.categoria.delete(0, END)

            # Preencher todos os campos ao qual registo irá ser editado
            self.nome.insert(0, parametros[1])
            self.preco.insert(0, parametros[2])
            self.categoria.insert(0, parametros[3])

            self.botão_editar['text'] = 'CONFIRMAR'
            self.editando = True
        else:
            self.atualizar_produtos(valor_id)

    def atualizar_produtos(self, id):
        nome = self.nome.get()
        preço = self.preco.get()
        categoria = self.categoria.get()

        parametros = [nome, preço, categoria]

        if '' in parametros:
            self.mensagem['text'] = 'Há campos que são obrigatórios sem preencher.'
        else:
            update_produto = session.query(Produtos).where(Produtos.id == id).first()
            update_produto.nome = nome
            update_produto.preço = float(preço.replace(',', '.'))
            update_produto.categoria = categoria
            session.commit()

            self.nome.delete(0, END)
            self.preco.delete(0, END)
            self.categoria.delete(0, END)

            for widget in self.tabela.winfo_children():
                widget.destroy()
            self.get_produtos()
            self.mensagem['text'] = f'Produto {self.nome.get()} atualizado com êxito'

        self.botão_editar['text'] = 'EDITAR'
        self.editando = False


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
