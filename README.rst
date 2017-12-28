=============
ckanext-extensionstheme
=============


------------
Requirements
------------

Compatible with CKAN 2.3+


Requires ckanext-showcase, ckanext-datarequests, ckanext-scheming:

* https://github.com/OpenGov-OpenData/ckanext-showcase

* https://github.com/conwetlab/ckanext-datarequests

* https://github.com/ckan/ckanext-scheming


Requires pandoc:

     sudo apt-get install pandoc


------------
Development Installation
------------

To install ckanext-extensionstheme:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Download the ckanext-extensionstheme github repository::

     cd /usr/lib/ckan/default/src
     git clone https://github.com/OpenGov-OpenData/ckanext-extensionstheme.git

3. Install the extension into your virtual environment::

     cd ckanext-extensionstheme
     python setup.py develop
     pip install -r dev-requirements.txt

4. Add ``extensions_theme`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

     ckan.plugins = ... extensions_theme showcase datarequests scheming_datasets

5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Add the following to the CKAN config file::

    scheming.dataset_schemas = ckanext.extensionstheme:ext_catalogue.json
    scheming.presets = ckanext.extensionstheme:dataset_presets.json
