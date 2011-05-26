require 'rubygems'
require 'curb'

task :default => 'svn:migrate'

REPO_DIRECTORY = './repos'
GITHUB_ACCOUNT_NAME = 'clured'
GITHUB_ACCOUNT_TOKEN = 'bc0c6979cd69c80f7f7d9a13f6e35758'

repos = %w[https://addons.omeka.org/svn/plugins/EadImporter/ https://addons.omeka.org/svn/plugins/NeatlineFeatures/ https://addons.omeka.org/svn/plugins/NeatlineMaps/ https://addons.omeka.org/svn/plugins/SolrSearch/ https://addons.omeka.org/svn/plugins/TeiDisplay/ https://addons.omeka.org/svn/plugins/VraCoreElementSet/]

namespace :svn do

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
      `ruby readme_scrape.rb #{plugin_name}`
      `mv README.md #{REPO_DIRECTORY}/#{plugin_name}/README.md`
      `cd #{path_to_repo} && curl -F 'login=#{GITHUB_ACCOUNT_NAME}' -F 'token=#{GITHUB_ACCOUNT_TOKEN}' https://github.com/api/v2/yaml/repos/create -F name=#{plugin_name}`
      `cd #{path_to_repo} && git remote add origin git@github.com:#{GITHUB_ACCOUNT_NAME}/#{plugin_name}.git`
      `cd #{path_to_repo} && git add .`
      `cd #{path_to_repo} && git commit -m 'Added new README.md file scraped from old wikis'`
      `cd #{path_to_repo} &&  git push origin master`
      `python convert.py #{GITHUB_ACCOUNT_NAME} #{plugin_name} #{GITHUG_ACCOUNT_TOKEN}`
      break
    end
  end

end
