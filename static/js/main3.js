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
    console.log(data);
    $.ajax({
        statusCode: {
            500: function() {
                alert("error");
                }
            },
        type : "POST",
        url : "/mysql",
        data: JSON.stringify(data),
        success: function(result) {
            console.log("Success!");
        },
        error: function(error) {
            console.log(error);
        }
    });
    // var data_1 = JSON.stringify(data);
    // console.log(data_1);
    window.location.replace('/mysql');
}

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
