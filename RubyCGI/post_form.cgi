#!C:/Ruby33-x64/bin/ruby.exe
# post_form.cgi
require "./RubyCGI"


# GET メソッドの場合
def onGET(cgi)
  # ERB を HTML に変換する。
  html = cgi.render("./views/post_form.erb", {"message" => "", "dirname" => "", "files" => []})
  # HTML をクライアントへ送信する。
  cgi.send_html(html)
end

# POST メソッドの場合
def onPOST(cgi)
  count = 0
  files = []
  dirname = cgi.get_param("dirname")
  Dir.foreach(dirname) {|file|
    if FileTest.file?(dirname + "/" + file)
      files.push(file)
      count += 1
    end
  }
  message = "ファイル数：#{count}"
  # ERB を HTML に変換する。
  html = cgi.render("./views/post_form.erb", {"message" => message, "dirname" => dirname, "files" => files})
  # HTML をクライアントへ送信する。
  cgi.send_html(html)
end


# RubyCGI クラスのインスタンス化
rcgi = RubyCGI.new
#rcgi = RubyCGI.new("./config.json", logging=true)
#rcgi.log("Start post_json.cgi")

# リクエストメソッドを判別してハンドラをコールする。
if rcgi.get?(false) or rcgi.get?(true)
  onGET(rcgi)
elsif rcgi.post?
  onPOST(rcgi)
else
  rcgi.send_error("METHOD_NOT_ALLOWED", '<html><p style="font-size:larger;color:red;">405 Method Not Allowed</p></html>')
end
