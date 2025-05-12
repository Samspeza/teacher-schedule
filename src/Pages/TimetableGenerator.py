import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))  
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'DbContext'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'UserControl'))
from ortools.sat.python import cp_model
from UserControl.config import (
    get_teacher_availability_for_timetable,
    get_teacher_data,
    get_disciplines,
    get_class_course,
    get_class_id,
    get_teacher_limits,
    days_of_week,
    time_slots  # ex: [(19, 20), (20, 21), (21, 22)]
)

class TimetableGenerator:
    def __init__(self):
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        coordinator_id=1
        # Carregando dados
        self.teachers = get_teacher_data(1)
        self.availability = get_teacher_availability_for_timetable()
        self.disciplines = get_disciplines(1)
        self.teacher_limits = get_teacher_limits(1)
        self.classes = get_class_id()
        self.days = days_of_week
        self.time_blocks = time_slots

        self.variables = []

    def generate(self):
        """
        Gera as variáveis e restrições para a grade horária usando OR-Tools.
        """
        teacher_ids = list(self.teachers.keys())
        coordinator_id = 1

        for discipline in self.disciplines:
            discipline_id = discipline['id']
            class_id = discipline['class_id']
            required_hours = float(discipline['weekly_hours'])

            periods_needed = []
            if required_hours == 1.5:
                periods_needed = [1, 0.5]  # Um bloco inteiro (3h) e meio bloco (1h)
            elif required_hours == 3:
                periods_needed = [1, 1]  # Dois blocos inteiros (2x3h)
            else:
                periods_needed = [0.5, 0.5, 0.5]  # Exemplo para 1.5h com blocos menores

            for day in self.days:
                for start_block_index in range(len(self.time_blocks)):
                    for teacher_id in teacher_ids:
                        var = self.model.NewBoolVar(f'd_{discipline_id}_t_{teacher_id}_d_{day}_b_{start_block_index}')
                        self.variables.append((var, discipline, teacher_id, day, start_block_index))

        # Exemplo de restrição: respeitar disponibilidade dos professores
        for var, discipline, teacher_id, day, block_index in self.variables:
            if not self.availability.get((teacher_id, day, block_index), False):
                self.model.Add(var == 0)

                # --- Restrição: garantir que cada disciplina seja alocada na carga horária total ---
        from collections import defaultdict

        discipline_allocation = defaultdict(list)
        for var, discipline, teacher_id, day, block_index in self.variables:
            discipline_id = discipline['id']
            discipline_allocation[discipline_id].append(var)

        for discipline in self.disciplines:
            discipline_id = discipline['id']
            required_hours = float(discipline['weekly_hours'])

            # Cada bloco tem 1h (ex: 19-20, 20-21, 21-22)
            blocks_required = int(required_hours)

            # Garante alocação de tempo total da disciplina
            self.model.Add(sum(discipline_allocation[discipline_id]) >= blocks_required)

        # --- Restrição: um professor não pode estar em dois lugares no mesmo horário ---
        for teacher_id in self.teachers:
            for day in self.days:
                for block_index in range(len(self.time_blocks)):
                    overlapping_vars = [
                        var for var, _, t_id, d, b in self.variables
                        if t_id == teacher_id and d == day and b == block_index
                    ]
                    self.model.Add(sum(overlapping_vars) <= 1)

        # --- Restrição: blocos contínuos para disciplinas de 3h ---
        # Se uma disciplina tem 3h semanais, ela pode usar um único professor em blocos contínuos
        for discipline in self.disciplines:
            if float(discipline['weekly_hours']) == 3:
                discipline_id = discipline['id']
                for teacher_id in self.teachers:
                    for day in self.days:
                        for b in range(len(self.time_blocks) - 2):  # precisa de 3 blocos seguidos
                            block_vars = []
                            for i in range(3):
                                for var, d, t_id, d_day, b_index in self.variables:
                                    if (
                                        d['id'] == discipline_id and
                                        t_id == teacher_id and
                                        d_day == day and
                                        b_index == b + i
                                    ):
                                        block_vars.append(var)
                            if len(block_vars) == 3:
                                # Se um dos blocos for alocado, aloque os 3
                                self.model.AddBoolOr(block_vars).OnlyEnforceIf(block_vars[0])
                                self.model.Add(sum(block_vars) == 3).OnlyEnforceIf(block_vars[0])

        # --- Restrição: limite diário de aulas por professor ---
        for teacher_id in self.teachers:
            limit = self.teacher_limits.get(teacher_id, 3)  # padrão: 3 blocos por dia
            for day in self.days:
                teacher_day_vars = [
                    var for var, _, t_id, d, _ in self.variables
                    if t_id == teacher_id and d == day
                ]
                self.model.Add(sum(teacher_day_vars) <= limit)

        # --- Restrição: evitar que disciplinas compartilhem o mesmo laboratório ao mesmo tempo ---
        # (Exemplo simples, se quiser posso expandir para caso com `get_available_lab`)
        discipline_day_block = defaultdict(list)
        for var, discipline, _, day, block_index in self.variables:
            discipline_day_block[(day, block_index)].append(var)
        for key, vars_list in discipline_day_block.items():
            self.model.Add(sum(vars_list) <= len(self.classes))  # máximo 1 por turma por bloco


        status = self.solver.Solve(self.model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return self.extract_schedule()
        else:
            return None

def extract_schedule(self):
    schedule = []

    for var, discipline, teacher_id, day, block_index in self.variables:
        if self.solver.Value(var):
            start, end = self.time_blocks[block_index].split('-')
            schedule.append({
                "DIA": day,
                "INÍCIO": start,
                "TÉRMINO": end,
                "DISCIPLINA": discipline['name'],
                "PROFESSOR": self.teachers[teacher_id]['name'],
                "TURMA": self.classes[discipline['class_id']]['name']
            })

    # Ordena por dia e início para facilitar leitura
    schedule.sort(key=lambda x: (x["DIA"], x["INÍCIO"]))
    return schedule

def on_generate():
    generator = TimetableGenerator()
    schedule = generator.generate()
    if schedule:
        msg = "\n".join([f"{s['day']} - {s['time']}: {s['discipline']} com {s['teacher']}" for s in schedule])
        messagebox.showinfo("Grade Gerada", msg)
    else:
        messagebox.showerror("Erro", "Não foi possível gerar uma grade viável.")

# Interface Gráfica
def create_interface():
    root = tk.Tk()
    root.title("Gerador de Grade de Aulas")

    label = tk.Label(root, text="Clique para gerar a grade de aulas com OR-Tools")
    label.pack(pady=10)

    button = tk.Button(root, text="Gerar Grade", command=on_generate, bg="green", fg="white", height=2, width=20)
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_interface()
