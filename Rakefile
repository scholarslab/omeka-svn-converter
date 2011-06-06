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

      # Clone the repo from SVN.
      `cd #{CONFIG['settings']['repo_directory']} && git svn clone -s #{repo}`

      # Slide out the name of the plugin, set path.
      plugin_name = repo[37..-2]
      path_to_repo = "#{CONFIG['settings']['repo_directory']}/#{plugin_name}"

      # Scrape the old readme and convert to .md format, move
      # new README.md file into the cloned plugin directory.
      generate_readme(plugin_name)
      `mv README.md #{CONFIG['settings']['repo_directory']}/#{plugin_name}/README.md`

      # Create the new repo on github.
      if CONFIG['settings']['github_organization_name'] != ''
        `cd #{path_to_repo} && curl -F 'login=#{CONFIG['settings']['github_account_name']}' -F 'token=#{CONFIG['settings']['github_account_token']}' \
             https://github.com/api/v2/yaml/repos/create -F name=#{CONFIG['settings']['github_organization_name']}/#{plugin_name}`
      else
        `cd #{path_to_repo} && curl -F 'login=#{CONFIG['settings']['github_account_name']}' -F 'token=#{CONFIG['settings']['github_account_token']}' \
             https://github.com/api/v2/yaml/repos/create -F name=#{plugin_name}`
      end

      # Add origin, add/commit, push.
      if CONFIG['settings']['github_organization_name'] != ''
        `cd #{path_to_repo} && git remote add origin git@github.com:#{CONFIG['settings']['github_organization_name']}/#{plugin_name}.git`
      else
        `cd #{path_to_repo} && git remote add origin git@github.com:#{CONFIG['settings']['github_account_name']}/#{plugin_name}.git`
      end
      `cd #{path_to_repo} && git add .`
      `cd #{path_to_repo} && git commit -m 'Added new README.md file scraped from old wikis'`
      `cd #{path_to_repo} && git push origin master`

      # Run the python script to migrate the Trac tickets to Github issues.
      `python convert.py #{CONFIG['settings']['github_account_name']} #{CONFIG['settings']['github_organization_name']} #{plugin_name} #{CONFIG['settings']['github_account_token']}`

      # Pause at the end of the loop, as as to avoid overloading the API.
      sleep CONFIG['settings']['api_wait']

    end
  end



end
