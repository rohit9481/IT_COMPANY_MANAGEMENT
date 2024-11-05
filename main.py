from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection details
db_config = {
    'user': 'root',     # Replace with your MySQL username
    'password': 'rohit',  # Replace with your MySQL password
    'host': 'localhost',     # Replace with your database host if needed
    'database': 'it_company_db'
}

# Database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Route to view all projects with status and assigned employees
@app.route('/projects')
def view_projects():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT p.Project_ID, p.Project_Name, p.Start_Date, p.End_Date, p.Status, 
           GROUP_CONCAT(e.First_Name, ' ', e.Last_Name SEPARATOR ', ') AS Assigned_Employees
    FROM project p
    LEFT JOIN employee_project ep ON p.Project_ID = ep.Project_ID
    LEFT JOIN employee e ON ep.Employee_ID = e.Employee_ID
    GROUP BY p.Project_ID
    """
    cursor.execute(query)
    projects = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('projects.html', projects=projects)

# Route to add a new employee
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['date_of_birth']
        hire_date = request.form['date_of_hire']
        salary_id = request.form['salary_id']
        department_id = request.form['department_id']
        branch_id = request.form['branch_id']
        team_id = request.form['team_id']
        position = request.form['position']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO employee (First_Name, Last_Name, Date_of_Birth, Date_of_Hire, Salary_ID, 
                                  Department_ID, Branch_ID, Team_ID, Position)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, dob, hire_date, salary_id, department_id, branch_id, team_id, position))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('home'))

    return render_template('add_employee.html')

# Route to add a new project
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        duration = request.form['duration']
        department_id = request.form['department_id']
        budget = request.form['budget']
        status = request.form['status']
        client_id = request.form['client_id']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO project (Project_Name, Start_Date, End_Date, Duration, 
                                 Department_ID, Budget, Status, Client_ID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (project_name, start_date, end_date, duration, department_id, budget, status, client_id))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('view_projects'))

    return render_template('add_project.html')

if __name__ == '__main__':
    app.run(debug=True)
