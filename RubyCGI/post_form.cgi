#!C:/Program Files/Ruby31-x64/bin/ruby.exe
# post_form.cgi
require "./RubyCGI"

# RubyCGI クラスをインスタンス化する。
rcgi = RubyCGI.new

count = 0
files = []
message = ""

# メソッドの種別による処理
if rcgi.request_method == "GET"
  # GET メソッドの時
  dirname = ""
else
  # POST メソッドの時
  dirname = rcgi.get_param("dirname")
  Dir.foreach(dirname) {|file|
    if FileTest.file?(dirname + "/" + file)
      files.push(file)
      count += 1
    end
  }
  message = "ファイル数：#{count}"
end

# ERB を HTML に変換する。
html = rcgi.render("./views/post_form.erb", {"message":message, "dirname":dirname, "files":files})
# HTML をクライアントへ送信する。
rcgi.send_html(html)