Los siguientes son requisitos para este servidor:
    - python 3.x
    - Flask	0.12.2	0.12.2
    - Jinja2	2.10	2.10
    - MarkupSafe	1.0	1.0
    - Werkzeug	0.14.1	0.14.1
    - click	6.7	6.7
    - itsdangerous	0.24	0.24
    - numpy	1.14.2	1.14.2
    - pandas	0.22.0	0.22.0
    - pip	9.0.1	10.0.0
    - python-dateutil	2.7.2	2.7.2
    - pytz	2018.4	2018.4
    - setuptools	28.8.0	39.0.1
    - six	1.11.0	1.11.0
    - xlrd	1.1.0	1.1.0
    - SQLAlchemy	1.2.6	1.2.7
    conda install -c conda-forge cufflinks-py -y
    conda install -c conda-forge flask-excel -y
    conda install -c anaconda xlutils -y
    conda install -c anaconda pymongo -y


command:
conda install -c conda-forge tqdm
conda install -y Flask Jinja2 MarkupSafe Werkzeug click itsdangerous numpy pandas pip
conda install -y python-dateutil pytz setuptools six xlrd SQLAlchemy pymssql
conda install -y ipyparallel
pip install wfastcgi
pip install hmmlearn

Aplicativos adicionales:

    - PI-SDK (version 2014 mínimo)
    - AF-Client (version 2016 mínimo)
    conda install -c pythonnet pythonnet
    conda install wfastcgi

Create sql-classes:
run in the cmd, and copy the 'model' file to classes folder:
sqlacodegen mssql+pymssql://sivo:sivoer@DOP-WKSTAADO:1433/sivo --outfile models.py

IIS Instalation:
Handler Mappings:
    C:\ProgramData\Anaconda3\python.exe | C:\ProgramData\Anaconda3\Lib\site-packages\wfastcgi.py


Fix problem when using plotly and IIS:
C:\ProgramData\Anaconda3\lib\site-packages\plotly\optional_imports.py
