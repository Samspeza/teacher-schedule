# Sistema de Alocação de Professores e Grade de Aulas

Este projeto é um sistema para alocar automaticamente professores em turmas de cursos, gerando uma grade de aulas com base nas disponibilidades dos professores e nas limitações de dias de trabalho. A aplicação utiliza uma interface gráfica construída com Tkinter e armazena as informações em um banco de dados SQLite.

---

## Funcionalidades

- **Cadastro de Professores e Disponibilidades:**  
  Permite cadastrar professores e registrar os dias da semana em que estão disponíveis, além de definir um limite de dias por semana para alguns professores.

- **Cadastro de Turmas e Horários:**  
  Possibilita o cadastro de turmas (ex.: "CC1", "ADS1", etc.) e a definição dos intervalos de tempo para as aulas.

- **Alocação Automática de Professores:**  
  O sistema aloca automaticamente os professores nas turmas, respeitando suas disponibilidades e os limites de carga horária. Durante a alocação, o algoritmo testa e aplica regras para evitar conflitos de horário.

- **Geração de Grade de Aulas:**  
  Gera uma grade de aulas para cada turma com base nas alocações dos professores.  
  **Observação:** No momento, o sistema gera as turmas juntas, pois está sendo testado o modelo de resolução do problema de alocação. Em versões futuras, as particularidades serão ajustadas para que cada turma seja gerada individualmente. Quando as tabelas de disciplinas para cada turma forem implementadas, será possível visualizar um modelo completo e detalhado da grade.

- **Interface Gráfica e Edição:**  
  A grade gerada é exibida em uma interface gráfica com Tkinter. Além de visualizar, o usuário pode:
  - Navegar entre diferentes soluções de alocação.
  - Criação manual de grades conforme a escolha da turma específica. Permitindo, assim, a escolha dos professores e disciplicas respectivas.
  - Editar ou excluir manualmente a alocação de professores. Caso uma edição cause conflito, o sistema verifica e realoca automaticamente conforme necessário.

- **Salvamento e Gerenciamento de Grades:**  
  As grades geradas podem ser salvas (inicialmente em formato JSON, armazenadas como um file.path no sqllite3) e gerenciadas por meio de uma aba específica. Nesta área, é possível:
  - Visualizar as grades salvas.
  - Editar uma grade já salva anteriormente, substituindo o arquivo raiz.
  - Re-salvar uma grade específica.
  - Excluir uma grade que não seja mais necessária.

---

## Arquitetura

### Banco de Dados

O sistema utiliza um banco de dados SQLite com as seguintes tabelas:

- **teachers:**  
  Armazena informações sobre os professores (nome e, quando aplicável, o limite de dias que podem lecionar por semana).

- **teacher_availability:**  
  Registra os dias da semana em que cada professor está disponível.

- **classes:**  
  Contém os dados das turmas (ex.: "CC1", "ADS1", etc.).

- **time_slots:**  
  Define os intervalos de tempo para as aulas (ex.: "19:10 - 20:25", "20:25 - 20:45", "20:45 - 22:00").

- **schedule:**  
  Armazena a alocação dos professores para cada turma e horário.

- **saved_grades:**  
  Armazena as grades salvas, com informações como nome, conteúdo e o caminho do arquivo JSON correspondente.

### Arquivos do Projeto

- **database.py:**  
  Funções para criar o banco de dados e as tabelas necessárias.

- **models.py:**  
  Funções para inserir e recuperar dados (professores, disponibilidades, etc.) do banco de dados.

- **main.py:**  
  Script principal para inicializar o banco de dados e inserir dados de exemplo (professores, turmas, disponibilidades).  
  **Nota:** Utiliza as configurações definidas em `config.py`.

- **generate_timetable.py:**  
  Contém a lógica para gerar a grade de aulas automaticamente, alocando os professores de acordo com suas disponibilidades e os horários definidos.

- **gui.py:**  
  Exibe a grade gerada em uma interface gráfica com Tkinter, permitindo a navegação entre as soluções de alocação e a edição manual das alocações.

- **teacherschedule.py:**  
  Contém a aplicação `TimetableApp`, que gerencia a criação e a visualização das grades de aulas.

- **saved_grades.py:**  
  Gerencia a visualização e o re-salvamento das grades salvas, por meio da classe `SavedGradesApp`.

- **config.py:**  
  Define as configurações do sistema, como a lista de turmas, dias da semana, intervalos de tempo, professores, disponibilidades e limites específicos de dias para alguns professores.

---

## Requisitos

- **Python 3.x**  
- **Tkinter:** Para a interface gráfica (já incluso na maioria das distribuições do Python).  
- **SQLite:** Banco de dados leve e integrado ao Python.

---

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/sistema-grade-aulas.git
   cd sistema-grade-aulas
   ```

2. **Verifique as dependências:**  
   O Tkinter e o SQLite já estão inclusos na maioria das instalações do Python. Certifique-se de que está utilizando o Python 3.x.

3. **Crie o banco de dados e as tabelas:**

   Execute o arquivo `database.py`:

   ```bash
   python database.py
   ```

4. **Adicione dados de exemplo:**

   Execute o arquivo `main.py` para cadastrar professores, turmas e suas disponibilidades:

   ```bash
   python main.py
   ```

5. **Geração e Visualização da Grade:**

   - Para gerar a grade de aulas, execute:

     ```bash
     python generate_timetable.py
     ```

   - Para visualizar a grade gerada em uma interface gráfica, execute:

     ```bash
     python gui.py
     ```

6. **Gerenciamento de Grades Salvas:**

   Para visualizar e gerenciar as grades salvas, execute:

   ```bash
   python saved_grades.py
   ```

---

## Como Usar

1. **Cadastro de Professores e Turmas:**  
   Execute `main.py` para cadastrar professores, suas disponibilidades e as turmas disponíveis.

2. **Geração da Grade:**  
   Ao executar `generate_timetable.py`, o sistema aloca automaticamente os professores às turmas, considerando suas disponibilidades e limites de dias.  
   **Atenção:** Atualmente, todas as turmas são geradas juntas enquanto o modelo de alocação está em fase de testes. Em futuras versões, essa funcionalidade será refinada para gerar cada turma de forma individual.

3. **Visualização e Edição da Grade:**  
   Execute `gui.py` para abrir a interface gráfica onde:
   - Você pode visualizar a grade completa.
   - Navegar entre as diferentes soluções de alocação.
   - Editar manualmente as alocações, com o sistema verificando e resolvendo possíveis conflitos automaticamente.

4. **Gerenciamento de Grades Salvas:**  
   A aba "SALVOS" permite visualizar as grades salvas, re-salvar ou excluir uma grade específica.

---

## Considerações Finais

- **Desenvolvimento Contínuo:**  
  O sistema ainda está em desenvolvimento. Atualmente, o algoritmo de alocação gera todas as turmas juntas para teste, mas em breve cada turma terá sua alocação ajustada individualmente. Além disso, com a criação das tabelas de disciplinas para cada turma, será possível visualizar um modelo completo e integrado da grade de aulas.

- **Interface:**  
  O design atual é simples e momentâneo, servindo para ilustrar o fluxo de trabalho. Planejo aprimorar o visual da interface em futuras atualizações.

---

*Desenvolvido com dedicação e inspirado na busca por soluções eficientes para a gestão de horários e alocação de professores.*
