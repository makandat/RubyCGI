#!C:/Program Files/Ruby31-x64/bin/ruby.exe
# file_upload.cgi
require "./RubyCGI"

# RubyCGI クラスをインスタンス化する。
rcgi = RubyCGI.new

message = ""

# メソッドの種別による処理
if rcgi.request_method == "POST"
  # POST メソッドの時、アップロードされたファイルを C:/temp にファイル保存する。
  file = rcgi.save_file("file1", "C:/temp")
  message = "Upload OK: \"#{file.original_filename}\""
end

# ERB を HTML に変換する。
html = rcgi.render("./views/file_upload.erb", {"message":message})
# HTML をクライアントへ送信する。
rcgi.send_html(html)