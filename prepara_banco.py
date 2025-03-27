import json
import mysql.connector
from werkzeug.security import generate_password_hash

# Carregar a configuração do arquivo JSON
def carregar_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

# Configuração do banco de dados
config = carregar_config()

# Conectar ao MySQL
def conectar_mysql():
    return mysql.connector.connect(
        host=config['host'],
        user=config['usuario'],
        password=config['senha']
    )

# Criar o banco de dados
def criar_banco():
    try:
        conn = conectar_mysql()
        cursor = conn.cursor()

        # Criar o banco de dados se não existir
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['db_name']}")
        print(f"Banco de dados '{config['db_name']}' criado ou já existente.")
        
        # Selecionar o banco de dados
        cursor.execute(f"USE {config['db_name']}")
        
        # Criar a tabela users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                nome VARCHAR(50) PRIMARY KEY,
                senha VARCHAR(255) NOT NULL
            )
        """)
        print("Tabela 'users' criada ou já existente.")
        
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao criar banco ou tabela: {err}")
    finally:
        cursor.close()
        conn.close()

# Adicionar usuários com senha hash
def adicionar_usuarios():
    usuarios = [
        {"nome": "Gabriel", "senha": "aaa"},
        {"nome": "user2", "senha": "senha456"},
        {"nome": "user3", "senha": "senha789"}
    ]
    
    # Conectar ao MySQL
    conn = conectar_mysql()
    cursor = conn.cursor()

    try:
        # Selecionar o banco de dados
        cursor.execute(f"USE {config['db_name']}")

        for usuario in usuarios:
            senha_hash = generate_password_hash(usuario["senha"])
            
            # Inserir usuário, se não existir
            cursor.execute("SELECT * FROM users WHERE nome = %s", (usuario["nome"],))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO users (nome, senha) VALUES (%s, %s)", 
                               (usuario["nome"], senha_hash))
                print(f"Usuário '{usuario['nome']}' adicionado com sucesso!")
            else:
                print(f"Usuário '{usuario['nome']}' já existe.")

        # Commit das alterações
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao adicionar usuários: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Criar o banco de dados e a tabela
    criar_banco()

    # Adicionar os usuários
    adicionar_usuarios()
