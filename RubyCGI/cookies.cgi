#!C:/Ruby33-x64/bin/ruby.exe
# cookies.cgi
require "./RubyCGI"

# POST メソッドのリクエストハンドラ
def onPOST(cgi)
  cgi.send_error("METHOD_NOT_ALLOWED", "<p style='color:red;'>POST はサポートされていません。</p>")
end

# パラメータ無しの GET メソッドのリクエストハンドラ
def onGET_NonQuery(cgi)
  if cgi.cookies.has_key?("counter")
    count = cgi.cookies["counter"][0].to_i + 1
  else
    count = 0
  end
  html = cgi.render("./views/cookies.erb", {"message" => "counter = #{count}"})
  counter = cgi.make_cookie("counter", [count.to_s])
  cgi.send_html(html, status="OK", cookies=[counter.to_s])
end

# パラメータ有りの GET メソッドのリクエストハンドラ
def onGET_Query(cgi)
  count = cgi.get_param("counter")
  html = cgi.render("./views/cookies.erb", {"message" => "counter = #{count}"})
  counter = cgi.make_cookie("counter", [count])
  cgi.send_html(html, status="OK", cookies=[counter])
end 

# RubyCGI クラスをインスタンス化
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