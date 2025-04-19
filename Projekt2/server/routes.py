from flask import render_template, redirect, url_for, flash
from server import app
from server.forms import FilterForm, UpdateEmployeeForm, UpdateDepartmentForm, AddDepartmentForm, AddEmployeeForm
from server.databasehandler import execute, get_list
from server.data import create_employee, create_department, get_object, name_to_id

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    filter_form = FilterForm()
    query = []
    
    if filter_form.validate_on_submit():
        search = filter_form.search.data
        query = get_list("SELECT namn, telefon, avdelning FROM anstalld WHERE namn LIKE ?", (search + '%',))
    else:
        query = get_list("SELECT namn, telefon, avdelning FROM anstalld")

    employees = []
    for employee in query:
        employees.append(create_employee(name=employee[0], telephone=employee[1], department=employee[2]))
        
    departments = get_departments()
        
    for employee in employees:
        for department in departments:
            if employee['department'] == department['id']:
                employee['department'] = department['name']
    
    return render_template('index.html', filter_form=filter_form, employees=employees)

@app.route('/showemployee')
def show_employee():
    employees = []
    for employee in get_list("SELECT id, namn FROM anstalld"):
        employees.append(create_employee(id=employee[0], name=employee[1]))
    
    return render_template('show_employee.html', employees=employees)

@app.route("/deleteemployee/<id>")
def delete_employee(id):
    execute("DELETE FROM anstalld WHERE id = ?", id)
    flash(f'Deleted employee: {id}', 'success')
    return redirect(url_for('show_employee'))

@app.route('/showdepartment')
def show_department():
    return render_template('show_department.html', departments=get_departments())

@app.route('/updatedepartment/<id>', methods=['POST', 'GET'])
def update_department(id):
    update_department_form = UpdateDepartmentForm()
    
    query = get_list("SELECT namn FROM avdelning WHERE avd_id = ?", (id,))
    department = create_department(id=id, name=query[0][0])
    
    if update_department_form.validate_on_submit():
        name = update_department_form.name.data
        
        if name == department['name']:
            flash('Nothing changed', 'danger')
        else:
            execute("UPDATE avdelning SET namn = ? WHERE avd_id = ?", (name, id))
            flash('Succefully updated department', 'success')
    
        department['name'] = name
    
    update_department_form.name.data = department['name']
    
    return render_template('update_department.html', update_department_form=update_department_form, id=id)

@app.route('/updateemployee/<id>', methods=['POST', 'GET'])
def update_employee(id):
    update_employee_form = UpdateEmployeeForm()
    
    employees = []
    for employee in get_list("SELECT id, namn, telefon, lon, chef, avdelning FROM anstalld"):
        employees.append(create_employee(id=employee[0], name=employee[1], telephone=employee[2], salary=employee[3], boss=employee[4], department=employee[5]))
   
    departments = get_departments()
        
    employee = get_object(id, employees)
    
    update_employee_form.boss.choices = [e['name'] for e in employees if e['id'] != employee['id']]
    update_employee_form.department.choices = [d['name'] for d in departments]
    
    if update_employee_form.validate_on_submit():
        name = update_employee_form.name.data
        telephone = update_employee_form.telephone.data
        salary = update_employee_form.salary.data
        boss = update_employee_form.boss.data
        department = update_employee_form.department.data
        
        department_id = name_to_id(department, departments)
        boss_id = name_to_id(boss, employees)
        
        if name == employee['name'] and telephone == employee['telephone'] and salary == employee['salary'] and boss_id == employee['boss'] and department_id == employee['department']:
            flash('Nothing changed', 'danger')
        else:
            execute("UPDATE anstalld SET namn = ?, telefon = ?, lon = ?, chef = ?, avdelning = ? WHERE id = ?", (name, telephone, salary, boss_id, department_id, id))
            
            employee['name'] = name
            employee['telephone'] = telephone
            employee['salary'] = salary
            employee['boss'] = boss
    
            flash('Succesfully updated employee', 'success')
        return redirect(url_for('update_employee', id=id))
        
    boss = update_employee_form.boss.data
    department = update_employee_form.department.data
    
    update_employee_form.name.data = employee['name']
    update_employee_form.telephone.data = employee['telephone']
    update_employee_form.salary.data = employee['salary']
    
    return render_template('update_employee.html', update_employee_form=update_employee_form)

@app.route('/addemployee', methods=['POST', 'GET'])
def add_employee():
    add_employee_form = AddEmployeeForm()
    
    employees = []
    for employee in get_list("SELECT id, namn FROM anstalld"):
        employees.append(create_employee(id=employee[0], name=employee[1]))

    departments = get_departments()
    
    add_employee_form.boss.choices = [e['name'] for e in employees]
    add_employee_form.department.choices = [d['name'] for d in departments]
    
    if add_employee_form.validate_on_submit():
        name = add_employee_form.name.data
        telephone = add_employee_form.telephone.data
        salary = add_employee_form.salary.data
        boss = add_employee_form.boss.data
        department = add_employee_form.department.data
        
        department_id = name_to_id(department, departments)
        boss_id = name_to_id(boss, employees)
                
        execute("INSERT INTO anstalld (namn, telefon, lon, chef, avdelning) VALUES (?, ?, ?, ?, ?)", (name, telephone, salary, boss_id, department_id))
        flash(f'Added employee {name}', 'success')
    
    return render_template('add_employee.html', add_employee_form=add_employee_form)

@app.route('/addepartment', methods=['POST', 'GET'])
def add_department():
    add_department_form = AddDepartmentForm()
    
    if add_department_form.validate_on_submit():
        id = add_department_form.id.data
        name = add_department_form.name.data
        
        for department in get_departments():
            if id == department['id']:
                flash('ID already exists', 'danger')
                return redirect(url_for('add_department'))
        
        execute("INSERT INTO avdelning (avd_id, namn) VALUES (?, ?)", (id, name))
        flash(f'Created department {name}', 'success')
    
    return render_template('add_department.html', add_department_form=add_department_form)

def get_departments() -> list:
    departments = []
    for department in get_list("SELECT avd_id, namn FROM avdelning"):
        departments.append(create_department(id=department[0], name=department[1]))
    return departments