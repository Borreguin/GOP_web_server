from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from classes import models as mdl

# creating the engine and session
engine = create_engine('mssql+pymssql://sivo:sivoer@DOP-WKSTAADO:1433/sivo')
ses = Session(engine)

id = ses.query(mdl.CFGTipoUnidadNegocio.IdTipoUnidadNegocio)\
    .filter(mdl.CFGTipoUnidadNegocio.Nombre == "Generación").first()
id = id.IdTipoUnidadNegocio


rs = ses.query(mdl.CFGUnidadNegocio.Codigo, mdl.CFGUnidadNegocio.IdUNegocio).\
    filter(mdl.CFGUnidadNegocio.IdTipoUnidadNegocio == id).all()

unidades = ses.query(mdl.CFGUnidad.Codigo, mdl.CFGUnidad.Nombre).\
    filter(mdl.CFGUnidad.FechaBaja == None).all()


for cod, name in unidades:
    print(cod, name)

#for r in rs:
#    print(r.Codigo, r.IdUNegocio)

# rudimentary relationships are produced
#session.add(CFG_Barra(email_address="foo@bar.com", user=User(name="foo")))
#session.commit()

# collection-based relationships are by default named
# "<classname>_collection"
# print(u1.address_collection)