import json
import jwt
import psycopg2
import os

# Configurar variáveis de ambiente no Lambda
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")

def lambda_handler(event, context):
    try:
        # Ler o corpo da requisição
        body = json.loads(event.get('body', '{}'))
        cpf = body.get("cpf")

        if not cpf:
            return {"statusCode": 400, "body": json.dumps({"error": "CPF obrigatório"})}

        # Conectar ao PostgreSQL
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cur = conn.cursor()

        # Buscar o usuário pelo CPF
        cur.execute("SELECT id FROM clientes WHERE cpf = %s", (cpf,))
        user = cur.fetchone()

        # Fechar conexão
        cur.close()
        conn.close()

        if user:
            # Gerar JWT
            token = jwt.encode({"cpf": cpf}, SECRET_KEY, algorithm="HS256")
            return {"statusCode": 200, "body": json.dumps({"token": token})}
        else:
            return {"statusCode": 401, "body": json.dumps({"error": "CPF não encontrado"})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
