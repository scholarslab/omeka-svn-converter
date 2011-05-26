require 'nokogiri'
require 'open-uri'
require 'mcbean'
require 'yaml'

# 
# This rake script helps automate the migration of SVN repositories to Github
#
# Author:: Scholars' Lab
# Copyright:: Copyright (c) 2011 The Board and Visitors of the University of Virginia
# License:: http://www.apache.org/licenses/LICENSE-2.0.html Apache 2 License

task :default => 'svn:migrate'

config = YAML.load(File.read('config.yml'))

# Use the McBean gem to convert HTML documentation to Markdown
def generate_readme(plugin_name)

  page = Nokogiri::HTML(open(DOCUMENTATION_BASE + plugin_name))

  content_div = page.css('#primary').to_html

  markdown = McBean.fragment(content_div).to_markdown

  File.open('README.md', 'w') do |file|
    file.puts markdown
  end

end

namespace :svn do


  desc 'List configuration items'
  task :config do
    puts config.inspect
  end

  desc 'Create a directory for the repositories'
  task :setup do
    FileUtils.mkdir_p(REPO_DIRECTORY)
  end

  desc 'Migrate the repositories'
  task :migrate => [:setup]  do
    repos.each do |repo|
      `cd #{REPO_DIRECTORY} && git svn clone -s #{repo}`
      plugin_name = repo[37..-2] # Slice the name out of the plugin out of the URL
      path_to_repo = "#{REPO_DIRECTORY}/#{plugin_name}"
      #`ruby readme_scrape.rb #{plugin_name}`
      generate_readme(plugin_name)
      `mv README.md #{REPO_DIRECTORY}/#{plugin_name}/README.md`
      `cd #{path_to_repo} && curl -F 'login=#{GITHUB_ACCOUNT_NAME}' -F 'token=#{GITHUB_ACCOUNT_TOKEN}'\
           https://github.com/api/v2/yaml/repos/create -F name=#{plugin_name}`
      `cd #{path_to_repo} && git remote add origin git@github.com:#{GITHUB_ACCOUNT_NAME}/#{plugin_name}.git`
      `cd #{path_to_repo} && git add .`
      `cd #{path_to_repo} && git commit -m 'Added new README.md file scraped from old wikis'`
      `cd #{path_to_repo} && git push origin master`
      `python convert.py #{GITHUB_ACCOUNT_NAME} #{plugin_name} #{GITHUB_ACCOUNT_TOKEN}`
      sleep 60 # Necessary to keep script from exceeding the GitHub API's rate limiting.
      break
    end
  end



end
