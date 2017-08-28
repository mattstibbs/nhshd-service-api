var rootUrl = 'http://localhost:8080/DWP-P2-DR/app/appservices'

$(document)
		.ready(
				function() {
					if (window.location.href == "http://localhost:8080/TaxCredit/tcpage2.html") {
						document.getElementById("result").innerHTML = localStorage.nino;
					}
				});

$('#btnSave').click(function() {
	createTcapplication();
	return false;
});
$('#btnFindAll').click(function() {
	findAllAndBuildTable();
});


function createTcapplication() {

	$
			.ajax({
				type : 'POST',
				contentType : 'application/json',
				// dataType: "html",
				url : rootUrl + '/create',
				data : formToJson(),
				success : function(data, textStatus, jqXHR) {
					console.log(textStatus);
					if (textStatus == "success") {
						message=" "
							localStorage.setItem("message", message);
						window.location.href = "http://localhost:8080/TaxCredit/summary.html"
					} else {
						message="You have already applied. Please call 0800 123456 to discuss your existing claim"
						localStorage.setItem("message", message);
						window.location.href = "http://localhost:8080/TaxCredit/tcpage1.html"
					}
				},
				error : function(jqXHR, textStatus, errorThrown) {
					alert('error: ' + textStatus)
				}
			});

}

function formToJson() {

	var selected = $("input[type='radio']:checked").val();

	var jsonUser = JSON.stringify({
		"email" : $('#email').val(),
		"nino" : $('#result').html(),
		"housingType" : selected,
		"children" : $('#children').val(),
		"ratePerChild" : "0",
		"monthlyRate" : "0",
		"status" : "new"
	});

	return jsonUser;
}

function findAllAndBuildTable() {

	$.ajax({
		type : 'GET',
		url : rootUrl,

		success : function(data, textStatus, jqXHR) {
			buildTable(data);
		}
	});
}

function buildTable(arr) {
	// console.log('buildTable(): ' + arr);
	var out = "<table><tr>" + "<th>Email</th>" + "<th>NINO</th>"
			+ "<th>Housing Type</th>" + "<th>Number Of Children</th>"
			+ "<th>Rate per Child</th>" + "<th>Monthly Payment</th>"
			+ "<th>Status</th></tr>";
	for (var i = 0; i < arr.length; i++) {
		var housingType= arr[i].housingType;
		var nino = arr[i].nino;
		var children = arr[i].children;
		out += "<tr><td>" + arr[i].email + '</td><td>' + nino
				+ '</td><td>' + housingType + '</td><td>'
				+ children + '</td><td>' + arr[i].ratePerChild
				+ '</td><td>' + arr[i].monthlyRate + '</td><td>'
				+ arr[i].status + '</td><td>'
				+ '<button id="allow--'  +nino
				+ '">Allow</button></td><td>'
				+ '<button id="reject-' + nino
				+ '">Reject</button></td></tr>';
	
	
		$('#tableOutput').on('click', '#allow--' + nino, function() {
			console.log('Show added id: ' + this.id);
		
			$.ajax({
				//contentType : 'application/json',
				type : 'PUT',
				//data : this.id,
					url : rootUrl + '/' + this.id + '/allow/',
				success : function(data, textStatus, jqXHR) {
					console.log(data);
				}
			});
		});

		$('#tableOutput').on('click', '#reject-' + nino, function() {
			console.log('Show added id: ' + this.id);
			$.ajax({
		//		contentType : 'application/json',				
				type : 'PUT',
			url : rootUrl + '/' + this.id + '/reject',
				success : function(data, textStatus, jqXHR) {
					console.log(data);
				}
			});
		});
	}
	out += "</table>";
	$("#tableOutput").html(out);
	}

function checkEmail() {
	document.getElementById("output2").innerHTML = ""
	var email = $('#email').val();
	console.log(email);


	if( /(.+)@(.+){2,}\.(.+){2,}/.test(email) ){
		document.getElementById('output2').innerHTML = "";
		document.getElementById('housingType1').focus();
	} else {
		document.getElementById('output2').innerHTML = "Incorrect format for email address ";
		document.getElementById('email').focus();
	}
	
}
