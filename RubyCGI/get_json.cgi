#!C:/Ruby33-x64/bin/ruby.exe
# get_json.cgi
require "./RubyCGI"

rcgi = RubyCGI.new
if rcgi.query_string == ""
  html = rcgi.render("./views/get_json.erb")
  rcgi.send_html(html)
else
  x = rcgi.get_param("x").to_f
  y = rcgi.get_param("y").to_f
  z = Complex(x, y)
  data = {"abs"=>z.abs, "arg"=>z.arg}
  rcgi.send_json(data)
end