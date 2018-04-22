from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from . import functions
import re,logging
logging.basicConfig(filename='first.log',level=logging.DEBUG, format=' %(asctime)s -%(levelname)s- %(message)s')
logging.disable(logging.CRITICAL)#->Comment this if debugging

def index(request):
    """
    This is the index Page.
    The if statement is true only when the user enters the contact form.
    The entered data is stored in the file.
    """
    if request.method=="POST":
        user_name=request.POST.get("user_name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        functions.save_in_file('/Dashboard/files/messages.txt',user_name,email,subject,message)
        return render(request,'Dashboard/index.html')
    else:
        return render(request,'Dashboard/index.html')


def signup(request):
    """
    Has 2 parts.
    1->If the request method is POST(i.e if the user enters the data and clicks signup):
           Take the contents from the form and writes in the file(signup.txt).
           Login Page is opened.
    2->Else:
            Signup page is opened.
    """
    if request.method=='POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        if not functions.check_if_exist('/Dashboard/files/signup.txt',user_name,email):
            functions.save_in_file('/Dashboard/files/signup.txt',user_name,password,email,phone_number)
            #redirect is used because the url is not changed when render is done..
            return redirect('http://127.0.0.1:8000/index/login/')
        else:
            return HttpResponse("The username is already used.....!")
    else:
        return render(request,'Dashboard/signup.html')


def login(request):
    """
    Has 2 parts.
    1->If the form is not filled it waits and displays the form(else part).
    2->If the form is filled.
           When the login button is clicked then the authentication is done and the respective pages are opened.
    """
    if request.method=='POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if functions.authenticate('/Dashboard/files/signup.txt',user_name,password):
            #Saves the username in session(Dictionary like DataStructure).Saving it in session
            #because we cannot pass 2nd argument to redirect...
            request.session['user_name']=user_name
            return redirect('http://127.0.0.1:8000/index/dashboard/')
        else:
            return HttpResponse("Not Authenticated....!Please Signup First.....!")
    else:    
        return render(request,'Dashboard/login.html')


def dashboard(request):
    return render(request,"Dashboard/dashboard.html",{'user_name':request.session.get('user_name')})

def discussion(request):
    """
    Gets the contents from the file and displays it
    If is executed if the comment is done and sibmitted.
    The else part displays the comments.
    """
    if request.method=='POST':
        comment = request.POST.get('message')
        #Every question has a different file for comments numbered based on their questions.
        #We will take the question number from the url path save the comment in that file.
        functions.save_in_file('/Dashboard/files/discussions/discussion{}.txt'.format(request.get_full_path().split('/')[-2]),comment)
        return HttpResponse(comment)
    else:
        #Since each discussion has its own file for comments we will display the contents only from that file the number is again got from the url path.
        discussions = functions.get_comments('/Dashboard/files/discussions/discussion{}.txt'.format(request.get_full_path().split('/')[-2]))
        return render(request,"Dashboard/discussion.html",{'discussions':discussions,'user_name':request.session.get('user_name'),'length':len(discussions),'question_number':request.get_full_path().split('/')[-2]})

def practice(request):
    """
    Returns the view of practice.html and pass the questions as dictionary.
    """
    questions = functions.get_contents('/Dashboard/files/questions.txt')
    #This was done to remove the Question number from The questions...(see the questions.txt)..to get an idea
    # temp = []
    # for question in questions:
    #     temp.append(question[2:])
    # questions = temp
    #zip with range is required so that there will be the question numbers along with the question.
    #These question numbers will be seen in the url After a question is clicked
    # questions = zip(questions,range(len(questions)))
    questions = (map(lambda x:x.split('|'),questions))#->Thought this one line would be much more efficient than the above lines
    logging.debug(questions)
    return render(request,'Dashboard/practice.html',{'questions':questions})

def question(request):
    """
    Returns the page which displays the questions And waits for user to give the answer.
    The files are opened and the contents the sent to the html file.
    """
    #Get the question selected we can get this from the path(url)
    question_number = request.get_full_path().split('/')[-1]
    #We should pass the Regular expression to the function
    #'#####' -> is used to deifferentiate between records....
    pattern = re.compile(r'\$\${}.*?#####'.format(question_number),re.DOTALL)
    contents = functions.get_contents("/Dashboard/files/question_details.txt",pattern)
    # '#' -> Each feild is separated by #
    contents = contents.split('#')
    # This is the Header(Question)...Which was selected.
    name = functions.get_question("/Dashboard/files/questions.txt",question_number)
    #Pass all as different because it was not working as expected
    return render(request,"Dashboard/question.html",{'task':contents[0],'input_format':contents[1],'output_format':contents[2],'sample_input':contents[3],'sample_output':contents[4],'name':name,'question_number':question_number})

def leaderboard(request):
    return render(request,"Dashboard/leaderboard.html")

def answer(request):
    return render(request,"Dashboard/answer.html",{'question_number':request.get_full_path().split('/')[-2]})

def profile(request):
    return render(request,"Dashboard/profile.html")
