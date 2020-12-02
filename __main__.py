"""
This is an api developed to Mercado Bitcoin improof my hard skills at developing
First of all to run this api, you are gonna need Python 3.8 or higher installed in your computer
If you dont have a installation of python, you can follow this steps:
1. you need install chocolatey, if you dont have it, just follow this link:
https://chocolatey.org/install
2. After choco(chocolatey) installed, just follow this link:
https://chocolatey.org/packages/python/3.8.0
Now, with python installed, in your console line acessing the project foulder,
paste the following command:
pip3 install -r requirements.txt
After this you are ready to run this project, Congratulations!!!!
"""

from Importation.Csv2Sql import importCsv2SqliteTable
path2csv = 'DEINFO_AB_FEIRASLIVRES_2014.csv'#Required
path2db = ''#if not passed, will get db root from url_db in db.py
print(importCsv2SqliteTable(path2csv))
#Just wait a few seconds and our Sqlite db will be created

"""
To run this application and save all his logs into a txt, you need to run with the following command:
python __main__.py >> log.txt 2>&1
Obs.: After running the first time, please run just the file app.py, just to avoid useless importation
You can also give a look at the postman documentation at:
https://documenter.getpostman.com/view/13666713/TVmMfH2B
Or if you choice swagger, when the api is running, you can acess the route:
http://127.0.0.1:5000/api/doc/swagger.json
and import as a json in your web swagger
"""

import app
