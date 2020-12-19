// jquery for client views
$('#headingStudent').click(function () {
    $('#studentView').collapse('hide');
});

// jquery for tutor views
$('#headingTutor').click(function () {
    $('#tutorView').collapse('hide');
});

// jquery for subjects show
$('#headingSubjects').click(function () {
    $('#subjectsView').collapse('hide');
});

// jquery for timeslots show
$('#headingTimeslots').click(function () {
    $('#timeslotsView').collapse('hide');
});

// jquery for Classes show
$('#headingClasses').click(function () {
    $('#ClassesView').collapse('hide');
});

// jquery for setting up the DataTables on the admin page
$(document).ready(function () {
    $('#studentTable').DataTable();
    $('#tutorTable').DataTable();
    $('#subjectTable').DataTable();
    $('#timeslotTable').DataTable();
    $('#classesTable').DataTable();
    $('.dataTables_length').addClass('bs-select');
});

// jquery for deleting students
$(document).on("click", ".deleteStudent", function () {
    var studentID = $(this).data('username');
    $('#modalDeleteStudent').val( studentID );
});

// jquery for deleting tutor
$(document).on("click", ".deleteTutor", function () {
    var tutorID = $(this).data('username');
    $('#modalDeleteTutor').val( tutorID );
});

// jquery for editing subjects
$(document).on("click", ".editSubject", function () {
    var subjectName = $(this).data('edit');
    $('#modalEditSubject').val( subjectName );
    $('#editSubjectName').val( subjectName );

    var maxStudentNum = $(this).data('student');
    $('#editSubjectMaxStudent').val( maxStudentNum );

    var maxTutorNum = $(this).data('tutor');
    $('#editSubjectMaxTutor').val( maxTutorNum );
});

// jquery for deleting subjects
$(document).on("click", ".deleteSubject", function () {
    var subject = $(this).data('delete');
    $('#modalDeleteSubject').val( subject );
});

// jquery for editing timeslots
$(document).on("click", ".editTimeslot", function () {
    var timeslot = $(this).data('edit');
    $('#modalEditTimeslot').val( timeslot );
    $('#editTimeslotStart').val( timeslot );
});

// jquery for deleting timeslots
$(document).on("click", ".deleteTimeslot", function () {
    var timeslot = $(this).data('delete');
    $('#modalDeleteTimeslot').val( timeslot );
});

// jquery for updating class tutors that can be edited.
$(document).on("click", ".editClassTutor", function (event) {
    // Empty existing modal's old/new tutor choices.
    $('#originalClassTutor').empty();
    $('#newClassTutor').empty();

    // Pulling current tutor for row.
    var currentTutors = $(this).closest('td').prev()["0"].innerText;
    if (currentTutors[0]) {
        currentTutors = currentTutors.replace(/\s+/g, " ").substring(0, currentTutors.length).split(" , ");
        currentTutors.sort();
    } else {
        currentTutors = [];
    }

    // Incoming data for available tutors is a JSON object. Save that and create an array of its keys.
    var availableTutors = Object.keys($(this).data('edit'));
    /* Parse available tutors, creating an option for each. Skips tutors currently assigned to class.
        If the current and available tutors are the same, it nullifies changes to tutors. */
    if (JSON.stringify(currentTutors) != JSON.stringify(availableTutors)) {
        // Re-setting the new tutor drop down and submit button.
        $('#newClassTutor').prop('disabled', false);
        $('#modalEditClassTutor').next('button').prop('disabled', false);

        // Enables current tutor drop down if there are tutors assigned. Disables it if not.
        if (currentTutors[0]) {
            $('#originalClassTutor').prop('disabled', false);
        } else {
            $('#originalClassTutor').append($("<option></option>").text("TUTOR NEEDED FOR CLASS."));
            $('#originalClassTutor').prop('disabled', true);
        }

        // Parse current tutors, creating an option for each.
        $.each(currentTutors, function (index, value) {
            $('#originalClassTutor').append($("<option></option>")
                                .attr("value", value)
                                .text(value));
        });

        // Parse available tutors, only listing them in the drop down if they're not current tutors.
        $.each(availableTutors, function (index, value) {
            if (jQuery.inArray(value, currentTutors) == -1) {
                $('#newClassTutor').append($("<option></option>").attr("value", value).text(value));
            }
        });
    } else {
        // In the case where there's a current tutor, but no other tutors available.
        $('#originalClassTutor').append($("<option></option>").text("NO OTHER TUTORS ARE AVAILABLE."));
        $('#originalClassTutor').prop('disabled', true);
        $('#newClassTutor').append($("<option></option>").text("NO OTHER TUTORS ARE AVAILABLE."));
        $('#newClassTutor').prop('disabled', true);
        $('#modalEditClassTutor').next('button').prop('disabled', true);
    }
});

// jquery for updating class tutors
$(document).on("click", ".editClassTutor", function () {
    var oldTutorID = $(this).data('edit');
    var newTutorID = $(this).data('edit');
    var classID = $(this).data('class');
    $('#modalEditClassTutor').val( classID );
    $('#originalTutorID').val( oldTutorID[$('#originalClassTutor').val()] );
    $('#newTutorID').val( newTutorID[$('#newClassTutor').val()] );

    // Dynamically updates selection value.
    $("#originalClassTutor").change(function () {
        $('#originalTutorID').val( oldTutorID[$('#originalClassTutor').val()] );
    });
    $("#newClassTutor").change(function () {
        $('#newTutorID').val( newTutorID[$('#newClassTutor').val()] );
    });
});

// jquery for deleting class tutors
$(document).on("click", ".deleteClass", function () {
    var classID = $(this).data('delete');
    $('#modalDeleteClass').val( classID );
});
