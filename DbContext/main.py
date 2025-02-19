# main.py
from database import create_tables
from models import insert_teacher, get_teachers, insert_availability

def main():
    create_tables()

    teacher_id = insert_teacher("Allan", max_days=3)
    print(f"Professor inserido com ID: {teacher_id}")

    insert_availability(teacher_id, ["Segunda", "Quarta", "Sexta"])

    teachers = get_teachers()
    print("Professores cadastrados:")
    for teacher in teachers:
        print(f"ID: {teacher[0]}, Nome: {teacher[1]}")

if __name__ == "__main__":
    main()
