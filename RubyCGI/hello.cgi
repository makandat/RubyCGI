#!C:/Ruby33-x64/bin/ruby.exe
require "./RubyCGI"

rcgi = RubyCGI.new
rcgi.out("text/plain") {"Hello RubyCGI v" + RubyCGI.Version}