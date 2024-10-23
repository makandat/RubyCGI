#!C:/Ruby33-x64/bin/ruby.exe
# get_json.cgi
require "./RubyCGI"

# RubyCGI クラスをインスタンス化する。
rcgi = RubyCGI.new

# リクエストメソッド別の処理
if rcgi.get?(false)
  # パラメータ無しの場合
  html = rcgi.render("./views/get_json.erb")
  rcgi.send_html(html)
elsif rcg.get?(true)
  # パラメータ有りの場合
  x = rcgi.get_param("x").to_f
  y = rcgi.get_param("y").to_f
  z = Complex(x, y)
  data = {"abs"=>z.abs, "arg"=>z.arg}
  rcgi.send_json(data)
else
  # GET 以外のメソッドはエラーとする。
  rcgi.send_error("NOT_IMPLEMENTED")
end