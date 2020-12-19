from flask import render_template, url_for, redirect, request, flash
from cmlz_tutoring import app, bcrypt
from cmlz_tutoring.forms import *
from cmlz_tutoring.models import *
import json
from datetime import datetime


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/account', methods=['GET', 'POST'])
def account():
    # Grabbing subjectName from all rows from Subjects table.
    subjectsTable = Subjects.query.with_entities(Subjects.subjectName).all()
    subjects = [subject.subjectName for subject in subjectsTable]
    # Grabbing dataAndTime from all rows from Timeslots table.
    timeslotsTable = Timeslots.query.with_entities(Timeslots.dataAndTime).all()
    timeslots = [timeslot.dataAndTime for timeslot in timeslotsTable]

    eform = EditApptForm()
    eform.editTime.choices = timeslots
    nform = NewApptForm()
    nform.newTime.choices = timeslots
    nform.newSubject.choices = subjects
    cform = CancelApptForm()
    uform = UpdateInformationForm()
    dform = DeleteAccountForm()

    student = Students.query.filter_by(userName=request.args['username']).first()
    mess = request.args['mess']
    
    # new appoitnment request
    if request.method == 'POST' and nform.validate_on_submit() and nform.nsubmit.data:
        message="NA"
        time = Timeslots.query.filter_by(dataAndTime=nform.newTime.data).first()
        tID = time.timeslotID
        subject = Subjects.query.filter_by(subjectName=nform.newSubject.data).first()
        sID = subject.subjectID
        date = nform.newDate.data
        cExist = Classes.query.filter_by(apptdate=date, subjectID=sID, timeslotID=tID).first()
        if cExist is None:
            newc = Classes(subjectID=sID, timeslotID=tID, apptdate=date, maxStudent=False, maxTutor=False)
            db.session.add(newc)
            db.session.commit()
            cID = newc.classID
            stuID = student.studentID
            newsc = StudentsClasses(studentID=stuID, classID=cID)
            db.session.add(newsc)
            db.session.commit()
            # print(newc.classID, newsc.studentClassID, flush=True)
        else:
            stuID = student.studentID
            existc = Classes.query.filter_by(apptdate=date, subjectID=sID, timeslotID=tID).first()
            cID= existc.classID
            # check uniqueness of class and student in StudentsClasses
            csCheck = StudentsClasses.query.filter_by(classID=cID, studentID=stuID).count()
            if csCheck > 0:
                message = "You're already registered for that class!"
                return redirect(url_for('account', username=student.userName, mess=message))
            # check if class is at max
            cstudents = StudentsClasses.query.filter_by(classID=cID).count()
            smax = subject.maxStudentNum
            atMax = existc.maxStudent
            if not atMax and cstudents < smax:
                newsc = StudentsClasses(studentID=stuID, classID=cID)
                db.session.add(newsc)
                db.session.commit()
            elif not atMax and cstudents == smax:
                existc.maxStudent = True
                db.session.commit()
                message = "We're sorry, that class is full. Please select a different day and/or time."
            else:
                message = "We're sorry, that class is full. Please select a different day and/or time."
        return redirect(url_for('account', username=student.userName, mess=message))
    
    # edit student info request
    if request.method == 'POST' and uform.validate_on_submit() and uform.usubmit.data:
        newfname = uform.newFirstName.data
        newuname = uform.newUserName.data
        if len(newfname) == 0 and len(newuname) == 0:
            message = "No updates were made."
        else:
            message = "Updates made to: "
            if len(newfname) > 0:
                student.firstName = newfname
                db.session.commit()
                message = message + "first name     "
            if len(newuname) > 0:
                student.userName = newuname
                db.session.commit()
                message = message + "user name"
        return redirect(url_for('account', username=student.userName, mess=message))
    
    # delete account request
    if request.method == 'POST' and dform.validate_on_submit() and dform.delsubmit.data:
        print("Inside delete form", flush=True)
        # find all studentsclasse
        allsclasses = StudentsClasses.query.filter_by(studentID=student.studentID)
        for each in allsclasses:
            cID=each.classID
            StudentsClasses.query.filter_by(studentID=student.studentID, classID=cID).delete()
            db.session.commit()
            cstudents = StudentsClasses.query.filter_by(classID=cID).count()
            if cstudents == 0:
                # delete from tutorsClasses
                tutorclass = TutorsClasses.query.filter_by(classID=cID)
                for tclass in tutorclass:
                    tID = tclass.tutorClassID
                    TutorsClasses.query.filter_by(tutorClassID=tID).delete()
                    db.session.commit()
                # delete class
                Classes.query.filter_by(classID=cID).delete()
                db.session.commit()
        # delete student
        Students.query.filter_by(studentID=student.studentID).delete()
        db.session.commit()
        return redirect(url_for('home'))
    
    # edit appointment request
    if request.method == 'POST' and eform.validate_on_submit() and eform.esubmit.data:
        print("Inside edit form", flush=True)
        message="NA"
        months = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
        stuID = student.studentID
        oldD = eform.oldDate.data
        month = oldD[4:7]
        oldD2 = oldD[11:15]+'-'+months[month]+'-'+oldD[8:10]
        oldT = oldD[16:21]
        oldS = eform.oldSubject.data
        eDate = eform.editDate.data
        eTime = eform.editTime.data
        time = Timeslots.query.filter_by(dataAndTime=oldT).first()
        tID = time.timeslotID
        subject = Subjects.query.filter_by(subjectName=oldS).first()
        sID = subject.subjectID
        cExist = Classes.query.filter_by(apptdate=oldD2, subjectID=sID, timeslotID=tID).first()
        if cExist is None:
            message = "We're sorry, we cannot find a record of that class."
            return redirect(url_for('account', username=student.userName, mess=message))
        else:
            cID = cExist.classID
            stuID = student.studentID
            newTime = Timeslots.query.filter_by(dataAndTime=eTime).first()
            ntID = newTime.timeslotID
            # verify not already in the class.
            cExist2 = Classes.query.filter_by(apptdate=eDate, subjectID=sID, timeslotID=ntID).first()
            if cExist2 is not None:
                cID2 = cExist2.classID
                inClass = StudentsClasses.query.filter_by(classID=cID2, studentID=stuID).count()
                if inClass > 0:
                    message = "You're already registered for that class."
                    return redirect(url_for('account', username=student.userName, mess=message))
            # if only student in class, update. Otherwise, create new class and insert into studentsclasses
            cstudents = StudentsClasses.query.filter_by(classID=cID).count()
            if cstudents == 1 and cExist2 is None:
                db.session.commit()
                cExist.apptdate = eDate
                db.session.commit()
                cExist.timeslotID = ntID
                db.session.commit()
            elif cstudents == 1 and cExist2 is not None:
                # verify not at maxStudent
                cID2 = cExist2.classID
                cstudents = StudentsClasses.query.filter_by(classID=cID2).count()
                smax = subject.maxStudentNum
                atMax = cExist2.maxStudent
                # if so unable due to being at max and return
                if atMax:
                    message = "Sorry, this class is full. Please select a different date and/or time."
                    return redirect(url_for('account', username=student.userName, mess=message))
                # otherwise, delete from studentsclasses, delete from classes, and add new
                StudentsClasses.query.filter_by(classID=cID, studentID=stuID).delete()
                db.session.commit()
                Classes.query.filter_by(classID=cID).delete()
                db.session.commit()
                newsc = StudentsClasses(studentID=stuID, classID=cID2)
                db.session.add(newsc)
                db.session.commit()
            elif cstudents > 1:
                newc = Classes(subjectID=sID, timeslotID=ntID, apptdate=eDate, maxStudent=False, maxTutor=False)
                db.session.add(newc)
                db.session.commit()
                newcID = newc.classID
                newsc = StudentsClasses(studentID=stuID, classID=newcID)
                db.session.add(newsc)
                db.session.commit()
                # check if at maxStudent and update accordingly
                cstudents = StudentsClasses.query.filter_by(classID=cID).count()
                smax = subject.maxStudentNum
                atMax = existc.maxStudent
                if atMax and cstudents < smax:
                    cExist.maxStudent = False
                    db.session.commit()
            return redirect(url_for('account', username=student.userName, mess=message))
    
    # cancel appt request
    if request.method == 'POST' and cform.validate_on_submit() and cform.submit.data:
        classInfo = cform.delDate.data
        stuID = student.studentID
        StudentsClasses.query.filter_by(studentID=stuID, classID=classInfo).delete()
        db.session.commit()
        cstudents = StudentsClasses.query.filter_by(classID=classInfo).count()
        if cstudents < 1:
            TutorsClasses.query.filter_by(classID=classInfo).delete()
            db.session.commit()
            Classes.query.filter_by(classID=classInfo).delete()
            db.session.commit()
        return redirect(url_for('account', username=student.userName, mess="NA"))
    
    # get request student info and appointments for display
    name = student.firstName
    test=StudentsClasses.query.filter_by(studentID=student.studentID).all()
    appointments =[]
    calAppt= []
    for row in test:
        rc = row.classID
        cinfo = Classes.query.filter_by(classID=rc).first()
        fulldate = cinfo.apptdate
        tID= cinfo.timeslotID
        subID = cinfo.subjectID
        time = Timeslots.query.filter_by(timeslotID=tID).first()
        asub = Subjects.query.filter_by(subjectID=subID).first()
        sname = asub.subjectName
        thetime = (time.dataAndTime).strftime("%H:%M")
        caldate = fulldate.strftime("%Y-%m-%d")+' '+thetime
        wday = fulldate.strftime("%a")
        d = caldate[8:10]
        m = caldate[5:7]
        tempA = {'day': d,'month': m, 'subject': sname, 'weekday': wday, 'time': thetime, 'notes': 'N/A', 'cID': rc}
        tempC = {'subject': sname, 'date': caldate}
        appointments.append(tempA)
        calAppt.append(tempC)
        print(mess, flush=True)
    return render_template('account.html', name=name, calAppt=calAppt, appointments=appointments,
                           eform=eform, nform=nform, cform=cform, uform=uform, dform=dform, mess=mess, username=student.userName)


@app.route('/lessons', methods=['GET', 'POST'])
def lessons():
    cform = CancelApptForm()
    aform = TutorApptForm()
    uform = UpdateInformationForm()
    dform = DeleteAccountForm()
    # print('After render_template  cform:', cform.submit.data, ' aform:', aform.tsubmit.data, flush=True)
    tutor = Tutors.query.filter_by(userName=request.args['username']).first()
    name = tutor.firstName
    subject = Subjects.query.filter_by(subjectName=tutor.tutorSubject).first()
    subID = subject.subjectID
    sn =subject.subjectName
    
    # cancel appointment request
    if request.method == 'POST' and cform.submit.data and cform.validate_on_submit():
        months = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
        info = cform.delDate.data
        y = info[11:15]
        m = info[4:7]
        d = info[8:10]
        date = y+'-'+months[m]+'-'+d
        t = info[16:21]
        timerow = Timeslots.query.filter_by(dataAndTime=t).first()
        tID = timerow.timeslotID
        canclass = Classes.query.filter_by(apptdate=date, subjectID=subID, timeslotID=tID).first()
        ccID = canclass.classID
        tutID = tutor.tutorID
        TutorsClasses.query.filter_by(tutorID=tutID, classID=ccID).delete()
        db.session.commit()
        return redirect(url_for('lessons', username=tutor.userName))
    
    # accept new appointment request
    if request.method == 'POST' and aform.tsubmit.data and aform.validate_on_submit():
        cID = aform.addDate.data
        print(cID, flush=True)
        tutID = tutor.tutorID
        newtc = TutorsClasses(tutorID=tutID, classID=cID)
        db.session.add(newtc)
        db.session.commit()
        return redirect(url_for('lessons', username=tutor.userName))
    
    # update tutor info request
    if request.method == 'POST' and uform.validate_on_submit() and uform.usubmit.data:
        newfname = uform.newFirstName.data
        newuname = uform.newUserName.data
        if len(newfname) == 0 and len(newuname) == 0:
            message = "No updates were made."
        else:
            message = "Updates made to: "
            if len(newfname) > 0:
                tutor.firstName = newfname
                db.session.commit()
                message = message + "first name     "
            if len(newuname) > 0:
                tutor.userName = newuname
                db.session.commit()
                message = message + "user name"
        return redirect(url_for('lessons', username=tutor.userName, mess=message))
    
    # delete tutor account
    if request.method == 'POST' and dform.validate_on_submit() and dform.delsubmit.data:
        print("Inside delete form", flush=True)
        # find all studentsclasse
        alltclasses = TutorsClasses.query.filter_by(tutorID=tutor.tutorID)
        for each in alltclasses:
            cID=each.classID
            TutorsClasses.query.filter_by(tutorID=tutor.tutorID, classID=cID).delete()
            db.session.commit()
        # delete student
        Tutors.query.filter_by(tutorID=tutor.tutorID).delete()
        db.session.commit()
        return redirect(url_for('home'))

    # get request tutor appointment info for display
    appointments = []
    openAppts = []
    check = Classes.query.filter_by(subjectID=subID).all()
    test=TutorsClasses.query.filter_by(tutorID=tutor.tutorID).all()
    for row in test:
        rc = row.classID
        cinfo = Classes.query.filter_by(classID=rc).first()
        fulldate = cinfo.apptdate
        tID= cinfo.timeslotID
        time = Timeslots.query.filter_by(timeslotID=tID).first()
        thetime = (time.dataAndTime).strftime("%H:%M")
        caldate = fulldate.strftime("%Y-%m-%d")+' '+thetime
        temp = {'subject': sn, 'date': caldate}
        appointments.append(temp)
        # print(temp, flush=True)
    for row in check:   
        rc = row.classID 
        cExist = TutorsClasses.query.filter_by(classID=rc).first()
        if cExist is None:
            fulldate = row.apptdate
            wday = fulldate.strftime("%a")
            tID = row.timeslotID
            time = Timeslots.query.filter_by(timeslotID=tID).first()
            theTime = time.dataAndTime.strftime("%H:%M")
            d = fulldate.strftime("%d")
            m = fulldate.strftime("%b")
            temp ={'subject': sn, 'day': d, 'month': m, 'weekday': wday, 'time': theTime, 'cID': rc }
            openAppts.append(temp)
    # print(appointments, flush=True)
    # print(openAppts, flush=True)
    return render_template('lessons.html', username=tutor.userName, name=name, cform=cform, aform=aform, uform=uform, dform=dform, appointments=appointments, openAppt=openAppts)
  

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None

    # Handling any direct attempts at accessing /admin route.
    if request.method == 'GET':
        return redirect(url_for('home'))

    # Handling all POST requests.
    if request.method == 'POST' and not request.form.get('userName'):
        if request.form.get('modalDeleteStudent'):
            # Getting studentID.
            studentInfo = [request.form.get('modalDeleteStudent')]
            currentView = delete_student(studentInfo)
        elif request.form.get('modalDeleteTutor'):
            # Getting tutorID.
            tutorInfo = [request.form.get('modalDeleteTutor')]
            currentView = delete_tutor(tutorInfo)
        elif request.form.get('addSubject'):
            # Getting new subject info from the form.
            subjectInfo = [request.form.get('subjectName').lower().title(),
                           request.form.get('maxStudent'),
                           request.form.get('maxTutor')]
            error = add_subject(subjectInfo)
            currentView = 'subjects'
        elif request.form.get('modalEditSubject'):
            # Getting updated subject info from the form.
            subjectInfo = [request.form.get('modalEditSubject').lower().title(),
                           request.form.get('subjectName').lower().title(),
                           request.form.get('maxStudent'),
                           request.form.get('maxTutor')]
            error = edit_subject(subjectInfo)
            currentView = 'subjects'
        elif request.form.get('modalDeleteSubject'):
            # Getting subject info from the form
            subjectInfo = [request.form.get('modalDeleteSubject')]
            currentView = delete_subject(subjectInfo)
        elif request.form.get('addTimeslot'):
            # Getting new timeslot info from the form.
            timeslotInfo = [request.form.get('newTimeslot')]
            error = add_timeslot(timeslotInfo)
            currentView = 'timeslots'
        elif request.form.get('modalEditTimeslot'):
            # Getting updated timeslot info from the form.
            timeslotInfo = [request.form.get('modalEditTimeslot'),
                            request.form.get('timeslot')]
            error = edit_timeslot(timeslotInfo)
            currentView = 'timeslots'
        elif request.form.get('modalDeleteTimeslot'):
            # Getting timeslot info from the form.
            timeslotInfo = [request.form.get('modalDeleteTimeslot')]
            currentView = delete_timeslot(timeslotInfo)
        elif request.form.get('modalEditClassTutor'):
            classTutorInfo = [request.form.get('originalTutorID'),
                              request.form.get('modalEditClassTutor'),
                              request.form.get('newTutorID')]
            currentView = edit_class_tutor(classTutorInfo)
        elif request.form.get('modalDeleteClass'):
            classInfo = [request.form.get('modalDeleteClass')]
            delete_classes(classInfo)
            db.session.commit()
            currentView = 'classes'
        else:
            return 'Hmmm you should not be seeing this!'
    else:
        currentView = None

    # Getting all rows from Students, Tutors, Subjects, Timeslots, and Classes tables
    students = get_all_students()
    tutors = get_all_tutors()
    subjects = get_all_subjects()
    timeslots = get_all_timeslots()
    classes = get_all_classes()

    return render_template('admin.html', students=students, tutors=tutors, subjects=subjects,
                           timeslots=timeslots, classes=classes, currentView=currentView, error=error)


def delete_student(studentInfo):
    studentID = Students.query.filter_by(userName=studentInfo[0]).first().studentID
    # Deleting student from all studentClasses rows.
    studentsClassesID = [row.studentClassID for row in StudentsClasses.query.filter_by(studentID=studentID).all()]
    if studentsClassesID:
        for studentClassID in studentsClassesID:
            StudentsClasses.query.filter_by(studentClassID=studentClassID).delete()
    # Deleting student from Students Table.
    Students.query.filter_by(userName=studentInfo[0]).delete()
    db.session.commit()
    return 'students'


def delete_tutor(tutorInfo):
    tutorID = Tutors.query.filter_by(userName=tutorInfo[0]).first().tutorID
    # Deleting student from all studentClasses rows.
    tutorsClassesID = [row.tutorClassID for row in TutorsClasses.query.filter_by(tutorID=tutorID).all()]
    if tutorsClassesID:
        for tutorClassID in tutorsClassesID:
            TutorsClasses.query.filter_by(tutorClassID=tutorClassID).delete()
    # Deleting student from Tutors Table.
    Tutors.query.filter_by(userName=tutorInfo[0]).delete()
    db.session.commit()
    return 'tutors'


def add_subject(subjectInfo):
    if not Subjects.query.filter_by(subjectName=subjectInfo[0]).first():
        subject = Subjects(subjectName=subjectInfo[0], maxStudentNum=subjectInfo[1], maxTutorNum=subjectInfo[2])
        db.session.add(subject)
        db.session.commit()
        return None
    else:
        return 'SUB_ADD'


def edit_subject(subjectInfo):
    if not Subjects.query.filter_by(subjectName=subjectInfo[1]).first() or subjectInfo[0] == subjectInfo[1]:
        subject = Subjects.query.filter_by(subjectName=subjectInfo[0]).first()
        subject.subjectName = subjectInfo[1]
        subject.maxStudentNum = subjectInfo[2]
        subject.maxTutorNum = subjectInfo[3]
        update_tutor_subject('edit', subjectInfo[0], subjectInfo[1])
        db.session.commit()
        return None
    else:
        return 'SUB_EDIT'


def delete_subject(subjectInfo):
    subjectID = Subjects.query.filter_by(subjectName=subjectInfo[0]).first().subjectID
    # Grabbing IDs of classes that have the subject.
    classInfo = [row.classID for row in Classes.query.filter_by(subjectID=subjectID).all()]
    if classInfo:
        delete_classes(classInfo)
    # Deleting subject from db.
    Subjects.query.filter_by(subjectName=subjectInfo[0]).delete()
    # Deleting any tutors that taught this subject
    update_tutor_subject('delete', subjectInfo[0])
    db.session.commit()
    return 'subjects'


def add_timeslot(timeslotInfo):
    if not Timeslots.query.filter_by(dataAndTime=timeslotInfo[0]).first():
        timeslot = Timeslots(dataAndTime=timeslotInfo[0])
        db.session.add(timeslot)
        db.session.commit()
        return None
    else:
        return 'TS_ADD'


def edit_timeslot(timeslotInfo):
    if not Timeslots.query.filter_by(dataAndTime=timeslotInfo[1]).first() or timeslotInfo[0] == timeslotInfo[1]:
        timeslot = Timeslots.query.filter_by(dataAndTime=timeslotInfo[0]).first()
        timeslot.dataAndTime = timeslotInfo[1]
        db.session.commit()
        return None
    else:
        return 'TS_EDIT'


def delete_timeslot(timeslotInfo):
    timeslotID = Timeslots.query.filter_by(dataAndTime=timeslotInfo[0]).first().timeslotID
    # Grabbing IDs of classes that have the timeslot.
    classInfo = [row.classID for row in Classes.query.filter_by(timeslotID=timeslotID).all()]
    if classInfo:
        delete_classes(classInfo)
    # Deleting timeslot from db.
    Timeslots.query.filter_by(dataAndTime=timeslotInfo[0]).delete()
    db.session.commit()
    return 'timeslots'


def edit_class_tutor(classTutorInfo):
    if classTutorInfo[0]:
        originalTutorClass = TutorsClasses.query.filter_by(tutorID=classTutorInfo[0], classID=classTutorInfo[1]).first()
        originalTutorClass.tutorID = classTutorInfo[2]
        db.session.commit()
    else:
        newTutorClass = TutorsClasses(tutorID=classTutorInfo[2], classID=classTutorInfo[1])
        db.session.add(newTutorClass)
        db.session.commit()
    return 'classes'


def get_all_students():
    students = []
    studentsTable = Students.query.with_entities(Students.firstName, Students.lastName, Students.email,
                                                 Students.userName).all()
    for row in studentsTable:
        student = {'firstName': row[0],
                   'lastName': row[1],
                   'email': row[2],
                   'username': row[3]}
        students.append(student)
    return students


def get_all_tutors():
    tutors = []
    tutorsTable = Tutors.query.with_entities(Tutors.tutorID, Tutors.firstName, Tutors.lastName, Tutors.email,
                                             Tutors.userName, Tutors.tutorSubject).all()
    for row in tutorsTable:
        if row[4] != 'admin':
            tutor = {'firstName': row[1],
                     'lastName': row[2],
                     'email': row[3],
                     'username': row[4],
                     'subject': row[5]}
            tutors.append(tutor)
    return tutors


def get_all_subjects():
    subjects = []
    subjectsTable = Subjects.query.with_entities(Subjects.subjectName, Subjects.maxStudentNum, Subjects.maxTutorNum).all()
    for row in subjectsTable:
        subject = {'name': row[0],
                   'maxStudent': row[1],
                   'maxTutor': row[2]}
        subjects.append(subject)
    return subjects


def get_all_timeslots():
    timeslots = []
    timeslotsTable = Timeslots.query.with_entities(Timeslots.dataAndTime).all()
    for row in timeslotsTable:
        timeslot = {'start': row[0]}
        timeslots.append(timeslot)
    return timeslots


def get_all_classes():
    classes = []
    classesTable = Classes.query.with_entities(Classes.classID, Classes.subjectID, Classes.timeslotID,
                                               Classes.maxStudent, Classes.maxTutor, Classes.apptdate).all()
    for row in classesTable:
        # Grabbing all students-classes rows for current class, then grabbing the students' first and last names.
        studentsClasses = [row.studentID for row in StudentsClasses.query.filter_by(classID=row[0]).all()]
        studentsInClass = [Students.query.filter_by(studentID=student).first().firstName + ' '
                        + Students.query.filter_by(studentID=student).first().lastName
                        for student in studentsClasses]

        # Grabbing all tutors-classes rows for current class, then grabbing the tutors' first and last names.
        tutorsClasses = [row.tutorID for row in TutorsClasses.query.filter_by(classID=row[0]).all()]
        tutorsInClass = {}
        for tutor in tutorsClasses:
            tutorsInClass[Tutors.query.filter_by(tutorID=tutor).first().firstName + ' ' + Tutors.query.filter_by(tutorID=tutor).first().lastName] = tutor

        # Grabbing class-specific info of subject, timeslot and tutors able to teach it.
        subject = Subjects.query.filter_by(subjectID=row[1]).first().subjectName
        timeslot = Timeslots.query.filter_by(timeslotID=row[2]).first().dataAndTime
        availableTutorsDict = {}
        tutorsTable = Tutors.query.with_entities(Tutors.tutorID, Tutors.firstName, Tutors.lastName, Tutors.email,
                                             Tutors.userName, Tutors.tutorSubject).all()
        for tutorRow in tutorsTable:
            if tutorRow[4] != 'admin' and tutorRow[5] == subject:
                availableTutorsDict[tutorRow[1] + ' ' + tutorRow[2]] = tutorRow[0]

        classRow = {'apptdate': datetime.strptime(str(row[5]), '%Y-%m-%d').strftime('%B %d' + ', '+ '%Y'),
                    'classID': row[0],
                    'subject': subject,
                    'timeslot': timeslot,
                    'studentsInClass': studentsInClass,
                    'tutorsInClass': tutorsInClass,
                    'availableTutors': json.dumps(availableTutorsDict)}
        classes.append(classRow)
    return classes


def delete_classes(classInfo):
    for classToDelete in classInfo:
        # Deleting all rows with class from StudentClasses Table.
        studentsClassesID = [row.studentClassID for row in StudentsClasses.query.filter_by(classID=classToDelete).all()]
        if studentsClassesID:
            for studentClassID in studentsClassesID:
                StudentsClasses.query.filter_by(studentClassID=studentClassID).delete()
        # Deleting all rows with class from TutorsClasses Table.
        tutorsClassesID = [row.tutorClassID for row in TutorsClasses.query.filter_by(classID=classToDelete).all()]
        if tutorsClassesID:
            for tutorClassID in tutorsClassesID:
                TutorsClasses.query.filter_by(tutorClassID=tutorClassID).delete()
        # Deleting class from db.
        Classes.query.filter_by(classID=classToDelete).delete()


def update_tutor_subject(function, subjectName, newSubjectName=None):
    if function == 'delete':
        Tutors.query.filter_by(tutorSubject=subjectName).delete()
    elif function == 'edit':
        for tutor in Tutors.query.filter_by(tutorSubject=subjectName).all():
            tutor.tutorSubject = newSubjectName


@app.route('/register-student', methods=['GET', 'POST'])
def register_student():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Students(firstName=form.firstName.data, lastName=form.lastName.data, userName=form.userName.data,
                           email=form.email.data, password=hashed_password)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('account', username=form.userName.data, mess="NA"))
    return render_template('register-student.html', form=form)


@app.route('/register-tutor', methods=['GET', 'POST'])
def register_tutor():
    form = TutorRegistrationForm()

    # Grabbing all rows from Subjects table.
    subjectsTable = Subjects.query.with_entities(Subjects.subjectName).all()
    subjects = [subject.subjectName for subject in subjectsTable]
    subjects.insert(0, '-- Please Choose a Subject --')
    form.tutorSubject.choices = subjects

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        tutor = Tutors(tutorSubject=form.tutorSubject.data, firstName=form.firstName.data, lastName=form.lastName.data,
                       userName=form.userName.data, email=form.email.data, password=hashed_password)
        db.session.add(tutor)
        db.session.commit()
        return redirect(url_for('lessons', username=form.userName.data))
    return render_template('register-tutor.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.userType.data == 'student':
            student = Students.query.filter_by(userName=form.userName.data).first()
            if student and bcrypt.check_password_hash(student.password, form.password.data):
                '''
                In here is where we will route the student their personal account page.
                Right now, a successful login attempt routes them to the student registration page.
                '''
                return redirect(url_for('account', username=form.userName.data, mess="NA"))
            else:
                form.password.errors.append('Username or password incorrect. Check that you are logging in correctly as a student or tutor.')
        elif form.userType.data == 'tutor':
            tutor = Tutors.query.filter_by(userName=form.userName.data).first()
            if tutor.userName == 'admin' and bcrypt.check_password_hash(tutor.password, form.password.data):
                return redirect(url_for('admin'), code=307)
            if tutor and bcrypt.check_password_hash(tutor.password, form.password.data):
                '''
                In here is where we will route the tutor their personal account page.
                Right now, a successful login attempt routes them to the tutor registration page.
                '''
                return redirect(url_for('lessons', username=form.userName.data))
            else:
                form.password.errors.append('Username or password incorrect. Check that you are logging in correctly as a student or tutor.')

    return render_template('login.html', form=form)


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
