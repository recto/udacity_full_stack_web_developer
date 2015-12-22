# P5 Item Catalog
## Contents
* database_setup.py - a script to define database schema.
* populate_catalog.py - a script to populate catalog data.
* application.py - Web Application.

## How to run Item Catalog application
* go to P5_Item_Catalog directory.
* copy all directories and files under the above directory to vagrant/catalog.
* start the virtual machine.
* start vagrant ssh and go to /vagrant/catalog.
* perform 'python database_setup.py' to create database schema.
* perform 'python populate_catalog.py' to populate catalog data into the above.
* perform 'python application.py'.
* start web browser and go to http://localhost:8000.
* browse catalog menu without logging in.
* login with your google account.
* add categories/items.
* browse/update/delete categories/items you created the above.
