var months = {' 01 ':'Jan', ' 02 ':'Feb', ' 03 ':'Mar', ' 04 ':'Apr', ' 05 ':'May', ' 06 ':'Jun',
' 07 ':'Jul', ' 08 ':'Aug', ' 09 ':"Sep", ' 10 ':'Oct', ' 11 ':'Nov', ' 12 ':'Dec'};

// jQuery for togging current and cancel sections
$('.menu-item').click(function () {
    $('.collapse').collapse('hide');
});

// FullCalendar.io -> Current: receives object of appointments and is called from layout script
function addCalendar(data) {
    // copy data to adjust format
    var dataArr = [];
    for (i in data){
        dataArr.push(data[i]);
    }
    // mapping of objects. cm_local_branch contains a simplified mapping for new received data format
    data = dataArr.map(object=>{
        return {
            title: object.subject,
            start: object.date,
        }
    })
    // fullCalendar loads once page has finished
    document.addEventListener('DOMContentLoaded', function() {
        // First 9 lines can be copied as is. Appends calendar and sets view functionality and events.
        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: data,
            eventClick: function(info) {
                var osubject = info.event.title;
                var odate = info.event.start;
                // alert(typeof fulldate);
                $('#editAppt').modal();
                $('#od').val(odate);
                $('#os').val(osubject);
            },
            // dateClick functions are attached to each day of the month so useful for attaching
            // newappt form. If you have issues with sending date to form, try the wierd input 
            // previously discussed.
            dateClick: function(info) {
                var newDate=info.dateStr
                // alert('Date: ' + info.dateStr);
                $('#newAppt').modal();
                $('#nd').val(newDate);
            }
        });
        calendar.render();
    });    
};

// event edit popup


// Cancellation page
// Convert month# to month
function changeMonth() {
    var contentMonths = document.getElementsByClassName("month");
    for (var i=0; i<contentMonths.length; i++){
        contentMonths[i].innerText = months[contentMonths[i].innerText];
    }
};


// TODO: 
//   - add delete from database and confirm calendar functionality (rerendered from redirect)
//   - add new appointment clickdate functionality and form
//   - remap data to align with database
//   - if time, fix account settings dropdown to fall over contents
