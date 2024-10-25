# RubyCGI class v1.0.6

## 1 Overviews

### 1.1 Function

RubyCGI.rb is a module for CGI written in Ruby. This module includes RubyCGI class.

The RubyCGI class inherits the CGI class of Ruby, and the member of the CGI class is available. Furthermore, This class includes a lot of methods to make it easy to use it more. 
The following items are possible when you use this class.

   * Support of ERB (Embed Ruby template language): You can use ERB as a standard template engine.
   * It is easy to use the parameter of the posted form and can acquire it.
   * Support of HTTP file upload. (enctype="multipart/form-data")
   * Support of JSON request and response.
   * Support of web cookie handling..
   * Support of HTTP error status response
   * Support of the response handling of binary file (for example, picture files)
   * Support FormData object.

### 1.2 Usage

You copy RubyCGI.rb in your CGI folder and add *require "RubyCGI.rb"* to the beginning of your CGI code.

```#!/usr/bin/env ruby
require "./RubyCGI"
  .....
```

Then, I show an example code of simple CGI to send the plain text. (example of Windows)

```#!C:/Ruby33-x64/bin/ruby.exe
require "./RubyCGI"

rcgi = RubyCGI.new
rcgi.out("text/plain") {"Hello RubyCGI v" + RubyCGI.Version}
```

## 2 RubyCGI class

As RubyCGI class inherits Ruby's CGI class, you can use Ruby's CGI methods and properties in your code.

### 2.1 constructors

**RubyCGI.new(config="", logging=false)**

* config: Path of the configuration file which must be JSON format.
* logging: If this parameter is true, the method *log(message)* is available for logging.

### 2.2 Methods for Web Request

**String get_param(key, index=0)**

Get the request parameter(s). (Only GET not but POST) if the key does not exists, this method return "".

* key: The name of the parameter. (The name attribute value of the form)
* index: If a element which have the same name in the form, you can use this parameter.

**Bool get_check(key, index=0)**

If the parameters is from the checkbox in the form, this method returns the state as BOOL type.

* key: The name of the parameter. (The name attribute value of the form)
* index: If elements exists with the same name in the form, you can use this parameter.

**String get_cookie(key, index=0)**

Get the cookie value. If the key does not exists, this method return "".

* key: The name of the cookie.
* index: If a cookie with multiple values, you can use this parameter to specify them.

**String get_body()**

This method returns the request body, if the request method is "POST".

**Hash get_json()**

This method returns the Hash object converted from JSON, if the request method is "POST".

**Void save_file(key, copy_dir="")**

This method save the uploaded file to the directory specified by "copy_dir" parameter.

* key:  Name of the parameter。The form element must be <:input type="file" name="key"> .
* copy_dir: The directory to save the uploaded file.

**Bool post?()**

This method returns true, if the request method is "POST" else returns false.

**Bool get?(query=false)**

This method returns true, if the request method is "GET" else returns false.

    query: If query=false and  QUERY_STRING is empty, this returns true, If query=true and QUERY_STRING is not empty, this returns true.

### 2.3 Methods for Web Response

**String render(path, embed={})**

This method converts ERB template file to HTML string.

* path: The path of the template (.erb) file 
* embed: The data (Hash type) are embeded to erb file.

**String render_erb(strerb, embed={})**

This method converts ERB string to HTML string.

* strerb: The string of ERB.
* embed: The data (Hash type) are embeded to erb file.

**Void send_html(html, status="OK", cookies=[])**

This method responds the HTML to the client.

* html: HTML string (utf-8)
* status: Response status string（ex）"OK"
* cookies: Array of the CGI::Cookie object.

**Void send_text(text)**

This method responds text plain text string (utf-8) to the client.

    text: plain text string (utf-8)

**Void send_json(data)**

This method responds the JSON which is converted from Ruby's Hash data.

    data: the data of Hash type (utf-8)

**Void send_file(path, mime_type = "")**

This method respond the file which is specified with "path". 

* path: the path of the file to be sent to the client.
* mime_type: MIME type (ex) "application/json". If this is empty, then this will look up the mime type.

**CGI::Cookie make_cookie(name, values, options={})**

This method make a CGO::Cookie object with key is "name", value is "values".

* name: the key of the cookie.
* values:  Array of the cookie value. This "value" must be String.
* options: Hash of the cookie option.（ex）{"expires" => "..."}

**Void send_error(error, html="")**

This method respond the error status.

* error:  The string of the HTTP error. You can get the string form RubyCGI.Status property.
* html: HTML of the error message. If this is empty, set typical English error string.

### 2.4 Other methods

**String RubyCGI.Version**

A class property. You can get version strinng of this class.

**Hash RubyCGI.Status**

The hash with key of error status.
(ex) if key="NOT_FOUND" then value="404 Not Found"


**Hash settings**

The content of configuration file (readonly Hash type)


## 3 Examples

### 3.1 GET Form

Uing a form with method="GET"

ruby source

```#!C:/Ruby33-x64/bin/ruby.exe
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
```

erb source

```<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>GET Form</title>
 <link rel="stylesheet" href="/css/style.css" />
 <style>
  article {
    margin-left:15%;
    margin-right:15%;
    margin-top:30px;
  }
 </style>
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>GET Form</h1>
  <p style="padding:10px;text-align:center;"><a href="javascript:location='get_form.cgi'">Reset</a> | <a href="index.cgi">Index</a></p>
 </header>

 <!-- 本文 -->
 <article>
  <p>指定したディレクトリ内のファイル数とファイルサイズの合計を得る。</p>
  <form name="form1" method="GET">
   <div class="form_row">
    <label>ディレクトリ<br><input type="text" name="dirname" size="100" value="<%= dirname %>" /></label>
   </div>
   <div class="form_row">
    <label><input type="checkbox" name="recursive" />再帰的に検索</label>
   </div>
   <div style="margin-top:15px;margin-bottom:20px;">
    <button type="submit">送信する</button>
   </div>
  </form>
  <p class="message" id="message"><%= message %></p>
 </article>

 <!-- フッター -->
 <footer>
  <p>&nbsp;</p>
  <p style="text-align:center;"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
 </footer>
</body>
</html>
```

### 3.2 POST Form

Uing a form with method="POST"

ruby source
```#!C:/Ruby33-x64/bin/ruby.exe
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
```

erb source
```<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>POST Form</title>
 <link rel="stylesheet" href="/css/style.css" />
 <style>
  article {
    margin-left:15%;
    margin-right:15%;
    margin-top:30px;
  }
 </style>
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>POST Form</h1>
  <p style="padding:10px;text-align:center;"><a href="javascript:location='post_form.cgi'">Reset</a> | <a href="index.cgi">Index</a></p>
 </header>

 <!-- 本文 -->
 <article>
  <p>指定したディレクトリ内のファイル一覧を得る。</p>
  <form name="form1" method="POST">
   <div class="form_row">
    <label>ディレクトリ<br><input type="text" name="dirname" size="100" value="<%= dirname %>" /></label>
   </div>
   <div style="margin-top:15px;margin-bottom:20px;">
    <button type="submit">送信する</button>
   </div>
  </form>
  <p class="message" id="message"><%= message %></p>
  <ol style="margin-left:20%;font-size:small;">
  <% files.each {|file| %>
   <li><%= file %></li>
  <% } %>
  </ol>
 </article>

 <!-- フッター -->
 <footer>
  <p>&nbsp;</p>
  <p style="text-align:center;"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
 </footer>
</body>
</html>
```

### 3.3 File upload

Form with enctype="multipart/form-data"

ruby source
```#!C:/Ruby33-x64/bin/ruby.exe
# file_upload.cgi
require "./RubyCGI"

# RubyCGI クラスをインスタンス化する。
rcgi = RubyCGI.new

message = ""

# メソッドの種別による処理
if rcgi.post?
  # POST メソッドの時、アップロードされたファイルを C:/temp にファイル保存する。
  file = rcgi.save_file("file1", "C:/temp")
  message = "Upload OK: \"#{file.original_filename}\""
end

# ERB を HTML に変換する。
html = rcgi.render("./views/file_upload.erb", {"message":message})
# HTML をクライアントへ送信する。
rcgi.send_html(html)
```

erb source
```<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>File Upload</title>
 <link rel="stylesheet" href="/css/style.css" />
 <style>
  article {
    margin-left:15%;
    margin-right:15%;
    margin-top:30px;
  }
 </style>
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>File Upload</h1>
  <p style="padding:10px;text-align:center;"><a href="javascript:location='post_form.cgi'">Reset</a> | <a href="index.cgi">Index</a></p>
 </header>

 <!-- 本文 -->
 <article>
  <p>指定したファイルをアップロードする。</p>
  <form name="form1" method="POST" enctype="multipart/form-data">
   <div class="form_row">
    <label>ファイル<br><input type="file" name="file1" /></label>
   </div>
   <div style="margin-top:15px;margin-bottom:20px;">
    <button type="submit">アップロードする</button>
   </div>
  </form>
  <p class="message" id="message"><%= message %></p>
 </article>

 <!-- フッター -->
 <footer>
  <p>&nbsp;</p>
  <p style="text-align:center;"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
 </footer>
</body>
</html>
```

### 3.4 GET Text

Web service to get plain text.

ruby source
```#!C:/Ruby33-x64/bin/ruby.exe
# get_text.cgi
require "./RubyCGI"

rcgi = RubyCGI.new
if rcgi.get?(false)
  html = rcgi.render("./views/get_text.erb")
  rcgi.send_html(html)
else
  x = rcgi.get_param("x").to_f
  y = 5.0 / 9.0 * (x - 32.0)
  rcgi.send_text(y.to_s)
end
```

erb source
```<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>GET Text</title>
 <link rel="stylesheet" href="/css/style.css" />
 <style>
   h1 {
     text-align: center;
     color: crimson;
     padding: 10px;
   }
   a:link, a:visited {
     text-decoration: none;
     color: firebrick;
   }
 </style>
 <script>
  async function query() {
    const x = document.getElementById('X').value
    if (x == "") {
      x = 0
    }
    const res = await fetch("/cgi-bin/RubyCGI/get_text.cgi?x=" + x)
    const s = await res.text()
    const result = document.getElementById('result')
    result.innerText = "結果： " + s
  }
 </script>
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>GET Text</h1>
  <p style="padding:10px;text-align:center;"><a href="javascript:location='get_text.cgi'">Reset</a> | <a href="index.cgi">Index</a></p>
 </header>

 <!-- 本文 -->
 <article>
   <p>華氏温度を摂氏温度に変換する。</p>
   <form>
    <div><label>華氏温度: <input type="text" id="X" style="font-size:11pt;" /></label></div>
    <div style="margin-top:15px"><button type="button" id="button1" onclick="javascript:query()">送信</button></div>
   </form>
   <p id="result" class="message"></p>
 </article>

 <!-- フッター -->
 <footer>
  <p>&nbsp;</p>
  <p style="text-align:center;"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
 </footer>
</body>
</html>
```

### 3.5 GET JSON

Web service to get JSON.

ruby source
```#!C:/Ruby33-x64/bin/ruby.exe
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
```

erb source
```<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>GET JSON</title>
 <link rel="stylesheet" href="/css/style.css" />
 <style>
   h1 {
     text-align: center;
     color: crimson;
     padding: 10px;
   }
   a:link, a:visited {
     text-decoration: none;
     color: firebrick;
   }
 </style>
 <script>
  async function query() {
    const x = document.getElementById('X').value
    if (x == "") {
      x = 0
    }
    const y = document.getElementById('Y').value
    if (y == "") {
      y = 0
    }
    const res = await fetch(`/cgi-bin/RubyCGI/get_json.cgi?x=${x}&y=${y}`)
    const z = await res.json()
    const result = document.getElementById('result')
    result.innerText = `絶対値： ${z["abs"]}, 偏角：${z["arg"]}`
  }
 </script>
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>GET JSON</h1>
  <p style="padding:10px;text-align:center;"><a href="javascript:location='get_json.cgi'">Reset</a> | <a href="index.cgi">Index</a></p>
 </header>

 <!-- 本文 -->
 <article>
   <p>複素数の絶対値、偏角を返す。</p>
   <form>
    <div><label>複素数の実部: <input type="text" id="X" style="font-size:11pt;" /></label></div>
    <div><label>複素数の虚部: <input type="text" id="Y" style="font-size:11pt;" /></label></div>
    <div style="margin-top:15px"><button type="button" id="button1" onclick="javascript:query()">送信</button></div>
   </form>
   <p id="result" class="message"></p>
 </article>

 <!-- フッター -->
 <footer>
  <p>&nbsp;</p>
  <p style="text-align:center;"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
 </footer>
</body>
</html>
```

### 3.6 GET Image

Getting image files.

ruby source
```#!C:/Ruby33-x64/bin/ruby.exe
# get_image.cgi
require "./RubyCGI"

rcgi = RubyCGI.new

if rcgi.query_string == ""
  rcgi.send_html(rcgi.render("./views/get_image.erb"))
else
  path = rcgi.get_param("path")
  rcgi.send_file(path)
end
```

erb source
```<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>GET Image</title>
 <link rel="stylesheet" href="/css/style.css" />
 <style>
   h1 {
     text-align: center;
     color: crimson;
     padding: 10px;
   }
   a:link, a:visited {
     text-decoration: none;
     color: firebrick;
   }
   figure {
     padding:15px;
   }
 </style>
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>GET Image</h1>
  <p style="padding:10px;text-align:center;"><a href="javascript:location='get_json.cgi'">Reset</a> | <a href="index.cgi">Index</a></p>
 </header>

 <!-- 本文 -->
 <article>
  <section style="display:flex;">
   <figure><img src="/cgi-bin/RubyCGI/get_image.cgi?path=./img/Alice.jpg"></figure>
   <figure><img src="/cgi-bin/RubyCGI/get_image.cgi?path=./img/Hestia.jpg"></figure>
   <figure><img src="/cgi-bin/RubyCGI/get_image.cgi?path=./img/Anohana.jpg"></figure>
  </section>
 </article>

 <!-- フッター -->
 <footer>
  <p>&nbsp;</p>
  <p style="text-align:center;"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
 </footer>
</body>
</html>
```

### 3.7 POST JSON

Web service with JSON parameters.

ruby source
```#!C:/Ruby33-x64/bin/ruby.exe
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
```

erb source
```<!DOCTYPE html>
<!-- post_json.erb v1.0.5 -->
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>POST JSON</title>
 <link rel="stylesheet" href="/css/style.css" />
 <style>
 </style>
 <script>
  window.onload = ()=>{
    const button1 = document.getElementById("button1")
    const result = document.getElementById("result")
    button1.addEventListener("click", async (event) => {
      const path = document.getElementById("path").value.replaceAll("\\", "/")
      const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
      const body = `{"path":"${path}"}`
      const res = await fetch("/cgi-bin/RubyCGI/post_json.cgi", {"method":"POST", headers, body})
      const data = await res.json()
      let s = `ファイルサイズ：${data.size}, 最終更新日：${data.lastwrite}, モード：${data.mode.toString(8)}`
      result.innerText = "OK: " + s
    })
  }
 </script>
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>POST JSON</h1>
  <p style="padding:10px;text-align:center;"><a href="javascript:location='post_json.cgi'">Reset</a> | <a href="index.cgi">Index</a></p>
 </header>

 <!-- 本文 -->
 <article>
  <p>指定したファイルの属性を返す。</p>
  <form>
   <div class="form_row"><label>ファイルのパス名：<input type="text" id="path" size="100" /></label></div>
   <div style="padding:10px"><button type="button" id="button1">送信</button></div>
  </form>
  <p id="result" class="message"></p>
 </article>

 <!-- フッター -->
 <footer>
  <p>&nbsp;</p>
  <p style="text-align:center;"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
 </footer>
</body>
</html>
```

### 3.8 POST FormData

Web service with a FormData object parameter.

ruby source
```#!C:/Ruby33-x64/bin/ruby.exe
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
```

erb source
```<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>POST FormData</title>
 <link rel="stylesheet" href="/css/style.css" />
 <style>
   h1 {
     text-align: center;
     color: crimson;
     padding: 10px;
   }
   a:link, a:visited {
     text-decoration: none;
     color: firebrick;
   }
 </style>
 <script>
  async function query() {
    //headers = {"Content-Type":"multipart-formdata"}
    body = new FormData(form1)
    const res = await fetch("/cgi-bin/RubyCGI/post_formdata.cgi", {"method":"POST", body})
    const val = await res.text()
    const result = document.getElementById('result')
    result.innerText = "結果： " + val
  }
 </script>
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>POST FormData</h1>
  <p style="padding:10px;text-align:center;"><a href="javascript:location='post_formdata.cgi'">Reset</a> | <a href="index.cgi">Index</a></p>
 </header>

 <!-- 本文 -->
 <article>
   <p>cm と inch を相互変換する。</p>
   <form name="form1">
    <div><label>長さの値: <input type="text" name="length" style="font-size:11pt;" /></label></div>
    <fieldset style="margin-top:10px; margin-bottom:20px; width:40%;">
      <label><input type="radio" name="convert" value="1" checked="checked" /> ｃｍからインチへ</label><br />
      <label><input type="radio" name="convert" value="2" /> インチからｃｍへ</label>
    </fieldset>
    <div style="margin-top:15px"><button type="button" id="button1" onclick="javascript:query()">送信</button></div>
   </form>
   <p id="result" class="message"></p>
 </article>

 <!-- フッター -->
 <footer>
  <p>&nbsp;</p>
  <p style="text-align:center;"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
 </footer>
</body>
</html>
```

### 3.9 Cookies

Using a cookie example.

ruby source
```#!C:/Ruby33-x64/bin/ruby.exe
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
```

erb source
```<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>Cookies</title>
 <link rel="stylesheet" href="/css/style.css" />
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>Cookies</h1>
  <p style="padding:10px;text-align:center;"><a href="javascript:location='cookies.cgi'">Reset</a> | <a href="index.cgi">Index</a></p>
 </header>

 <!-- 本文 -->
 <article>
   <p>Reset メニューをクリックするとカウントアップする。</p>
   <p style="margin-left:10%;padding:15px;font-size:larger;">
    <a href="/cgi-bin/RubyCGI/cookies.cgi?counter=0">カウントをリセットする。</a>&nbsp;|&nbsp;
    <a href="/cgi-bin/RubyCGI/cookies.cgi">カウントを増やす。</a><br />
   </p>
   <p id="result" class="message"><%= message %></p>
 </article>

 <!-- フッター -->
 <footer>
  <p>&nbsp;</p>
  <p style="text-align:center;"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
 </footer>
</body>
</html>
```

### 3.10 Error Status

Respond error status.

ruby source
```#!C:/Ruby33-x64/bin/ruby.exe
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
```

erb source
```<!DOCTYPE html>
<html lang="ja">
<head>
 <meta charset="utf-8" />
 <meta name="viewport" content="width=device-width,initial-scale=1" />
 <title>Error Status</title>
 <link rel="stylesheet" href="/css/style.css" />
</head>

<body>
 <!-- ヘッダー -->
 <header>
  <h1>Error Status</h1>
  <p style="padding:10px;text-align:center;"><a href="javascript:location='error_status.cgi'">Reset</a> | <a href="index.cgi">Index</a></p>
 </header>

 <!-- 本文 -->
 <article>
  <ul>
   <li><a href="/cgi-bin/RubyCGI/error_status.cgi?error=NOT_FOUND">NOT FOUND</a></li>
   <li><a href="/cgi-bin/RubyCGI/error_status.cgi?error=SERVER_ERROR">SERVER ERROR</a></li>
   <li><a href="/cgi-bin/RubyCGI/error_status.cgi?error=BAD_REQUEST">BAD REQUEST</a></li>
  </ul>
  <p id="result" class="message"></p>
 </article>

 <!-- フッター -->
 <footer>
  <p>&nbsp;</p>
  <p style="text-align:center;"><a href="#top">TOP</a></p>
  <p>&nbsp;</p>
  <p>&nbsp;</p>
 </footer>
</body>
</html>

```
