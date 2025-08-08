from werkzeug.security import generate_password_hash
from app import db, Usuario  # Importe seu modelo de usuário

hashed_password = generate_password_hash("1234")  # Criptografa a senha
novo_usuario = Usuario(username="admin", password=hashed_password)

db.session.add(novo_usuario)
db.session.commit()

print("Usuário criado com sucesso!")
