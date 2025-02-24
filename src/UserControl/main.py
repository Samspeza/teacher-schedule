# main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'DbContext')))

from config import teachers, teacher_limits, classes, days_of_week, time_slots
from database import create_tables
from models import insert_teacher, insert_availability, get_teachers, get_teacher_availability


def main():
    create_tables()
    for teacher_name, available_days in teachers.items():
        max_days = teacher_limits.get(teacher_name, None)
        teacher_id = insert_teacher(teacher_name, max_days=max_days)
        print(f"Professor {teacher_name} inserido com ID: {teacher_id}")

        insert_availability(teacher_id, available_days)

    teachers_from_db = get_teachers()
    print("Professores cadastrados:")
    for teacher in teachers_from_db:
        print(f"ID: {teacher[0]}, Nome: {teacher[1]}")

    print("\nDisponibilidades dos professores:")
    for teacher in teachers_from_db:
        teacher_id = teacher[0]
        availability = get_teacher_availability(teacher_id)
        available_days = [day for days in teachers.values() for day in days]

        print(f"Professor ID {teacher_id} - Disponível em: {', '.join(available_days)}")

    print("\nConfigurações atuais:")
    print("Classes disponíveis:", ", ".join(classes))
    print("Dias da semana:", ", ".join(days_of_week))
    print("Intervalos de tempo:", ", ".join(time_slots))
    print("\nLimite de dias por professor:")
    for teacher, limit in teacher_limits.items():
        print(f"{teacher}: {limit} dias")


if __name__ == "__main__":
    main()
