#!C:/Ruby33-x64/bin/ruby.exe
# post_json.cgi
require "./RubyCGI"

# POST メソッドハンドラ
def onPOST(cgi)
  data = cgi.get_json()
  path = data["path"]
  if FileTest.exist?(path)
    sts = File::Stat.new(path)
    size = sts.size
    lastwrite = sts.mtime.to_s
    mode = sts.mode
    result = {"size" => size, "lastwrite" => lastwrite, "mode" => mode}
  else
    # ファイルが存在しないとき
    result = {"size" => -1, "lastwrite" => -1, "mode" => -1}
  end
  cgi.send_json(result)
end

# GET メソッドハンドラ (クエリーなし)
def onGET_NonQuery(cgi)
  cgi.send_html(cgi.render("./views/post_json.erb"))
end

# GETT メソッドハンドラ (クエリーあり)
def onGET_Query(cgi)
  cgi.send_error("BAD_REQUEST", "<p style='color:red;'>400 Bad Request</p>")
end

# RubyCGI クラスのインスタンス化
rcgi = RubyCGI.new
#rcgi = RubyCGI.new("./config.json", logging=true)
#rcgi.log("Start post_json.cgi")

# リクエストメソッドを判別してハンドラをコールする。
if rcgi.request_method == "POST"
  onPOST(rcgi)
elsif rcgi.get?(false)
  onGET_NonQuery(rcgi)
elsif rcgi.get?(true)
  onGET_Query(rcgi)
else
  rcgi.send_error("METHOD_NOT_ALLOWED", '<html><p style="font-size:larger;color:red;">405 Method Not Allowed</p></html>')
end
