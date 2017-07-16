/**
 * Created by Leo on 16/07/2017.
 */

function submit_feedback(){
    var stars = document.getElementsByClassName('active')
    var rating = stars.length


    var url = window.location.href.split('/')
    var service = url[url.length - 1]
    console.log(service)
    $.post('http://ec2-13-58-211-169.us-east-2.compute.amazonaws.com/api/feedback', {dm: service, stars: rating, latitude:0, longitude:0}, function(res){
        console.log(res.status)
        //window.location.replace('/pages/thankyou')
    })
    // fetch('http://ec2-13-58-211-169.us-east-2.compute.amazonaws.com/api/feedback', {
    //     method: 'POST',
    //     headers: new Headers({'content-type': 'application/JSON'}),
    //     body: JSON.stringify({dm: service, stars: rating, latitude:0, longitude:0})
    // })

}

var submit_button = document.getElementById('submit').addEventListener('click', submit_feedback)

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