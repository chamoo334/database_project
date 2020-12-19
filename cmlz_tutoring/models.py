from cmlz_tutoring import db


class Students(db.Model):
    """
    Records the students that require tutoring in whatever classes/subject they need.
    A M:M relationship between Students-Classes will be implemented via an intersection table housing the studentID
and classID as foreign keys.
    """
    studentID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    firstName = db.Column(db.String(60), nullable=False)
    lastName = db.Column(db.String(60), nullable=False)
    userName = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    studentsClasses = db.relationship('StudentsClasses', backref='student', lazy=True)


class Tutors(db.Model):
    """
    Records the tutors that will be assigned to a class in order to tutor the students. Tutors can only tutor a
single subject, but multiple classes of that subject, to ensure proficiency among our staff.
    A M:M relationship between Tutors-Classes will be implemented via an intersection table housing the tutorID
and classID as foreign keys.
    """
    tutorID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    tutorSubject = db.Column(db.String(60), nullable=False)
    firstName = db.Column(db.String(60), nullable=False)
    lastName = db.Column(db.String(60), nullable=False)
    userName = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    tutorsClasses = db.relationship('TutorsClasses', backref='tutor', lazy=True)


class Subjects(db.Model):
    """
    Records the subjects that we offer, and the maximum number of students we will allow to be tutored in a single
class of this subject.
    A 1-M relationship between Subjects-Classes will be implemented with subjectID as the FK inside of Classes.
    """
    subjectID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    subjectName = db.Column(db.String(60), nullable=False, unique=True)
    maxStudentNum = db.Column(db.Integer, nullable=False)
    maxTutorNum = db.Column(db.Integer, nullable=False)
    classes = db.relationship('Classes', backref='subject', lazy=True)


class Timeslots(db.Model):
    """
    Records the timeslot’s date and time.
    A 1-M relationship between Timeslots-Classes will be implemented with timeslotID as the FK inside of Classes.
    """
    timeslotID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    dataAndTime = db.Column(db.Time, nullable=False, unique=True)
    classes = db.relationship('Classes', backref='timeslot', lazy=True)


class Classes(db.Model):
    """
    Records the various classes that we offer, detailing the classes’ timeslot, subject and whether it’s at
capacity for tutors/students.
    A M:M relationship between Students-Classes and Tutors-Classes will be implemented via an intersection table
that is described above. A 1-M relationship between Subjects-Classes and Timeslots-Classes will be implemented with
subjectID and timeslotID as FK inside of Classes.
    """
    classID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    subjectID = db.Column(db.Integer, db.ForeignKey('subjects.subjectID'),nullable=False)
    timeslotID = db.Column(db.Integer, db.ForeignKey('timeslots.timeslotID'),nullable=False)
    maxStudent = db.Column(db.Boolean, nullable=False)
    maxTutor = db.Column(db.Boolean, nullable=False)
    apptdate = db.Column(db.Date, nullable=False)
    studentsClasses = db.relationship('StudentsClasses', backref='class', lazy=True)
    tutorsClasses = db.relationship('TutorsClasses', backref='class', lazy=True)


class StudentsClasses(db.Model):
    """
    Intersection table to handle the M-M relationship between Students and Classes.
    """
    studentClassID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey('students.studentID'),nullable=False)
    classID = db.Column(db.Integer, db.ForeignKey('classes.classID'),nullable=False)


class TutorsClasses(db.Model):
    """
    Intersection table to handle the M-M relationship between Tutors and Classes.
    """
    tutorClassID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    tutorID = db.Column(db.Integer, db.ForeignKey('tutors.tutorID'),nullable=False)
    classID = db.Column(db.Integer, db.ForeignKey('classes.classID'),nullable=False)

# TODO: update classes maxStudent and MaxTutor to integer
