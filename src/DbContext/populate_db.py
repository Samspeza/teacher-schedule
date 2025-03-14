import sqlite3
from database import DB_NAME, create_tables
from models import (
    insert_discipline, insert_teacher, insert_availability, insert_class, insert_teacher_limit, insert_time_slot, get_teachers, 
    clear_teachers, clear_classes, clear_time_slots, clear_availability, reset_ids
)

classes = [f"CC{i}" for i in range(1, 9)] + [f"ADS{i}" for i in range(1, 3)] + ["ADS3P", "ADS3R"] + [f"ADS{i}" for i in range(4, 5)]
class_coordinator = {}

for class_name in classes:
    if class_name.startswith("CC"):
        class_coordinator[class_name] = 1  
    elif class_name.startswith("ADS"):
        class_coordinator[class_name] = 2  

days_of_week = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

time_slots = [
    "19:10 - 20:25",  # 1ª aula
    "20:25 - 20:45",  # Intervalo
    "20:45 - 22:00"   # 2ª aula
]

teachers = {
    "Lidiana": {"days": ["Segunda", "Terça", "Sexta"], "coordinator_id": 1},
    "Diogo": {"days": ["Segunda"], "coordinator_id": 1},
    "Flávio": {"days": ["Terça", "Quarta"], "coordinator_id": 1},
    "André": {"days": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], "coordinator_id": 1},
    "Jucilene": {"days": ["Quarta"], "coordinator_id": 1},
    "Joao Otávio": {"days": ["Segunda", "Terça", "Quarta", "Quinta"], "coordinator_id": 1},
    "Allan": {"days": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], "coordinator_id": 1},
    "Valter": {"days": ["Terça", "Quarta"], "coordinator_id": 1},
    "Fábio": {"days": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], "coordinator_id": 1},
    "Cícero": {"days": ["Segunda", "Terça", "Quarta"], "coordinator_id": 1},
    "Elio": {"days": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], "coordinator_id": 1},
    "Evandro": {"days": ["Quinta"], "coordinator_id": 1},
    "Taisa": {"days": ["Segunda", "Quarta", "Quinta"], "coordinator_id": 1},
    "Rogerio": {"days": ["Segunda", "Terça", "Quarta", "Quinta"], "coordinator_id": 1},
    "Franco": {"days": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"], "coordinator_id": 1},
    "Joao Marcelo": {"days": ["Segunda", "Terça", "Sexta"], "coordinator_id": 1},
    "Janayna": {"days": ["Segunda"], "coordinator_id": 1}
}

disciplines = [
    ("CC4", "AR", "Arquitetura de Redes", 1.5, "T", 5, 1),
    ("CC5", "AR", "Arquitetura de Redes", 1.5, "T", 5, 1),
    ("CC4", "CG", "Comp. Gráfica", 1.5, "T", 5, 1),
    ("CC5", "CG", "Comp. Gráfica", 1.5, "T", 5, 1),
    ("CC4", "AC", "Arquitetura de Computadores", 1.5, "T", 5, 1),
    ("CC5", "AC", "Arquitetura de Computadores", 1.5, "T", 5, 1),
    ("CC4", "LFA", "Ling. Formais e Autom.", 1.5, "T", 5, 1),
    ("CC5", "LFA", "Ling. Formais e Autom.", 1.5, "T", 5, 1),
    ("CC4", "IA", "Inteligência Artificial", 3, "T", 5, 1),
    ("CC4", "SO", "Sistemas Operacionais", 3, "T/P", 5, 1),
    ("CC5", "IA", "Inteligência Artificial", 3, "T", 5, 1),
    ("CC5", "SO", "Sistemas Operacionais", 3, "T/P", 5, 1),
    ("CC2", "LPOO", "Ling. Programação OO", 4.5, "1T/2P", 3, 1),
    ("CC2", "BD", "Banco de Dados", 4.5, "2T/1P", 3, 1),
    ("CC3", "LPOO", "Ling. Programação OO", 4.5, "1T/2P", 3, 1),
    ("CC3", "BD", "Banco de Dados", 4.5, "2T/1P", 3, 1),
    ("CC2", "AG", "Álgebra Linear", 1.5, "1T/2P", 3, 1),
    ("CC3", "AG", "Álgebra Linear", 1.5, "1T/2P", 3, 1),
    ("CC2", "BD", "Banco de Dados", 4.5, "2T/1P", 3, 1),
    
    ("CC6", "AA", "Análise de Algoritmo", 1.5, "1T/2P", 3, 1),
    ("CC6", "FRV", "Fund. Realidade Virtual / Aum", 3, "1T/2P", 3, 1),
    ("CC6", "SD", "Sistemas Distribuídos", 3, "1T/2P", 3, 1),
    ("CC6", "TCI", "TCI", 1.5, "1T/2P", 3, 1),
    ("CC6", "ES", "Engenharia de Software", 3, "1T/2P", 3, 1),
    
    ("CC7", "AA", "Análise de Algoritmo", 1.5, "1T/2P", 3, 1),
    ("CC7", "FRV", "Fund. Realidade Virtual / Aum", 3, "1T/2P", 3, 1),
    ("CC7", "SD", "Sistemas Distribuídos", 3, "1T/2P", 3, 1),
    ("CC7", "TCI", "TCI", 1.5, "1T/2P", 3, 1),
    ("CC7", "ES", "Engenharia de Software", 3, "1T/2P", 3, 1),
    
    ("CC8", "TCII", "TCII", 1.5, "1T/2P", 3, 1),
    ("CC8", "QS", "Qualidade de Software", 3, "1T/2P", 3, 1),
    ("CC8", "SD", "Sistemas Distribuídos", 3, "1T/2P", 3, 1),
    ("CC8", "OS", "Orientação Estágio", 1, "1T/2P", 3, 1),

    ("CC1", "FC", "Física para Computação", 1.5, "1T/2P", 3, 1),
    ("CC1", "PWR", "Programação Web Responsiva", 1.5, "1T/2P", 3, 1),
    ("CC1", "ER", "Engenharia de Requisistos", 1.5, "1T/2P", 3, 1),
    ("CC1", "IHC", "Interface Humano Computador", 1.5, "1T/2P", 3, 1),
    ("CC1", "DDM", "Des. Dispositivos Móveis", 1.5, "1T/2P", 3, 1),
    ("CC1", "TMA", "Tópicos de Matemática Aplicada", 1.5, "1T/2P", 3, 1),

    ("ADS3P", "POO", "Programa O.O.", 3, "T/P", 3, 2),
    ("ADS3P", "ESII", "Engenharia de Software II", 3, "T/P", 3, 2),
    ("ADS3P", "BD", "Banco de Dados", 3, "T/P", 3, 2),
    ("ADS3P", "ASOO", "Analise Sistemas O.O.", 3, "T/P", 3, 2),
    ("ADS3P", "IU", "Interface com Usuário", 3, "T/P", 3, 2),
    ("ADS3R", "POO", "Programa O.O.", 3, "T/P", 3, 2),
    ("ADS3R", "ESII", "Engenharia de Software II", 3, "T/P", 3, 2),
    ("ADS3R", "BD", "Banco de Dados", 3, "T/P", 3, 2),
    ("ADS3R", "ASOO", "Analise Sistemas O.O.", 3, "T/P", 3, 2),
    ("ADS3R", "IU", "Interface com Usuário", 3, "T/P", 3, 2),

    ("ADS1", "PLP", "Pensamento Lógico Comp. Python", 3, "T/P", 1, 2),
    ("ADS1", "IC", "Infraestrutura Computacional", 3, "T", 1, 2),
    ("ADS1", "TIC", "Tec da Informação e Comunicação", 3, "T", 1, 2),
    ("ADS1", "MAT", "Matemática e Estatística", 3, "T", 1, 2),
    
    ("ADS4", "OC", "Organização de Computadores", 3, "T", 1, 2),
    ("ADS4", "FSO", "Fundamentos SO", 3, "T", 1, 2),
    ("ADS4", "PSI", "Princípios de SI", 3, "T", 1, 2),
]

class_coordinator = {
    "CC1": 1, "CC2": 1, "CC3": 1, "CC4": 1, "CC5": 1, "CC6": 1, "CC7": 1, "CC8": 1,
    "ADS1": 2, "ADS2": 2, "ADS3P": 2, "ADS3R": 2, "ADS4": 2
}

def populate_disciplines():
    print("Criando tabelas no banco de dados...")
    create_tables()
    
    print("Populando banco de dados com disciplinas...")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for course, sigla, name, hours, type_, class_number, coordinator_id in disciplines:
        insert_discipline(course, sigla, name, hours, type_, class_number, coordinator_id)
    
    conn.commit()
    conn.close()
    print("Disciplinas inseridas com sucesso!")

populate_disciplines()

teacher_limits = {
    "Lidiana": 3,
    "Diogo": 1,
    "Flávio": 2,
    "André": 5,
    "Jucilene": 1,
    "Joao Otávio": 4,
    "Allan": 1,
    "Valter": 2,
    "Fábio": 5,
    "Cícero": 3,
    "Elio": 3,
    "Evandro": 1,
    "Taisa": 3,
    "Rogerio": 4,
    "Franco": 5,
    "Joao Marcelo": 3,
    "Janayna": 1
}


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

        # Inserção de professores, suas disponibilidades e limites
    for teacher_name, data in teachers.items():
        coordinator_id = data["coordinator_id"]
        available_days = data["days"]
        
        teacher_id = insert_teacher(teacher_name, coordinator_id)

        insert_availability(teacher_id, available_days, coordinator_id)
        limit = teacher_limits.get(teacher_name)  
        if limit is not None:
            insert_teacher_limit(teacher_id, limit, coordinator_id)


    # Inserir as classes e os coordenadores das classes
    for class_name, coordinator_id in class_coordinator.items():
        print(f"Classe: {class_name}, Coordenador: {coordinator_id}")
        insert_class(class_name, coordinator_id)

    # Inserir os slots de tempo
    for slot in time_slots:
        insert_time_slot(slot)
    
    print("Banco de dados populado com sucesso!")
populate_database()
