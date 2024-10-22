#!C:/Program Files/Ruby31-x64/bin/ruby.exe
# get_image.cgi
require "./RubyCGI"

rcgi = RubyCGI.new

if rcgi.query_string == ""
  rcgi.send_html(rcgi.render("./views/get_image.erb"))
else
  path = rcgi.get_param("path")
  rcgi.send_file(path)
end
