from io import FileIO
from sys import path
from django.db.models import constraints
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# Create your views here.
from django.http import HttpResponse,Http404
from django.shortcuts import render, redirect
from .forms import UsersSignupForm, UsersLoginForm
from customauth.models import MyUser
from codeRS.models import Solved, Problem
import datetime
import os

months = {
  1:'Jan',
  2:'Feb',
  3:'Mar',
  4:'Apr',
  5:'May',
  6:'June',
  7:'July',
  8:'Aug',
  9:'Sep',
  10:'Oct',
  11:'Nov',
  12:'Dec'
}

def index(request):
    d = datetime.datetime.now()
    return render(request,'codeRS/signup.html',{'dt':d})
    #return HttpResponse("Hello, world. You're at the codeRS index.")

def pending(request):
    return HttpResponse('<h1>This feature is yet to be implemented</h1>')
def sign(request):
    if request.method == 'POST':
        form = UsersSignupForm(request.POST)
        if form.is_valid()==True:
            if form.is_already_present() == True:
                messages.error(request,'User with this email id already exists') 
            else:
                first_name = form.cleaned_data['name'].split()[0]
                try:
                    last_name =  form.cleaned_data['name'].split()[1]
                except IndexError:
                    last_name = ''
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                usr = MyUser.objects.create_user(
                password = password,
                email = email,
                fname = first_name,
                lname = last_name,
                )
                usr.save()
                messages.success(request,'Account created Successfully. You can login low..')
        else:
            messages.error(request,'Error in one or more form fields') 
    else:
        form = UsersSignupForm()
    return render(request,'codeRS/sign.html')

def dashboard(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    cpp_completed = len(Solved.objects.filter(pid__language='cpp',uid=request.user.id))
    py_completed = len(Solved.objects.filter(pid__language='python',uid=request.user.id))

    py_total = len(Problem.objects.filter(language='python'))
    cpp_total = len(Problem.objects.filter(language='cpp'))
    try:
        cpp_per = int((cpp_completed/cpp_total)*100)
    except ZeroDivisionError:
        cpp_per = 0
    
    try:
        py_per = int((py_completed/py_total)*100)
    except ZeroDivisionError:
        py_per=0
    global months
    xValues = []
    yValues = []
    today = datetime.date.today()
    for i in range(7):
        date = today - datetime.timedelta(days=i)
        problems_solved = Solved.objects.filter(time=date,uid=request.user.id)
        yValues.insert(0,len(problems_solved))
        if i>1:
            xValues.insert(0,str(date.day) + '-' + months[date.month])
        elif i == 0:
            xValues.insert(0,'Today')
        else:
            xValues.insert(0,'Yesterday')
    
    return render(request,'codeRS/index.html',{'x':xValues,'y':yValues,'cppPer':cpp_per,'pyPer':py_per})

def login_(request):
    if request.method == 'POST':
        form = UsersLoginForm(request.POST)
        if form.is_valid()==True:
            print('Form valid')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            usr = authenticate(request,email = email,password=password)
            if usr is not None:
                login(request,usr)
                request.session['email'] = email
                return redirect('/dashboard/')
            messages.error(request,'Invalid credentials')
    return render(request,'codeRS/login.html')

def logout_(request):
    messages.success(request,'Logged out successfully')
    logout(request)
    return redirect("/login/")

def problems(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    print('Inside problems')
    if request.method == 'GET' :
        print('Inside get')
        lang = 'cpp'
        try:
            id_ = request.GET['id']
            if id_ == '1':
                All_unsolved = showProblem(request,'cpp')
                lang = 'cpp'
            elif id_ == '2':
                All_unsolved = showProblem(request,'python')
                lang = 'python'
            else:
                messages.error(request,'Bad request')
                logout(request)
                return redirect("/login/")
            return render(request,'codeRS/questions.html',{'problems':All_unsolved,'language':lang})
        except KeyError:
            print('Not got id')
            return redirect('/dashboard/')
    return redirect('/dashboard/')

def showProblem(request,lang):
    print('Inside show prolm')
    Solved_ids = Solved.objects.filter(pid__language=lang,uid = request.user.id)
    All_unsolved = Problem.objects.filter(language=lang)
    return All_unsolved

def showSignupForm(request):
    if request.method == 'POST':
        fm = UsersSignupForm(request.POST)
        if fm.is_valid()==True:
            print('First Name: ',fm.cleaned_data['first_name'])
            print('Last Name: ',fm.cleaned_data['last_name'])
            print('Password: ',fm.cleaned_data['password'])
            print('Email: ',fm.cleaned_data['email'])
    else:
        fm = UsersSignupForm()
    return render(request,'signup.html',{'form':fm})

def code(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    if request.method == 'GET' or request.method == 'POST': 
        try:
            print('See noi: ',os.getcwd())
            id_ =  request.GET['id']
            path_problem = os.getcwd()+os.sep+'problems'+os.sep+str(id_)
            run_path = path_problem + os.sep + 'run.exe'
            out_path = path_problem + os.sep + 'out.txt'
            f = open(path_problem+os.sep+'starter.txt','r')
            starter = f.read()
            f.close()
            if request.method == 'POST':
                fname=''
                code_content = request.POST.get('code-written','')
                if id_ == '1':
                    fname='submit.cpp'
                else:
                    fname='submit.py'
                f_code = open(path_problem + os.sep + fname,'w')
                f_code.write(code_content)
                f_code.close()
                test_folder_path = path_problem + os.sep + 'TestCases'
                testfile_path = path_problem + os.sep + 'TestCases' + os.sep + 'test.txt'
                status = os.system('g++ ' + path_problem + os.sep + fname +' -o ' + run_path)
                if status == 1:
                    messages.error(request,'Compilation error occurred')

                print(run_path)
                print(testfile_path)
                print(out_path)
                os.system(run_path + '< ' + testfile_path + ' >' + out_path)
                
                f_ref = open(test_folder_path + os.sep + 'ref.txt','r')
                ref_list = f_ref.read().splitlines()
                f_ref.close()

                f_out = open(out_path,'r')
                output_list = f_out.read().splitlines()
                f_out.close()

                for i in range(len(ref_list)):
                    try:
                        ref = ref_list[i]
                        out = output_list[i]
                        if ref == out:
                            print(' Output ',i, 'passed')
                        else:
                            print('MISMATCH')
                    except IndexError:
                        print('Mismatch')
                if ref_list == output_list:
                    User = MyUser.objects.get(pk=request.user.id)
                    User.score += Problem.objects.get(pk=int(id_)).score
                    User.save()

                    solved = Solved(uid = request.user, pid = Problem.objects.get(pk=int(id_)))
                    solved.save()

            print("PAth = ",os.getcwd())
            qset = Problem.objects.get(pk=int(id_))
            key = qset.impKey
            desc = qset.description.replace('<'+key+'>',"<div class='desc-back'>")
            desc = desc.replace('</'+key+'>','</div>')

            sampleout = qset.example.replace('<'+key+'>',"<div class='desc-back'>")
            sampleout = sampleout.replace('</'+key+'>','</div>')

            iformat = qset.inputf.replace('<'+key+'>',"<div class='desc-back'>")
            iformat = iformat.replace('</'+key+'>','</div>')

            oformat = qset.outputf.replace('<'+key+'>',"<div class='desc-back'>")
            oformat = oformat.replace('</'+key+'>','</div>')

            constraints = qset.contraints 

            explanation = qset.explanation.replace('<'+key+'>',"<div class='desc-back'>")
            explanation = explanation.replace('</'+key+'>','</div>')
            return render(request,'codeRS/code.html',{
                'starter':starter,
                'problem':qset,
                'description':desc,
                "example":sampleout,
                'inputf':iformat,
                'outputf':oformat,
                'constraints':constraints,
                'explanation':explanation})
        except KeyError:
            return redirect('/dashboard/')
        except FileNotFoundError:
            os.chdir(r'../..')

    return render(request,'codeRS/code.html')

def download(request):
    if request.user.is_anonymous:
        messages.warning('You are not allowed to access this page')
        return redirect('/login/')
    if request.user.is_admin:
        f = open(os.getcwd()+os.sep+'data'+os.sep+'data.csv','w')
        dates = Solved.objects.order_by().values_list('time').distinct()
        users = Solved.objects.values_list('uid').distinct()
        for date in dates:
            for user in users:
                row = Solved.objects.filter(uid = user[0], time=date[0])
                for val in row:
                    f.write(str(val.pid.id)+',')
                if row:
                    f.write('\n')
        f.close()

        if os.path.exists(os.getcwd()+os.sep+'data'+os.sep+'data.csv'):
            with open(os.getcwd()+os.sep+'data'+os.sep+'data.csv', 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(os.getcwd()+os.sep+'data'+os.sep+'data.csv')
                return response
        raise Http404        
