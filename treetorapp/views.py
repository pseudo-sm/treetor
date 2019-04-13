from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
import json
import pyrebase
import difflib
from datetime import datetime
from django.contrib import auth as authe
from functools import wraps
from django.urls import reverse
config = {
    'apiKey': "AIzaSyDXqt9Hu_sk_ndXasZzXWdBF2bAGlQwF-g",
    'authDomain': "treetor-75b14.firebaseapp.com",
    'databaseURL': "https://treetor-75b14.firebaseio.com",
    'projectId': "treetor-75b14",
    'storageBucket': "treetor-75b14.appspot.com",
    'messagingSenderId': "717881166373"
  };


firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

# Create your views here.
def student_login_required(function):
    @wraps(function)
    def wrapper(request, *args, **kw):
        if auth.current_user is None:
            return HttpResponseRedirect('/signin/')
        else:
            id = auth.current_user["localId"]
            type = db.child("users").child("students").child(id).get().val()
            if type is None:

                return HttpResponseRedirect('/signin/')
            else:
                return function(request, *args, **kw)
    return wrapper
def teacher_login_required(function):
    @wraps(function)
    def wrapper(request, *args, **kw):
        if auth.current_user is None:
            return HttpResponseRedirect('/signin/')
        else:
            id = auth.current_user["localId"]
            type = db.child("users").child("teachers").child(id).get().val()
            if type is None:

                return HttpResponseRedirect('/signin/')
            else:
                return function(request, *args, **kw)
    return wrapper

def institute_login_required(function):
    @wraps(function)
    def wrapper(request, *args, **kw):
        if auth.current_user is None:
            return HttpResponseRedirect('/signin/')
        else:
            id = auth.current_user["localId"]
            type = db.child("users").child("institutes").child(id).get().val()
            if type is None:

                return HttpResponseRedirect('/signin/')
            else:
                return function(request, *args, **kw)
    return wrapper

def home(request):

    return render(request,"index.html")

def signup(request):

    return render(request,"signup.html")
def post_signup(request):
    email = request.POST.get("email")
    name = request.POST.get("name")
    password = request.POST.get("password")
    type = request.POST.get("type")
    auth.create_user_with_email_and_password(email,password)
    auth.sign_in_with_email_and_password(email,password)
    uid = auth.current_user['localId']
    if type == "student":
        db.child("users").child('students').child(uid).update({'score':'Not Updated',"name":name,"email":email,'gender':'Not Updated','dob':'Not Updated','languages':'Not Updated','phone':'Not Updated','address':'Not Updated','hobbies':'Not Updated','interests':'Not Updated','sports':'Not Updated','guardian name':'Not Updated','guardian email':'Not Updated','guardian phone':'Not Updated','guardian dob':'Not Updated','guardian relation':'Not Updated','guardian occupation':'Not Updated','guardian qualification':'Not Updated','school':'Not Updated','class':'Not Updated','treetor center':'Not Updated','board':'Not Updated','percentage':'Not Updated','subjects':'Not Updated','best at':'Not Updated','weak at':'Not Updated','old tuition':'Not Updated','facebook':"Not Updated"})
        return HttpResponseRedirect('/student-profile/')
    else:
        db.child("users").child('teachers').child(uid).update({'Experience':'Not Updated',"name":name,"email":email,'gender':'Not Updated','dob':'Not Updated','languages':'Not Updated','phone':'Not Updated','address':'Not Updated','Qualification':'Not Updated','Treetor institutes':"Not Updated",'old tuition':'Not Updated',"facebook":"Not Updated","rank":"N/A","score":"N/A","rating":"N/A"})
        return HttpResponseRedirect('/teacher-profile/')

def enrollment_form(request):

    return render(request,"enrollment_form.html")

def signin(request):

    return render(request,"login.html")
def post_signin(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    auth.sign_in_with_email_and_password(email,password)
    uid = auth.current_user["localId"]
    students = dict(db.child("users").child("students").get().val()).keys()
    institutes = dict(db.child("users").child("institutes").get().val()).keys()
    teachers = dict(db.child("users").child("teachers").get().val()).keys()
    if uid in students:
        return HttpResponseRedirect("/student-profile/")
    elif uid in institutes:
        return HttpResponseRedirect("/institution-profile/")
    else:
        return HttpResponseRedirect("/teacher-dashboard/")
def submit(request):


    name = request.POST.get("name")
    subjects = request.POST.getlist("subjects[]")
    fees = request.POST.getlist("fees[]")
    teachers = request.POST.getlist("teachers[]")
    capacity = request.POST.getlist("capacity[]")
    total_teachers = request.POST.get("total_teachers")
    experience = request.POST.get("experience")
    offdays = request.POST.get("offdays")
    area = request.POST.get("area")
    total_capacity = request.POST.get("total_capacity")
    next_session = request.POST.get("session")
    house_students = request.POST.get("house_student")
    house_teachers = request.POST.get("house_teachers")
    best_at = request.POST.get("bestats")
    remarks = request.POST.get("remarks")

    count = db.child("count").get().val()
    count = count+1
    db.child("enrollment").child(count).update({"name":name, "teachers":total_teachers,"experience":experience,"offdays":offdays,"area":area,"total_capacity":total_capacity,"next session":next_session,"house students":house_students,"house teachers":house_teachers,"best at":best_at,"remarks":remarks})
    for i in range(len(subjects)):
        subject = subjects[i]
        fee = fees[i]
        cap = capacity[i]
        teacher = teachers[i]
        db.child("enrollment").child(count).child("subject details").update({subject:0})
        db.child("enrollment").child(count).child("subject details").child(subject).update({"fee":fee,"capacity":cap,"teacher":teacher})
    db.update({"count":count})
    return render(request,"enrollment_form.html",{"message":True})

def search(request):
    search = request.GET.get("search")
    data = dict(db.child("users").child("institutes").get().val())
    teachers = dict(db.child("users").child("teachers").get().val())
    results = []
    subjects = []
    courses_send = []
    for institute in data:
        if difflib.SequenceMatcher(a=search.lower(),b = (str(data[institute]["name"]).lower())).ratio() > 0.5 or difflib.SequenceMatcher(a=search.lower(),b = (str(data[institute]["area"]).lower())).ratio() > 0.3 :
            results.append({"name":data[institute]["name"],"address":data[institute]["area"]})
        if search.lower() in str(data[institute]["name"]).lower() and {"name":data[institute]["name"],"address":data[institute]["area"]} not in results:
            courses_res =  ",".join(list(data[institute]["courses"].keys()))
            results.append({"name":data[institute]["name"],"address":data[institute]["area"],"courses":courses_res})
        if data[institute].get("courses"):
            courses = data[institute]["courses"]
            for course in courses:

                if difflib.SequenceMatcher(a=search.lower(),b = (course.lower())).ratio() > 0.3:
                    courses_send.append({"name":data[institute]["name"],"address":data[institute]["area"],"course":course,"duration":data[institute]["courses"][course]["duration"],"off":data[institute]["courses"][course]["off"],"hours":data[institute]["courses"][course]["hours"],"price":data[institute]["courses"][course]["price"]})

    if len(results) ==  0:
        empty_results=1
    else:
        empty_results=0

    if len(courses_send) ==  0:
        empty_courses=1
    else:
        empty_courses=0
    return render(request,"ser_res.html",{"results":results,"empty_results":empty_results,"courses":courses_send,"empty_courses":empty_courses})
def institution_form(request):

    return render(request,"institution-form.html")
def institution_submit(request):

    name = request.POST.get("name")
    area = request.POST.get("area")
    email = request.POST.get("email")
    password = request.POST.get("password")
    classes = request.POST.getlist("classes[]")
    classes = ",".join(classes)
    year = request.POST.get("year")
    number_students = request.POST.get("no_students")
    number_teachers = request.POST.get("no_teachers")
    type = request.POST.getlist("type[]")
    type = ",".join(type)
    auth.create_user_with_email_and_password(email,password)
    auth.sign_in_with_email_and_password(email,password)
    uid = auth.current_user["localId"]
    now = datetime.now()
    date = str(now.date())
    db.child("users").child("institutes").child(uid).update({"name":name,"area":area,"email":email,"classes":classes,"year":year,"number students":number_students,"number teachers":number_teachers,"type":type,"signup time":date})
    return HttpResponseRedirect("/institution-form/")
def profile_form(request):

    return render(request,"profile-form.html")

def profile_submit(request):


    request.session['name'] = request.POST.get("name")
    request.session['subjects'] = request.POST.getlist("subjects[]")
    request.session['age'] = request.POST.get("age")
    request.session['experience'] = request.POST.get("yoe")
    request.session['prev'] = request.POST.get("prev")
    request.session['area'] = request.POST.get("area")
    request.session['works_at'] = request.POST.get("worksat")
    request.session['nx_session'] = request.POST.get("session")
    request.session['private'] = request.POST.get("private")
    request.session['qualifications'] = request.POST.get("qualifications")
    return HttpResponseRedirect("/schedule/")

def schedule(request):


    return render(request,"sub_schedule.html")

def post_schedule(request):

    uid = auth.current_user["localId"]
    boards = request.POST.getlist("boards[]")
    subjects = request.POST.getlist("subjects[]")
    monday = request.POST.getlist("monday[]")
    tuesday = request.POST.getlist("tuesday[]")
    wednessday = request.POST.getlist("wednessday[]")
    thursday = request.POST.getlist("thursday[]")
    friday = request.POST.getlist("friday[]")
    saturday = request.POST.getlist("saturday[]")
    sunday = request.POST.getlist("sunday[]")
    return HttpResponseRedirect("/institution-dashboard/")

@student_login_required
def student_profile(request):
    count = 0
    uid = auth.current_user["localId"]
    data=dict(db.child("users").child("students").child(uid).get().val())
    name = data["name"]
    gender = data['gender']
    dob = data['dob']
    languages = data['languages']
    phone = data['phone']
    email = data['email']
    address = data['address']
    facebook = data['facebook']
    hobbies = data['hobbies']
    interests = data['interests']
    sports = data['sports']
    g_name = data['guardian name']
    g_mail = data['guardian email']
    g_phone = data['guardian phone']
    g_dob = data['guardian dob']
    g_relation = data['guardian relation']
    school = data['school']
    percentage = data['percentage']
    std = data['class']
    treetor_center = data['treetor center']
    board = data['board']
    subjects = data['subjects']
    best_at = data['best at']
    weak_at = data['weak at']
    older_tuitions = data['old tuition']
    for i in data:
        if data[i] != "Not Updated":
            count+=1
    count = int(count*100/28)
    data = {"name":name,"email":email,'gender':gender,'dob':dob,'languages':languages,'phone':phone,'address':address,'facebook':facebook,'hobbies':hobbies,'interests':interests,'sports':sports,'g_name':g_name,'g_mail':g_mail,'g_phone':g_phone,'g_dob':g_dob,'school':school,'relation':g_relation,'std':std,'percentage':percentage,'treetor_center':treetor_center,'subjects':subjects,'best_at':best_at,'weak_at':weak_at,'old':older_tuitions,'board':board,"count":count}

    return render(request,"student_profile.html",data)
def student_dashboard(request):

    return render(request,"student_dashboard.html")
def student_schedule(request):

    return render(request,"student_schedule.html")
def teacher_dashboard(request):
    uid = auth.current_user["localId"]
    institutes = dict(db.child("users").child("institutes").get().val())
    institutes_id = list(institutes.keys())
    names = {}
    for institute in institutes_id:
        names.update({institute:institutes[institute]["name"]})
    this = db.child("users").child("teachers").child(uid).get().val()
    teacher_name = this["name"]
    return render(request,"teacher_dashboard.html",{"names":names,"teacher_name":teacher_name})

@teacher_login_required
def teacher_profile(request):
    count=0
    uid = auth.current_user["localId"]
    teacher = dict(db.child("users").child("teachers").child(uid).get().val())
    exp = teacher["Experience"]
    qualification = teacher["Qualification"]
    treetor = teacher["Treetor institutes"]
    address = teacher["address"]
    dob = teacher["dob"]
    mail = teacher["email"]
    fb = teacher["facebook"]
    gender = teacher["gender"]
    languages = teacher["languages"]
    name = teacher["name"]
    ot = teacher["old tuition"]
    phone = teacher["phone"]
    for i in teacher:
        if teacher[i] != "Not Updated":
            count+=1
    count = int(count*100/28)
    data = {"exp":exp,"qualification":qualification,"treetor":treetor,"address":address,"dob":dob,"mail":mail,"fb":fb,"gender":gender,"languages":languages,"name":name,"ot":ot,"phone":phone,"count":count}
    return render(request,"teacher_profile.html",data)
def basic_update(request):

    uid = auth.current_user["localId"]
    teachers = dict(db.child("users").child("teachers").get().val())
    if uid in teachers:
        user = "teachers"
    else:
        user = "students"

    gender = request.GET.get("gender")
    dob = request.GET.get("dob")
    languages = request.GET.get("languages")
    db.child("users").child(user).child(uid).update({"gender":gender,"dob":dob,"languages":languages})
    all = True
    return HttpResponse(json.dumps(all), content_type='application/json')
def career_update(request):

    uid = auth.current_user["localId"]
    exp = request.GET.get("exp")
    qualification = request.GET.get("qualification")
    treetor = request.GET.get("treetor")
    ot = request.GET.get("ot")
    db.child("users").child("teachers").child(uid).update({"Experience":exp,"Qualification":qualification,"Treetor institutes":treetor,"old tuition":ot})
    all = True
    return HttpResponse(json.dumps(all), content_type='application/json')
def contact_update(request):

    uid = auth.current_user["localId"]
    teachers = dict(db.child("users").child("teachers").get().val())
    if uid in teachers:
        user = "teachers"
    else:
        user = "students"

    phone = request.GET.get("phone")
    email = request.GET.get("email")
    address = request.GET.get("address")
    facebook = request.GET.get("facebook")
    db.child("users").child(user).child(uid).update({"phone":phone,"email":email,"address":address,"facebook":facebook})
    all = True
    return HttpResponse(json.dumps(all), content_type='application/json')
def personal_update(request):

    interests = request.GET.get("interests")
    hobbies = request.GET.get("hobbies")
    sports = request.GET.get("sports")
    uid = auth.current_user["localId"]
    db.child("users").child("students").child(uid).update({"interests":interests,"hobbies":hobbies,"sports":sports})
    all = True
    return HttpResponse(json.dumps(all), content_type='application/json')
def guardian_update(request):
    gname = request.GET.get("gname")
    gmail = request.GET.get("gmail")
    gphone = request.GET.get("gphone")
    gdob = request.GET.get("gdob")
    grelation = request.GET.get("grelation")
    uid = auth.current_user["localId"]
    db.child("users").child("students").child(uid).update({"guardian name":gname,"guardian relation":grelation,"guardian dob":gdob,"guardian phone":gphone,"guardian email":gmail})
    all = True
    return HttpResponse(json.dumps(all), content_type='application/json')
def academic_update(request):

    school = request.GET.get("school")
    std = request.GET.get("std")
    subjects = request.GET.get("subjects")
    tc = request.GET.get("tc")
    ot = request.GET.get("ot")
    per = request.GET.get("per")
    wa = request.GET.get("wa")
    ba = request.GET.get("ba")

    uid = auth.current_user["localId"]
    db.child("users").child("students").child(uid).update({"school":school,"class":std,"subjects":subjects,"treetor center":tc,"old tuition":ot,"percentage":per,"weak at":wa,"best at":ba})
    all = True
    return HttpResponse(json.dumps(all), content_type='application/json')



def top_5_students(request):
    return render(request,"top_5_students.html")
def institution_courses(request):
    return render(request,"institution_courses.html")
def institution_list(request):
    return render(request,"institution_list.html")

@institute_login_required
def institution_profile(request):

    uid = auth.current_user["localId"]
    institution = dict(db.child("users").child("institutes").child(uid).get().val())
    users = dict(db.child("users").child("teachers").get().val())
    teachers_all = dict(db.child("users").child("teachers").get().val())
    name = institution["name"]
    classes = institution["classes"]
    area = institution["area"]
    teachers = institution["number teachers"]
    students = institution["number students"]
    email = institution["email"]
    type = institution["type"]
    subject_name = []
    duration = []
    off = []
    hours = []
    class_1 = []
    time = []
    price = []
    subjects = []
    pending = False
    pending_list = {}
    course_names = []
    all_teachers_inst = {}
    institution_data = {"name":name,"classes":classes,"area":area,"teachers":teachers,"students":students,"email":email,"type":type}
    if institution.get("courses") is not None:
        print('below')
        courses = institution["courses"]
        for course in courses:
            duration.append(institution["courses"][course]["duration"])
            course_names.append(course)
            all_class =  list(institution["courses"][course]["class"].keys())
            class_1.append(",".join(all_class))
            off.append(institution["courses"][course]["off"])
            price.append(institution["courses"][course]["price"])
            all_subjects = list(institution["courses"][course]["subjects"].keys())
            subjects.append(",".join(all_subjects))
    courses_send = (zip(course_names,duration,off,class_1,price,subjects))
    if institution.get("pending") is not None:
        pl = list(institution["pending"].keys())
        pending = len(pl)
        for id in pl:
            pending_list.update({id:teachers_all[id]["name"]})

    if institution.get("teachers") is not None:
        teacher_list = list(institution["teachers"].keys())
        for teacher in teacher_list :
            all_teachers_inst.update({teacher:teachers_all[teacher]["name"]})
        return render(request,"institution_profile.html",{"institution":institution_data,"pending":pending,"pending_list":pending_list,"all_teachers":all_teachers_inst,"courses":courses_send})
    else:
        return render(request,"institution_profile.html",{"institution":institution_data,"done":True,"courses":courses_send})
def make_teacher(request):


    uid = auth.current_user["localId"]
    db.child("users").child("institutes").child(uid).child("teacher").update({'score':'Not Updated','teacher name':"Not Updated",'gender':'Not Updated','dob':'Not Updated','languages':'Not Updated','phone':'Not Updated','address':'Not Updated','hobbies':'Not Updated','interests':'Not Updated','sports':'Not Updated','guardian name':'Not Updated','guardian email':'Not Updated','guardian phone':'Not Updated','guardian dob':'Not Updated','guardian relation':'Not Updated','guardian occupation':'Not Updated','guardian qualification':'Not Updated','school':'Not Updated','class':'Not Updated','treetor center':'Not Updated','board':'Not Updated','percentage':'Not Updated','subjects':'Not Updated','best at':'Not Updated','weak at':'Not Updated','old tuition':'Not Updated','facebook':"Not Updated"})
    all = True
    return HttpResponse(json.dumps(all), content_type='application/json')

def institution_update(request):
    uid = auth.current_user["localId"]
    classes = request.GET.get("classes")
    teachers = request.GET.get("teachers")
    students = request.GET.get("students")
    area = request.GET.get("area")
    type = request.GET.get("type")
    all = True
    db.child("users").child("institutes").child(uid).update({"area":area,"classes":classes,"number students":students,"number teachers":teachers,"type":type})
    return HttpResponse(json.dumps(all),content_type='application/json')

def add_courses(request):

    uid = auth.current_user["localId"]
    duration = request.GET.get("duration")
    off = request.GET.get("off")
    hours = request.GET.get("hours")
    name = request.GET.get("name")
    time = request.GET.get("time")
    price = request.GET.get("price")
    subject = request.GET.get("subjects")
    teachers = request.GET.get("teachers","not assigned")
    std = request.GET.get("class")
    subjects = []
    hours_list= []
    teachers_list = []
    class_list = []
    subj = subject[1:len(subject)-1].split(',')
    t = teachers[1:len(teachers)-1].split(',')
    h = hours[1:len(hours)-1].split(',')
    p = std[1:len(std)-1].split(',')
    for i in subj:
        subjects.append(i[1:len(i)-1])
    for i in h:
        hours_list.append(i[1:len(i)-1])
    for i in t:
        teachers_list.append(i[1:len(i)-1])
    for i in p:
        class_list.append(i[1:len(i)-1])

    db.child("users").child("institutes").child(uid).child("courses").child(name).update({"duration":duration,"price":price,"time":time,"off":off,"class":std})
    for i in range(len(subj)):
        db.child("users").child("institutes").child(uid).child("courses").child(name).child("subjects").child(subjects[i]).update({"teacher":teachers_list[i],"hours":hours_list[i]})
    for i in range(len(class_list)):
        db.child("users").child("institutes").child(uid).child("courses").child(name).child("class").update({"'"+str(class_list[i])+"'":0})
    all=True
    return HttpResponse(json.dumps(all),content_type='application/json')

def add_teachers(request):

    teacher = request.GET.get("new_teacher")
    all = True
    return HttpResponse(json.dumps(all),content_type='application/json')

def institution_teachers(request):
    return render(request,"institution_teachers.html")
def all_students(request):
    return render(request,"all_students.html")
def comment_unit(request):
    return render(request,"comment_unit.html")

# exp = request.POST.get("Experience")
#     qualification = request.POST.get("Qualification")
#     treetor = request.POST.get("Treetor Institutes")
#     address = request.POST.get("address")
#     dob = request.POST.get("dob")
#     mail = request.POST.get("email")
#     fb = request.POST.get("facebook")
#     gender = request.POST.get("gender")
#     languages = request.POST.get("languages")
#     name = request.POST.get("name")
#     ot = request.POST.get("old tuition")
#     phone = request.POST.get("phone")

def logout(request):
    auth.current_user = None
    authe.logout()
    return HttpResponseRedirect('/signin/')
def demo_request(request):
    name = request.GET.get("name")
    email = request.GET.get("email")
    wap = request.GET.get("wap")
    timestamp = int(datetime.now().timestamp())
    date = str(datetime.fromtimestamp(timestamp).date())
    time = str(datetime.fromtimestamp(timestamp).time())
    timestamp = str(timestamp)
    db.child("Querries").child(timestamp).update({"date":date,"time":time,"name":name,"email":email,"wap":wap})
    all = True
    return HttpResponse(json.dumps(all),content_type='application/json')

def institution_details(request):

    auth.sign_in_with_email_and_password("teacher2@gmail.com","password")
    uid = auth.current_user["localId"]
    name = request.GET.get("name")
    institutes = dict(db.child("users").child("institutes").get().val())
    all = False
    for institute in institutes:
        if name == institutes[institute]["name"]:
            db.child("users").child("institutes").child(institute).child("pending").update({uid:0})
    return HttpResponse(json.dumps(all),content_type='application/json')
def accept_request(request):


    accepted = request.GET.get("accepted");
    uid = auth.current_user["localId"]
    db.child("users").child("institutes").child(uid).child("pending").child(accepted).remove()
    db.child("users").child("institutes").child(uid).child("teachers").update({accepted:0})
    all = True
    return HttpResponse(json.dumps(all),content_type="application/json")

def change_picture(request):

    image = request.POST.get("image")
    all = True
    return HttpResponseRedirect("/institution-profile/")


def quiz_response(request):

    roll = request.GET.get('roll')
    answer = request.GET.get('answer')
    uid = request.GET.get('uid')
    ongoing = db.child("users").child("teachers").child(uid).child("ongoing").get().val()
    correct = db.child("users").child("teachers").child(uid).child("quiz").child(ongoing).child("correct").get().val()
    if correct == answer:
        marks = db.child("marks").get().val()
        marks+=1
        db.update({"marks":marks})

    return JsonResponse(marks)

def show_response(request):

    marks = db.child("marks").get().val()

    return HttpResponse("Marks : "+str(marks))
