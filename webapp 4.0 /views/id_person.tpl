<!DOCTYPE html>
<html>
<head>
<style>
body {
  background-color: lightblue;
}

h1 {
  color: white;
  text-align: center;
  font-family: Arial,Helvetica,sans-serif;
}
h2 {
  font-family: Arial,Helvetica,sans-serif;
  font-size: 30px;
}

p {
  font-family: Arial,Helvetica,sans-serif;
  font-size: 15px;
}
button{
  position: absolute;
  left: 260px;


}
</style>
</head>
<body>


<ul>

<br><h1>Personal Page</h1><br>
<h2>Your id is {{id}}</h2><br>
<p>Show personal data:<a href="http://127.0.0.1:8080/showperson/{{id}}"> <button>Personal Data </button></a></p>
<!--Comentario:teste a mudanca de html de resultados APAGAR-->
<!--<p>New checkin:<a href="http://127.0.0.1:8080/newcheckin/{{id}}"> New Checkin </a></p>-->
<p>Show all checkins:<a href="http://127.0.0.1:8080/showcheckin/{{id}}"> <button>Checkins</button></a></p>
<p>Delete Personal Data:<a href="http://127.0.0.1:8080/deleteperson/{{id}}"> <button>Delete Personal Data</button> </a></p>
<h2>Show all personal records:</h2><br>
<p>Show personal all data(JSON):<a href="http://127.0.0.1:8080/show_data_person/{{id}}"> <button>Personal Data </button></a></p>
<p>Show personal all data:<a href="http://127.0.0.1:8080/show_data_person2/{{id}}"> <button>Personal Data</button> </a></p>
<br><p>Return:<a href="http://127.0.0.1:8080/client"> Return </a></p>
