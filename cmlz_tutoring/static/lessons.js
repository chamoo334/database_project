var months = {' 01 ':'Jan', ' 02 ':'Feb', ' 03 ':'Mar', ' 04 ':'Apr', ' 05 ':'May', ' 06 ':'Jun',
' 07 ':'Jul', ' 08 ':'Aug', ' 09 ':"Sep", ' 10 ':'Oct', ' 11 ':'Nov', ' 12 ':'Dec'};

// jQuery for togging current and cancel sections
$('.menu-item').click(function () {
    $('.collapse').collapse('hide');
});

// FullCalendar.io -> Current: receives object of appointments and is called from layout script
function addCalendar(data) {
    // console.log(data);
    var dataArr = [];
    for (i in data){
        dataArr.push(data[i]);
        // console.log(dataArr[i]);
    }
    // TODO: remap according to database
    data = dataArr.map(object=>{
        return {
            title: object.subject,
            start: object.date,
            // extendedProps: {
            //     times: dAndT[1],
            // }
        }
    })
    document.addEventListener('DOMContentLoaded', function() {
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
                var odate = info.event.start;
                // alert(odate);
                $('#cancelAppt').modal();
                $('#od').val(odate);
            }
        });
        calendar.render();
    });    
};


function add_click(clicked_id){
    var temp = clicked_id.substring(4);
    var tappt = '#teachAppt'+temp;
    $(tappt).modal();
    var elements = document.querySelectorAll('.ad');
    elements.forEach(function(element){
        element.value = temp;
    });
    console.log('JS: '+temp);
};

// Convert month# to month
function changeMonth() {
    var contentMonths = document.getElementsByClassName("month");
    for (var i=0; i<contentMonths.length; i++){
        contentMonths[i].innerText = months[contentMonths[i].innerText];
    }
};