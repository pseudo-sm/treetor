"""pdoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^quiz-response/',views.quiz_response,name="quiz_response"),
    url(r'^apply/',views.apply,name="apply"),
    url(r'^show-marks/',views.show_response,name="show_response"),
    url(r'^student-profile/',views.student_profile,name="student_profile"),
    url(r'^search/',views.search,name="search"),
    url(r'^change-picture/',views.change_picture,name="change_picture"),
    url(r'^student-dashboard/',views.student_dashboard,name="student_dashboard"),
    url(r'^student-schedule/',views.student_schedule,name="student_schedule"),
    url(r'^teacher-dashboard/',views.teacher_dashboard,name="teacher_dashboard"),
    url(r'^teacher-profile/',views.teacher_profile,name="teacher_profile"),
    url(r'^basic-update/',views.basic_update,name="basic_update"),
    url(r'^career-update/',views.career_update,name="career_update"),
    url(r'^contact-update/',views.contact_update,name="contact_update"),
    url(r'^personal-update/',views.personal_update,name="personal_update"),
    url(r'^guardian-update/',views.guardian_update,name="guardian_update"),
    url(r'^academic-update/',views.academic_update,name="academic_update"),
    url(r'^top-5/',views.top_5_students,name="top_5_students"),
    url(r'^courses/',views.view_courses,name="courses"),
    url(r'^institution-profile/',views.institution_profile,name="institution_profile"),
    url(r'^add-batch/',views.add_batch,name="add_batch"),
    url(r'^institution-courses/',views.institution_courses,name="institution_courses"),
    url(r'^institution-form/',views.institution_form,name="institution_form"),
    url(r'^institution-submit/',views.institution_submit,name="institution_submit"),
    url(r'^institution-list/',views.institution_list,name="institution_list"),
    url(r'^accept-request/',views.accept_request,name="accept_request"),
    url(r'^institution-teachers/',views.institution_teachers,name="institution_teachers"),
    url(r'^institution-update/',views.institution_update,name="institution_update"),
    url(r'^institution-details/',views.institution_details,name="institution_details"),
    url(r'^change-picture/',views.change_picture,name="change_picture"),
    url(r'^make-teacher/',views.add_as_teacher,name="make_teacher"),
    url(r'^add-courses/',views.add_courses,name="add_courses"),
    url(r'^add-teachers/',views.add_teachers,name="add_teachers"),
    url(r'^students/',views.all_students,name="all_students"),
    url(r'^accept-students/',views.accept_students,name="accept_students"),
    url(r'^suggestion-box/',views.comment_unit,name="comment_unit"),
    url(r'^signup/',views.signup,name="signup"),
    url(r'^post_signup/',views.post_signup,name="post_signup"),
    url(r'^post_signin/',views.post_signin,name="post_signin"),
    url(r'^post_schedule/',views.post_schedule,name="post_schedule"),
    url(r'^schedule/',views.schedule,name="schedule"),
    url(r'^profile-form/',views.profile_form,name="profile_form"),
    url(r'^institution-form/',views.institution_form,name="institution_form"),
    url(r'^signin/',views.signin,name="signin"),
    url(r'^enrollment-form/',views.enrollment_form,name="enrollment_form"),
    url(r'^submit/',views.submit,name="submit"),
    url(r'^profile_submit/',views.profile_submit,name="profile_submit"),
    url(r'^logout',views.logout,name="logout"),
    url(r'^demo',views.demo_request,name="demo_request"),
    url(r'',views.home,name="home"),


]
