/**
 * Created by Leo on 16/07/2017.
 */

function submit_feedback(){
    var stars = document.getElementsByClassName('active');
    var rating = stars.length;


    var url = window.location.href.split('/');
    var service = url[url.length - 1];
    console.log(service);
    var data = {dm: service, stars: rating};
    // console.log(data);

    // $.post('0.0.0.0:5000/mysql', data, function(res){
    //     console.log('Success!');
    //     window.location.replace('/mysql');
    //   })
    // console.log("TEST");
    // window.location.replace('/mysql');
    // JSON.stringify(data)

    $.ajax({
        statusCode: {
            500: function() {
                alert("error");
                }
            },
        type : "POST",
        url : "/mysql",
        data: JSON.stringify(data, null, '\t'),
        //contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            console.log("Success!");
        },
        error: function(error) {
            console.log(error);
        }
    });

    console.log(data);
    window.location.replace('/database');
}



// $.ajax({
//     type: 'POST',
//     url: window.location.href,
//     data: JSON.stringify(response),
//     dataType: 'json',
//     contentType: 'application/json; charset=utf-8'
// }).done(function(msg) {
//     alert("Data Saved: " + msg);
// });

document.getElementById('submit').addEventListener('click', submit_feedback)

var stars = document.getElementsByClassName('fa-star')
Array.prototype.forEach.call(stars, function(star){
    star.addEventListener('click', choose_rating)
})

function choose_rating(event){
    console.log(event.target.id)
    var id = event.target.id
    var stars = document.getElementsByClassName('fa-star')
    Array.prototype.forEach.call(stars, function(star){
        star.classList.remove("active")
        if (star.id <= id){
            star.classList.add("active")
        }
    })
}

// var radios = document.getElementsByName('attended');
//
// //console.log(radios[0])
// //console.log(radios[1])
//
// function check_attendance(){
//     var length = radios.length
//
//     for (var i = 0; i < length; i++) {
//         if (radios[i].checked) {
//         //var attended = radios[i].value;
//             console.log('TEST')
//         //alert(radios[i].value);
//         // only one radio can be logically checked, don't check the rest
//         break;
//         }
//     }
// }
//
// document.getElementsByName('attended').addEventListener('click', check_attendance)