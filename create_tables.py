import psycopg2

def get_db_connection():
  return psycopg2.connect(
  host="localhost",
  port="5432",
  database="company_db",
  user="example_user",
  password="example_password"
 )
def create_tables():

  connection = get_db_connection()
  cursor = connection.cursor()

  # Відділи (Departments)
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Departments (
    dept_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    room_number INT CHECK (room_number BETWEEN 701 AND 710)
    );
  """)

  # Посади (Positions)
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Positions (
    position_id SERIAL PRIMARY KEY,
    position_name VARCHAR(50) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    bonus_percentage DECIMAL(5, 2) NOT NULL
    );
  """)

  # Співробітники (Employees)
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employees (
    employee_id SERIAL PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    patronymic VARCHAR(50),
    address TEXT,
    phone VARCHAR(20),
    education VARCHAR(50) NOT NULL,
    dept_id INT,
    position_id INT,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id) ON DELETE SET 
    NULL,
    FOREIGN KEY (position_id) REFERENCES Positions(position_id) ON DELETE 
    SET NULL
    );
  """)

  # Проекти (Projects)
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    deadline DATE NOT NULL,
    funding DECIMAL(15, 2) NOT NULL
    );
  """)

  # Виконання проектів (ProjectAssignments)
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS ProjectAssignments (
    assignment_id SERIAL PRIMARY KEY,
    project_id INT,
    dept_id INT,
    start_date DATE NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id),
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
    );
  """)

  connection.commit()

  cursor.close()
  connection.close()

create_tables()
