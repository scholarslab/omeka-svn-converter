# Omeka SVN -> GitHub Migration
This rake script automates the process of moving Omeka plugin
repositories from SVN to GitHub. The script:

- Migrates the repositories;
- Scrapes the wikis from Omeka.org and converts them to README.md files.
- Migrates all existing Trac tickets for the plugin into the GitHub Issues platform.

## Instructions
- Change config.yml.example -> config.yml;
- Enter values for empty github account name, account token, and
organization name;
- Add the URLs for each of the repos;
- To do the migration, use:
        rake svn:migrate
- To scrub out the generated directory structure and start over (useful
if the GitHub API hangs up, or something else goes wrong), use:
        rake svn:clean

## Organizations vs. User Accounts
-If the github organization name parameter is set in the config.yml file,
the rake script will migrate the repository to the organization,
assuming the supplied github user account has access privileges. If the
organization name is left blank, the script will migrate the
repository directly to the individual user account.
