require "cgi"
require "cgi/cookie"
require "erb"
require "json"
require "logger"

# ERB を利用できる CGI クラス
class RubyCGI < CGI
  @@VERSION = "1.0.5"
  @@Status = {
    "OK" => "200 OK",
    "PARTIAL_CONTENT" => "206 Partial Content",
    "MULTIPLE_CHOICES" => "300 Multiple Choices",
    "MOVED" => "301 Moved Permanently",
    "REDIRECT" => "302 Found",
    "NOT_MODIFIED" => "304 Not Modified",
    "BAD_REQUEST" => "400 Bad Request",
    "AUTH_REQUIRED" => "401 Authorization Required",
    "FORBIDDEN" => "403 Forbidden",
    "NOT_FOUND" => "404 Not Found",
    "METHOD_NOT_ALLOWED" => "405 Method Not Allowed",
    "NOT_ACCEPTABLE" => "406 Not Acceptable",
    "LENGTH_REQUIRED" => "411 Length Required",
    "PRECONDITION_FAILED" => "412 Rrecondition Failed",
    "SERVER_ERROR" => "500 Internal Server Error",
    "NOT_IMPLEMENTED" => "501 Method Not Implemented",
    "BAD_GATEWAY" => "502 Bad Gateway",
    "VARIANT_ALSO_VARIES" => "506 Variant Also Negotiates"
  }

  # コンストラクタ
  def initialize(config="", logging=false)
    super()
    begin
      @settings = {}
      if File.exist?(config)
        s = File.read(config)
        @settings = JSON.load(s)
        @logger = nil
        if logging
          if @settings.has_key?("logfile")
            @logger = Logger.new(@settings["logfile"])
          else
            @logger = Logger.new(STDERR)
          end
        end
      end
    rescue
      $stderr.puts "初期化に失敗しました。設定ファイルの内容が間違っていないかチェックしてください。"
    end
  end
  
  # ログを取る。
  def log(message, level=Logger::Severity::INFO)
    if not @logger.nil?
      message = "<nil>" if message.nil?
      message = message.to_s
      @logger.add(level, message)
    end
  end

  # パラメータを得る。
  def get_param(key, index=0)
    result = ""
    if params.has_key?(key)
      value = params[key]
      if value.nil?
        result = ""
      elsif value.is_a?(Array)
        result = value[index]
      end
    end
    return result
  end

  # パラメータがチェックボックスのON/OFFの場合、その値を BOOL で得る。
  def get_check(key, index=0)
    result = false
    if not params.nil? and params.has_key?(key)
      value = params[key]
      if value.nil?
        result = false
      elsif value.is_a?(Array)
        if value[index].nil? or value[index] == ""
          result = false
        else
          result = true
        end
      elsif value != ""
        result = true
      else
        result = false
      end
    else
      result = false
    end
    return result
  end
  
  # POST メソッドの body を得る。(content_type が x-www-urlencoded, multipart/form-data でない場合)
  def get_body()
    body = params.keys[0]
    return body
  end
  
  # POST された body が JSON の場合、ハッシュに変換する。
  def get_json()
    if request_method != "POST"
      return {}
    end
    if content_type != "application/json"
      return {}
    end
    body = get_body()
    data = JSON.load(body)
    return data
  end

  # アップロードされたファイルを指定したディレクトリに保存する。。
  def save_file(key, copy_dir="")
    if not @files.has_key?(key)
      return []
    end
    file = @files[key]
    if copy_dir != ""
      path = copy_dir + "/" + file.original_filename
      File.binwrite(path, file.read)
    end
    return file
  end
  
  # リクエストメソッドが "POST" かどうか。
  def post?()
    return request_method == "POST"
  end
  
  # リクエストメソッドが "GET" かどうか。query は、QUERY_STRING が空かどうかをチェックする。
  def get?(query=false)
    b = false
    if request_method == "GET"
      if query
        b = query_string != ""
      else
        b = query_string == ""      
      end
    end
    return b
  end

  # ERB ファイルの内容を HTML に変換する。
  def render(path, embed={})
    s = File.read(path)
    ERB.new(s).result_with_hash(embed)
  end

  # ERB 文字列を HTML に変換する。
  def render_erb(strerb, embed={})
    ERB.new(strerb).result_with_hash(embed)
  end

  # HTML をクライアントへ送る。cookies は CGI::Cookie の配列とする。
  def send_html(html, status="OK", cookies=[])
    if status == "OK" and cookies.size == 0
      out {html}
    else
     if status != "OK"
       out({"status" => status}) {html}
     else
       out({"cookie" => cookies}) {html}
     end
    end
  end

  # プレーンテキストをクライアントへ送る。
  def send_text(text)
    out("text/plain") {text.to_s}
  end

  # JSON をクライアントへ送る。
  def send_json(data)
    json = JSON.generate(data)
    out("application/json") {json}
  end

  # ファイルをクライアントへ送る。
  def send_file(path, mime_type = "")
    mime = mime_type
    if mime == ""
      ext = File.extname(path).downcase()
      case ext
        when ".jpg"
          mime = "image/jpeg"
        when ".png"
          mime = "image/png"
        when ".gif"
          mime = "image/jpeg"
        when ".svg"
          mime = "image/svg"
        when ".pdf"
          mime = "application/pdf"
        when ".html"
          mime = "text/html"
        when ".xml"
          mime = "application/xml"
        when ".mp3"
          mime = "audio/mpeg"
        when ".mp4"
          mime = "video/mp4"
        else
          mime = "text/plain"
      end
    end
    buff = File.binread(path)
    out(mime) {buff}
  end 

  # クッキーオブジェクトを作る。 (注意) values は値の配列かつ要素はすべて文字列であること。
  def make_cookie(name, values, options={})
   if options.size == 0
     return CGI::Cookie.new({'name' => name, 'value' => values})
   else
     hash = {'name' => name, 'value' => values}.merge(options)
     return CGI::Cookie.new(hash)
   end
  end

  # エラーページを返す。
  # error は "NOT_FOUND", "SERVER_ERROR", "FORBIDDEN", "BAD_REQUEST", "NOT_IMPLEMENTED", "METHOD_NOT_ALLOWED", "NOT_ACCETABLE" etc.
  def send_error(error, html="")
    if html == ""
      html = '<h2 style="color:red;padding:40px;">' + @@Status[error] + '</h2>'
    end
    out({"status" => error, "type" => "text/html"}) {html}
  end

  # クラスのバージョン
  def self.Version
    @@VERSION
  end

  # エラーステータス
  def self.Status
    @@Status
  end

  # 設定ファイルの内容
  attr_reader :settings
end