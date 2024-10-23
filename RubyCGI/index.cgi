#!C:/Ruby33-x64/bin/ruby.exe
require "./RubyCGI"

CONFIG = "./config.json"
rcgi = RubyCGI.new(CONFIG)
html = rcgi.render("./views/index.erb", {"title"=>"RubyCGI", "ver"=>RubyCGI.Version, "config"=>JSON.pretty_generate(rcgi.settings)})
rcgi.send_html(html)