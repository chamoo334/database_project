from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField, TimeField, IntegerField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NoneOf, ValidationError
from cmlz_tutoring.models import *


class StudentRegistrationForm(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    userName = StringField('Username', validators=[InputRequired(), Length(min=3, max=20, message="Username must be between 3 and 20 characters long.")])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('New Password', validators=[InputRequired()])
    confirmPassword = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_userName(self, userName):
        student = Students.query.filter_by(userName=userName.data).first()
        if student:
            raise ValidationError('That username is currently taken by another student. Please choose another.')

    def validate_email(self, email):
        student = Students.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('That email is currently in use by another student. Please choose another.')


class TutorRegistrationForm(FlaskForm):
    tutorSubject = SelectField('Subject:', validators=[InputRequired(), NoneOf('-- Please Choose a Subject --', message='A subject must be chosen.')])
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    userName = StringField('Username', validators=[InputRequired(), Length(min=3, max=20, message="Username must be between 3 and 20 characters long.")])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('New Password', validators=[InputRequired()])
    confirmPassword = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_userName(self, userName):
        tutor = Tutors.query.filter_by(userName=userName.data).first()
        if tutor:
            raise ValidationError('That username is currently taken by another tutor. Please choose another.')

    def validate_email(self, email):
        tutor = Tutors.query.filter_by(email=email.data).first()
        if tutor:
            raise ValidationError('That email is currently in use by another tutor. Please choose another.')


class LoginForm(FlaskForm):
    userType = RadioField('Label', choices=[('student','Student'),('tutor','Tutor')], default='student', validators=[InputRequired()])
    userName = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class UpdateInformationForm(FlaskForm):
    newFirstName = StringField('Change First Name')
    newUserName = StringField('Change User Name')
    usubmit = SubmitField('Update!')

class DeleteAccountForm(FlaskForm):
    delsubmit = SubmitField('Delete!')
    
class EditApptForm(FlaskForm):
    # TODO: confirm and/or fix date representation
    oldDate = StringField()
    oldSubject = StringField()
    editDate = DateField('Select a date:', format='%Y-%m-%d', validators=[InputRequired()])
    editTime = SelectField('Select a time:', validators=[InputRequired()])
    esubmit = SubmitField('Reschedule')


class NewApptForm(FlaskForm):
    #TODO: verify all data is entered, confirm and fix date representation,
    # figure out best way to obtain student id and selected date
    newDate = StringField()
    newSubject = SelectField('Select a subject:', validators=[InputRequired()])
    newNote = StringField('Notes:', validators=[Length(max=20, message="Please limit notes to 20 characters.")])
    newTime = SelectField('Select a time:', validators=[InputRequired()])
    nsubmit = SubmitField('Schedule')


class CancelApptForm(FlaskForm):
    delDate = StringField()
    submit = SubmitField('Cancel')


class TutorApptForm(FlaskForm):
    addDate = StringField()
    submit = SubmitField('Yes!')
    tsubmit = SubmitField('Yes!')

class ChangeTutor(FlaskForm):
    newTutor = SelectField('Select a new tutor:', choices=[('Zach'), ('Chantel')], validators=[InputRequired()])
    submit = SubmitField('Change Tutor')

class SubjectEdit(FlaskForm):
    newSubject = StringField('Enter the new subject title:')
    newMaxStudent = IntegerField('Enter the new maximum number of students:')
    newMaxTutors = IntegerField('Enter the new maximum number of tutors:')
    submit = SubmitField('Confirm')

class TimeslotEdit(FlaskForm):
    newStart = TimeField('Enter new start time:')
    newEnd = TimeField('Enter new end time:')
    submit = SubmitField('Confirm')
