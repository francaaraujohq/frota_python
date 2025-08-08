# Importando SQLite3
import sqlite3

# Criando conexão
try:
    con = sqlite3.connect('frota.db')
    print('Conexão Efetuada.')
except sqlite3.Error as e:
    print('Erro na conexão', e)

# Criando tabela de Login
try:
    with con:
        cur = con.cursor()
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS Usuario(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
                )
            """
        )
        print('Tabela Usuario Criada.')

except sqlite3.Error as e:
    print('Erro ao criar tabela Usuario', e)

# Criando tabela de Veículos
try:
    with con:
        cur = con.cursor()
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS Veiculo(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                placa TEXT UNIQUE NOT NULL,
                modelo TEXT NOT NULL,
                ano INTEGER NOT NULL,
                id_usuario INTEGER NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES Usuario(id) 
                ON UPDATE CASCADE ON DELETE CASCADE
                )
            """
        )
        print('Tabela Veiculo Criada.')

except sqlite3.Error as e:
    print('Erro ao criar tabela Veiculo', e)

# Fechando conexão
con.close()
