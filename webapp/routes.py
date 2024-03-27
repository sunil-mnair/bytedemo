import os,json,markdown,requests
import os.path as op

from webapp import app,project_dir
from webapp import bcrypt
from webapp import custom_data

from webapp.forms import *
from webapp.models import *
from webapp.login import *
from webapp.mail import *
from webapp.fun_apps import *

# from webapp.data_processing import predict_with_ml
from webapp import qrcode

from flask_admin import Admin
from flask_login import login_required, login_user,logout_user
from flask import render_template,request, redirect,url_for,Response,jsonify,flash,send_file,session

from werkzeug.utils import secure_filename

# from werkzeug.security import generate_password_hash, check_password_hash

# from sqlalchemy.inspection import inspect
from sqlalchemy import extract,func,desc

# Enable File Upload in Admin
from flask_admin.contrib.fileadmin import FileAdmin

from flask_mail import Message

from bs4 import BeautifulSoup

# import urllib library 
from urllib.request import urlopen 

if 'home' in project_dir:
    project_dir += '/mysite'

def get_quiz():

    quiz_json = urlopen('https://raw.githubusercontent.com/sunil-mnair/curriculum/master/json/quiz.json') 
    quizapp = json.loads(quiz_json.read()) 

    return quizapp

def get_survey():
    survey_json = urlopen('https://raw.githubusercontent.com/sunil-mnair/curriculum/master/json/survey.json') 
    surveyapp = json.loads(survey_json.read())
    return surveyapp

countries_json = urlopen('https://raw.githubusercontent.com/sunil-mnair/curriculum/master/json/countries.json') 
countries = json.loads(countries_json.read())

complaints_json = urlopen('https://raw.githubusercontent.com/sunil-mnair/curriculum/master/json/complaint.json') 
complaints = json.loads(complaints_json.read())



# Generates a Quiz Link if a quiz exists for the course
def quiz_exists(cname):

    quiz_link = False
    try:
        get_quiz()[cname]
    except:
        pass
    else:
        quiz_link = True

    return quiz_link

# To know if all the responses have been gathered
def get_quiz_responses(course):
     # Select all Quiz Responses

    year = datetime.now(uae).year
    month = datetime.now(uae).month
    day = datetime.now(uae).day
    
    quiz_responses = db.session.query(QuizResults.response,QuizMaster.question)\
                .filter(Student.studentName == session["student"],\
                    QuizResults.student_id == Student.id,\
                    QuizResults.course_id == course.id,\
                    QuizMaster.id == QuizResults.question_id,\
                    extract('year', QuizResults.created_dt) == year,\
                    extract('month', QuizResults.created_dt) == month,\
                    extract('day', QuizResults.created_dt) == day).all()
    
    return quiz_responses

# To know if all the responses have been gathered
def get_survey_responses(course):
     # Select all Survey Responses

    year = datetime.now(uae).year
    month = datetime.now(uae).month
    day = datetime.now(uae).day
    
    survey_responses = db.session.query(SurveyMaster.question)\
                .distinct(SurveyResults.question_id,SurveyResults.student_id)\
                .filter(Student.studentName == session["student"],\
                    SurveyResults.student_id == Student.id,\
                    SurveyResults.course_id == course.id,\
                    SurveyMaster.id == SurveyResults.question_id,\
                    extract('year', SurveyResults.created_dt) == year,\
                    extract('month', SurveyResults.created_dt) == month,\
                    extract('day', SurveyResults.created_dt) == day).all()
    
    return survey_responses



@app.route('/admin/extract_lessons')
def extract_lessons():
    lessons = list()

    if request.args.get('q'):
        course_id = int(request.args.get('q'))

        lesson_ = db.session.query(Lesson).\
            filter(Lesson.courseId == course_id).\
                order_by(Lesson.lessonOrder).all()


        for lesson in lesson_:

            lessons.append(
                {
                            "id":lesson.id,
                            "lessonName":lesson.lessonName,
                            "lessonOrder":lesson.lessonOrder
                })

    return jsonify(lessons = lessons)



@login_manager.user_loader
def load_user(user_id):
# since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

admin = Admin(app,index_view=MainAdminIndexView(),template_mode='bootstrap3')
admin.add_view(AllModelView(User,db.session,category="Students"))
admin.add_view(StudentView(Student,db.session,category="Students"))
admin.add_view(QuizResultsView(QuizResults,db.session,category="Students"))
admin.add_view(SurveyResultsView(SurveyResults,db.session,category="Students"))

admin.add_view(CourseView(Course,db.session,category="Course"))
admin.add_view(LessonView(Lesson,db.session,category="Course"))
admin.add_view(AllModelView(UserCourse,db.session,category="Course"))

admin.add_view(AllModelView(Activity,db.session))

# Add a Custom Page to Admin
# admin.add_view(LessonOrderView(name='Lesson Order', endpoint='lesson_order',category="Course"))

path = op.join(op.dirname(__file__), 'static')
admin.add_view(FileAdmin(path, '/static/images/', name='Images'))


@app.template_filter()
def duration(x):
    x = x.seconds
    return f'{x//60} min {x%60} secs'

@app.template_filter()
def dateformat(x):
    x = x.strftime("%d-%b-%Y %H:%M")
    return x


# Beginning of Routes

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

@app.route("/countries")
def get_countries():
    country = request.args.get("country")
    capital = None

    if country:
        country = country.title()
        if [c for c in countries if c["name"]==country]:
            #return jsonify([c for c in countries if c["name"]==country][0])
            return render_template('country_data.html',country=[c for c in countries if c["name"]==country][0])

        else:
            return jsonify([{'country':country,'capital':capital}][0])
    else:
        return jsonify(countries)


@app.route("/complaints")
def get_complaint():
    return jsonify(complaints)


@app.route('/login',methods=['GET','POST'])
def login():

    title = "Login"

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        # check_password is a method inside the User class in models.py
        if not user or not user.check_password(attempted_password=form.password.data):
            flash('Username/Password is incorrect',"warning")
            return redirect(url_for('login')) # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user,remember=form.remember.data)
        return redirect(url_for('index'))

    return render_template('login.html',title = title,form=form,logo=custom_data["logo"])

@app.route('/signup',methods=['GET','POST'])
def signup():
    title = "Sign Up"
    form = SignupForm()

    if form.validate_on_submit():

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(username=form.username.data, 
                        password_check=form.password.data)
        # Refers to models.py to understand password_check usage

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash("Successfully registered, kindly Login","success")
        # code to validate and add user to database goes here
        return redirect(url_for('login'))
    
    return render_template('signup.html',form=form,logo=custom_data["logo"])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out","info")
    return redirect(url_for('index'))


@app.route('/',methods=['GET','POST'])
@login_required
def index():

    if "student" not in session:
        return redirect(url_for('register_student',logo=custom_data["logo"]))
    
    else:
        student = db.session.query(Student).filter(Student.studentName == session['student']).first()

    # questionnaire = db.session.query(Questionnaire).\
    #         filter(Questionnaire.studentId == student.id).all()
    
    # if not questionnaire:
    #     return redirect(url_for('questionnaire'))

    courses = db.session.query(Course).\
            filter(UserCourse.userId == current_user.id,\
                Course.id == UserCourse.courseId).all()


    return render_template("courses.html",
    courses = courses,
    logo=custom_data["logo"],
    title=custom_data["page_title"])

@app.route('/register',methods=['GET','POST'])
def register_student():
    form = RegisterForm()

    if form.validate_on_submit():
        
        def name_check(x):
            if any(chr.isdigit() for chr in x):
                flash("Please provide your correct name","danger")
                return False

            return x.strip().title()

        if name_check(request.form["fullname"]):
            session["student"] = name_check(request.form["fullname"])
        else:
            
            return redirect(url_for('register_student'))
        
        # Add New Student to Database
        check_student = db.session.query(Student).\
            filter(Student.studentName == session["student"]).all()

        if not check_student:
            student = Student()
            student.studentName = session["student"]
            student.profession = request.form["position"]
            student.department = request.form["department"]

            db.session.add(student)
            db.session.commit()
        else:
            return redirect(url_for('index'))

    # Can show the errors if any
    if form.errors:
        for err in form.errors.values():
            flash(err,category="danger")
    
    return render_template("register.html",form=form,logo=custom_data["logo"])


@app.route('/course/<int:id>',methods=['GET','POST'])
@login_required
def course(id):

    session["course"] = id

    course = Course.query.get_or_404(id)

    html = markdown.markdown(course.courseDescription)

    lessons = db.session.query(Lesson)\
        .join(Course, Course.id == Lesson.courseId)\
        .filter(Course.id == id)\
        .order_by(Lesson.lessonOrder).all()

    

    return render_template("course.html",
    lessons = lessons, course = course,
    html = html,
    quiz_link = quiz_exists(course.courseName),
    logo=custom_data["logo"],
    title = course.courseName)


@app.route('/view_lesson/<int:id>',methods=['GET','POST'])
@login_required
def viewlesson(id):

    lesson = Lesson.query.get_or_404(id)
    course = Course.query.get_or_404(lesson.courseId)
    # courseid = lesson.courseId

    lessons = db.session.query(Lesson)\
        .join(Course, Course.id == Lesson.courseId)\
        .filter(Course.id == course.id)\
        .order_by(Lesson.lessonOrder).all()
    
    soup = BeautifulSoup(lesson.lessonDescription, 'html.parser')

    # Find all h2 headings for ToC
    h2s = [h2.text.strip() for h2 in soup.find_all('h2')]
        

    session["lessonNM"] = lesson.lessonName

    html = markdown.markdown(lesson.lessonDescription)

    return render_template("view_lesson.html",
    course = course, lesson = lesson,lessons = lessons,html = html,
    h2s=h2s,
    quiz_link=quiz_exists(course.courseName),
    title = lesson.lessonName,
    logo=custom_data["logo"])


@app.route('/lesson_order/',methods=['GET','POST'])
@login_required
def lesson_order():
    if current_user.username == 'sunil.nair':
        courses = db.session.query(Course).all()


        if request.method == 'POST':
            lesson_dict = request.form
            for x in list(request.form):
                lesson = Lesson.query.filter(Lesson.id == int(x)).first()
                lesson.lessonOrder = int(lesson_dict.getlist(x)[0])

                db.session.commit()

            return redirect(url_for('lesson_order'))
        return render_template('lesson_order.html',courses = courses)

    else:
        return redirect(url_for('index'))
    

@app.route('/quiz_results',methods=['GET','POST'])
@login_required
def quiz_results():

    # Format - quiz_results?date=14224&course=13

    date = request.args.get('date')
    c_id = request.args.get('course')

    course = Course.query.get_or_404(int(c_id))

    today = datetime.now(uae)

    if date:
        today = datetime.strptime(date,"%d%m%y")
        #today = datetime.now(uae)-timedelta(days=day)

    year = today.year
    month = today.month
    day = today.day

    quiz_results = db.session.query(Student.studentName,\
    func.sum(QuizResults.response).label('score'),\
    func.count(QuizResults.response).label('questions'),\
    func.min(QuizResults.created_dt).label('start_time'),\
    func.max(QuizResults.created_dt).label('end_time'))\
                .filter(QuizResults.student_id == Student.id,\
                    extract('year', QuizResults.created_dt) == year,\
                    extract('month', QuizResults.created_dt) == month,\
                    extract('day', QuizResults.created_dt) == day,\
                    Student.studentName != 'Demo')\
                 .order_by(desc(func.sum(QuizResults.response)))\
                 .group_by(Student.studentName).all()
    

    return render_template("quiz/quiz_results.html",
                           quiz_results = quiz_results,
                           logo='/static/images/company_logo.png',
                           today=today,
                           title = custom_data["page_title"])


@app.route('/select_quiz',methods=['GET','POST'])
@login_required
def select_quiz():
    user_id = current_user.id
    courses = db.session.query(Course).\
        filter(Course.id == UserCourse.courseId,\
            UserCourse.userId == user_id).all()

    # Display only those courses which have a quiz in the json file
    courses = [course for course in courses if course.courseName in list(get_quiz().keys())]

    if request.method == 'POST':
        session["course"] = int(request.form["selected_course"])

        return redirect(url_for('quiz'))

    return render_template('quiz/select_quiz.html',
                           courses = courses,
                           title = custom_data["page_title"])

@app.route('/select_survey',methods=['GET','POST'])
@login_required
def select_survey():
    user_id = current_user.id
    courses = db.session.query(Course).\
        filter(Course.id == UserCourse.courseId,\
            UserCourse.userId == user_id).all()

    # Display only those courses which have a quiz in the json file
    courses = [course for course in courses if course.courseName in list(get_survey().keys())]

    if request.method == 'POST':
        session["course"] = int(request.form["selected_course"])

        return redirect(url_for('survey'))

    return render_template('quiz/select_survey.html',
                           courses = courses,
                           title = custom_data["page_title"])






@app.route('/quiz',methods=['GET','POST'])
@login_required
def quiz():
    course = Course.query.get_or_404(session["course"])

    check = ''
    quiz_responses = ''
    percentage = float()

    # Stores all questions, choice and correct answer
    # we use index[0] to extract the list from the dictionary
    session["quiz"] = [{theme:questions} for (theme,questions) in get_quiz().items() if theme == course.courseName][0]

    # Stores Question Count of Quiz
    session["total_quiz"] = len(session["quiz"][course.courseName])

    # Get Quiz Responses
    quiz_responses = get_quiz_responses(course)

    # If all the quiz responses have been posted, forward to results
    if session["total_quiz"] == len(quiz_responses):
        return render_template("quiz/end_quiz.html",
                               quiz_responses = quiz_responses,
                               logo=custom_data["logo"])

    if request.method == 'POST':
        quiz_answer = request.form["given_answer"]
        check = db.session.query(QuizResults)\
                .filter(Student.studentName == session["student"],\
                    QuizResults.student_id == Student.id,\
                    QuizResults.question_id == QuizMaster.id,\
                    QuizMaster.question == session["current_quiz"]["question"],\
                    QuizResults.course_id == course.id).all()

        if check:
            flash("Your Response for the previous question was already recorded. The quiz does not accept multiple submissions","info")
        else:
            quiz_response = QuizResults()

            extract_student = db.session.query(Student).\
            filter(Student.studentName == session["student"]).all()[0]


            quiz_response.student_id = extract_student.id
            quiz_response.course_id = course.id
            quiz_response.created_dt = datetime.now(uae)

            extract_question = db.session.query(QuizMaster).\
            filter(QuizMaster.question == session["current_quiz"]["question"]).all()[0]

            quiz_response.question_id = extract_question.id

            if quiz_answer == session['current_quiz']['answer']:
                message =f"Correct!! {session['current_quiz']['explanation']}"
                flash(message,"success")

                quiz_response.response = 1

            else:
                message =f"Wrong!! The Correct answer was {session['current_quiz']['answer']}. {session['current_quiz']['explanation']}"
                flash(message,"danger")
                quiz_response.response = 0


            question_stats = db.session.query(QuizResults.question_id,\
            func.sum(QuizResults.response).label('correct'),\
            func.count(QuizResults.response).label('total'))\
                        .filter(QuizResults.question_id == QuizMaster.id,\
                        QuizMaster.question == session['current_quiz']['question'])\
                 .group_by(QuizResults.question_id).all()

            if question_stats:
                question_stats = question_stats[0]
                percentage = round((question_stats[1]/question_stats[2])*100,2)

            db.session.add(quiz_response)
            db.session.commit()

        # Proceed to Next Question

        # if question id number is less than total number of questions
        if session["current_quiz"]["id"] < session["total_quiz"]:
            # for the current course use the question id as the index, this will fetch the next question
            session["current_quiz"] = [game for game in session["quiz"][course.courseName]][session["current_quiz"]["id"]]
        else:
            quiz_responses = get_quiz_responses(course)
            return render_template("quiz/end_quiz.html",quiz_responses = quiz_responses,
                                   logo=custom_data["logo"])

    else:
        session["current_quiz"] = [game for game in session["quiz"][course.courseName]][0]


    return render_template("quiz/start_quiz.html",quiz_responses = quiz_responses,
    check=check,logo=custom_data["logo"],percentage=percentage)

@app.route('/survey',methods=['GET','POST'])
@login_required
def survey():
    course = Course.query.get_or_404(session["course"])

    check = ''
    survey_responses = ''

    # Stores all questions, choice and correct answer
    # we use index[0] to extract the list from the dictionary
    session["survey"] = [{theme:questions} for (theme,questions) in get_survey().items() if theme == course.courseName][0]

    # Stores Question Count of Quiz
    session["total_survey"] = len(session["survey"][course.courseName])

    # Get Quiz Responses
    survey_responses = get_survey_responses(course)
    print(survey_responses)

    # If all the quiz responses have been posted, forward to results
    if session["total_survey"] == len(survey_responses):
        return render_template("quiz/end_survey.html",
                               survey_responses = survey_responses,
                               logo=custom_data["logo"])

    if request.method == 'POST':
        print(session["current_survey"])
        survey_answers = request.form.getlist('selected_choice')
        
        check = db.session.query(SurveyResults)\
                .filter(Student.studentName == session["student"],\
                    SurveyResults.student_id == Student.id,\
                    SurveyResults.question_id == SurveyMaster.id,\
                    SurveyMaster.question == session["current_survey"]["question"],\
                    SurveyResults.course_id == course.id).all()

        if check:
            flash("Your Response for the previous question was already recorded.","info")
        else:

            extract_student = db.session.query(Student).\
                filter(Student.studentName == session["student"]).all()[0]

            extract_question = db.session.query(SurveyMaster).\
                filter(SurveyMaster.question == session["current_survey"]["question"]).all()[0]

            
            
            for choice in survey_answers:
                survey_response = SurveyResults()
                survey_response.student_id = extract_student.id
                survey_response.course_id = course.id
                survey_response.created_dt = datetime.now(uae)
                survey_response.question_id = extract_question.id
                survey_response.response = choice
                
                db.session.add(survey_response)
                db.session.commit()
            
            flash("Your submission was recieved","info")

        # Proceed to Next Question

        # if question id number is less than total number of questions
        if session["current_survey"]["id"] < session["total_survey"]:
            # for the current course use the question id as the index, this will fetch the next question
            session["current_survey"] = [game for game in session["survey"][course.courseName]][session["current_survey"]["id"]]
        else:
            survey_responses = get_survey_responses(course)
            return render_template("quiz/end_survey.html",survey_responses = survey_responses,
                                   logo=custom_data["logo"])

    else:
        session["current_survey"] = [game for game in session["survey"][course.courseName]][0]
        # session["current_survey"] = session["survey"]


    return render_template("quiz/start_survey.html",
                           survey_responses = survey_responses,
    check=check,logo=custom_data["logo"])

@app.route('/survey_results',methods=['GET','POST'])
@login_required
def survey_results():

    # Format - quiz_results?date=14224&course=13

    date = request.args.get('date')
    c_id = request.args.get('course')

    course = Course.query.get_or_404(int(c_id))

    today = datetime.now(uae)

    if date:
        today = datetime.strptime(date,"%d%m%y")
        #today = datetime.now(uae)-timedelta(days=day)

    year = today.year
    month = today.month
    day = today.day

    survey_results = db.session.query(SurveyMaster.question,SurveyResults.response,\
    func.count(SurveyResults.response).label('questions'))\
                .filter(SurveyMaster.id == SurveyResults.question_id,\
                    extract('year', SurveyResults.created_dt) == year,\
                    extract('month', SurveyResults.created_dt) == month,\
                    extract('day', SurveyResults.created_dt) == day)\
                 .order_by(SurveyMaster.id)\
                 .group_by(SurveyResults.response).all()

    sr = {}
    for s in survey_results:
        if not s[0] in sr:
            sr[s[0]] = [(s[1],s[2])]
        else:
            sr[s[0]].append((s[1],s[2]))
    
    print(sr)

    return render_template("quiz/survey_results.html",
                           sr = sr,
                           logo='/static/images/company_logo.png',
                           today=today,
                           title = custom_data["page_title"])


@app.route('/quiz_survey_process')
@login_required
def quiz_survey_process():

    # Quiz Process
    quiz_collection = [[s['question'] for s in q] for (theme,q) in get_quiz().items()]
    quiz_counter = 0
    for q in quiz_collection:
        for question in q:
            search_question = db.session.query(QuizMaster).\
                filter(QuizMaster.question == question).all()
            if not search_question:
                quiz_counter += 1
                quiz_master = QuizMaster()
                quiz_master.question = question

                db.session.add(quiz_master)
                db.session.commit()

    # Survey Process
    survey_collection = [[s['question'] for s in q] for (theme,q) in get_survey().items()]
    survey_counter = 0
    for q in survey_collection:
        for question in q:
            search_question = db.session.query(SurveyMaster).\
                filter(SurveyMaster.question == question).all()
            if not search_question:
                survey_counter += 1
                survey_master = SurveyMaster()
                survey_master.question = question

                db.session.add(survey_master)
                db.session.commit()
    

    return f"""{quiz_counter} questions added to Quiz master and {survey_counter} questions were added to Survey Master"""


@app.route('/activities',methods=['GET','POST'])
@login_required
def activity():

    activity = Activity.query.all()

    return render_template("activities.html", activity = activity,logo=custom_data["logo"],title=custom_data["page_title"])


@app.route("/qr_code_generator",methods=["GET", "POST"])
def qr_code_app():


    if request.method == "POST":
        getURL = request.form["url"]
        print(getURL)
        #getURL = request.args.get("data", "")
        #return send_file(qrcode(getURL, mode="raw"), mimetype="image/png")
        return render_template("qr_code_generator.html",getURL=getURL)


    return render_template("qr_code_generator.html")


@app.template_filter()
def greeting(name):

    if datetime.now().hour >= 24:
        return f'Good Morning {name}'
    if datetime.now().hour >= 12:
        return f'Good Afternoon {name}'
    elif datetime.now().hour >= 16:
        return f'Good Evening {name}'

@app.template_filter()
def pluralize(number):
    if int(number) <= 1:
        return 'min.'
    else:
        return 'mins'

@app.route("/feedback",methods=['GET','POST'])
def feedback():
    if "student" not in session:
        print("Student not in session")
        return render_template("register.html")

    if request.method == "POST":
        feedback_dict = request.form
        feedback_list = []
        print(feedback_dict)
        for x in list(request.form):
            feedback_list.append(feedback_dict.getlist(x))

        print(feedback_list)

        # Update Student Table
        student = Student.query.filter_by(studentName = session["student"]).first()
        student.company = feedback_list[0][0]
        student.profession = feedback_list[1][0]

        db.session.commit()

        # Add Entry to Feedback Rating
        rating = FeedbackRating()
        rating.student_id = student.id
        rating.rating = int(feedback_list[2][0])
        rating.objective = int(feedback_list[5][0])
        rating.comments = feedback_list[6][0]

        db.session.add(rating)
        db.session.commit()

        # Add Entry to Likes
        for like in feedback_list[3]:
            likes = FeedbackFeatureOutcome()
            likes.student_id = student.id
            likes.feature_id = int(like)
            likes.outcome = 1

            db.session.add(likes)
            db.session.commit()

        # Add Entry to Likes
        for dislike in feedback_list[4]:
            dislikes = FeedbackFeatureOutcome()
            dislikes.student_id = student.id
            dislikes.feature_id = int(dislike)
            dislikes.outcome = 0

            db.session.add(dislikes)
            db.session.commit()

        flash(f"Thank you {current_user.username}. Your response have been recorded","success")

        return redirect(url_for('feedback_results'))

    return render_template("feedback.html")

@app.route("/feedback_results",methods=['GET','POST'])
def feedback_results():

    ratings = db.session.query(FeedbackRating.rating,
        func.count(FeedbackRating.rating).label('rating'))\
        .group_by(FeedbackRating.rating).all()

    total_ratings = sum([r[1] for r in ratings])

    objs = db.session.query(FeedbackRating.objective,
        func.count(FeedbackRating.objective).label('objective'))\
        .group_by(FeedbackRating.objective).all()

    total_objs = sum([o[1] for o in objs])

    comments = db.session.query(FeedbackRating.comments)\
        .filter(func.char_length(FeedbackRating.comments)>=25)\
        .order_by(desc(FeedbackRating.id)).limit(10).all()


    likes = db.session.query(FeedbackFeatureOutcome.feature_id,FeedbackFeature.feature,\
        func.count(FeedbackFeatureOutcome.feature_id).label('feature'))\
        .filter(FeedbackFeatureOutcome.feature_id == FeedbackFeature.id,\
        FeedbackFeatureOutcome.outcome == 1)\
        .group_by(FeedbackFeatureOutcome.feature_id)\
        .order_by(desc(func.count(FeedbackFeatureOutcome.feature_id))).all()

    total_likes = sum([l[2] for l in likes])

    dislikes = db.session.query(FeedbackFeatureOutcome.feature_id,FeedbackFeature.feature,\
        func.count(FeedbackFeatureOutcome.feature_id).label('feature'))\
        .filter(FeedbackFeatureOutcome.feature_id == FeedbackFeature.id,\
        FeedbackFeatureOutcome.outcome == 0)\
        .group_by(FeedbackFeatureOutcome.feature_id)\
        .order_by(desc(func.count(FeedbackFeatureOutcome.feature_id))).all()

    total_dislikes = sum([l[2] for l in dislikes])

    return render_template("feedback_results.html",
    likes=likes,total_likes=total_likes,objs=objs,
    dislikes=dislikes,total_dislikes=total_dislikes,
    ratings=ratings,total_ratings=total_ratings,total_objs=total_objs,
    comments=comments)



@app.route("/word_cookies_cheat",methods=["GET", "POST"])
def word_cookies_cheat():
    errors = ""
    result = ""
    letters = ""

    with app.open_resource('static/english_words.txt') as file:
        wordlist = [x.strip() for x in file.readlines()]

    if request.method == "POST":
        if request.form["letters"] is not None:
            letters = request.form["letters"]
            result = find_words(letters,wordlist)
        else:
            errors += f'Please Enter Letters'

    return render_template("word_cookies_cheat.html",solution=result, error_msg=errors)

@app.route("/moon_phase_calculator",methods=["GET", "POST"])
def moon_phase_calculator_func():
    errors = ""
    result = ""
    next_full = ""
    next_new = ""

    next_full = nextphasefm()
    next_new = nextphasenm()


    if request.method == "POST":
        selecteddate = request.form["date"]

        if selecteddate !='':
            result = specificdate(selecteddate)
        else:
            errors += f'Please select a Date'

    return render_template("moon_phase_calculator.html",moonphase=result,nextfull=next_full, nextnew = next_new, error_msg=errors)

@app.route("/typoglycemia",methods=["GET","POST"])
def can_still_read():
    errors = ""
    sentence = None
    result=''
    if request.method == "POST":
        if request.form["sentence"] is not None:
            try:
                sentence = request.form["sentence"]
                result = jumble(sentence)
            except:
                errors += f'Please type a sentence'
        else:
            errors += f'Please type a sentence'

    return render_template("typoglycemia.html",title="Can you read this?",s=result, error_msg=errors)



@app.route("/editor",methods=["GET","POST"])
def editor():
    return render_template("editor.html")

@app.route("/credentials")
def credentials():
    return render_template("credentials.html",logo=custom_data["logo"])

@app.route("/instructor")
def instructor():

    # response = requests.get("https://www.bytesizetrainings.com/sn_clients")

    clients = ["emirates_nbd.png","asyad.png","ministry_of_education_ethiopia.png","das_holding.png","royal_sun_alliance.png","etisalat.png","icbc.png","dubai insurance.png","ecc.png","asm_global.png","network_international.png","dwtc.png","fab.png","ajman bank.png","nmdc.png","al sagr insurance.png","arabia_insurance.png","standard chartered.png","insurance house.png","al_etihad_credit_bureau.png","joyalukkas.png","noor takaful.png","rotana.png","al_fujairah_national_insurance_co.png","commercial bank of dubai.png","fidelity_united_insurance.png","mtn.png","medgulf.png","adnic.png","enoc.png","adnoc.png","ega.png","abkuwait.png","takaful_emarat.png","bank of baroda.png","salama.png","sbb.png","arab bank.png","hsbc.png","almasraf.png","nbq.png","wio bank.png","credit_agricole_ci_bank.png","aafaq.png","coca_cola_arena.png","methaq_takaful_insurance_company.png","saudi_national_bank.png","adamjee_insurance.png","emirates_insurance.png","united_bank_limited.png","bank_of_khartoum.png","tokio marine nichido.png","union insurance.png","barclays bank.png","adib.png","invest bank.png","adcb.png","almarai.png","mashreq_bank.png","select.png","schem.png","national_bonds.png","sharjah_islamic_bank.png","al khaliji_france.png","rak bank.png","national_bank_oman.png","alliance.png","cbi.png","blom bank.png","national_general_insurance.png","aig.png","vodafone.png","central bank.png","daman_national_health_insurance.png","dubai islamic bank.png","bank_alfalah.png","united arab bank.png","efg_hermes.png","citibank.png","dubai_national_insurance_reinsurance.png","alain_farms.png","nbf.png","expo_city_dxb.png","takaful.png"]

    return render_template("instructor.html",
                           logo=custom_data["logo"],
                           clients=clients)