#!C:/Ruby33-x64/bin/ruby.exe
# error_status.cgi
require "./RubyCGI"

def onPOST(cgi)
  cgi.send_error("METHOD_NOT_ALLOWED", "<p style='color:red;'>POST はサポートされていません。</p>")
end

def onGET_NonQuery(cgi)
  html = cgi.render("./views/error_status.erb")
  cgi.send_html(html)
end

def onGET_Query(cgi)
  error = cgi.get_param("error")
  message = RubyCGI.Status[error]
  cgi.send_error(error, "<h2 style='color:darkred;padding:40px;'>#{message}</h2>")
end 


#rcgi = RubyCGI.new("./config.json", true)
#rcgi.log("Start logging.")
rcgi = RubyCGI.new

# リクエストメソッドを判別してハンドラをコールする。
if rcgi.post?
  onPOST(rcgi)
elsif rcgi.get?(false)
  onGET_NonQuery(rcgi)
elsif rcgi.get?(true)
  onGET_Query(rcgi)
else
  rcgi.send_error("METHOD_NOT_ALLOWED", '<html><p style="font-size:larger;color:red;">405 Method Not Allowed</p></html>')
end
