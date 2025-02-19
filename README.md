# Sistema de Alocação de Professores e Grade de Aulas

Este projeto é um sistema para alocar automaticamente professores em turmas de cursos, gerando uma grade de aulas com base nas disponibilidades dos professores e nas limitações de dias de trabalho. A grade é exibida por meio de uma interface gráfica construída com Tkinter. O sistema utiliza um banco de dados SQLite para armazenar as informações de professores, turmas, horários e suas respectivas alocações.

## Funcionalidades

- **Cadastro de Professores**: Professores podem ser cadastrados no banco de dados, incluindo a definição de sua disponibilidade (dias da semana em que estão disponíveis).
- **Cadastro de Turmas e Horários**: Permite o cadastro de turmas e horários de aulas.
- **Alocação Automática de Professores**: O sistema aloca automaticamente os professores nas turmas, respeitando suas disponibilidades e limites de carga horária semanal.
- **Geração de Grade de Aulas**: Gera uma grade de aulas para cada turma, respeitando as alocações de professores e suas disponibilidades.
- **Interface Gráfica**: A grade de aulas gerada é exibida em uma interface gráfica com Tkinter, permitindo ao usuário visualizar e navegar por diferentes soluções de alocação de professores.
- **Edição de Professores e Alocações**: Usuários podem editar a alocação de professores diretamente na interface gráfica, permitindo a atualização da disponibilidade e alocações no banco de dados.
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

- **database.py**: Contém funções para criar o banco de dados e as tabelas.
- **models.py**: Contém funções para inserir dados nas tabelas do banco de dados, como professores, turmas, horários e disponibilidades.
- **main.py**: Contém o código principal para inicializar o banco de dados e inserir dados de exemplo.
- **generate_timetable.py**: Contém a lógica para gerar a grade de aulas, alocando professores automaticamente e respeitando as regras de disponibilidade.
- **gui.py**: Contém o código para exibir a grade de aulas gerada em uma interface gráfica usando Tkinter.

## Requisitos

- Python 3.x
- Tkinter (para a interface gráfica)
- SQLite (para o banco de dados)

## Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/seu-usuario/sistema-grade-aulas.git
   cd sistema-grade-aulas
   ```

2. **Instale as dependências**:

   O Tkinter já está incluído no Python, portanto, você só precisa garantir que o SQLite (que é uma biblioteca padrão) esteja disponível.

3. **Execute o banco de dados**:

   Para criar o banco de dados e as tabelas, execute o arquivo `database.py`:

   ```bash
   python database.py
   ```

4. **Adicione professores, turmas e disponibilidades**:

   Com o banco de dados configurado, adicione os dados de professores, turmas e suas disponibilidades executando o arquivo `main.py`:

   ```bash
   python main.py
   ```

5. **Gere e visualize as grades de aulas**:

   Para gerar a grade de aulas, execute o arquivo `generate_timetable.py`:

   ```bash
   python generate_timetable.py
   ```

   Para exibir a grade gerada, execute o arquivo `gui.py`:

   ```bash
   python gui.py
   ```

## Como Usar

- **Cadastro de Professores e Turmas**: Ao rodar `main.py`, você poderá cadastrar professores e suas disponibilidades. As turmas também podem ser cadastradas nesse passo.
- **Geração da Grade**: Ao rodar `generate_timetable.py`, o sistema gera automaticamente a grade de aulas para as turmas cadastradas, levando em conta as disponibilidades dos professores e os horários definidos.
- **Visualização da Grade**: Ao rodar `gui.py`, a grade de aulas gerada é exibida em uma interface gráfica. A interface permite que você navegue pelas diferentes soluções de alocação e veja os professores alocados para cada aula, considerando o dia e o horário.

