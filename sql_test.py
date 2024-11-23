import psycopg2
from prettytable import PrettyTable

def get_db_connection():
  return psycopg2.connect(
  host="localhost",
  port="5432",
  database="company_db",
  user="example_user",
  password="example_password"
  )
def execute_queries():
  connection = get_db_connection()
  cursor = connection.cursor()

  # 1. Робітники з окладом більше 2000 грн, сортування за прізвищем
  cursor.execute(
    """
      SELECT last_name, first_name, salary FROM Employees
      JOIN Positions ON Employees.position_id = Positions.position_id
      WHERE salary > 2000
      ORDER BY last_name;
    """
  )

  table = PrettyTable(["Прізвище", "Ім'я", "Оклад"])
  
  for row in cursor.fetchall():
    table.add_row(row)
    print("Робітники з окладом більше 2000 грн:\n", table)

  # 2. Середня зарплатня в кожному відділі
  cursor.execute(
    """
      SELECT Departments.name, AVG(Positions.salary) AS avg_salary FROM 
      Employees
      JOIN Departments ON Employees.dept_id = Departments.dept_id
      JOIN Positions ON Employees.position_id = Positions.position_id
      GROUP BY Departments.name;
    """
  )
  table = PrettyTable(["Назва відділу", "Середня зарплатня"])

  for row in cursor.fetchall():
    table.add_row(row)
    print("\nСередня зарплатня в кожному відділі:\n", table)

  # 3. Всі проекти в обраному відділі (введіть ID відділу)
  selected_dept_id = int(input("Введіть ID відділу для перегляду проектів: "))
  cursor.execute(
    """
      SELECT Projects.project_name FROM ProjectAssignments
      JOIN Projects ON ProjectAssignments.project_id = Projects.project_id
      WHERE ProjectAssignments.dept_id = %s;
    """, (selected_dept_id,))
  
  table = PrettyTable(["Назва проекту"])

  for row in cursor.fetchall():
    table.add_row(row)
    print(f"\nПроекти у відділі з ID {selected_dept_id}:\n", table)

  # 4. Кількість працівників у кожному відділі
  cursor.execute(
    """
      SELECT Departments.name, COUNT(Employees.employee_id) AS 
      employee_count FROM Employees
      JOIN Departments ON Employees.dept_id = Departments.dept_id
      GROUP BY Departments.name;
    """
  )

  table = PrettyTable(["Назва відділу", "Кількість працівників"])

  for row in cursor.fetchall():
    table.add_row(row)
    print("\nКількість працівників у кожному відділі:\n", table)

  # 5. Розмір премії для кожного співробітника
  cursor.execute(
    """
      SELECT last_name, first_name, salary, (salary * bonus_percentage / 
      100) AS bonus FROM Employees
      JOIN Positions ON Employees.position_id = Positions.position_id;
    """
  )
  table = PrettyTable(["Прізвище", "Ім'я", "Оклад", "Премія"])
  
  for row in cursor.fetchall():
    table.add_row(row)
    print("\nРозмір премії для кожного співробітника:\n", table)
    
  # 6. Кількість працівників за рівнем освіти в кожному відділі
  cursor.execute(
    """
      SELECT Departments.name, education, COUNT(Employees.employee_id) AS 
      employee_count FROM Employees
      JOIN Departments ON Employees.dept_id = Departments.dept_id
      GROUP BY Departments.name, education;
    """
  )
  table = PrettyTable(["Назва відділу", "Освіта", "Кількість працівників"])
  
  for row in cursor.fetchall():
    table.add_row(row)
    print("\nКількість працівників за рівнем освіти в кожному відділі:\n", table)
    
  # Закриваємо з'єднання
  cursor.close()
  connection.close()
  
if __name__ == "__main__":
 execute_queries()



