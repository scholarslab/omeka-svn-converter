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

task :default => 'svn:list_repos'

CONFIG = YAML.load(File.read('config.yml'))

# Use the McBean gem to convert HTML documentation to Markdown
def generate_readme(plugin_name)

  page = Nokogiri::HTML(open(CONFIG['settings']['documentation_base'] + plugin_name))

  content_div = page.css('#primary').to_html

  markdown = McBean.fragment(content_div).to_markdown

  File.open('README.md', 'w') do |file|
    file.puts markdown
  end

end

namespace :svn do

  desc 'List configuration items'
  task :config do
    puts CONFIG['settings'].inspect
  end

  desc 'List repos to migrate to Github'
  task :list_repos do 
    CONFIG['settings']['repos'].each do |repo|
       puts repo
     end
  end

  desc 'Clean up the migration directory'
  task :clean do
    FileUtils.rm_rf(CONFIG['settings']['repo_directory'])
  end

  desc 'Create a directory for the repositories'
  task :setup do
    FileUtils.mkdir_p(CONFIG['settings']['repo_directory'])
  end

  desc 'Migrate the repositories'
  task :migrate => [:setup]  do
    CONFIG['settings']['repos'].each do |repo|
      `cd #{CONFIG['settings']['repo_directory']} && git svn clone -s #{repo}`
      plugin_name = repo[37..-2] # Slice the name out of the plugin out of the URL
      path_to_repo = "#{CONFIG['settings']['repo_directory']}/#{plugin_name}"
      generate_readme(plugin_name)
      `mv README.md #{CONFIG['settings']['repo_directory']}/#{plugin_name}/README.md`
      `cd #{path_to_repo} && curl -F 'login=#{CONFIG['settings']['github_account_name']}' -F 'token=#{CONFIG['settings']['github_account_token']}' \
           https://github.com/api/v2/yaml/repos/create -F name=#{plugin_name}`
      `cd #{path_to_repo} && git remote add origin git@github.com:#{CONFIG['settings']['github_account_name']}/#{plugin_name}.git`
      `cd #{path_to_repo} && git add .`
      `cd #{path_to_repo} && git commit -m 'Added new README.md file scraped from old wikis'`
      `cd #{path_to_repo} && git push origin master`
      `python convert.py #{CONFIG['settings']['github_account_name']} #{plugin_name} #{CONFIG['settings']['github_account_token']}`
      sleep CONFIG['settings']['api_wait']
    end
  end



end
