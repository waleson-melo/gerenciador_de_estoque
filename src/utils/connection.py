import sqlite3
import os


class Connection:

    def __init__(self):
        self.create_tables()
        self.default_data()

    def connect_db(self):
        if not os.path.isdir('.gerenciador_de_estoque/database'):
            os.makedirs('.gerenciador_de_estoque/database')

        self.conn = sqlite3.connect(
            '.gerenciador_de_estoque/database/dbsistema.db')

        self.cursor = self.conn.cursor()

    def desconect_db(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):
        self.connect_db()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS "usuarios" (
                "pk_id_usuario"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                "cpf_usua"	TEXT(11) NOT NULL UNIQUE,
                "nome_usua"	TEXT(50) NOT NULL,
                "telefone_usua"	TEXT(11),
                "endereco_usua"	TEXT(70),
                "senha_usua"	TEXT(11) NOT NULL,
                "observacao_usua"	TEXT(100)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS "categorias" (
                "pk_id_categoria"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                "nome_cate"	TEXT(30) NOT NULL UNIQUE
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS "produtos" (
                "pk_id_produto"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                "codigo_barra_prod"	TEXT,
                "nome_prod" TEXT(30) NOT NULL,
                "preco_prod" REAL NOT NULL,
                "quantidade_prod" INTEGER NOT NULL,
                "descricao_prod" TEXT(30),
                "fk_categoria" INTEGER NOT NULL,
                FOREIGN KEY ("fk_categoria")
                REFERENCES "categorias"("pk_id_categoria")
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS "compras" (
                "pk_id_compra"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                "valor_total_comp"	REAL NOT NULL,
                "data_comp"	TEXT NOT NULL 
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS "compra_produto" (
                "pk_id_compra_produto"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                "fk_compra"	INTEGER NOT NULL,
                "fk_produto" INTEGER NOT NULL,
                "quantidade_produto" INTEGER NOT NULL
            );
        """)

        self.desconect_db()

    def default_data(self):
        self.connect_db()

        # se a quantidade for 0 é adcionado um usuario padrao
        quant_usuarios = self.cursor.execute("""
                    SELECT count(1) FROM usuarios
                """).fetchall()

        quant_usuarios = list(quant_usuarios)[0]

        if quant_usuarios[0] == 0:
            self.cursor.execute("""
                INSERT INTO usuarios (cpf_usua, nome_usua, senha_usua) 
                VALUES ('00000000000', 'admin', 'admin')
            """)

        self.desconect_db()
