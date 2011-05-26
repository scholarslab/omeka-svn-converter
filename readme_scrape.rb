# Takes one argument from cli - the name of the plugin/repo

require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'mcbean'

page = Nokogiri::HTML(open('http://omeka.org/codex/Plugins/' + ARGV[0]))

content_div = page.css('#primary').to_html

markdown = McBean.fragment(content_div).to_markdown

File.open('README.md', 'w') do |file|
  file.puts markdown
end
