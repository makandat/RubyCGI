#!C:/Program Files/Ruby31-x64/bin/ruby.exe
# post_formdata.cgi
require "./RubyCGI"

# POST メソッドハンドラ
def onPOST(cgi)
  length = cgi.get_param("length").to_f
  convert = cgi.get_param("convert").to_i
  s = ""
  if convert == 1
    s = (length / 2.54).to_s
  else
    s = (length * 2.54).to_s
  end
  cgi.send_text(s)
end

# GET メソッドハンドラ (クエリーなし)
def onGET_NonQuery(cgi)
  cgi.send_html(cgi.render("./views/post_formdata.erb"))
end

# GETT メソッドハンドラ (クエリーあり)
def onGET_Query(cgi)
  cgi.send_html(cgi.render("./views/post_formdata.erb"))
end


# RubyCGI クラスのインスタンス化
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

