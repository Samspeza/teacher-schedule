from models import insert_teacher, insert_availability, insert_class, insert_time_slot, get_teachers

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
    existing_teachers = get_teachers()
    
    if existing_teachers:
        print("O banco de dados já foi populado.")
        return

    print("Populando banco de dados...")

    for class_name in classes:
        insert_class(class_name)

    for slot in time_slots:
        insert_time_slot(slot)

    for teacher, available_days in teachers.items():
        teacher_id = insert_teacher(teacher, teacher_limits.get(teacher, None))  
        insert_availability(teacher_id, available_days)

    print("Banco de dados populado com sucesso!")
populate_database()
