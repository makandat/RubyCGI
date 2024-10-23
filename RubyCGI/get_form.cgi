#!C:/Ruby33-x64/bin/ruby.exe
# get_form.cgi
require "./RubyCGI"

# ディレクトリ内のファイルの数と総バイト数を求める。
def get_content(dirname, recursive)
  count = 0
  sum = 0
  if recursive
    Dir.glob('**/*', File::FNM_DOTMATCH, base: dirname).each {|file|
      path = dirname + "/" + file
      if File.exist?(path)
        count += 1
        sum += File.size(path)
      end
    }
  else
    Dir.foreach(dirname) { |file|
      path = dirname + "/" + file
      if File.exist?(path)
        count += 1
        sum += File.size(path)
      end
    }
  end
  return [count, sum]
end

# GET メソッドでクエリーなしの場合
def onGET_NonQuery(cgi)
  # ERB を HTML に変換する。
  html = cgi.render("./views/get_form.erb", {"message" => "", "dirname" => ""})
  # HTML をクライアントへ送信する。
  cgi.send_html(html)
end

# GET メソッドでクエリーありの場合
def onGET_Query(cgi)
  dirname = cgi.get_param("dirname")
  recursive = cgi.get_check("recursive")
  result = get_content(dirname, recursive)
  message = "ファイル数：#{result[0]}　総バイト数：#{result[1]}"
  # ERB を HTML に変換する。
  html = cgi.render("./views/get_form.erb", {"message" => message, "dirname" => dirname})
  # HTML をクライアントへ送信する。
  cgi.send_html(html)
end


# RubyCGI クラスのインスタンス化
rcgi = RubyCGI.new
#rcgi = RubyCGI.new("./config.json", logging=true)
#rcgi.log("Start post_json.cgi")

# リクエストメソッドを判別してハンドラをコールする。
if rcgi.get?(false)
  onGET_NonQuery(rcgi)
elsif rcgi.get?(true)
  onGET_Query(rcgi)
else
  rcgi.send_error("METHOD_NOT_ALLOWED", '<html><p style="font-size:larger;color:red;">405 Method Not Allowed</p></html>')
end
