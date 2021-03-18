import pytest
import System
import Staff
import Student


#Start of required tests for 7.1

#1 Login - System.py
def test_login(grading_system):
        
        #test user
        username = 'akend3'
        password = '123454321'

        grading_system.login(username,password)
        users = grading_system.users
        user = grading_system.usr
        #Check against json
        assert isinstance(user,Student.Student) == True

        assert users[username]['password'] == user.password
        assert users[username]['courses'] == user.courses
        

#2 Check Password - System.py 
def test_check_password(grading_system):
        passCheck = [('akend3','123454321'), ('hdjsr7', 'pass1234')]
        failCheck = [('akend3','8675309') , ('hdjsr7', 'nevergonnagiveyouup')]

        for user in passCheck:
            assert grading_system.check_password(user[0],user[1]) == True
        for user in failCheck:
            assert grading_system.check_password(user[0],user[1]) == False

#3 Change Grade - Staff.py
def test_change_grade(grading_system):
        users = grading_system.users
        grading_system.login('saab','boomr345')
        grading_system.usr.change_grade('yted91','software_engineering','assignment1',85)
        assert users['yted91']['courses']['software_engineering']['assignment1']['grade'] == 85

#4 Create Assignment - Staff.py
def test_create_assignment(grading_system):
        courses = grading_system.courses
        grading_system.login('saab','boomr345')
        assignment = "Quiz1"
        date_due = '2/20/21'
        course = 'comp_sci'
        grading_system.usr.create_assignment(assignment, date_due, course)
        assert courses[course]['assignments'][assignment]['due_date'] == date_due

#5 Add Student - Professor.py
def test_add_student(grading_system):
    

    grading_system.login('saab','boomr345')
    name = "yted91"
    course = 'comp_sci'
    #fails here. not sure if intentional
    grading_system.usr.add_student(name,course)
    users = grading_system.users
    assert course in users[name]['courses']


#6 Drop Student - Professor.py
def test_drop_student(grading_system):

    grading_system.login('goggins','augurrox')
    teacher = grading_system.usr
    name = "yted91"
    course = "software_engineering"
    teacher.drop_student(name,course)
    users = grading_system.users
    
    try:
        users[name]['courses'][course] 
        assert False
    except KeyError:
        assert True

#7 Submit Assignment - Student.py
def test_submit_assignment(grading_system):
    username = 'akend3'
    password = '123454321'
    grading_system.login(username,password)
    course = 'databases'
    assignment = 'assignment1'
    date = '2/4/20'
    submission = "Student Submission"
    grading_system.usr.submit_assignment(course,assignment,submission,date)
    users = grading_system.users
    
    assert users[username]['courses'][course][assignment]['submission'] == submission
    assert users[username]['courses'][course][assignment]['submission_date'] == date
    assert users[username]['courses'][course][assignment]['ontime'] == False

#8 Check On Time - Student.py
def test_check_ontime(grading_system):
    username = 'akend3'
    password = '123454321'
    grading_system.login(username,password)
    due_date = '1/2/20'
    sub_date =  '1/3/21'
    assert grading_system.usr.check_ontime(due_date,sub_date) == True
    assert grading_system.usr.check_ontime(sub_date,due_date) == False

#9 Check Grades - Student.py
def test_check_grades(grading_system):
    username = 'akend3'
    password = '123454321'
    grading_system.login(username,password)
    course = 'comp_sci'
    grades = grading_system.usr.check_grades(course)
    users = grading_system.users
    
    assert grades == [['assignment1',users[username]['courses'][course]['assignment1']['grade']],['assignment2',users[username]['courses'][course]['assignment2']['grade']]]
    
#10 View Assignments - Student.py
def test_view_assignments(grading_system):
    username = 'akend3'
    password = '123454321'
    grading_system.login(username,password)
    course = 'databases'
    assignments = grading_system.usr.view_assignments(course)
    assert assignments == [['assignment1',"1/6/20"],['assignment2',"2/6/20"]]


#11 View Assignment in class not in
#Student should not be able to view assignments for classes they aren't in 
def test_view_assignments_wrong_class(grading_system):
    username = 'akend3'
    password = '123454321'
    grading_system.login(username,password)
    course = 'cloud_computing'
    assignments = grading_system.usr.view_assignments(course)
    assert assignments == None
    #assignments should be empty, because student is not in cloud computing
    
#12 Password Restrictions
#Check_Password should not accept harmful or malformed passwords (longer than 256 characters)
def test_check_toolong_password(grading_system):
        username = 'akend3'
        password = '8t5Ob8x54fZaiu4l7Apw6sT7bXxvBRrSFTAsvnjsJUC7fOU41sGoNtKTjCDm1IWOMXnUHCwIQVMvJ53b2eICOMlzgXFMXFXJL3fWFkrkX5OgH9t2x40ZVsXILxaldncIiVgax4kvZq1slnCo5GP3qANPqyt1atghPebRLK8UZdipFmwssHRoET7dpZqsPNNK9WAZynQk'

        try: 
            grading_system.check_password(username,password)
            assert False
        except BufferError:
            assert True
                  
#13 Teacher Create assignment for class they don't teach
# A teacher should only be able to create an assignment for a class they teach
def test_create_assignment_wrong_class(grading_system):
        courses = grading_system.courses
        grading_system.login('saab','boomr345')
        assignment = "Quiz1"
        date_due = '3/30/21'
        course = 'databases'
        grading_system.usr.create_assignment(assignment, date_due, course)
        #should be empty, since saab does not teach databases
        assert courses[course]['assignments'][assignment]['due_date'] == None

#14 Submit Check Due Date
#The due date should be not on time, since this assignment was late
def test_submit_assignment_due_date(grading_system):
    username = 'akend3'
    password = '123454321'
    grading_system.login(username,password)
    course = 'databases'
    assignment = 'assignment2'
    date = '2/20/20'
    submission = "Database Assignment 2"
    grading_system.usr.submit_assignment(course,assignment,submission,date)
    
    users = grading_system.users
    assert users[username]['courses'][course][assignment]['ontime'] == False
#15 Check grade - Staff.py
#Staff should not be able to check grades for classes they don't teach 
def test_check_grades_staff(grading_system):
    username = 'saab'
    password = 'boomr345'
    student = 'hdjsr7'
    grading_system.login(username,password)
    course = 'databases'
    grades = grading_system.usr.check_grades(student,course)
    users = grading_system.users
    #should be empty, especially since student isn't in saab's course
    assert grades == None

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem
