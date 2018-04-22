import os,re,logging
logging.basicConfig(filename='first.log',level=logging.DEBUG, format=' %(asctime)s -%(levelname)s- %(message)s')
#logging.disable(logging.CRITICAL)# -> This line stops logging.DEBUG to display....!If you want logging.dubug to display the comment this line...!

def save_in_file(filename,*details):
    """
    Writes the contents in the file(The name is passed as arument)
    get_id -> Return the id for the current insertng record
    '|' -> Is taken as Delimiter between fields.
    '\\n'(New Line) -> Is taken as a Delimiter between records.
    """
    id = str(get_id(filename))
    # path = filename.split('/') This was done to keep it compatible with Windows...
    # filename = os.sep.join(path)
    with open(os.getcwd()+filename,'a') as file:
        for detail in details:
            detail+='|'
            file.write(detail)
        file.write(id)
        file.write('\n')

def authenticate(filename,*credentials):
    """
    Opens the given file and checks for the given data. 
    If present it returns True.
    else returns false.
    """
    #Regular expression to check for username and password.
    #pattern = re.compile('^({0}.*{1})'.format(credentials[0],credentials[1]))->Commented beacause it was not working as expected.
    users = open(os.getcwd()+filename).readlines()
    for user in users:
        details = user.split('|')#'|'->used as delimiter between feilds.
        if credentials[0] == details[0] and credentials[1] == details[1]:#1st feild is user_name the second is password.
            return True
    return False

def get_id(filename):
    """
    Returns the next id in the given file.
    """
    try:
        last_record = open(os.getcwd()+filename).readlines()[-1]
        #Id is the last feild of each record.Hence the max id is the last feild of the last record.
        max_id = last_record.split('|')[-1]
        return int(max_id)+1
    except:
        #This is executed if the file has Zero records i.e 1 will be the id of the first record.
        return 1

def check_if_exist(filename,*data):
    """
    Checks if an email or usrname already exists in file(During signup).
    """
    records = open(os.getcwd()+filename).readlines()
    user_name,password = data[0],data[1]
    for record in records:
        feilds = record.split('|')
        #0th feild is the user_name 2nd feild is the email(These 2 shuould be unique for every record(user)).
        if feilds[0]==user_name or feilds[2]==password:
            return True
    return False

def get_contents(filename,*pattern):
    """
    Returns the contents of the given file.
    """
    if pattern:
        file_contents = open(os.getcwd()+filename).read()
        question = pattern[0].findall(file_contents)[0]
        question = re.sub('#####',"",question)
        question = re.sub(r'\$\$\d',"",question)
        return question
    return open(os.getcwd()+filename).readlines()

def get_comments(filename):
    """
    Returns the contents from the file like the whole html is returned(Used in discussions(see discussion.txt to get an idea)).
    """
    #Regular expression to split each comment '|[1-9]+'->is used as delimiter between record [1-9]->Number of the comment.
    pattern = re.compile(r'\|\d+')
    contents = pattern.split(open(os.getcwd()+filename).read())
    logging.debug(contents)
    return contents

def get_question(filename,question_number):
    """
    Returns the question of the given number
    """
    #Finds all questions with the given question number(There will be only on question with one question_number)
    question = re.findall(r"{}\|.*".format(question_number),open(os.getcwd()+filename).read())
    logging.debug(question)
    # Question is a list of only one element.....question[0]->is the question.....The first 2 digits are the id of the qestion.
    # We remove the first 2 letters and return the rest
    # question = re.sub(r'{}\|'.format(question_number),"",question[0])-> Commented because a better solution was found
    # logging.debug(question)
    return question[0][2:]