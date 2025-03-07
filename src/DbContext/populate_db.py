import sqlite3
from database import DB_NAME, create_tables
from models import (
    insert_discipline, insert_teacher, insert_availability, insert_class, insert_teacher_limit, insert_time_slot, get_teachers, 
    clear_teachers, clear_classes, clear_time_slots, clear_availability, reset_ids
)

classes = [f"CC{i}" for i in range(1, 9)] + [f"ADS{i}" for i in range(1, 3)] + ["ADS3P", "ADS3R"] + [f"ADS{i}" for i in range(4, 5)]
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
    ("CC4", "AR", "Arquitetura de Redes", 1.5, "T", 5),
    ("CC5", "AR", "Arquitetura de Redes", 1.5, "T", 5),
    ("CC4", "CG", "Comp. Gráfica", 1.5, "T", 5),
    ("CC5", "CG", "Comp. Gráfica", 1.5, "T", 5),
    ("CC4", "AC", "Arquitetura de Computadores", 1.5, "T", 5),
    ("CC5", "AC", "Arquitetura de Computadores", 1.5, "T", 5),
    ("CC4", "LFA", "Ling. Formais e Autom.", 1.5, "T", 5),
    ("CC5", "LFA", "Ling. Formais e Autom.", 1.5, "T", 5),
    ("CC4", "IA", "Inteligência Artificial", 3, "T", 5),
    ("CC4", "SO", "Sistemas Operacionais", 3, "T/P", 5),
    ("CC5", "IA", "Inteligência Artificial", 3, "T", 5),
    ("CC5", "SO", "Sistemas Operacionais", 3, "T/P", 5),
    ("CC2", "LPOO", "Ling. Programação OO", 4.5, "1T/2P", 3),
    ("CC2", "BD", "Banco de Dados", 4.5, "2T/1P", 3),
    ("CC3", "LPOO", "Ling. Programação OO", 4.5, "1T/2P", 3),
    ("CC3", "BD", "Banco de Dados", 4.5, "2T/1P", 3),
    ("CC2", "AG", "Álgebra Linear", 1.5, "1T/2P", 3),
    ("CC3", "AG", "Álgebra Linear", 1.5, "1T/2P", 3),
    ("CC2", "BD", "Banco de Dados", 4.5, "2T/1P", 3),
    
    ("CC6", "AA", "Análise de Algoritmo", 1.5, "1T/2P", 3),
    ("CC6", "FRV", "Fund. Realidade Virtual / Aum", 3, "1T/2P", 3),
    ("CC6", "SD", "Sistemas Distribuídos", 3, "1T/2P", 3),
    ("CC6", "TCI", "TCI", 1.5, "1T/2P", 3),
    ("CC6", "ES", "Engenharia de Software", 3, "1T/2P", 3),
    
    ("CC7", "AA", "Análise de Algoritmo", 1.5, "1T/2P", 3),
    ("CC7", "FRV", "Fund. Realidade Virtual / Aum", 3, "1T/2P", 3),
    ("CC7", "SD", "Sistemas Distribuídos", 3, "1T/2P", 3),
    ("CC7", "TCI", "TCI", 1.5, "1T/2P", 3),
    ("CC7", "ES", "Engenharia de Software", 3, "1T/2P", 3),
    
    ("CC1", "FC", "Física para Computação", 1.5, "1T/2P", 3),
    ("CC1", "PWR", "Programação Web Responsiva", 1.5, "1T/2P", 3),
    ("CC1", "ER", "Engenharia de Requisistos", 1.5, "1T/2P", 3),
    ("CC1", "IHC", "Interface Humano Computador", 1.5, "1T/2P", 3),
    ("CC1", "DDM", "Des. Dispositivos Móveis", 1.5, "1T/2P", 3),
    ("CC1", "TMA", "Tópicos de Matemática Aplicada", 1.5, "1T/2P", 3),

    ("ADS3P", "POO", "Programa O.O.", 3, "T/P", 3),
    ("ADS3P", "ESII", "Engenharia de Software II", 3, "T/P", 3),
    ("ADS3P", "BD", "Banco de Dados", 3, "T/P", 3),
    ("ADS3P", "ASOO", "Analise Sistemas O.O.", 3, "T/P", 3),
    ("ADS3P", "IU", "Interface com Usuário", 3, "T/P", 3),
    ("ADS3R", "POO", "Programa O.O.", 3, "T/P", 3),
    ("ADS3R", "ESII", "Engenharia de Software II", 3, "T/P", 3),
    ("ADS3R", "BD", "Banco de Dados", 3, "T/P", 3),
    ("ADS3R", "ASOO", "Analise Sistemas O.O.", 3, "T/P", 3),
    ("ADS3R", "IU", "Interface com Usuário", 3, "T/P", 3),
    ("ADS1", "PLP", "Pensamento Lógico Comp. Python", 3, "T/P", 1),
    ("ADS1", "IC", "Infraestrutura Computacional", 3, "T", 1),
    ("ADS1", "TIC", "Tec da Informação e Comunicação", 3, "T", 1),
    ("ADS1", "MAT", "Matemática e Estatística", 3, "T", 1),
    ("ADS4", "OC", "Organização de Computadores", 3, "T", 1),
    ("ADS4", "FSO", "Fundamentos SO", 3, "T", 1),
    ("ADS4", "PSI", "Princípios de SI", 3, "T", 1),
    
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
