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
</style>
</head>
<body>


<ul>

<h1>All Records list Page:</h1>
  %for key, x in res.iteritems():
      <h2>{{key}}</h2>
      %for item, seg in x.iteritems():
      <li>{{item}}-> {{seg}}</li>
      <br/>
      %end
  %end


<!-- Teste de uniformazação para prints-->
<!-- TENTAR FAZER ARVORE com tabs-->
<h1>All Personal Classes Records list Page:</h1>

<!---->
%for key, x in res.iteritems():
  %if key=="person_0":
    <h2>Person Class Records:</h2>
    %for item, seg in x.iteritems():
    <p>&nbsp {{item}}-> {{seg}}</p>
    %end
  %end
%end
%for key, x in res.iteritems():
  %if key=="checkin_0":
    <h2>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp1 Check in Class Records:</h2>
    %for item, seg in x.iteritems():
    <p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp {{item}}-> {{seg}}</p>
    %end
  %end
%end
%for key, x in res.iteritems():
  %if key=="checkin_1":
    <h2>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp2 Check in Class Records:</h2>
    %for item, seg in x.iteritems():
    <p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp {{item}}-> {{seg}}</p>
    %end
  %end
%end
%for key, x in res.iteritems():
  %if key=="grade_0":
    <h2>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp1 Grade Class Records:</h2>
    %for item, seg in x.iteritems():
    <p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp {{item}}-> {{seg}}</p>
    %end
  %end
%end
%for key, x in res.iteritems():
  %if key=="grade_1":
    <h2>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp2 Grade Class Records:</h2>
    %for item, seg in x.iteritems():
    <p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp {{item}}-> {{seg}}</p>
    %end
  %end
%end
<!---->




</ul>
</body>
</html>
