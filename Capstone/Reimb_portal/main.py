from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
import config
from models import db, Employee, Department, Request
from forms import RegisterForm, LoginForm, ReimbursementForm
from seed_data import initialize_database
from logging_config import logger

# App setup
app = Flask(__name__)

# Load configuration
app.config.from_object(config.config["default"])

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# DB connection
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


# User loader function
@login_manager.user_loader
def load_user(emp_id):
    return Employee.query.get(int(emp_id))


# ROUTES TO WEBPAGES

@app.route("/")
def index():
    logger.info('Redirecting to login page')
    return redirect(url_for('login'))


def openDashBoard(user):
    logger.info(f'Opening dashboard for user: {user.email}, Role: {user.role}')
    if user.role == "ADMIN":
        return redirect(url_for('admin_dashboard', admin_id=user.emp_id))
    elif user.role == "MANAGER":
        return redirect(url_for('manager_dashboard', manager_id=user.emp_id))
    else:
        return redirect(url_for('employee_dashboard', employee_id=user.emp_id))

# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            try:
                user = Employee.query.filter_by(email=login_form.email.data).first()
                if user and user.check_password(login_form.password.data):
                    login_user(user)
                    session['user_email'] = user.email
                    flash(f"Logged in successfully! Welcome {user.first_name} {user.last_name}", "success")
                    logger.info(f'User {user.email} logged in successfully')
                    return openDashBoard(user=user)
                else:
                    flash('Invalid email or password!', 'error')
                    logger.warning(f'Invalid login attempt for email: {login_form.email.data}')
                    return redirect(url_for('login'))
            except Exception as e:
                logger.error(f'Error while logging in: {e}')
                return f'Error while logging in: {e}'
        else:
            flash('Enter a valid email!', 'error')
            logger.warning('Invalid email format submitted')
    
    logger.info(f'Login page rendered')
    return render_template('login.html', form=login_form)

@app.route("/logout")
@login_required
def logout():
    user_email = session.get('user_email')
    logout_user()
    if user_email:
        logger.info(f'User {user_email} logged out')
    session.pop('user_email', None)
    return redirect(url_for('login'))


# REGISTER PAGE
@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    # Collecting department choices
    departments = Department.query.all()
    register_form.department.choices += [(dept.dept_id, dept.name) for dept in departments]

    if request.method == "POST":
        if register_form.validate_on_submit():
            user = Employee.query.filter_by(email=register_form.email.data).all()
            if user:
                flash(f'Email id already exits!', 'error')
                logger.warning(f'Attempt to register with existing email: {register_form.email.data}')
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(register_form.password.data)

            new_user = Employee(
                first_name = register_form.first_name.data,
                last_name = register_form.last_name.data,
                email = register_form.email.data,
                password = hashed_password,
                contact_no = register_form.contact_no.data,
                department_id = register_form.department.data,
                role = 'MANAGER' if int(register_form.role.data)==2 else 'USER'
            )

            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please login.', 'success')
                logger.info(f'New user registered: {register_form.email.data}')
                return redirect(url_for('login'))
            except Exception as e:
                logger.error(f'Error while registering user: {e}')
                return f'Error while registering: {e}'
    logger.info(f'Register page rendered')
    return render_template('register.html', form=register_form)

def set_response_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# ADMIN DASHBOARD
@app.route("/admin_dashboard/<int:admin_id>", methods=["GET", "POST"])
@login_required
def admin_dashboard(admin_id:int):
    admin = load_user(admin_id)
    if admin.role != "ADMIN":
        flash('Not Authorised!','error')
        logger.warning(f'Unauthorized access attempt by user: {admin.email}')
        return redirect(url_for('login'))
    
    departments = Department.query.all()
    department_employees = []
    department_claims = []
    selected_department_id = None

    if request.method == "POST":
        selected_department_id = request.form.get("selected_department_id")
        action = request.form.get("action")

        if action == "delete_department" and selected_department_id:
            try:
                Department.query.filter_by(dept_id=selected_department_id).delete()
                db.session.commit()
                flash('Department deleted successfully!','success')
                logger.info(f'Department ID {selected_department_id} deleted successfully')
            except Exception as e:
                flash(f'Error while deleting department: {e}','error')
                logger.error(f'Error while deleting department ID {selected_department_id}: {e}')
            return redirect(url_for('admin_dashboard', admin_id=admin_id))
        elif action == "add_department":
            new_department_name = request.form.get("new_department_name")
            if new_department_name:
                new_department = Department(name=new_department_name)
                try:
                    db.session.add(new_department)
                    db.session.commit()
                    flash('Department added successfully!','success')
                    logger.info(f'Department {new_department_name} added successfully')
                except Exception as e:
                    flash(f'Error while adding new department: {e}','error')
                    logger.error(f'Error while adding new department {new_department_name}: {e}')
            return redirect(url_for('admin_dashboard', admin_id=admin_id))
        else:
            if selected_department_id:
                department_claims = (
                    db.session.query(Request, Employee)
                    .join(Employee, Employee.emp_id == Request.emp_id)
                    .filter(Employee.department_id == selected_department_id)
                    .all())
                department_employees = Employee.query.filter_by(department_id=selected_department_id).all()
    
    claims_with_managers = []
    for claim, employee in department_claims:
        manager = Employee.query.get(claim.manager_id)
        claims_with_managers.append((claim, employee, manager))

    response = make_response(render_template('admin_dashboard.html', admin_id=admin_id, user=admin, departments=departments,
                           employees=department_employees, claims=claims_with_managers,
                           selected_department_id=selected_department_id))
    
    response = set_response_header(response)
    logger.info(f'Admin dashboard rendered for Admin ID {admin_id}')
    return response


@app.route("/admin_dashboard/<int:admin_id>/delete_employee/<int:employee_id>", methods=["POST"])
@login_required
def delete_employee(admin_id: int, employee_id: int):
    employee = Employee.query.get(employee_id)
    selected_department_id = request.form.get("selected_department_id")
    if employee:
        try:
            db.session.delete(employee)
            db.session.commit()
            flash(f'Employee ID: {employee_id} deleted!', 'error')
            logger.info(f'Employee ID {employee_id} deleted successfully')
        except Exception as e:
            flash(f'Error while deleting employee: {e}', 'error')
            logger.error(f'Error while deleting employee ID {employee_id}: {e}')
    else:
        flash('Employee not found.', 'error')
        logger.warning(f'Attempt to delete non-existing employee ID: {employee_id}')
    return redirect(url_for('admin_dashboard', admin_id=admin_id, selected_department_id=selected_department_id))


# @app.route("/admin_dashboard/<int:admin_id>/distribute_managers/<int:dept_id>", methods=["POST"])
# @login_required
# def distribute_managers(admin_id: int, dept_id: int):
#     pending_department_claims = Request.query.filter_by(status='PENDING').all()
#     department_managers = Employee.query.filter_by(department_id=dept_id).filter_by(role='MANAGER').all()
#     claims_count = len(pending_department_claims)
#     managers_count = len(department_managers)
#     claims_per_manager = claims_count//managers_count


@app.route("/admin_dashboard/<int:admin_id>/assign_manager/<int:req_id>", methods=["POST"])
@login_required
def assign_manager(admin_id: int, req_id: int):
    claim = Request.query.get(req_id)
    manager_id = request.form.get("manager")
    selected_department_id = request.form.get("selected_department_id")
    if claim and manager_id:
        try:
            claim.manager_id = manager_id
            db.session.commit()
            flash(f'Assigned Manager to the claim request id: {req_id}', 'success')
            logger.info(f'Manager ID {manager_id} assigned to request ID {req_id}')
        except Exception as e:
            flash(f'Error while assigning manager: {e}', 'error')
            logger.error(f'Error while assigning manager ID {manager_id} to request ID {req_id}: {e}')

    return redirect(url_for('admin_dashboard', admin_id=admin_id, selected_department_id=selected_department_id))


@app.route("/admin_dashboard/<int:user_id>/approve_reject_claim/<int:req_id>", methods=["POST"])
@app.route("/manager_dashboard/<int:user_id>/approve_reject_claim/<int:req_id>", methods=["POST"])
@login_required
def approve_reject_claim(user_id: int, req_id: int):
    current_user = load_user(user_id)
    claim = Request.query.get(req_id)
    action = request.form.get("action")
    if claim:
        if current_user.role == 'ADMIN' or current_user.emp_id == claim.manager_id:
            comments = request.form["comments"]
            if action == "approve_claim":
                try:
                    claim.status = "APPROVED"
                    claim.comments = comments
                    db.session.commit()
                    flash(f'Request ID: {req_id} Approved!', 'success')
                    logger.info(f'Request ID {req_id} approved by Admin ID {user_id}')
                except Exception as e:
                    flash(f'Error while approving claim: {e}', 'error')
                    logger.error(f'Error while approving request ID {req_id} by Manager ID {user_id}: {e}')
            else:
                if comments:
                    try:
                        claim.status = "REJECTED"
                        claim.comments = request.form["comments"]
                        db.session.commit()
                        flash(f'Request ID: {req_id} Rejected!', 'error')
                        logger.info(f'Request ID {req_id} rejected by Admin ID {user_id}')
                    except Exception as e:
                        flash(f'Error while rejecting claim: {e}', 'error')
                        logger.error(f'Error while rejecting request ID {req_id} by Manager ID {user_id}: {e}')
                flash('Provide comments for rejection','error')
        else:
            flash('You do not have permission to perform this action.', 'error')
    else:
        flash('Request not found.', 'error')

    if current_user.role == 'ADMIN':
        return redirect(url_for('admin_dashboard', admin_id=user_id))
    elif current_user.role == 'MANAGER':
        return redirect(url_for('manager_dashboard', manager_id=user_id))

# MANAGER DASHBOARD
@app.route('/manager_dashboard/<int:manager_id>')
@login_required
def manager_dashboard(manager_id):
    manager = Employee.query.get(manager_id)
    if manager.role != "MANAGER":
        flash('Not Authorised!','error')
        logger.warning(f'Unauthorized access attempt by user: {manager.email}')
        return redirect(url_for('login'))
    try:
        manager_requests = Request.query.filter_by(emp_id=manager_id).all()
        employee_requests = (
            db.session.query(Request, Employee)
            .join(Employee, Employee.emp_id == Request.emp_id)
            .filter(Request.manager_id == manager_id)
            .all()
            )
        logger.info(f'Fetched claims for manager ID {manager_id}')
    except Exception as e:
        logger.error(f'Error while fetching claims for manager ID {manager_id}: {e}')
        return f'Error while fetching claims: {e}'
    
    claims_with_employee_details = []
    for claim, employee in employee_requests:
        claims_with_employee_details.append((claim, employee))
    
    response = make_response(render_template('manager_dashboard.html', manager_id=manager_id, user=manager, my_claims = manager_requests, claims=claims_with_employee_details))

    response = set_response_header(response)

    logger.info(f'Manager dashboard rendered for manager ID {manager_id}')        
    return response


# EMPLOYEE DASHBOARD
@app.route('/employee_dashboard/<int:employee_id>')
@login_required
def employee_dashboard(employee_id):
    employee = Employee.query.get(employee_id)
    employee_requests = Request.query.filter_by(emp_id=employee_id).all()

    response = make_response(render_template('employee_dashboard.html', employee_id=employee_id, user=employee, my_claims=employee_requests))
    
    response = set_response_header(response)

    logger.info(f'Employee dashboard rendered for employee ID {employee_id}')        
    return response


def max_claim_amount(expense_type) -> int:
    if expense_type=="Travelling":
        return 15000
    elif expense_type=="Relocation":
        return 20000
    else:
        return 5000


# REIMBURSEMENT SUBMISSION PAGE
@app.route("/dashboard/<int:user_id>/submitreimbursement", methods=["GET", "POST"])
@login_required
def submit_reimbursement(user_id):
    user = load_user(user_id)
    form = ReimbursementForm()

    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            amount = form.amount.data
            expense_type = form.expense_type.data
            receipt = form.receipt.data

            if not email == user.email:
                flash('Invalid email! Please enter your email.', 'error')
                logger.warning(f'Invalid email submitted for reimbursement: {email}')
                return redirect(url_for('submit_reimbursement', user_id=user_id))

            upper_limit = max_claim_amount(expense_type)
            if amount > upper_limit:
                flash(f'Amount exceeds upper limit {upper_limit} for {expense_type}')
                logger.warning(f'Amount {amount} exceeds upper limit {upper_limit} for expense type {expense_type}')
                return redirect(url_for('submit_reimbursement', user_id=user_id))

            filename = None
            
            # Assuming there is an admin added in DB
            admin = Employee.query.filter_by(role="ADMIN").first()

            new_request = Request(
                emp_id=user_id,
                amount=amount,
                expense_type=expense_type,
                manager_id=admin.emp_id,
                proof=filename
            )

            try:
                db.session.add(new_request)
                db.session.commit()
                logger.info(f'New reimbursement request submitted by user ID {user_id}')

                if receipt:
                    req_id = new_request.req_id

                    # Generating unique filename with req_id and employee_id
                    filename = secure_filename(receipt.filename)
                    unique_filename = f'{user_id}_{req_id}_{filename}'

                    # Saving the receipt with new filename
                    receipt.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
                    
                    new_request.proof = unique_filename

                    db.session.commit()
                    logger.info(f'Receipt saved for request ID {req_id} by user ID {user_id}')

                flash('Reimbursement request submitted successfully!', 'success')
                if user.role == "MANAGER":
                    return redirect(url_for('manager_dashboard', manager_id=user_id))
                else:
                    return redirect(url_for('employee_dashboard', employee_id=user_id))

            except Exception as e:
                logger.error(f'Error while submitting reimbursement request for user ID {user_id}: {e}')
                return f'Error while submitting request: {e}'
        
    return render_template('submit_reimbursement.html', user_id=user_id, user=user, form=form)


# Function to assign initial admin
# def assignAdmin():
#     try:
#         if not Employee.query.filter_by(role='ADMIN').first():
#             hashed_password = generate_password_hash(config.admin_password)
#             admin = Employee(
#                 first_name="Admin",
#                 last_name="User",
#                 email="admin@nucleusteq.com",
#                 password=hashed_password,
#                 role="ADMIN"
#             )
#             db.session.add(admin)
#             db.session.commit()
#     except Exception as e:
#         print(f'Error while assigning Admin!')

# def addDepartments():
#     try:
#         if not Department.query.all():
#             IT_dept = Department(name="IT")
#             Sales_dept = Department(name="Sales")
#             HR_dept = Department(name="HR")

#             db.session.add(IT_dept)
#             db.session.add(Sales_dept)
#             db.session.add(HR_dept)

#             db.session.commit() 
#     except Exception as e:
#         print(f'Error while adding initial Departments!')


if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        initialize_database(app)
        logger.info('Reimbursement Database initialized')
    app.run()