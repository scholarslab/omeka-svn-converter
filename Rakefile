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
end
