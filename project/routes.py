from flask import *
from project import db
from project.model import Student, SupplementaryExam
from project.forms import LoginForm, RegisterForm, SupplementaryExamForm
from flask_login import login_user, current_user, logout_user, login_required

admin = Blueprint('admin',__name__)

@admin.route('/')
def index():
    db.drop_all()
    db.create_all()
    return render_template('index.html')

@admin.route('/login', methods=['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(rollno = form.rollno.data).first()
        if student is not None and student.check_password(form.password.data) :
            flash('Logged in successfully.')
            login_user(student)
            return redirect(url_for('admin.dashboard', rollno=student.rollno))
        else:
            flash('User is not registered.')
            return render_template('login.html', form = form)
    return render_template('login.html', form=form)


@admin.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Student(
                name=form.name.data,
                rollno=form.rollno.data,
                branch=form.branch.data,
                official_email=form.official_email.data,
                password=form.password.data,
                )
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('admin.loginPage'))
    return render_template('register.html', form=form)

@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('admin.index'))

@admin.route('/user/<rollno>/dashboard')
@login_required
def dashboard(rollno):
    student = Student.query.filter_by(rollno=rollno).first_or_404()
    return render_template('dashboard.html', student=student)


@admin.route('/user/<rollno>/register_exam', methods=['GET', 'POST'])
@login_required
def registerExam(rollno):
    student = Student.query.filter_by(rollno=rollno).first_or_404()
    form = SupplementaryExamForm()
    if form.validate_on_submit():
        supplementary_exam = SupplementaryExam(
                                rollno=form.rollno.data,
                                name=form.name.data,
                                subject_code=form.subject_code.data,            
                                branch=form.branch.data,
                                )
        db.session.add(supplementary_exam)
        db.session.commit()
        flash('Thanks for registering for exam. Once your payment status is uploaded & detected you will be eligible to give the exam.')
        return redirect(url_for('admin.dashboard', rollno=rollno))
    return render_template('register_exam.html', form=form)
