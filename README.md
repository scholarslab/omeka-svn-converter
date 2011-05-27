# Omeka Plugin SVN to Github Converts

For the impatient:

    git clone git://github.com/scholarslab/omeka-svn-converter.git
    cd omeka-svn-converter
    bundle install
  
Edit the config.yml

Github_api_token on [Github](https://github.com/account/admin) (under
Account Admin).

Run the migration:

    rake svn:migrate
