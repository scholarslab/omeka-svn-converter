# Omeka Plugins: Migrate SVN to Github

This package moves Omeka plugins from SVN to GitHub, generates README.md
files from existing wikis, and migrates open Trac tickets into the
GitHub Issues platform.

## Installation

- git clone git://github.com/scholarslab/omeka-svn-converter.git
- cd omeka-svn-converted
- bundle install

## Usage

- Rename or duplicate the config.yml.example as config.yml and edit the file with GitHub account name, token, and
  list of repositories to be migrated. The account token can be found at
Accont Settings > Account Admin.
- From the omeka-svn-converter folder, run the migration with:

        rake svn:migrate

- To wipe out the "repos" directory created by the script and start
  over, use the clean task:

        rake svn:clean
