import sqlite3
from database import DB_NAME, create_tables
from models import (
    insert_teacher, insert_availability, insert_class, insert_teacher_limit, insert_time_slot, get_teachers, 
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
