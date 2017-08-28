var rootUrl = 'http://localhost:8080/DWP-P2-DR/app/claimant'

	$(document)
	.ready(
			function() {
				if (window.location.href == "http://localhost:8080/TaxCredit/tcpage1.html") {
					var mess = document.getElementById('output').innerHTML;					
					if (!localStorage.message){
						document.getElementById('output').innerHTML = "Hello and welcome to the Tax Credit Application page";	
					} else {
						document.getElementById('output').innerHTML = localStorage.message;
					}
				}
			});	
$('#btnFindClaimantbyNino').click(function() {
	findClaimantByNino();
	return false;
});


function findClaimantByNino() {

	var nino = $('#nino').val();
	localStorage.setItem("nino", nino);
	// Could be global. Takes the place of all following error callbacks.
	$(function() {
		$.ajaxSetup({
			error : function(jqXHR, exception) {
				message="Incorrect National Insurance number. Please try again"
					localStorage.setItem("message", message);	
				if (jqXHR.status === 0) {
					console.log('Not connect.\n Verify Network.');
				} else if (jqXHR.status == 404) {
					console.log('404: requested page not found. [404]');
				} else if (jqXHR.status == 500) {
					console.log('500: internal Server Error [500].');
				} else if (exception === 'parsererror') {
					console.log('parsererrr: requested JSON parse failed.');
				} else if (exception === 'timeout') {
					console.log('timeout: time out error.');
				} else if (exception === 'abort') {
					console.log('abort: AJAX request aborted.');
				} else {
					console.log('Uncaught Error.\n' + jqXHR.responseText);
				}
			}
		});
	});

	document.getElementById('ninoForm').submit();

}

