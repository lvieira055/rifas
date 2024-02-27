from flask import Flask, render_template, request, redirect, url_for
from banco import Banco
app = Flask(__name__)

#conexao com o banco de dados

banco = Banco()
try:
    banco.createTables(banco)
except:
    print("Banco já existe...")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    banco = Banco()
    conn = banco.conexao.cursor()
    conn.execute('''SELECT clientes.id, clientes.nome, clientes.idade, contato.telefone, endereco.rua, endereco.numero, endereco.cidade FROM clientes
                 left join contato on clientes.id = contato.idcliente
                 left join endereco on clientes.id = endereco.idcliente''')
    clientes = conn.fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/novo_cliente', methods=['GET','POST'])
def novo_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        sexo = request.form['sexo']
        CPF = request.form['cpf']

        banco = Banco()
        conn = banco.conexao.cursor()
        conn.execute("INSERT INTO clientes (nome, idade, sexo, cpf) VALUES(?,?,?,?)",(nome, idade, sexo, CPF))
        banco.conexao.commit()
        banco.conexao.close()
        return redirect(url_for('clientes'))
    return render_template('novo_cliente.html')

@app.route('/removerCliente/<string:idcliente>', methods=['GET', 'POST'])
def removerCliente(idcliente):
    banco = Banco()
    conn = banco.conexao.cursor()
    conn.execute('DELETE FROM clientes where id = '+idcliente)
    banco.conexao.commit()
    conn.close()
    return redirect(url_for('/clientes'))

@app.route('/editar_cliente/<string:idcliente>', methods=['GET', 'POST'])
def editar_cliente(idcliente):
    banco = Banco()
    conn = banco.conexao.cursor()
    conn.execute("select * from clientes where id = "+idcliente)
    
    cliente = conn.fetchall()

    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        sexo = request.form['sexo']
        CPF = request.form['cpf']
        conn = banco.conexao.cursor()
        conn.execute("UPDATE clientes set nome = '"+nome+"', idade = "+idade+", sexo = '"+sexo+"', cpf = '"+CPF+"' where id = '"+idcliente+"'")
        banco.conexao.commit()
        banco.conexao.close()
        return redirect(url_for('clientes'))
    return render_template('editar_cliente.html',cliente=cliente)

@app.route('/produtos')
def produtos():
    banco = Banco()
    conn = banco.conexao.cursor()
    conn.execute('''SELECT produto.codigo, produto.nome, produto.custo, produto.tipo, estoque.quatidade FROM produto
        left join estoque on estoque.produto = produto.codigo''')
    produtos = conn.fetchall()
    conn.close()
    return render_template('produtos.html', produtos=produtos)

@app.route('/novo_produto', methods=['GET','POST'])
def novo_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        custo = request.form['custo']
        tipo = request.form['tipo']
        estoque = request.form['estoque']
    
        banco = Banco()
        conn = banco.conexao.cursor()
        #insere o produto na tabela de produto
        conn.execute("INSERT INTO produto (nome, custo, tipo) VALUES(?,?,?)",(nome, custo, tipo))
        banco.conexao.commit()
        conn = banco.conexao.cursor()
        #pega o id que foi gerado para o produto para dar insert no estoque.
        conn.execute("SELECT max(produto.codigo) FROM produto")
        idproduto=  conn.fetchall()
        #itera sobre o retorno do banco e insere o id produto no estoque junto com sua quantidade de estoque.
        for produto in idproduto:
            print(produto[0])
            conn = banco.conexao.cursor()
            conn.execute("INSERT INTO estoque (produto, quatidade) VALUES(?,?)",(produto[0], estoque))
            banco.conexao.commit()          

        banco.conexao.close()
        return redirect(url_for('produtos'))
    return render_template('novo_produto.html')

@app.route('/removerProduto/<string:idproduto>', methods=['GET', 'POST'])
def removerProduto(idproduto):
    banco = Banco()
    conn = banco.conexao.cursor()
    conn.execute('DELETE FROM produto where codigo = '+idproduto)
    banco.conexao.commit()
    conn = banco.conexao.cursor()
    conn.execute('DELETE FROM estoque where produto = '+idproduto)
    banco.conexao.commit()
    conn.close()
    return redirect(url_for('produtos'))

@app.route('/editar_produto/<string:idproduto>', methods=['GET', 'POST'])
def editar_produto(idproduto):
    banco = Banco()
    conn = banco.conexao.cursor()
    conn.execute('''select produto.codigo, produto.nome, produto.custo, produto.tipo,
                 estoque.quatidade from produto 
                 left join estoque on estoque.produto = produto.codigo
                 where codigo = '''+idproduto)
    
    produto = conn.fetchall()

    if request.method == 'POST':
        nome = request.form['nome']
        custo = request.form['custo']
        tipo = request.form['tipo']
        estoque = request.form['estoque']

        conn = banco.conexao.cursor()
        conn.execute("UPDATE produto set nome = '"+nome+"', custo = "+custo+", tipo = '"+tipo+"' where codigo = '"+idproduto+"'")
        banco.conexao.commit()
        conn = banco.conexao.cursor()
        conn.execute("UPDATE estoque set quatidade ="+estoque+" where produto ="+idproduto)
        banco.conexao.commit()
        banco.conexao.close()
        return redirect(url_for('produtos'))
    return render_template('editar_produto.html',produto=produto)
    

@app.route('/novo_contato/<string:idcliente>/', methods=['GET','POST'])
def novo_contato(idcliente):
    return redirect(url_for('clientes'))


@app.route('/criar_contato/<string:idcliente>', methods=['GET','POST'])
def criar_contato(idcliente):
    contato = request.form['telefone']
    print("teste",contato)
    banco = Banco()
    conn = banco.conexao.cursor()
    conn.execute("INSERT INTO contato (idcliente, telefone) VALUES(?,?)",(idcliente, contato))
    banco.conexao.commit()
    banco.conexao.close()
    return render_template('novo_contato.html', cliente=idcliente)
    



@app.route('/nova_rifa', methods=['GET','POST'])
def nova_rifa():
    pass

if __name__ == '__main__':
    app.run(debug=True)