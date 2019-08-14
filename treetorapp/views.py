from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from requests.exceptions import HTTPError
from django.views.decorators.csrf import csrf_exempt
import json
import pyrebase
import difflib
from datetime import datetime
from django.contrib import auth as authe
from functools import wraps
import requests
import random
from math import sin, cos, sqrt, atan2
import json
from django.views.decorators.csrf import csrf_exempt
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

def find_user(uid):

    all = dict(db.child("users").get().val())
    if uid in all["students"]:
        parent = "students"
    elif uid in all["teachers"] and uid not in all["institutes"]:
        parent = "teachers"
    else:
        parent = "institutes"
    return parent

def home(request):

    timestamp = int(datetime.now().timestamp())
    db.child("hits").update({timestamp:0})
    if auth.current_user is not None:
        user = find_user(auth.current_user["localId"])
        if user == "students":
            return render(request,"index.html",{"xyz":True,"profile":"student-profile/"})
        elif user == "teachers":
            return render(request,"index.html",{"xyz":True,"profile":"teacher-profile/","dashboard":"teacher-dashboard/"})
        else:
            return render(request,"index.html",{"xyz":True,"profile":"institution-profile/"})
    else:
        return render(request,"index.html",{"yuo":True})
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
        db.child("users").child('students').child(uid).update({'score':'Not Updated',"name":name,"email":email,'gender':'Not Updated','dob':'Not Updated','languages':'Not Updated','phone':'Not Updated','address':'Not Updated','hobbies':'Not Updated','interests':'Not Updated','sports':'Not Updated','guardian name':'Not Updated','guardian email':'Not Updated','guardian phone':'Not Updated','guardian dob':'Not Updated','guardian relation':'Not Updated','guardian occupation':'Not Updated','guardian qualification':'Not Updated','school':'Not Updated','class':'Not Updated','treetor center':'Not Updated','board':'Not Updated','percentage':'Not Updated','subjects':'Not Updated','best at':'Not Updated','weak at':'Not Updated','old tuition':'Not Updated','facebook':"Not Updated","rank":"N/A"})
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
    try:
        auth.sign_in_with_email_and_password(email,password)
    except HTTPError:
        return render(request,"login.html",{"fail":True})
    uid = auth.current_user["localId"]
    students = dict(db.child("users").child("students").get().val()).keys()
    institutes = dict(db.child("users").child("institutes").get().val()).keys()
    teachers = dict(db.child("users").child("teachers").get().val()).keys()

    if uid in students:
        return HttpResponseRedirect("/")
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
    from operator import itemgetter
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY1NmMzZGQyMWQwZmVmODgyZTA5ZTBkODY5MWNhNWM3ZjJiMGQ2MjEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJlZXRvci03NWIxNCIsImF1ZCI6InRyZWV0b3ItNzViMTQiLCJhdXRoX3RpbWUiOjE1NTYwNjA0MDYsInVzZXJfaWQiOiJqRGRZY2FlQ2diVnVmRGF1UHo0ZlVkYlZpRW4yIiwic3ViIjoiakRkWWNhZUNnYlZ1ZkRhdVB6NGZVZGJWaUVuMiIsImlhdCI6MTU1NjA2MDQwNywiZXhwIjoxNTU2MDY0MDA3LCJlbWFpbCI6InRyaWRlbnRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInRyaWRlbnRAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.TCFqZ_Z6DEp8a9yWxJx1w19dsxPR-0iuVdV3vfpZg1DI2Ss4N44Jph7YUrNNk3BFPHjY_Gp6wA5nxrNRZ2eB367sOyzXgyHAxDgOY-fyBI14xtIrV7xK6NZ1VfMG383Mcx6fEVatpZkx1O8XvZ0Ir-d_Fwz0Bw60hTuTLXu9WAjCH-lchnqMAO5qIvMN6Rx0Aay9vcFHJB7IVHgeKg-AWkh2pC1XYkT7jP45gT0BvudmRwH1QyVACsHFJQ6QQ1Gk6vgkW0UyaAr_N3Hz1Gj4T0QyWD0x7BO3fVwkpUQOa0lyE4GWl7o9Zw3UCk5NUI4fgLsm_rJ3IeYV5TIr7ImS9w"
    if search is not "":
        for institute in data:
            if difflib.SequenceMatcher(a=search.lower(),b = (str(data[institute]["name"]).lower())).ratio() > 0.3 or difflib.SequenceMatcher(a=search.lower(),b = (str(data[institute]["area"]).lower())).ratio() > 0.3 :
                match = difflib.SequenceMatcher(a=search.lower(),b = (str(data[institute]["name"]).lower())).ratio()
                image = storage.child("users").child("institutes").child(institute).child(institute).get_url(token)
                r = requests.get(image)
                if r.status_code == 404:
                    image = "../static/images/enterprise.png"
                courses_res = ""
                if data[institute].get("courses") is not None:
                        courses_res =  ",".join(list(data[institute]["courses"].keys()))
                geo = {}
                if data[institute].get("geolocation") is not None:
                    lat = data[institute]["geolocation"]["latitude"]
                    lon = data[institute]["geolocation"]["longitude"]
                    geo.update({"lat":lat,"lon":lon})
                results.append({"match":match,"name":data[institute]["name"],"address":data[institute]["area"],"id":institute,"image":image,"courses":courses_res,"geo":geo})
            if search.lower() in str(data[institute]["name"]).lower() and {"name":data[institute]["name"],"address":data[institute]["area"]} not in results:
                match = 0.1
                if data[institute].get("courses") is not None:
                    image = storage.child("users").child("institutes").child(institute).get_url(token)
                    r = requests.get(image)
                    if r.status_code == 404:
                        image = "../static/images/enterprise.png"
                    courses_res =  ",".join(list(data[institute]["courses"].keys()))
                    geo = {}
                    if data[institute].get("geolocation") is not None:
                        print(institute)
                        lat = data[institute]["geolocation"]["latitude"]
                        lon = data[institute]["geolocation"]["longitude"]
                        geo.update({"lat":lat,"lon":lon})
                    results.append({"match":match,"image":image,"name":data[institute]["name"],"address":data[institute]["area"],"courses":courses_res,"id":institute,"geo":geo})
            if data[institute].get("courses"):
                courses = data[institute]["courses"]
                for course in courses:
                    if difflib.SequenceMatcher(a=search.lower(),b = (course.lower())).ratio() > 0.3:
                        image = storage.child("users").child("institutes").child(institute).get_url(token)
                        r = requests.get(image)
                        if r.status_code == 404:
                            image = "../static/images/enterprise.png"
                        courses_res =  ",".join(list(data[institute]["courses"].keys()))
                        courses_send.append({"courses":courses_res,"image":image,"name":data[institute]["name"],"address":data[institute]["area"],"course":course,"duration":data[institute]["courses"][course]["duration"],"off":data[institute]["courses"][course]["off"],"price":data[institute]["courses"][course]["price"],"id":institute})
        timestamp = int(datetime.now().timestamp())
        db.child("search track").child(search).update({timestamp:0})
    if len(results) ==  0:
        empty_results=1
    else:
        empty_results=0

    if len(courses_send) ==  0:
        empty_courses=1
    else:
        empty_courses=0
    results.sort(key=lambda x: x["match"])
    if auth.current_user is not None:
        user = find_user(auth.current_user["localId"])
        if user == "students":
            return render(request,"ser_res.html",{"xyz":True,"profile":"student-profile/","results":results,"empty_results":empty_results,"courses":courses_send,"empty_courses":empty_courses})
        elif user == "teachers":
            return render(request,"ser_res.html",{"xyz":True,"profile":"teacher-profile/","dashboard":"teacher-dashboard/","results":results,"empty_results":empty_results,"courses":courses_send,"empty_courses":empty_courses})
        else:
            return render(request,"ser_res.html",{"xyz":True,"profile":"institution-profile/","results":results,"empty_results":empty_results,"courses":courses_send,"empty_courses":empty_courses})
    else:
        return render(request,"ser_res.html",{"yuo":True,"results":results,"empty_results":empty_results,"courses":courses_send,"empty_courses":empty_courses})

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

@student_login_required
def student_dashboard(request):

    uid = auth.current_user["localId"]
    student = dict(db.child("users").child("students").child(uid).get().val())
    institute = db.child("users").child("institutes").child(student["treetor center"]).get().val()
    report = {}
    for batch in institute["batches"]:
        if uid in institute["batches"][batch]["students"]:
            batch_id = batch
    if institute["batches"][batch_id].get("dailyreport") is not None:
        for session in institute["batches"][batch_id]["dailyreport"]:
            if institute["batches"][batch_id]["dailyreport"][session].get(uid) is not None:
                attendance = "P"
            else:
                attendance="A"
            date = datetime.fromtimestamp(int(session)/1000).date()
            report.update({str(date):{"attendance":attendance,"this":institute["batches"][batch_id]["dailyreport"][session][uid]["today"],"next":institute["batches"][batch_id]["dailyreport"][session][uid]["tomorrow"],"rating":institute["batches"][batch_id]["dailyreport"][session][uid]["rating"],"review":institute["batches"][batch_id]["dailyreport"][session][uid]["review"]}})
            details = {"name":student["name"],"score":student["score"]}
    return render(request,"student_dashboard.html",{"report":report,"details":details})

def student_schedule(request):

    return render(request,"student_schedule.html")
@teacher_login_required
def teacher_dashboard(request):
    names = {}
    uid = auth.current_user["localId"]
    institutes = dict(db.child("users").child("institutes").get().val())
    institutes_id = list(institutes.keys())
    names = {}
    this = db.child("users").child("teachers").child(uid).get().val()
    teacher_name = this["name"]
    for inst in institutes:
        names.update({inst:institutes[inst]["name"]})
    return render(request,"teacher_dashboard.html",{"names":names,"teacher_name":teacher_name,"also_inst":True})

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

    name = request.GET.get("name")
    gender = request.GET.get("gender")
    dob = request.GET.get("dob")
    languages = request.GET.get("languages")
    db.child("users").child(user).child(uid).update({"gender":gender,"dob":dob,"languages":languages,"name":name})
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

    also_teacher = False
    done = True
    uid = auth.current_user["localId"]
    all_teachers = dict(db.child("users").child("teachers").get().val())
    if uid in all_teachers:
        also_teacher = True
        done = False
    institution = dict(db.child("users").child("institutes").child(uid).get().val())
    users = dict(db.child("users").child("teachers").get().val())
    image = storage.child("users").child("institutes").child(uid).child(uid).get_url(auth.current_user["idToken"])
    r = requests.get(image)
    if r.status_code == 404:
        image = "../static/images/enterprise.png"
    teachers_all = dict(db.child("users").child("teachers").get().val())
    name = institution["name"]
    classes = institution["classes"]
    area = institution["area"]
    teachers = institution["number teachers"]
    students = institution["number students"]
    email = institution["email"]
    type1 = institution["type"]
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
    subject_id = []
    standards = []
    all_teachers_inst = {}
    courses_context = {}
    institution_data = {"name":name,"classes":classes,"area":area,"teachers":teachers,"students":students,"email":email,"type":type1}
    if institution.get("subjects") is not None:
        subjects = institution["subjects"]
        for subject in subjects:
            subject_id.append(subject)
            subject_name.append(subjects[subject]["subject"])
            standards.append(subjects[subject]["standard"])

    courses_send = (zip(subject_id,subject_name,standards))

    if institution.get("pending") is not None:
        pl = list(institution["pending"].keys())
        pending = len(pl)
        for id in pl:
            pending_list.update({id:teachers_all[id]["name"]})
    if institution.get("teachers") is not None:
        teacher_list = list(institution["teachers"].keys())
        for teacher in teacher_list :
            all_teachers_inst.update({teacher:teachers_all[teacher]["name"]})

    students_context = {}
    all_students = dict(db.child("users").child("students").get().val())
    time = institution["signup time"]
    month = str(int(time[5:7])+6)
    time = time[:4]+"/"+month+"/"+time[8:] + " 00:00:00"
    pending = institution["students"]
    pending_count = 0
    for student in pending:
        if pending[student] == 0:
            pending_count+=1
    if pending_count == 0:
        pending_students = ""
    else:
        pending_students = "( "+str(pending_count) + " )"
    batches = []
    batch_subjects = []
    students_batch = []
    batches_send = []
    if institution.get("batches") is not None:
        for batch in institution["batches"]:
            batches.append(batch)
            subj = []
            for subject in institution["batches"][batch]["subjects"]:
                subj.append(subject)
            batch_subjects.append(subj)
        for student in institution["students"]:
            students_batch.append(student)
        batches_send = zip(batches,batch_subjects,students_batch)
    if institution.get("students") is not None:
        for student in institution["students"]:
            if institution["students"][student] == 1:
                students_context.update({student:all_students[student]["name"]})
        return render(request,"institution_profile.html",{"pending_students":pending_students,"time":time,"image":image,"institution":institution_data,"pending":pending,"pending_list":pending_list,"all_teachers":all_teachers_inst,"subjects":courses_send,"done":done,"also_teacher":also_teacher,"all_students":students_context,"all_course":course_names,"batches":batches_send})
    else:
        return render(request,"institution_profile.html",{"pending_students":pending_students,"time":time,"image":image,"institution":institution_data,"done":done,"subjects":courses_send,"pending":pending,"pending_list":pending_list,"also_teacher":also_teacher,"all_students":students_context,"all_course":course_names,"batches":batches_send})
def make_teacher(request):


    uid = auth.current_user["localId"]
    db.child("users").child("institutes").child(uid).child("teacher").update({'score':'Not Updated','teacher name':"Not Updated",'gender':'Not Updated','dob':'Not Updated','languages':'Not Updated','phone':'Not Updated','address':'Not Updated','hobbies':'Not Updated','interests':'Not Updated','sports':'Not Updated','guardian name':'Not Updated','guardian email':'Not Updated','guardian phone':'Not Updated','guardian dob':'Not Updated','guardian relation':'Not Updated','guardian occupation':'Not Updated','guardian qualification':'Not Updated','school':'Not Updated','class':'Not Updated','treetor center':'Not Updated','board':'Not Updated','percentage':'Not Updated','subjects':'Not Updated','best at':'Not Updated','weak at':'Not Updated','old tuition':'Not Updated','facebook':"Not Updated"})
    db.child("users").child("teachers").child(uid).child("institutes").update({uid:0})
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

def add_subjects(request):

    uid = auth.current_user["localId"]
    subjects = request.GET.get("subjects")
    standard = request.GET.get("standard")
    subjects = json.loads(subjects)
    standard = json.loads(standard)
    for i in range(len(subjects)):
        subject_id = random.randint(100000,999999)
        db.child("users").child("institutes").child(uid).child("subjects").child(subject_id).update({"subject":subjects[i]})
        db.child("users").child("institutes").child(uid).child("subjects").child(subject_id).update({"standard":standard[i]})
    all = True
    return JsonResponse(json.dumps(all),content_type='application/json',safe=False)

def add_teachers(request):

    teacher = request.GET.get("new_teacher")
    all = True
    return HttpResponse(json.dumps(all),content_type='application/json')

def institution_teachers(request):
    return render(request,"institution_teachers.html")

@institute_login_required
def all_students(request):

    names = []
    emails = []
    schools = []
    schools = []
    scores = []
    ranks = []
    pnames = []
    pemails = []
    pschools = []
    pschools = []
    pscores = []
    pranks = []
    pids = []
    ids = []
    uid = auth.current_user["localId"]
    students = dict(db.child("users").child("students").get().val())
    try:
        this_students = dict(db.child("users").child("institutes").child(uid).child("students").get().val())
        for i in this_students:
            if this_students[i] == 1:
                ids.append(i)
                names.append(students[i]["name"])
                emails.append(students[i]["email"])
                schools.append(students[i]["school"])
                scores.append(students[i]["score"])
                ranks.append(students[i]["rank"])
            else:
                pids.append(i)
                pnames.append(students[i]["name"])
                pemails.append(students[i]["email"])
                pschools.append(students[i]["school"])
                pscores.append(students[i]["score"])
                pranks.append(students[i]["rank"])
    except TypeError:
        print("error")
        return render(request,"all_students.html",{"none":True})
    pending = zip(pids,pnames,pemails,pschools,pscores,pranks)
    context = zip(ids,names,emails,schools,scores,ranks)
    return render(request,"all_students.html",{"context":context,"pending":pending})

def accept_students(request):

    id = request.GET.get("id")
    uid = auth.current_user["localId"]
    db.child("users").child("institutes").child(uid).child("students").update({id:1})
    db.child("users").child("students").child(id).update({"treetor center":uid})
    content = True
    return JsonResponse(json.dumps(content),safe=False,content_type="json/application")

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
    authe.logout(request)
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
    all = Truealso_teacher = False
    done = True
    uid = auth.current_user["localId"]
    all_teachers = dict(db.child("users").child("teachers").get().val())
    if uid in all_teachers:
        also_teacher = True
        done = False
    institution = dict(db.child("users").child("institutes").child(uid).get().val())
    users = dict(db.child("users").child("teachers").get().val())
    image = storage.child("users").child("institutes").child(uid).child(uid).get_url(auth.current_user["idToken"])
    r = requests.get(image)
    if r.status_code == 404:
        image = "../static/images/enterprise.png"
    teachers_all = dict(db.child("users").child("teachers").get().val())
    name = institution["name"]
    classes = institution["classes"]
    area = institution["area"]
    teachers = institution["number teachers"]
    students = institution["number students"]
    email = institution["email"]
    type1 = institution["type"]
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
    courses_context = {}
    institution_data = {"name":name,"classes":classes,"area":area,"teachers":teachers,"students":students,"email":email,"type":type1}
    if institution.get("courses") is not None:
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
    btimes = []
    bid = []
    bcourse = []
    if institution.get("batches") is not None:
        for id in institution["batches"]:
            bcourse.append(institution["batches"][id]["course"])
            bid.append(id)
    batches = zip(bcourse,bid)

    students_context = {}
    all_students = dict(db.child("users").child("students").get().val())
    time = institution["signup time"]
    month = str(int(time[5:7])+6)
    time = time[:4]+"/"+month+"/"+time[8:] + " 00:00:00"
    pending = institution["students"]
    pending_count = 0
    for student in pending:
        if pending[student] == 0:
            pending_count+=1
    if pending_count == 0:
        pending_students = ""
    else:
        pending_students = "( "+str(pending_count) + " )"
    if institution.get("students") is not None:
        for student in institution["students"]:
            if institution["students"][student] == 1:
                students_context.update({student:all_students[student]["name"]})
        return render(request,"institution_profile.html",{"pending_students":pending_students,"time":time,"image":image,"institution":institution_data,"pending":pending,"pending_list":pending_list,"all_teachers":all_teachers_inst,"courses":courses_send,"done":done,"also_teacher":also_teacher,"all_students":students_context,"all_course":course_names,"batches":batches})
    else:
        return render(request,"institution_profile.html",{"pending_students":pending_students,"time":time,"image":image,"institution":institution_data,"done":done,"courses":courses_send,"pending":pending,"pending_list":pending_list,"also_teacher":also_teacher,"all_students":students_context,"all_course":course_names,"batches":batches})
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
    db.child("users").child("teachers").child(accepted).child("institutes").update({uid:0})
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


def view_courses(request):

    auth.sign_in_with_email_and_password("trident@gmail.com","password")
    uid = auth.current_user["localId"]
    course_name = []
    classes = []
    courses = dict(db.child("users").child("institutes").child(uid).child("courses").get().val())
    for i in courses:
        course_name.append(i)
        classes.append(list(courses[i]["class"].keys()))
    return render(request,"institution_courses.html")

def apply(request):

    if auth.current_user is not None:
        uid = auth.current_user["localId"]
        user_type = find_user(uid)
        id = auth.current_user["localId"]
        inst = request.GET.get("id")[1:]
        content = True
        if user_type == "students":
            db.child("users").child("institutes").child(inst).child("students").update({id:0})
    else:
        content = False
    return JsonResponse(json.dumps(content),content_type="application/json",safe=False)


def add_as_teacher(request):

    uid = auth.current_user["localId"]
    data = dict(db.child("users").child("institutes").child(uid).get().val())
    email = data["email"]
    name = data["name"]
    db.child("users").child('teachers').child(uid).update({'Experience':'Not Updated',"name":name,"email":email,'gender':'Not Updated','dob':'Not Updated','languages':'Not Updated','phone':'Not Updated','address':'Not Updated','Qualification':'Not Updated','Treetor institutes':"Not Updated",'old tuition':'Not Updated',"facebook":"Not Updated","rank":"N/A","score":"N/A","rating":"N/A"})
    db.child("users").child("institutes").child(uid).child("teachers").update({uid:0})
    return HttpResponseRedirect("/teacher-dashboard/")

def change_picture(request):

    uid = auth.current_user["localId"]
    image = request.FILES.get("dp")
    type_user = find_user(uid)
    storage.child("users").child(type_user).child(uid).child(uid).put(image,auth.current_user['idToken'])
    content = True
    return HttpResponseRedirect("/institution-profile/")

@institute_login_required
def add_batch(request):

    uid = auth.current_user["localId"]
    time = request.GET.get("time")
    subjects = request.GET.get("subjects")
    students = request.GET.get("students")
    subjects = json.loads(subjects)
    teachers = json.loads(request.GET.get("teachers"))
    # timings = request.GET.get("timings")
    # endtimings = request.GET.get("endtimings")
   # timings = json.loads(timings)
   # endtimings = json.loads(endtimings)
    students = json.loads(students)
    batch_id = random.randint(100000,999999)

    for student in students:
        db.child("users").child("institutes").child(uid).child("batches").child(batch_id).child("students").update({student:0})
        db.child("users").child("students").child(student).child("institutes").child(uid).child("batches").update({batch_id:0})
    for i in range(len(subjects)):
        db.child("users").child("institutes").child(uid).child("batches").child(batch_id).child("subjects").child(subjects[i]).update({"teacher":teachers[i]})
    content = batch_id
    return JsonResponse(json.dumps(content),content_type="application/json",safe=False)

@institute_login_required
def batches(request):
    uid = auth.current_user["localId"]
    bids = []
    bcourses = []
    bteachers = []
    btimes = []
    bstudents = []
    context_batches = []
    institute = dict(db.child("users").child("institutes").child(uid).get().val())
    teachers = dict(db.child("users").child("teachers").get().val())
    if institute.get("batches") is not None:
        all_batches = institute["batches"]
        for id in all_batches:
            bids.append(id)
            bcourses.append(all_batches[id]["course"])
            teacher = all_batches[id]["teacher"]
            bteachers.append(teachers[teacher]["name"])
            bstudents.append(list(all_batches[id]["students"].keys()))
    context_batches = zip(bids,bcourses,bteachers)
    return render(request,"batches.html",{"batches":context_batches})


@institute_login_required
def student_report(request):
    uid = auth.current_user["localId"]
    id = request.GET.get("id")
    content = {}
    institute = dict(db.child("users").child("institutes").child(uid).child("batches").child(id).get().val())
    students = institute["students"]
    all_students = dict(db.child("users").child("students").get().val())
    for student in students:
        content.update({student:{"name":all_students[student]["name"]}})

    classes = 0
    for session in institute["dailyreport"]:
        for student in institute["dailyreport"][session]:
            present = 0
            for session in institute["dailyreport"]:
                if int(institute["dailyreport"][session][student]["attendance"]) == 1:
                    present+=1
            classes+=1
            percentage = (present/classes)*100
            content[student].update({"attendance":percentage})

    return JsonResponse(json.dumps(content),content_type="json/application",safe=False)

def reset_password(request):

    email = request.GET.get("email")
    auth.send_password_reset_email(email)
    content = True
    return JsonResponse(json.dumps(content),content_type="json/application", safe=False)


def geolocation(request):

    lat = request.GET.get("latitude")
    lon = request.GET.get("longitude")
    if auth.current_user is not None:
        uid = auth.current_user["localId"]
        user_type = find_user(uid)
        if user_type == "institutes":
            db.child("users").child("institutes").child(uid).child("geolocation").update({"latitude":lat,"longitude":lon})
    else:
        timestamp = int(datetime.now().timestamp())
        db.child("visitors").child(timestamp).child("geolocation").update({"latitude":lat,"longitude":lon})
        institutes = dict(db.child("users").child("institutes").get().val())
        kms = {}
        for institute in institutes :
            if institutes[institute].get("geolocation") is not None:
                i_lat = float(institutes[institute]["geolocation"]["latitude"])
                i_lon = float(institutes[institute]["geolocation"]["longitude"])
                R = 6373.0
                lat = float(lat)
                lon = float(lon)
                dlon = i_lon - lon
                dlat = i_lat - lat
                a = (sin(dlat/2))**2 + cos(lat) * cos(i_lat) * (sin(dlon/2))**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                distance = R * c
                kms.update({institute:{"name":institutes[institute]["name"],"kms":distance}})
    content = True
    return JsonResponse(json.dumps(content),content_type="json/application",safe=False)


def coming(request):

    return render(request,"comingsoon.html")


def admin(request):
    count = {}
    hits = dict(db.child("hits").get().val())
    for hit in hits:
        date = datetime.fromtimestamp(int(hit)).date()
        if count.get(str(date)) is None:
            count.update({str(date):0})
        else:
            count[str(date)]+=1
    row = ""
    for date in count:
        row+="<tr><td>"+date+"</td><td>"+str(count[date])+"</td></tr>"
    return HttpResponse("<table cellspacing='2' border='2'><tr><th>Date</th><th>Hits</th></tr>"+row+"</table>")


def institution_public(request,uid):

    if auth.current_user is not None:
        cid = auth.current_user["localId"]
    all_teachers = dict(db.child("users").child("teachers").get().val())
    institution = dict(db.child("users").child("institutes").child(uid).get().val())
    token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY1NmMzZGQyMWQwZmVmODgyZTA5ZTBkODY5MWNhNWM3ZjJiMGQ2MjEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vdHJlZXRvci03NWIxNCIsImF1ZCI6InRyZWV0b3ItNzViMTQiLCJhdXRoX3RpbWUiOjE1NTYwNjA0MDYsInVzZXJfaWQiOiJqRGRZY2FlQ2diVnVmRGF1UHo0ZlVkYlZpRW4yIiwic3ViIjoiakRkWWNhZUNnYlZ1ZkRhdVB6NGZVZGJWaUVuMiIsImlhdCI6MTU1NjA2MDQwNywiZXhwIjoxNTU2MDY0MDA3LCJlbWFpbCI6InRyaWRlbnRAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbInRyaWRlbnRAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.TCFqZ_Z6DEp8a9yWxJx1w19dsxPR-0iuVdV3vfpZg1DI2Ss4N44Jph7YUrNNk3BFPHjY_Gp6wA5nxrNRZ2eB367sOyzXgyHAxDgOY-fyBI14xtIrV7xK6NZ1VfMG383Mcx6fEVatpZkx1O8XvZ0Ir-d_Fwz0Bw60hTuTLXu9WAjCH-lchnqMAO5qIvMN6Rx0Aay9vcFHJB7IVHgeKg-AWkh2pC1XYkT7jP45gT0BvudmRwH1QyVACsHFJQ6QQ1Gk6vgkW0UyaAr_N3Hz1Gj4T0QyWD0x7BO3fVwkpUQOa0lyE4GWl7o9Zw3UCk5NUI4fgLsm_rJ3IeYV5TIr7ImS9w"
    image = storage.child("users").child("institutes").child(uid).child(uid).get_url(token)
    r = requests.get(image)
    if r.status_code == 404:
        image = "../static/images/enterprise.png"
    teachers_all = dict(db.child("users").child("teachers").get().val())
    name = institution["name"]
    classes = institution["classes"]
    area = institution["area"]
    teachers = institution["number teachers"]
    students = institution["number students"]
    email = institution["email"]
    type1 = institution["type"]
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
    courses_context = {}
    institution_data = {"name":name,"classes":classes,"area":area,"teachers":teachers,"students":students,"email":email,"type":type1}
    if institution.get("courses") is not None:
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
    btimes = []
    bid = []
    bcourse = []
    if institution.get("batches") is not None:
        for id in institution["batches"]:
            bcourse.append(institution["batches"][id]["course"])
            bid.append(id)
    batches = zip(bcourse,bid)

    students_context = {}
    all_students = dict(db.child("users").child("students").get().val())
    time = institution["signup time"]
    month = str(int(time[5:7])+6)
    time = time[:4]+"/"+month+"/"+time[8:] + " 00:00:00"
    pending = institution["students"]
    pending_count = 0
    for student in pending:
        if pending[student] == 0:
            pending_count+=1
    if pending_count == 0:
        pending_students = ""
    else:
        pending_students = "( "+str(pending_count) + " )"
    if institution.get("students") is not None:
        for student in institution["students"]:
            if institution["students"][student] == 1:
                students_context.update({student:all_students[student]["name"]})
        return render(request,"institution_public.html",{"time":time,"image":image,"institution":institution_data,"all_teachers":all_teachers_inst,"courses":courses_send,"all_students":students_context,"all_course":course_names,"batches":batches})
    else:
        return render(request,"institution_public.html",{"time":time,"image":image,"institution":institution_data,"courses":courses_send,"all_students":students_context,"all_course":course_names,"batches":batches})


def edit_course(request):

    uid = auth.current_user["localId"]
    course = request.GET.get("course_name")
    content = dict(db.child("users").child("institutes").child(uid).child("courses").child(course).get().val())
    return JsonResponse(json.dumps(content),content_type="json/application",safe=False)


def fetch_batch(request):

    
    content = True
    return JsonResponse(json.dumps(content),content_type="json/application",safe=False)

def batch_timings(request):

    uid = auth.current_user["localId"]
    batch = request.GET.get("batch")
    subject = request.GET.get("subject")
    timings = json.loads(request.GET.get("timings"))
    endtimings = json.loads(request.GET.get("endtimings"))
    for i in (timings):
        if timings[i] is not "":
            db.child("users").child("institutes").child(uid).child("batches").child(batch).child("subjects").child(subject).child("timings").child(i).update({timings[i]:endtimings[i]})

    content = True
    return JsonResponse(json.dumps(content),content_type="json/application",safe=False)
'''
    Android APIs
'''
import calendar
from datetime import datetime
import sys
def batches(request):

    uid = request.GET.get("uid")
    date = request.GET.get("date")
    date = date.split("/")
    dt = datetime(int(date[0]),int(date[1]),int(date[2]))
    day = calendar.day_name[dt.weekday()].lower()
    this = dict(db.child("users").child("teachers").child(uid).get().val())
    all_institutes = dict(db.child("users").child("institutes").get().val())
    send_batches = []
    for institute in this["institutes"]:
        unit = all_institutes[institute]["batches"]
        for batch in unit:
            for subject in unit[batch]["subjects"]:
                print(unit[batch]["subjects"][subject])
                timing = unit[batch]["subjects"][subject]["timings"]
                if uid == unit[batch]["subjects"][subject]["teacher"] and timing.get(day) is not None:
                    start = int(str(list(timing[day].keys())[0])[:2])
                    end = int(str(timing[day][str(list(timing[day].keys())[0])])[:2])
                    duration = end-start
                    subject_name = all_institutes[institute]["subjects"][subject]["subject"] + " " + all_institutes[institute]["subjects"][subject]["standard"]
                    if unit[batch]["subjects"][subject].get("daily") is not None:
                        daily = unit[batch]["subjects"][subject].get("daily")
                        last_class = daily[list(daily.keys())[len(daily)-1]]["taught"]
                        next = daily[list(daily.keys())[len(daily)-1]]["next"]
                    else:
                        last_class = "-"
                    send_batches.append({"time":str(list(timing[day].keys())[0]),"subject":subject_name,"subject_id":subject,"duration":duration,"venue":all_institutes[institute]["name"],"last":last_class,"next":next,"uid":institute,"batch":batch})
    return JsonResponse(send_batches,safe=False)

def batch_students(request):

    send_students = []
    uid = request.GET.get("uid")
    batch_id = request.GET.get("batch")
    this = dict(db.child("users").child("institutes").child(uid).get().val())
    students = dict(db.child("users").child("students").get().val())
    batch = this["batches"][batch_id]["students"]
    for student in batch:
        send_students.append({"id":student,"name":students[student]["name"]})
    return JsonResponse(send_students,safe=False)

@csrf_exempt
def set_attendance(request):

    body = json.loads(request.GET.get("data"))
    institute = request.GET.get("uid")
    batch = request.GET.get("batch")
    subject_id = request.GET.get("subject_id")
    now = str(int(datetime.now().timestamp()))
    try:
        latest = dict(db.child("users").child("institutes").child(institute).child("batches").child(batch).child("subjects").child(subject_id).child("daily").child(now).get().val())
        if int(now) - int(list(latest.keys())[0]) < 3000:
            return JsonResponse([False],safe=False)
    except TypeError:
        pass
    for student in body :
        db.child("users").child("institutes").child(institute).child("batches").child(batch).child("subjects").child(subject_id).child("daily").child(now).child("attendance").update({student:body[student]})
    return JsonResponse([True],safe=False)

def set_rating(request):

    body = json.loads(request.GET.get("data"))
    institute = request.GET.get("uid")
    batch = request.GET.get("batch")
    teach = request.GET.get("teach")
    next = request.GET.get("next")
    subject = request.GET.get("subject")
    print(institute,batch,teach,next)
    now = str(int(datetime.now().timestamp()))
    student = list(body.keys())[0]
    latest = dict(db.child("users").child("institutes").child(institute).child("batches").child(batch).child("subjects").child(subject).child("daily").get().val())
    latest = list(latest.keys())[0]
    db.child("users").child("institutes").child(institute).child("batches").child(batch).child("subjects").child(subject).child("daily").child(latest).update({"taught":teach,"next":next})
    try:

        latest = dict(db.child("users").child("students").child(student).child("institutes").child(institute).child(batch).child("ratings").get().val())
        if int(now) - int(list(latest.keys())[0]) < 3000:
            return JsonResponse([True],safe=False)
    except TypeError:
        pass
    for student in body :
        db.child("users").child("students").child(student).child("institutes").child(institute).child(batch).child("ratings").child(now).update({"rate":body[student]})
    return JsonResponse([True],safe=False)

def get_students_batch(request):

    uid = request.GET.get("uid")
    date = request.GET.get("date")
    date = date.split("/")
    dt = datetime(int(date[0]),int(date[1]),int(date[2]))
    day = calendar.day_name[dt.weekday()].lower()
    institutes = dict(db.child("users").child("institutes").get().val())
    students = dict(db.child("users").child("students").get().val())
    student = students[uid]
    student_instiutes = student["institutes"]
    send_batches = []
    teachers = db.child("users").child("teachers").get().val()
    for institute in student_instiutes:
        for batch in institutes[institute]["batches"]:
            rating = 0
            total = 0
            if student["institutes"][institute].get(batch) is not None:
                for instance in student["institutes"][institute][batch]["ratings"]:
                    rating+=float(student["institutes"][institute][batch]["ratings"][instance]["rate"])
                    total+=1
                average_rating = rating/total
            else:
                average_rating = "-"
            present = 0
            total = 0
            unit = institutes[institute]["batches"][batch]
            for subject in institutes[institute]["batches"][batch]["subjects"]:
                teacher = institutes[institute]["batches"][batch]["subjects"][subject]["teacher"]
                teacher = teachers[teacher]["name"]
                timing = unit["subjects"][subject]["timings"]
                if uid in unit["students"] and timing.get(day) is not None:
                    if institutes[institute]["batches"][batch]["subjects"][subject].get("daily") is not None:
                        for instance in institutes[institute]["batches"][batch]["subjects"][subject]["daily"]:
                            if institutes[institute]["batches"][batch]["subjects"][subject]["daily"][instance]["attendance"][uid] == "1":
                                present+=1
                            total+=1
                        percent = present*100/total
                    start = int(str(list(timing[day].keys())[0])[:2])
                    end = int(str(timing[day][str(list(timing[day].keys())[0])])[:2])
                    duration = end-start
                    subject_name = institutes[institute]["subjects"][subject]["subject"] + " " + institutes[institute]["subjects"][subject]["standard"]
                    if unit["subjects"][subject].get("daily") is not None:
                        daily = unit["subjects"][subject].get("daily")
                        print(list(daily.keys()))
                        last_class = daily[list(daily.keys())[len(daily)-1]]["taught"]
                        next = daily[list(daily.keys())[len(daily)-1]]["next"]
                    else:
                        last_class = "-"
                    send_batches.append({"time":str(list(timing[day].keys())[0]),"subject":subject_name,"subject_id":subject,"duration":duration,"venue":institutes[institute]["name"],"last":last_class,"next":next,"uid":institute,"batch":batch,"attendance":percent,"teacher":teacher,"average":average_rating})
    return JsonResponse(send_batches,safe=False)

def all_students_teacher(request):
    '''
    institute standard name
    '''
    send = []
    uid = request.GET.get("uid")
    institutes = dict(db.child("users").child("institutes").get().val())
    students = dict(db.child("users").child("students").get().val())
    this = dict(db.child("users").child("teachers").child(uid).child("institutes").get().val())
    for institute in this:
        for batch in institutes[institute]["batches"]:
            students_temp = {}
            present = 0
            total = 0
            attendance = {}
            for student in institutes[institute]["batches"][batch]["students"]:
                for subject in institutes[institute]["batches"][batch]["subjects"]:
                    if institutes[institute]["batches"][batch]["subjects"][subject]["teacher"] == uid and institutes[institute]["batches"][batch]["subjects"][subject].get("daily") is not None:
                        for instance in institutes[institute]["batches"][batch]["subjects"][subject]["daily"]:
                            if institutes[institute]["batches"][batch]["subjects"][subject]["daily"][instance]["attendance"][student] == "1":
                                present+=1
                            total+=1
                        attendance.update({institutes[institute]["subjects"][subject]["subject"]+"-"+institutes[institute]["subjects"][subject]["standard"] : present*100/total})

                if students[student]["institutes"][institute].get(batch) is not None:
                    rating = 0
                    total = 0
                    for instance in students[student]["institutes"][institute][batch]["ratings"]:
                        rating+=float(students[student]["institutes"][institute][batch]["ratings"][instance]["rate"])
                        total+=1
                    average_rating = rating/total
                else:
                    average_rating = "-"
                students_temp.update({"uid":student,"name":students[student]["name"],"standard":students[student]["class"],"rating":average_rating})
            send.append({"batch":batch,"institute":institute,"institute_name":institutes[institute]["name"],"student":students_temp,"attendance":attendance})
    return JsonResponse(send,safe=False)
