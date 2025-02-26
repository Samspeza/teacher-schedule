import os

from database import DB_NAME, create_tables

# Deletando o banco de dados para recriar as tabelas
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

# Agora, recrie as tabelas chamando a função
create_tables()
