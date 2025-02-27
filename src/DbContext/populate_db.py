import sqlite3
from database import DB_NAME, create_tables
from models import (
    insert_discipline, insert_teacher, insert_availability, insert_class, insert_teacher_limit, insert_time_slot, get_teachers, 
    clear_teachers, clear_classes, clear_time_slots, clear_availability, reset_ids
)

classes = [f"CC{i}" for i in range(1, 9)] + [f"ADS{i}" for i in range(1, 5)]
days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

time_slots = [
    "19:10 - 20:25",  # 1ª aula
    "20:25 - 20:45",  # Intervalo
    "20:45 - 22:00"   # 2ª aula
]

teachers = {
    "Lidiana": ["Segunda", "Terça", "Sexta"],
    "Diogo": ["Segunda"],
    "Flávio": ["Terça", "Quarta"],
    "André": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
    "Jucilene": ["Quarta"],
    "Joao Otávio": ["Segunda", "Terça", "Quarta", "Quinta"],
    "Allan": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],  # Apenas 3 dias
    "Valter": ["Terça", "Quarta"],
    "Fábio": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
    "Cícero": ["Segunda", "Terça", "Quarta"],
    "Elio": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],  # Apenas 1 dia
    "Evandro": ["Quinta"],
    "Taisa": ["Segunda", "Quarta", "Quinta"],
    "Rogerio": ["Segunda", "Terça", "Quarta", "Quinta"],
    "Franco": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
    "Joao Marcelo": ["Segunda", "Terça", "Sexta"],
    "Janayna": ["Segunda"]
}

disciplines = [
    ("CC1", "AR", "Arquitetura de Redes", 1.5, "T", 5),
    ("CC1", "CG", "Comp. Gráfica", 1.5, "T", 5),
    ("CC1", "AC", "Arquitetura de Computadores", 1.5, "T", 5),
    ("CC1", "LFA", "Ling. Formais e Autom.", 1.5, "T", 5),
    ("CC1", "IA", "Inteligência Artificial", 3, "T", 5),
    ("CC1", "SO", "Sistemas Operacionais", 3, "T/P", 5),
    ("CC1", "LPOO", "Ling. Programação OO", 4.5, "1T/2P", 3),
    ("CC1", "BD", "Banco de Dados", 4.5, "2T/1P", 3),
    ("ADS1", "POO", "Programa O.O.", 3, "T/P", 3),
    ("ADS1", "ESII", "Engenharia de Software II", 3, "T/P", 3),
    ("ADS1", "BD", "Banco de Dados", 3, "T/P", 3),
    ("ADS1", "ASOO", "Analise Sistemas O.O.", 3, "T/P", 3),
    ("ADS1", "IU", "Interface com Usuário", 3, "T/P", 3),
    ("ADS1", "PLP", "Pensamento Lógico Comp. Python", 3, "T/P", 1),
    ("ADS1", "IC", "Infraestrutura Computacional", 3, "T", 1),
    ("ADS1", "TIC", "Tec da Informação e Comunicação", 3, "T", 1),
    ("ADS1", "MAT", "Matemática e Estatística", 3, "T", 1),
]

def populate_disciplines():
    print("Criando tabelas no banco de dados...")
    create_tables()
    
    print("Populando banco de dados com disciplinas...")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for course, sigla, name, hours, type_, class_number in disciplines:
        insert_discipline(course, sigla, name, hours, type_, class_number)
    
    conn.commit()
    conn.close()
    print("Disciplinas inseridas com sucesso!")

populate_disciplines()

teacher_limits = {"Allan": 3, "Elio": 1}

def populate_database():
    print("Criando tabelas no banco de dados...")
    create_tables()

    print("Limpando banco de dados...")
    clear_availability()
    clear_teachers()
    clear_classes()
    clear_time_slots()
    reset_ids()

    print("Populando banco de dados...")

    for class_name in classes:
        insert_class(class_name)

    for slot in time_slots:
        insert_time_slot(slot)

    for teacher, available_days in teachers.items():
        teacher_id = insert_teacher(teacher, teacher_limits.get(teacher, None))
        
        insert_availability(teacher_id, available_days)
        
        limit = teacher_limits.get(teacher, None)
        if limit is not None:
            insert_teacher_limit(teacher_id, limit)

    print("Banco de dados populado com sucesso!")
populate_database()
