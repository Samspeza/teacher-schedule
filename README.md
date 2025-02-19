# README: Sistema de Grade de Aulas

Este projeto é um sistema de alocação de professores para turmas de cursos, gerando automaticamente uma grade de aulas com base nas disponibilidades dos professores e nas limitações de dias de trabalho. O sistema também fornece uma interface gráfica usando Tkinter para exibir a grade de aulas gerada. O banco de dados SQLite é usado para armazenar informações sobre professores, turmas, horários e disponibilidades.

## Funcionalidades

- **Cadastro de Professores**: Professores podem ser cadastrados no banco de dados, incluindo a definição de sua disponibilidade (dias da semana em que estão disponíveis).
- **Alocação Automática de Professores**: O sistema aloca automaticamente os professores nas turmas, respeitando suas disponibilidades e limites de dias de trabalho.
- **Interface Gráfica**: A grade de aulas gerada é exibida em uma interface gráfica com Tkinter, permitindo ao usuário visualizar e navegar por várias soluções de alocação.
- **Banco de Dados**: O sistema usa SQLite para armazenar dados sobre professores, turmas, horários e a alocação de professores.

## Arquitetura

### Banco de Dados

O banco de dados SQLite contém as seguintes tabelas:

- **teachers**: Contém informações sobre os professores, incluindo nome e número máximo de dias que cada um pode lecionar por semana.
- **teacher_availability**: Armazena os dias da semana em que cada professor está disponível.
- **classes**: Armazena as turmas (ex: "CC1", "ADS1").
- **time_slots**: Define os horários das aulas (ex: "19:10 - 20:25", "20:25 - 20:45", "20:45 - 22:00").
- **schedule**: Armazena a alocação de professores para turmas em horários específicos.

### Arquivos

1. **`database.py`**: Contém funções para criar o banco de dados e as tabelas.
2. **`models.py`**: Contém funções para inserir dados nas tabelas do banco, como professores, turmas, horários e disponibilidades.
3. **`main.py`**: Contém o código principal para inicializar o banco de dados e inserir dados de exemplo.
4. **`generate_timetable.py`**: Contém a lógica para gerar a grade de aulas, alocando professores automaticamente e respeitando as regras de disponibilidade.
5. **`gui.py`**: Contém o código para exibir a grade de aulas gerada em uma interface gráfica usando Tkinter.

## Requisitos

- Python 3.x
- Tkinter (para a interface gráfica)
- SQLite (para o banco de dados)

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/sistema-grade-aulas.git
   cd sistema-grade-aulas
   ```

2. Instale as dependências:
   - Tkinter já está incluído no Python, então você só precisa de SQLite que é uma biblioteca padrão.

3. Execute o banco de dados:
   ```
   python database.py
   ```

4. Adicione professores, turmas e disponibilidades com o arquivo `main.py`:
   ```
   python main.py
   ```

5. Gere e visualize as grades de aulas:
   ```
   python generate_timetable.py
   python gui.py
   ```

## Como Usar

1. **Cadastro de Professores e Turmas**: Ao rodar `main.py`, você poderá cadastrar professores e suas disponibilidades.
2. **Geração da Grade**: Ao rodar `generate_timetable.py`, o sistema gera automaticamente a grade de aulas para as turmas cadastradas, com base nas disponibilidades dos professores e nos horários.
3. **Visualização da Grade**: Ao rodar `gui.py`, você verá a grade de aulas gerada na interface gráfica. Você pode navegar pelas soluções geradas e visualizar a alocação de professores por dia e horário.



