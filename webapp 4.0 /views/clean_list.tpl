

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

<h1>Clean list Page:</h1>
  %if len(res)==0:
  <h2>No Personal data records expired</h2>
  %end
  %for key, x in res.iteritems():
      <h2>{{key}}</h2>
      %for item, seg in x.iteritems():
      <li>{{item}}-> {{seg}}</li>
      <br/>
      %end
  %end
</ul>
</html>
