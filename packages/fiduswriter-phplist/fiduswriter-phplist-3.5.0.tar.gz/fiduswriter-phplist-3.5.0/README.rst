=====
FidusWriter-PHPList
=====

FidusWriter-PHPList is a Fidus writer plugin to connect a Fidus Writer instance
with an email list using PHPList. It allows users signing up on the Fidus Writer instance to also sign up for the email list.


Installation
-----------

1. Install Fidus Writer and PHPList 3.X if you haven't done so already.

2. Create an email list within PHPList if you don't have one already. Take note of the list ID.

3. Within PHPList, install the REST API plugin.

4. Setup an admin user with access rights to manage subscriber lists within PHPList.

5. Within the virtual environment set up for your Fidus Writer instance, install the version of the plugin corresponding to your Fidus Writer installation.
   If you are running Fidus Writer 3.4, the command is::

    pip install "fiduswriter-ojs<3.5"

6. Add "phplist" to your INSTALLED_APPS setting in the configuration.py file
   like this::

    INSTALLED_APPS += (
        ...
        'phplist',
    )

7. Add these settings to configuration.py::

    PHPLIST_BASE_URL # The URL of your PHPList installation
    PHPLIST_LOGIN # The PHPList user's username created in step 4
    PHPLIST_PASSWORD # The PHPList user's password created in step 4
    PHPLIST_SECRET (optional) # If you have set an obligatory secret within the PHPLIst REST API, set it here as well.
    PHPLIST_LIST_ID # The email list id found in step 2.

8. (Re)start your Fidus Writer server.
