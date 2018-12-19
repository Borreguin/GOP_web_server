

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
str_conn = 'mssql+pyodbc://sivo:sivoer@DOP-WKSTAADO/sivo'
engine = create_engine('mssql+pymssql://sivo:sivoer@DOP-WKSTAADO:1433/sivo')


# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
CFG_Unidad = Base.classes.CFG_Unidad
CFG_Barra = Base.classes.CFG_Barra

session = Session(engine)

# rudimentary relationships are produced
#session.add(CFG_Barra(email_address="foo@bar.com", user=User(name="foo")))
#session.commit()

# collection-based relationships are by default named
# "<classname>_collection"
# print(u1.address_collection)