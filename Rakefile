require 'rubygems'
require 'curb'
require 'mechanize'

task :default => 'svn:list'

repos = %w[https://addons.omeka.org/svn/plugins/EadImporter/ https://addons.omeka.org/svn/plugins/NeatlineFeatures/ https://addons.omeka.org/svn/plugins/NeatlineMaps/ https://addons.omeka.org/svn/plugins/SolrSearch/ https://addons.omeka.org/svn/plugins/TeiDisplay/ https://addons.omeka.org/svn/plugins/VraCoreElementSet/]


namespace :svn do
  desc 'List the repos to migrate to Github'

  task :list do
    repos.each do |repo|
      puts repo
    end
  end

  task :migrate do
    repos.each do |repo|
      system "git svn clone -s " + repo
      plugin_name = repo[37..-2]
      system "ruby readme_scrape.rb " + plugin_name
      system "mv README.md " + plugin_name + "/README.md"
      system "cd " + plugin_name
      github_account_name = "clured"
      github_account_api_token = "bc0c6979cd69c80f7f7d9a13f6e35758"
      system "curl -F 'login=" + github_account_name + "' -F 'token=" + github_account_api_token + "' https://github.com/api/v2/yaml/repos/create -F name=" + plugin_name
      system "git remote add origin git@github.com:" + github_account_name + "/" + plugin_name + ".git"
      system "git add ."
      system "git commit -m 'Added new README.md file scraped from old wikis'"
      system "git push origin master"
      system "cd .."
      system "python convert.py " + github_account_name + " " + plugin_name + " " + github_account_api_token
    end
  end

end
