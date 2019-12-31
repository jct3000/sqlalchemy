<html>
<ul>
<h1>Clean list Page:</h1>
  %for key, x in res.iteritems():
      <h2>{{key}}</h2>
      %for item, seg in x.iteritems():
      <li>{{item}}-> {{seg}}</li>
      <br/>
  %end
</ul>
</html>
