from faker import Faker
import random
import psycopg2

fake = Faker("uk_UA")

def get_db_connection():
 
  return psycopg2.connect(
    host="localhost",
    port="5432",
    database="company_db",
    user="example_user",
    password="example_password"
  )

def populate_data():
 
  connection = get_db_connection()
  cursor = connection.cursor()

  # Заповнення таблиці Departments
  departments = ["Програмування", "Дизайн", "ІТ", "HR", "Маркетинг"]

  for dept in departments:
    cursor.execute("""
      INSERT INTO Departments (name, phone, room_number) 
      VALUES (%s, %s, %s)
      """, (dept, f"+38067{random.randint(1000000, 9999999)}", random.randint(701, 710))
      )
    
  # Заповнення таблиці Positions
  positions = [("Інженер", 3000, 10), ("Редактор", 2500, 8), ("Програміст", 
  3500, 12)]

  for position in positions:
    cursor.execute("""
      INSERT INTO Positions (position_name, salary, bonus_percentage) 
      VALUES (%s, %s, %s)
      """, position
    )

  # Заповнення таблиці Employees
  for _ in range(17):
    last_name = fake.last_name()
    first_name = fake.first_name()
    patronymic = fake.first_name()
    address = fake.address()

    phone = f"+38067{random.randint(1000000, 9999999)}" # телефон в масці
    education = random.choice(["Спеціальна", "Середня", "Вища"])
    dept_id = random.randint(1, 5)
    position_id = random.randint(1, 3)

    cursor.execute("""
      INSERT INTO Employees (last_name, first_name, patronymic, address, phone, education, dept_id, position_id) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
      """, (last_name, first_name, patronymic, address, phone, education, dept_id, position_id)
    )

  # Заповнення таблиці Projects
  for _ in range(8):
    project_name = fake.company()
    deadline = fake.date_this_year()
    funding = random.randint(50000, 500000)
    cursor.execute("""
    INSERT INTO Projects (project_name, deadline, funding) VALUES (%s, %s, %s)
    """, (project_name, deadline, funding)
  )
    
  # Заповнення таблиці ProjectAssignments
  for _ in range(8):
    project_id = random.randint(1, 8)
    dept_id = random.randint(1, 5)
    start_date = fake.date_this_year()
    cursor.execute("""
    INSERT INTO ProjectAssignments (project_id, dept_id, start_date)
    VALUES (%s, %s, %s)
    """, (project_id, dept_id, start_date)
    )

  connection.commit()
  cursor.close()
  connection.close()
  
populate_data()