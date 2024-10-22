#!C:/Program Files/Ruby31-x64/bin/ruby.exe
# get_text.cgi
require "./RubyCGI"

rcgi = RubyCGI.new
if rcgi.query_string == ""
  html = rcgi.render("./views/get_text.erb")
  rcgi.send_html(html)
else
  x = rcgi.get_param("x").to_f
  y = 5.0 / 9.0 * (x - 32.0)
  rcgi.send_text(y.to_s)
end