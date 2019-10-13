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
from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    #mobile APIs
    url(r'^get-batches/',views.batches,name="batches"),
    url(r'^get-batch-students/',views.batch_students,name="batch_students"),
    url(r'^get-students-batches/',views.get_students_batch,name="batch_students"),
    url(r'^set-attendance/',views.set_attendance,name="set_attendance"),
    url(r'^set-rating/',views.set_rating,name="set_rating"),
    url(r'^all-students-teacher/',views.all_students_teacher,name="all_students_teacher"),
    url(r'^all-batches/',views.all_batches,name="all_batches"),
    url(r'^batch-students/',views.batch_students,name="batch_students"),
    path("diary-input/", views.diary_input, name="diary_input"),
    path("diary-output/", views.diary_output, name="diary_output"),
    path("mail-viewed/", views.mail_viewed, name="mail_viewed"),
    path("student-auth/", views.student_auth, name="student_auth"),
    path('student-profile/<slug:uid>', views.student_profile, name="student_profile"),

    #Mobile APis
    #admin apis
    url(r'^admin-add/',views.admin_add,name="admin_add"),
    url(r'^admin-submit/',views.admin_submit,name="admin_submit"),
    path('get-admin-batches/',views.get_admin_batches,name="get_admin_batches"),
    #admin apis
    url(r'^edit-timings',views.batch_timings,name="batch_timings"),
    path('institute-form/<slug:uid>',views.link_form,name="link_form"),
    path('add-data/',views.add_data,name="add_data"),
    path('student-form/<slug:uid>',views.student_form,name="student_form"),
    path('teacher-form/<slug:uid>',views.teacher_form,name="teacher_form"),
    path('student-form-submit/<slug:uid_inst>',views.student_form_submit,name="student_form_submit"),
    path('teacher-form-submit/<slug:uid_inst>',views.teacher_form_submit,name="teacher_form_submit"),
    url(r'^institute/(?P<uid>[\w\-]+)',views.institution_public,name="institution_public"),
    url(r'^quiz-response/',views.quiz_response,name="quiz_response"),
    url(r'^geolocation/',views.geolocation,name="geolocation"),
    url(r'^temp/',views.coming,name="temp"),
    url(r'^admin2/',views.admin,name="admin"),
    url(r'^apply/',views.apply,name="apply"),
    url(r'^show-marks/',views.show_response,name="show_response"),
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
    url(r'^batches/',views.batches,name="batches"),
    url(r'^student-report/',views.student_report,name="student_report"),
    url(r'^edit-course/',views.edit_course,name="edit_course"),
    url(r'^institution-courses/',views.institution_courses,name="institution_courses"),
    url(r'^institution-form/',views.link_form,name="institution_form"),
    path('send-mail-institute/<slug:uid>',views.send_mail_institute,name="send_mail_institute"),
    url(r'^institution-submit/',views.institution_submit,name="institution_submit"),
    url(r'^institution-list/',views.institution_list,name="institution_list"),
    url(r'^accept-request/',views.accept_request,name="accept_request"),
    url(r'^institution-teachers/',views.institution_teachers,name="institution_teachers"),
    url(r'^institution-update/',views.institution_update,name="institution_update"),
    url(r'^institution-details/',views.institution_details,name="institution_details"),
    url(r'^change-picture/',views.change_picture,name="change_picture"),
    url(r'^make-teacher/',views.add_as_teacher,name="make_teacher"),
    url(r'^add-subjects/',views.add_subjects,name="aqdd_subjects"),
    url(r'^add-teachers/',views.add_teachers,name="add_teachers"),
    url(r'^students/',views.all_students,name="all_students"),
    url(r'^accept-students/',views.accept_students,name="accept_students"),
    url(r'^suggestion-box/',views.comment_unit,name="comment_unit"),
    url(r'^signup/',views.signup,name="signup"),
    url(r'^reset-password/',views.reset_password,name="reset_password"),
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
from . import views

