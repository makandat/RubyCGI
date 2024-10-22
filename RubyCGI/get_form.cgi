#!C:/Program Files/Ruby31-x64/bin/ruby.exe
# get_form.cgi
require "./RubyCGI"

# RubyCGI クラスをインスタンス化する。
rcgi = RubyCGI.new

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

# クエリーパラメータがあるか？
if rcgi.query_string == ""
  # ない場合
  dirname = ""
  recursive = ""
  message = ""
else
  # ある場合
  dirname = rcgi.get_param("dirname")
  recursive = rcgi.get_check("recursive")
  result = get_content(dirname, recursive)
  message = "ファイル数：#{result[0]}　総バイト数：#{result[1]}"
end

# ERB を HTML に変換する。
html = rcgi.render("./views/get_form.erb", {"message":message, "dirname":dirname})
# HTML をクライアントへ送信する。
rcgi.send_html(html)