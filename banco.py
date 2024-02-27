import sqlite3
#test

class Banco():

    def __init__(self):
        self.conexao = sqlite3.connect('rifas.db')
        self.createTables()
        

    def createTables(self):
        c = self.conexao.cursor()
        #tabela clientes
        c.execute('''CREATE TABLE
        IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,               
            sexo TEXT,
            cpf TEXT UNIQUE
        )''')
        self.conexao.commit()
        c.close()

        c = self.conexao.cursor()
        #tabela contatos
        c.execute('''CREATE TABLE
        IF NOT EXISTS contato (
            idcliente INTEGER,            
            telefone TEXT,
            telefone2 TEXT,
            FOREIGN KEY(idcliente) references clientes(id)
                  
        )''')
        self.conexao.commit()
        c.close()

        c = self.conexao.cursor()
        #tabela endereco
        c.execute('''CREATE TABLE
        IF NOT EXISTS endereco (
            idcliente INTEGER,
            rua TEXT NOT NULL,
            numero INTEGER NOT NULL,
            bairro TEXT,
            cidade TEXT,
            CEP TEXT,
            FOREIGN KEY(idcliente) references clientes(id)
        )''')
        self.conexao.commit()
        c.close()

        c = self.conexao.cursor()
        #tabela nome
        c.execute('''CREATE TABLE
        IF NOT EXISTS nome (
            idrifa INTEGER,
            nome TEXT NOT NULL,
            idcliente INTEGER NOT NULL,
            valor DOUBLE NOT NULL,
            pago TEXT NOT NULL,
            FOREIGN KEY(idrifa) references rifa(id),
            FOREIGN KEY(idcliente) references clientes(id)
        )''')
        self.conexao.commit()
        c.close()        
        
        c = self.conexao.cursor()
        #tabela rifa
        c.execute('''CREATE TABLE
        IF NOT EXISTS rifa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            premio INTEGER NOT NULL,
            status TEXT,
            valortotal DOUBLE,
            FOREIGN KEY(premio) references produto(codigo)
        )''')
        self.conexao.commit()
        c.close()
        
        c = self.conexao.cursor()
        #tabela produto
        c.execute('''CREATE TABLE
        IF NOT EXISTS produto (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            custo NUMERIC(7,2) NOT NULL,
            tipo TEXT
        )''')
        self.conexao.commit()
        c.close()
        
        c = self.conexao.cursor()
        #tabela estoque
        c.execute('''CREATE TABLE
        IF NOT EXISTS estoque (
            produto INTEGER NOT NULL,
            quatidade INTEGER NOT NULL,
            FOREIGN KEY(produto) references produto(codigo)                 
        )''')
        self.conexao.commit()
        c.close()

        c = self.conexao.cursor()
        #tabela sorteio
        c.execute('''CREATE TABLE
        IF NOT EXISTS sorteio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idrifa INTEGER NOT NULL,
            ganhador TEXT,
            data DATE,
            status TEXT NOT NULL,
            FOREIGN KEY(idrifa) references rifa(id)

        )''')
        self.conexao.commit()
        c.close()                              