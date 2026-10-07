from flask import Flask
from flask import request
from flask import render_template
from datetime import date
import sqlite3
from sqlite3 import Error

#######################################################
# Instância da Aplicação Flask

app = Flask(__name__)

#######################################################
# 1. Cadastrar produtos

@app.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastrar():

    mensagem = ''

    if request.method == 'POST':
        descricao = request.form['descricao']
        precocompra = request.form['precocompra']
        precovenda = request.form['precovenda']
        datacriacao = date.today()

        mensagem = 'Erro - não cadastrado'

        if descricao and precocompra and precovenda:
            registro = (
                descricao,
                precocompra,
                precovenda,
                datacriacao
            )

            conn = None

            try:
                conn = sqlite3.connect('db-produtos.db')

                sql = '''
                    INSERT INTO produtos
                    (descricao, precocompra, precovenda, datacriacao)
                    VALUES (?, ?, ?, ?)
                '''

                cur = conn.cursor()
                cur.execute(sql, registro)
                conn.commit()

                mensagem = 'Sucesso - cadastrado'

            except Error as e:
                print(e)

            finally:
                if conn:
                    conn.close()

    return render_template(
        'cadastrar.html',
        mensagem=mensagem
    )


#######################################################
# 2. Listar produtos

@app.route('/produtos/listar', methods=['GET'])
def listar():

    conn = None

    try:
        conn = sqlite3.connect('db-produtos.db')

        sql = '''
            SELECT * FROM produtos
        '''

        cur = conn.cursor()
        cur.execute(sql)

        registros = cur.fetchall()

        return render_template(
            'listar.html',
            regs=registros
        )

    except Error as e:
        print(e)
        return 'Erro ao consultar produtos'

    finally:
        if conn:
            conn.close()


#######################################################
# Rota de Erro

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404


#######################################################
# Execução da Aplicação

if __name__ == '__main__':
    app.run(debug=True)