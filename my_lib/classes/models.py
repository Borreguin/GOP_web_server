# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, ForeignKey, Index, Integer, LargeBinary, Numeric, SmallInteger, String, Table, Time, Unicode, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql.base import BIT, SQL_VARIANT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AGTCaudalesNivelesHorario(Base):
    __tablename__ = 'AGT_CaudalesNivelesHorarios'
    __table_args__ = (
        Index('IX_AGT_CaudalesNivelesHorarios_Fecha_Hora', 'Fecha', 'Hora', 'Central', 'Cau_Ent_Prom', 'Cau_Ent_Hora', 'Cau_Des_Fondo', 'Nivel'),
        Index('IX_AGT_CaudalesNivelesHorarios_Central', 'Empresa', 'UNegocio', 'Embalse', 'Central', 'Fecha', 'Hora', 'Cau_Ent_Prom', 'Cau_Ent_Hora', 'Cau_Lat_Prom', 'Cau_Turbinado', 'Cau_Vertido', 'Cau_Des_Fondo', 'Nivel', 'Cota_Descarga', 'Altura_Neta', 'NombreArchivo', unique=True)
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Embalse = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    Cau_Ent_Prom = Column(Numeric(10, 2))
    Cau_Ent_Hora = Column(Numeric(10, 2))
    Cau_Lat_Prom = Column(Numeric(10, 2))
    Cau_Turbinado = Column(Numeric(10, 2))
    Cau_Vertido = Column(Numeric(10, 2))
    Cau_Des_Fondo = Column(Numeric(10, 2))
    Nivel = Column(Numeric(10, 2))
    Cota_Descarga = Column(Numeric(10, 2))
    Altura_Neta = Column(Numeric(10, 2))
    Agente = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCarga = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    NombreArchivo = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    NombreFicha = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class AGTCaudalesNivelesHorariosDiaActual(Base):
    __tablename__ = 'AGT_CaudalesNivelesHorariosDiaActual'
    __table_args__ = (
        Index('IDX_AGT_CaudalesNivelesHorariosDiaActual', 'Empresa', 'UNegocio', 'Embalse', 'Central', 'Fecha', 'Hora', 'Cau_Ent_Prom', 'Cau_Ent_Hora', 'Cau_Lat_Prom', 'Cau_Turbinado', 'Cau_Vertido', 'Cau_Des_Fondo', 'Nivel', 'Cota_Descarga', 'Altura_Neta', 'NombreArchivo', unique=True),
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Embalse = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    Cau_Ent_Prom = Column(Numeric(10, 2))
    Cau_Ent_Hora = Column(Numeric(10, 2))
    Cau_Lat_Prom = Column(Numeric(10, 2))
    Cau_Turbinado = Column(Numeric(10, 2))
    Cau_Vertido = Column(Numeric(10, 2))
    Cau_Des_Fondo = Column(Numeric(10, 2))
    Nivel = Column(Numeric(10, 2))
    Cota_Descarga = Column(Numeric(10, 2))
    Altura_Neta = Column(Numeric(10, 2))
    Agente = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCarga = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    NombreArchivo = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    NombreFicha = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class AGTEntrega(Base):
    __tablename__ = 'AGT_Entrega'
    __table_args__ = (
        Index('IX_AGT_Entrega_IXPrincipal', 'Fecha', 'Hora', 'Posicion', 'Subestacion', 'UNegocio', 'Empresa', 'MV', 'MVAR', 'EmpresaDestino', 'UNegocioDestino', unique=True),
        Index('IX_AGT_Entrega_Validacion', 'Fecha', 'Posicion', 'Hora', 'MV', 'MVAR', 'CodigoAgente')
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Subestacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Posicion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    MV = Column(Numeric(10, 2), nullable=False)
    MVAR = Column(Numeric(10, 2), nullable=False)
    EmpresaDestino = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    UNegocioDestino = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    CodigoAgente = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCarga = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    NombreArchivo = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    NombreFicha = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class AGTGeneracion(Base):
    __tablename__ = 'AGT_Generacion'
    __table_args__ = (
        Index('AGT_GeneracionUnidad', 'Central', 'Unidad', 'Fecha', 'Hora', 'MV', 'MVAR', unique=True),
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Unidad = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    MV = Column(Numeric(10, 2), nullable=False)
    MVAR = Column(Numeric(10, 2), nullable=False)
    Agente = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCarga = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    NombreArchivo = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    NombreFicha = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class AGTInformacionHidrologica(Base):
    __tablename__ = 'AGT_InformacionHidrologica'
    __table_args__ = (
        Index('IDX_AGT_InformacionHidrologica', 'Empresa', 'UNegocio', 'Embalse', 'Central', 'Fecha', 'Hora', 'Horas_Aper_Desfondo_dia', 'Caudal_Prom', 'Energia_Rem_Alm_Emb_Destino', 'Energia_Rem_Total_Almacenada', 'Vol_Almacenado', 'Vol_Turbinado', 'Vol_Vertido', 'Vol_Des_Fondo', 'Energia_Emergencia_Emb_Destino', 'NombreArchivo', 'Nivel', 'Res_Energetica', 'Energia_Rem_Almacenada', 'Embalse_Destino', unique=True),
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Embalse = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    Vol_Almacenado = Column(Numeric(10, 2))
    Vol_Turbinado = Column(Numeric(10, 2))
    Vol_Vertido = Column(Numeric(10, 2))
    Vol_Des_Fondo = Column(Numeric(10, 2))
    Vol_Util = Column(Numeric(10, 2))
    Horas_Aper_Desfondo_dia = Column(Numeric(10, 2))
    Caudal_Prom = Column(Numeric(10, 2))
    Nivel = Column(Numeric(10, 2))
    Res_Energetica = Column(Numeric(10, 2))
    Energia_Rem_Almacenada = Column(Numeric(10, 2))
    Embalse_Destino = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Energia_Rem_Alm_Emb_Destino = Column(Numeric(10, 2))
    Energia_Rem_Total_Almacenada = Column(Numeric(10, 2))
    Energia_Emergencia_Emb_Destino = Column(Numeric(10, 2))
    Agente = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCarga = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    NombreArchivo = Column(String(500, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    NombreFicha = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class AGTNovedade(Base):
    __tablename__ = 'AGT_Novedades'
    __table_args__ = (
        Index('IX_AGT_Novedades_IXPrincipal', 'Central', 'Unidad', 'Fecha', 'Hora', 'Evento', 'Causal', 'MW', 'Descripcion', unique=True),
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Unidad = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    Evento = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Causal = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    MW = Column(Numeric(10, 2))
    Descripcion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Agente = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCarga = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    NombreArchivo = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    NombreFicha = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class AGTProducConsumGa(Base):
    __tablename__ = 'AGT_ProducConsumGas'
    __table_args__ = (
        Index('IND_ConsumoGas', 'Fecha', 'COD_CENTRAL', 'COD_UNIDAD', unique=True),
    )

    IdGas = Column(Integer, primary_key=True)
    Fecha = Column(Date, nullable=False)
    COD_CENTRAL = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre_Central = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    COD_UNIDAD = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre_Unidad = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Produccion_MWh = Column(Numeric(10, 2), nullable=False)
    ConsumoGas_MPCD = Column(Numeric(10, 2), nullable=False)


class AGTPronosticosHidrologico(Base):
    __tablename__ = 'AGT_PronosticosHidrologicos'
    __table_args__ = (
        Index('IX_AGT_PronosticosHidrologicos_IXPrincipal', 'Empresa', 'UNegocio', 'Embalse', 'Central', 'FechaInicio', 'FechaFin', 'NSemana', 'Cau_Pronosticado', 'Limite_Inferior', 'Limite_Superior', 'Nivel_Confianza', unique=True),
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Embalse = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaInicio = Column(Date, nullable=False)
    FechaFin = Column(Date, nullable=False)
    NSemana = Column(Integer)
    Cau_Pronosticado = Column(Numeric(10, 2))
    Limite_Inferior = Column(Numeric(10, 2))
    Limite_Superior = Column(Numeric(10, 2))
    Nivel_Confianza = Column(Numeric(10, 2))
    Agente = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCarga = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    NombreArchivo = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    NombreFicha = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class CATGrupo(Base):
    __tablename__ = 'CAT_Grupos'

    Id_Grupo = Column(Integer, primary_key=True)
    Grupo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class CATTabla(Base):
    __tablename__ = 'CAT_Tablas'

    Id_Tabla = Column(Integer, primary_key=True)
    Id_Grupo = Column(ForeignKey('CAT_Grupos.Id_Grupo'), nullable=False)
    Nombre_Tabla = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Descripcion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))

    CAT_Grupo = relationship('CATGrupo')


class CFGBancoTransformadore(Base):
    __tablename__ = 'CFG_BancoTransformadores'

    IdBancoTransformador = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdBarraOrigen = Column(ForeignKey('CFG_Barra.IdBarra'), nullable=False, index=True)
    IdBarraDestino = Column(ForeignKey('CFG_Barra.IdBarra'), nullable=False, index=True)
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False)
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, server_default=text("(getdate())"))
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))

    CFG_Barra = relationship('CFGBarra', primaryjoin='CFGBancoTransformadore.IdBarraDestino == CFGBarra.IdBarra')
    CFG_Barra1 = relationship('CFGBarra', primaryjoin='CFGBancoTransformadore.IdBarraOrigen == CFGBarra.IdBarra')


class CFGBandaHoraria(Base):
    __tablename__ = 'CFG_BandaHoraria'

    IdBandaHoraria = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    HoraInicio = Column(Time, nullable=False)
    HoraFin = Column(Time, nullable=False)
    FactorPotenciaMin = Column(Numeric(10, 5), nullable=False)
    FactorPotenciaMax = Column(Numeric(10, 5), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaModificacion = Column(DateTime, server_default=text("(getdate())"))
    UsuarioModificador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaInicio = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    FechaExpiracion = Column(DateTime)
    Estado = Column(BIT, nullable=False)


class CFGBarra(Base):
    __tablename__ = 'CFG_Barra'
    __table_args__ = (
        Index('IX_CFG_Barra_ID', 'IdEmpresa', 'IdUNegocio', 'IdSubEstacion', 'IdBarra', 'VoltajeID', 'Norma_ID'),
        Index('IX_CFG_Barra', 'IdBarra', 'Codigo', 'Nombre')
    )

    IdBarra = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdTipoBarra = Column(ForeignKey('CFG_TipoBarra.IdTipoBarra'), nullable=False)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False)
    IdSubEstacion = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'), nullable=False)
    VoltajeID = Column(Integer, nullable=False, server_default=text("((1))"))
    Norma_ID = Column(ForeignKey('CFG_Voltajes_MAX_MIN.Norma_ID'))
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))

    CFG_Empresa = relationship('CFGEmpresa')
    CFG_SubEstacion = relationship('CFGSubEstacion')
    CFG_TipoBarra = relationship('CFGTipoBarra')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')
    CFG_Voltajes_MAX_MIN = relationship('CFGVoltajesMAXMIN')


class CFGCarga(Base):
    __tablename__ = 'CFG_Carga'

    IdCarga = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdTerminal = Column(ForeignKey('CFG_Terminal.IdTerminal'), nullable=False, index=True)
    IdNivelVoltaje = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False, index=True)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_Empresa = relationship('CFGEmpresa')
    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')
    CFG_Terminal = relationship('CFGTerminal')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGCentral(Base):
    __tablename__ = 'CFG_Central'
    __table_args__ = (
        Index('IDX_CFG_Central_FA_FB', 'FechaAlta', 'FechaBaja'),
    )

    IdCentral = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdTipoGeneracion = Column(ForeignKey('CFG_TipoGeneracion.IdTipoGeneracion'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    Direccion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    IdPais = Column(ForeignKey('CFG_Pais.IdPais'), nullable=False, index=True)
    IdProvincia = Column(ForeignKey('CFG_Provincia.IdProvincia'), nullable=False, index=True)
    IdCiudad = Column(ForeignKey('CFG_Ciudad.IdCiudad'), nullable=False, index=True)
    Telefono = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Fax = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Email = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT, nullable=False)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_Ciudad = relationship('CFGCiudad')
    CFG_Empresa = relationship('CFGEmpresa')
    CFG_Pai = relationship('CFGPai')
    CFG_Provincia = relationship('CFGProvincia')
    CFG_TipoGeneracion = relationship('CFGTipoGeneracion')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGCentralNivelVoltaje(Base):
    __tablename__ = 'CFG_CentralNivelVoltaje'

    Row_ID = Column(BigInteger, primary_key=True)
    IdCentral = Column(ForeignKey('CFG_Central.IdCentral'), nullable=False)
    IdNivelVoltaje = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    CFG_Central = relationship('CFGCentral')
    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')


class CFGCircuito(Base):
    __tablename__ = 'CFG_Circuito'

    IdCircuito = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdLinea = Column(ForeignKey('CFG_Linea.IdLinea'), nullable=False, index=True)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdNivelVoltaje = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False, index=True)
    NumCircuito = Column(SmallInteger, nullable=False)
    PerdDestOrigen = Column(Numeric(10, 2))
    PerdOriDest = Column(Numeric(10, 2))
    ProbFalla = Column(Numeric(10, 2))
    Reactancia = Column(Numeric(10, 2))
    Resistencia = Column(Numeric(10, 2))
    Susceptancia = Column(Numeric(10, 2))
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    IdSubestacionOri = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'))
    IdSubestacionDest = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'))

    CFG_Empresa = relationship('CFGEmpresa')
    CFG_Linea = relationship('CFGLinea')
    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')
    CFG_SubEstacion = relationship('CFGSubEstacion', primaryjoin='CFGCircuito.IdSubestacionDest == CFGSubEstacion.IdSubestacion')
    CFG_SubEstacion1 = relationship('CFGSubEstacion', primaryjoin='CFGCircuito.IdSubestacionOri == CFGSubEstacion.IdSubestacion')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGCiudad(Base):
    __tablename__ = 'CFG_Ciudad'

    IdCiudad = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdProvincia = Column(ForeignKey('CFG_Provincia.IdProvincia'), nullable=False, index=True)
    IdPais = Column(ForeignKey('CFG_Pais.IdPais'), nullable=False, index=True)
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_Pai = relationship('CFGPai')
    CFG_Provincia = relationship('CFGProvincia')


class CFGCompensador(Base):
    __tablename__ = 'CFG_Compensador'

    IdCompensador = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdSubestacion = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'), nullable=False, index=True)
    IdNivelVoltaje = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False, index=True)
    IdTipoCompensador = Column(ForeignKey('CFG_TipoCompensador.IdTipoCompensador'), nullable=False, index=True)
    MVAR_Nominal = Column(Numeric(20, 2))
    Num_Modulos = Column(SmallInteger)
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))

    CFG_Empresa = relationship('CFGEmpresa')
    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')
    CFG_SubEstacion = relationship('CFGSubEstacion')
    CFG_TipoCompensador = relationship('CFGTipoCompensador')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGDiaEspecial(Base):
    __tablename__ = 'CFG_DiaEspecial'

    IdDiaEspecial = Column(Integer, primary_key=True)
    IdTipo = Column(ForeignKey('CFG_TiposDias.IdTipo'), nullable=False)
    Fecha = Column(Date, nullable=False)
    Descripcion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaUltimaModificacion = Column(DateTime, server_default=text("(getdate())"))
    UsuarioModificador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))

    CFG_TiposDia = relationship('CFGTiposDia')


class CFGElementoTAG(Base):
    __tablename__ = 'CFG_ElementoTAG'
    __table_args__ = (
        Index('IX_CFG_ElementoTAG_ET', 'IdElemento', 'IdTAG'),
    )

    Row_ID = Column(BigInteger, primary_key=True)
    IdElemento = Column(Integer, nullable=False)
    IdTAG = Column(ForeignKey('CFG_TAG.IdTAG'), nullable=False)
    FechaAsociacion = Column(DateTime, nullable=False)
    UsuarioAsociacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))

    CFG_TAG = relationship('CFGTAG')


class CFGElementosConectado(Base):
    __tablename__ = 'CFG_ElementosConectados'

    IdElementoConectado = Column(Integer, primary_key=True)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdSubestacion = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'), nullable=False, index=True)
    IdBarra = Column(ForeignKey('CFG_Barra.IdBarra'), nullable=False, index=True)
    IdCarga = Column(ForeignKey('CFG_Carga.IdCarga'), nullable=False, index=True)
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_Barra = relationship('CFGBarra')
    CFG_Carga = relationship('CFGCarga')
    CFG_Empresa = relationship('CFGEmpresa')
    CFG_SubEstacion = relationship('CFGSubEstacion')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGEmbalse(Base):
    __tablename__ = 'CFG_Embalse'
    __table_args__ = (
        Index('IDX_CFG_Embalse_FA_FB', 'FechaAlta', 'FechaBaja'),
    )

    IdEmbalse = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, index=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, index=True)
    CD_EST_HID = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Tipo = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    VAL_CONS_AREA = Column(Numeric(10, 2))
    VAL_CONS_COTA = Column(Numeric(10, 2))
    VAL_CONS_FILT = Column(Numeric(10, 2))
    FACT_REG = Column(Numeric(10, 2))
    Idpais = Column(ForeignKey('CFG_Pais.IdPais'), nullable=False, index=True)
    IdProvincia = Column(ForeignKey('CFG_Provincia.IdProvincia'), nullable=False, index=True)
    IdCiudad = Column(ForeignKey('CFG_Ciudad.IdCiudad'), nullable=False, index=True)
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaModificacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    Cuenca = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    CFG_Ciudad = relationship('CFGCiudad')
    CFG_Provincia = relationship('CFGProvincia')
    CFG_Pai = relationship('CFGPai')


class CFGEmbalseTAG(Base):
    __tablename__ = 'CFG_Embalse_TAG'

    Row_ID = Column(BigInteger, primary_key=True)
    IdEmbalse = Column(ForeignKey('CFG_Embalse.IdEmbalse'), nullable=False)
    IdTAG = Column(ForeignKey('CFG_TAG.IdTAG'), nullable=False)
    UsuarioAsociacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaAsociacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))

    CFG_Embalse = relationship('CFGEmbalse')
    CFG_TAG = relationship('CFGTAG')


class CFGEmpresa(Base):
    __tablename__ = 'CFG_Empresa'
    __table_args__ = (
        Index('IDX_CFG_Empresa_FA_FB', 'FechaAlta', 'FechaBaja'),
    )

    IdEmpresa = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, index=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, index=True)
    Direccion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdCiudad = Column(ForeignKey('CFG_Ciudad.IdCiudad'), nullable=False, index=True)
    IdProvincia = Column(ForeignKey('CFG_Provincia.IdProvincia'), nullable=False, index=True)
    IdPais = Column(ForeignKey('CFG_Pais.IdPais'), nullable=False, index=True)
    Telefono = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Telefono1 = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Telefono2 = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Fax = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Contacto = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Email = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Contacto1 = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Email1 = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    Estado = Column(BIT)
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaInactivacion = Column(DateTime)
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_Ciudad = relationship('CFGCiudad')
    CFG_Pai = relationship('CFGPai')
    CFG_Provincia = relationship('CFGProvincia')


class CFGEmpresaTipoEmpresa(Base):
    __tablename__ = 'CFG_EmpresaTipoEmpresa'

    Row_ID = Column(BigInteger, primary_key=True)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False)
    IdTipoEmpresa = Column(ForeignKey('CFG_TipoEmpresa.IdTipoEmpresa'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    CFG_Empresa = relationship('CFGEmpresa')
    CFG_TipoEmpresa = relationship('CFGTipoEmpresa')


class CFGEquivalencia(Base):
    __tablename__ = 'CFG_Equivalencias'

    Row_ID = Column(Integer, primary_key=True)
    Alias = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Equivalencia = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Elemento = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Voltaje = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCreacion = Column(DateTime, nullable=False)


class CFGEstadoValidacion(Base):
    __tablename__ = 'CFG_EstadoValidacion'

    Row_ID = Column(BigInteger, primary_key=True)
    IdTipo = Column(Integer, nullable=False)
    NombreEstado = Column(String(40, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class CFGFact(Base):
    __tablename__ = 'CFG_Fact'

    IdFact = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdSubestacion = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'), nullable=False, index=True)
    PotenciaReactiva = Column(Numeric(10, 2))
    IdNivelVoltaje = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False)
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_Empresa = relationship('CFGEmpresa')
    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')
    CFG_SubEstacion = relationship('CFGSubEstacion')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGGrupoGeneracion(Base):
    __tablename__ = 'CFG_GrupoGeneracion'

    IdGrupoGeneracion = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, index=True)
    IdEmbalse = Column(ForeignKey('CFG_Embalse.IdEmbalse'), index=True)
    IdCentral = Column(ForeignKey('CFG_Central.IdCentral'), nullable=False, index=True)
    IdTipoGeneracion = Column(ForeignKey('CFG_TipoGeneracion.IdTipoGeneracion'), nullable=False, index=True)
    CONSUMO_AUXI = Column(Numeric(10, 2))
    FACTOR_IND_CORT = Column(Numeric(10, 2))
    FACTOR_IND_HIST = Column(Numeric(10, 2))
    FACTOR_PROM_PROD = Column(Numeric(10, 2))
    Generacion_Min = Column(Numeric(10, 2))
    Nivel_Salida = Column(Numeric(10, 2))
    NUM_UNID_GRUP = Column(Numeric(10, 2))
    POT_UNITARIA = Column(Numeric(10, 2))
    RENDIMIENTO = Column(Numeric(10, 2))
    TURBINAM_MAX = Column(Numeric(20, 5))
    TURBINAM_MIN = Column(Numeric(20, 5))
    CostoVariable = Column(Numeric(10, 5))
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT, nullable=False)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_Central = relationship('CFGCentral')
    CFG_Embalse = relationship('CFGEmbalse')
    CFG_TipoGeneracion = relationship('CFGTipoGeneracion')


class CFGGrupoGeneracionTAG(Base):
    __tablename__ = 'CFG_GrupoGeneracion_TAG'

    Row_ID = Column(BigInteger, primary_key=True)
    IdGrupoGeneracion = Column(ForeignKey('CFG_GrupoGeneracion.IdGrupoGeneracion'), nullable=False)
    IdTAG = Column(ForeignKey('CFG_TAG.IdTAG'), nullable=False)
    UsuarioAsociacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaAsociacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))

    CFG_GrupoGeneracion = relationship('CFGGrupoGeneracion')
    CFG_TAG = relationship('CFGTAG')


class CFGLTC(Base):
    __tablename__ = 'CFG_LTC'

    IdLTC = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdTransformador = Column(ForeignKey('CFG_Transformador.IdTransformador'), nullable=False)
    IdTipoLTC = Column(ForeignKey('CFG_TipoLTC.IdTipoLTC'), nullable=False)
    Num_Posiciones = Column(SmallInteger)
    Estado = Column(BIT, nullable=False)
    FechaCreacion = Column(DateTime, nullable=False)
    UsuarioCreador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaActualizacion = Column(DateTime)
    UsuarioActualizacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaBaja = Column(DateTime)
    FechaAlta = Column(DateTime, nullable=False, server_default=text("(getdate())"))

    CFG_TipoLTC = relationship('CFGTipoLTC')
    CFG_Transformador = relationship('CFGTransformador')


class CFGLTCTAG(Base):
    __tablename__ = 'CFG_LTC_TAG'
    __table_args__ = (
        Index('IX_CFG_LTC_TAG_LTCT', 'IdLTC', 'IdTAG'),
    )

    Row_ID = Column(BigInteger, primary_key=True)
    IdLTC = Column(ForeignKey('CFG_LTC.IdLTC'), nullable=False)
    IdTAG = Column(ForeignKey('CFG_TAG.IdTAG'), nullable=False)
    UsuarioCreador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False)
    FechaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_LTC = relationship('CFGLTC')
    CFG_TAG = relationship('CFGTAG')


class CFGLinea(Base):
    __tablename__ = 'CFG_Linea'
    __table_args__ = (
        Index('IDX_CFG_Linea_FA_FB', 'FechaAlta', 'FechaBaja'),
    )

    IdLinea = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdSubestacionOrigen = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'), nullable=False, index=True)
    IdSubestacionDestino = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'), nullable=False, index=True)
    IdNivelVoltaje = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False, index=True)
    IdPais = Column(SmallInteger)
    IdProvincia = Column(SmallInteger)
    Lim_OperacionContinuo = Column(Numeric(10, 2))
    Lim_Termico = Column(Numeric(10, 2))
    Lim_MaxOperacion = Column(Numeric(10, 2))
    Longitud = Column(Numeric(20, 2))
    Pot_MaxTransferencia = Column(Numeric(20, 2))
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))
    NumCircuitos = Column(SmallInteger, nullable=False)

    CFG_Empresa = relationship('CFGEmpresa')
    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')
    CFG_SubEstacion = relationship('CFGSubEstacion', primaryjoin='CFGLinea.IdSubestacionDestino == CFGSubEstacion.IdSubestacion')
    CFG_SubEstacion1 = relationship('CFGSubEstacion', primaryjoin='CFGLinea.IdSubestacionOrigen == CFGSubEstacion.IdSubestacion')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGNivelVoltaje(Base):
    __tablename__ = 'CFG_NivelVoltaje'

    IdNivelVoltaje = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), unique=True)
    Descripcion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NivelAlto = Column(Numeric(10, 2), index=True)
    NivelBajo = Column(Numeric(10, 2), index=True)
    FechaCreacion = Column(DateTime, server_default=text("(getdate())"))
    UsuarioCreador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaActualizacion = Column(DateTime, server_default=text("(getdate())"))
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioModificador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class CFGOrigenTAG(Base):
    __tablename__ = 'CFG_OrigenTAG'

    IdOrigenTAG = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class CFGPai(Base):
    __tablename__ = 'CFG_Pais'

    IdPais = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, index=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, index=True)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))


class CFGParametrosValidacion(Base):
    __tablename__ = 'CFG_ParametrosValidacion'

    Row_ID = Column(Integer, primary_key=True)
    IntervaloTiempo = Column(Time, nullable=False)
    Congelamiento = Column(Numeric(18, 1))
    Semanas = Column(SmallInteger, nullable=False)
    ReglaXi = Column(Numeric(10, 2), nullable=False)
    ComparadorX1 = Column(Numeric(10, 2), nullable=False)
    ComparadorX2 = Column(Numeric(10, 2), nullable=False)
    VoltajesXi = Column(Numeric(10, 2), nullable=False)
    GeneracionXi = Column(Numeric(10, 2), nullable=False)
    DeltaXi = Column(Numeric(10, 2), nullable=False)
    DeltaXii = Column(Numeric(10, 2))
    DeltaMVGen = Column(Numeric(10, 2), nullable=False)
    DeltaMVARGen = Column(Numeric(10, 2), nullable=False)
    EMailDatosAgentes = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UsuarioCreacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioModificador = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaActualizacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    SemanasVolt = Column(SmallInteger, nullable=False, server_default=text("((2))"))


class CFGParametrosTecnicosUnidad(Base):
    __tablename__ = 'CFG_Parametros_Tecnicos_Unidad'

    IdParametroTecnico = Column(Integer, primary_key=True)
    IdUnidad = Column(ForeignKey('CFG_Unidad.IdUnidad'), nullable=False)
    Pot_Min = Column(Numeric(10, 2))
    Inf_Adicional_Pot_Min = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    Pot_Efectiva = Column(Numeric(10, 2))
    Inf_Adicional_Pot_Efectiva = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    Pot_Min_Emergencia = Column(Numeric(10, 2))
    Inf_Adicional_Pot_Min_Emergencia = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoMaximoPotenciaMinimaEmerg = Column(Numeric(10, 2))
    Inf_Adicional_TiemMaxPotMinEmerg = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    Pot_Max_Emergencia = Column(Numeric(10, 2))
    Inf_Adicional_Pot_Max_Emergencia = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoMaximoPotenciaMaxEmerg = Column(Numeric(10, 2))
    Inf_Adicional_TiemMaxPotMaxEmerg = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    Pot_Max = Column(Numeric(10, 2))
    Inf_Adicional_Pot_Max = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoMaximoPotenciaMaxima = Column(Numeric(10, 2))
    Inf_Adicional_TiemMaxPotMaxima = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    Vel_TomaCargaNormal = Column(Numeric(10, 2))
    Inf_Adicional_Vel_TomaCargaNormal = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    Vel_TomaCargaEmergencia = Column(Numeric(10, 2))
    Inf_Adicional_Vel_TomaCargaEmergencia = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    VelocidadDescargaNormal = Column(Numeric(10, 2))
    Inf_Adicional_VelDescarNormal = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    VelocidadDescargaEmerg = Column(Numeric(10, 2))
    Inf_Adicional_VelDescarEmerg = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    CostoArranque = Column(Numeric(10, 2))
    Inf_Adicional_CostoArranque = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    MaximaGeneracion = Column(Numeric(10, 2))
    Inf_Adicional_MaximaGeneracion = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    MaximaAbsorcion = Column(Numeric(10, 2))
    Inf_Adicional_MaximaAbsorcion = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoMinimoOperacion = Column(Numeric(10, 2))
    Inf_Adicional_TiempoMinimoOperacion = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoFueraArranqueFrio = Column(Numeric(10, 2))
    Inf_Adicional_TiemFueraArranFrio = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoFueraArranqueTibio = Column(Numeric(10, 2))
    Inf_Adicional_TiemFueraArranTibio = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoFueraArranqueCaliente = Column(Numeric(10, 2))
    Inf_Adicional_TiemFueraArranCaliente = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoMinimoParada = Column(Numeric(10, 2))
    Inf_Adicional_TiemMinParada = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoMaximoOperacion = Column(Numeric(10, 2))
    Inf_Adicional_TiemMaxOperacion = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoMismoSentido = Column(Numeric(10, 2))
    Inf_Adicional_TiemMismoSentido = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoSentidoContrario = Column(Numeric(10, 2))
    Inf_Adicional_TiemSentidoContrario = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoArranqueFrio = Column(Numeric(10, 2))
    Inf_Adicional_TiemArranFrio = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoArranqueTibio = Column(Numeric(10, 2))
    Inf_Adicional_TiemArranTibio = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TiempoArranqueCaliente = Column(Numeric(10, 2))
    Inf_Adicional_TiemArranCaliente = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    TasaIndisponibilidad = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Inf_Adicional_TasaIndisponibilidad = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    Estatismo = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Inf_Adicional_Estatismo = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    AporteRegulacionVoltaje = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Inf_Adicional_AporteRegVoltaje = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    ConsumoAuxiliares = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Inf_Adicional_ConsumoAuxiliares = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    ArranqueSalida = Column(SmallInteger)
    Inf_Adicional_ArranqueSalida = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    CapacidadArranque = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Inf_Adicional_CapacidadArranque = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    ReleBajaFrecuencia = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Inf_Adicional_ReleBajaFrecuencia = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    ReleSobreFrecuencia = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Inf_Adicional_ReleSobreFrecuencia = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    ReleBajoVoltaje = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Inf_Adicional_ReleBajoVoltaje = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    ReleAltoVoltaje = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Inf_Adicional_ReleAltoVoltaje = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    ReleVHZ = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Inf_Adicional_ReleVHZ = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion1 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion2 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion3 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion4 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion5 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion6 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion7 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion8 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion9 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion10 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Estado = Column(BIT, nullable=False)
    FechaIngreso = Column(DateTime, nullable=False)
    FechaModificacion = Column(DateTime)

    CFG_Unidad = relationship('CFGUnidad')


class CFGPosicion(Base):
    __tablename__ = 'CFG_Posicion'
    __table_args__ = (
        Index('IND_POSICION_ESTADO', 'Estado', 'FechaAlta', 'IdPosicion', 'Codigo', 'IdSubestacion', 'TipoPosicion', 'FechaBaja'),
    )

    IdPosicion = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdSubestacion = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'), nullable=False, index=True)
    IdNivelVoltaje = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False, index=True)
    TipoPosicion = Column(Integer, nullable=False, server_default=text("((1))"))
    FechaCreacion = Column(DateTime, nullable=False)
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, server_default=text("(getdate())"))
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_Empresa = relationship('CFGEmpresa')
    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')
    CFG_SubEstacion = relationship('CFGSubEstacion')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGPosicionElemento(Base):
    __tablename__ = 'CFG_PosicionElemento'

    ROW_ID = Column(Integer, primary_key=True)
    IdPosicion = Column(ForeignKey('CFG_Posicion.IdPosicion'), nullable=False)
    IdElemento = Column(Integer, nullable=False)
    IdTipoElemento = Column(Integer, nullable=False)
    FechaCeacion = Column(DateTime, nullable=False)
    FechaModificacion = Column(DateTime)
    UsuarioCreador = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT, nullable=False, server_default=text("((1))"))

    CFG_Posicion = relationship('CFGPosicion')


class CFGPosicionUnidad(Base):
    __tablename__ = 'CFG_PosicionUnidad'

    Row_ID = Column(Integer, primary_key=True)
    IdPosicion = Column(ForeignKey('CFG_Posicion.IdPosicion'), nullable=False, index=True)
    IdUnidad = Column(ForeignKey('CFG_Unidad.IdUnidad'), nullable=False, index=True)
    FechaAsociacion = Column(DateTime, nullable=False)
    UsuarioAsociacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaInicio = Column(DateTime, nullable=False)
    FechaFin = Column(DateTime, nullable=False)

    CFG_Posicion = relationship('CFGPosicion')
    CFG_Unidad = relationship('CFGUnidad')


class CFGPosicionUnidadHoraria(Base):
    __tablename__ = 'CFG_PosicionUnidadHoraria'

    Row_ID = Column(Integer, primary_key=True)
    IdPosicion = Column(ForeignKey('CFG_Posicion.IdPosicion'), nullable=False)
    IdUnidad = Column(ForeignKey('CFG_Unidad.IdUnidad'), nullable=False)
    FechaInicio = Column(DateTime, nullable=False)
    FechaFin = Column(DateTime, nullable=False)
    FechaAsociacion = Column(DateTime, nullable=False)
    UsuarioAsociacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    CFG_Posicion = relationship('CFGPosicion')
    CFG_Unidad = relationship('CFGUnidad')


class CFGPosicionesConectada(Base):
    __tablename__ = 'CFG_PosicionesConectadas'

    IdPosicionConectada = Column(Integer, primary_key=True)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdSubestacion = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'), nullable=False, index=True)
    IdPosicion = Column(ForeignKey('CFG_Posicion.IdPosicion'), nullable=False, index=True)
    IdElementoConectado = Column(ForeignKey('CFG_ElementosConectados.IdElementoConectado'), nullable=False)
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))

    CFG_ElementosConectado = relationship('CFGElementosConectado')
    CFG_Empresa = relationship('CFGEmpresa')
    CFG_Posicion = relationship('CFGPosicion')
    CFG_SubEstacion = relationship('CFGSubEstacion')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGPrioridad(Base):
    __tablename__ = 'CFG_Prioridad'

    IdPrioridad = Column(Integer, primary_key=True)
    Prioridad = Column(String(10, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class CFGProvincia(Base):
    __tablename__ = 'CFG_Provincia'

    IdProvincia = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdPais = Column(ForeignKey('CFG_Pais.IdPais'), nullable=False)
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    FechaultimaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_Pai = relationship('CFGPai')


class CFGSubEstacion(Base):
    __tablename__ = 'CFG_SubEstacion'

    IdSubestacion = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdPais = Column(ForeignKey('CFG_Pais.IdPais'), nullable=False, index=True)
    IdProvincia = Column(ForeignKey('CFG_Provincia.IdProvincia'), nullable=False, index=True)
    IdCiudad = Column(ForeignKey('CFG_Ciudad.IdCiudad'), nullable=False, index=True)
    IdZona = Column(ForeignKey('CFG_Zona.IdZona'), nullable=False)
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaModificacion = Column(DateTime, server_default=text("(getdate())"))
    Estado = Column(BIT)

    CFG_Ciudad = relationship('CFGCiudad')
    CFG_Empresa = relationship('CFGEmpresa')
    CFG_Pai = relationship('CFGPai')
    CFG_Provincia = relationship('CFGProvincia')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')
    CFG_Zona = relationship('CFGZona')


class CFGSubEstacionNivelVoltaje(Base):
    __tablename__ = 'CFG_SubEstacionNivelVoltaje'

    Row_ID = Column(BigInteger, primary_key=True)
    IdSubestacion = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'), nullable=False)
    IdNivelVoltaje = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')
    CFG_SubEstacion = relationship('CFGSubEstacion')


class CFGTAG(Base):
    __tablename__ = 'CFG_TAG'
    __table_args__ = (
        Index('IX_CFG_TAG_TipoTag', 'TAG', 'IdOrigenTAG', 'IdTipoTAG'),
    )

    IdTAG = Column(Integer, primary_key=True)
    TAG = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Descripcion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    IdOrigenTAG = Column(ForeignKey('CFG_OrigenTAG.IdOrigenTAG'), nullable=False)
    IdTipoTAG = Column(ForeignKey('CFG_TipoTAG.IdTipoTAG'), nullable=False, index=True)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaModificacion = Column(DateTime, server_default=text("(getdate())"))
    Prioridad = Column(ForeignKey('CFG_Prioridad.IdPrioridad'), nullable=False)

    CFG_OrigenTAG = relationship('CFGOrigenTAG')
    CFG_TipoTAG = relationship('CFGTipoTAG')
    CFG_Prioridad = relationship('CFGPrioridad')


t_CFG_Tag_PiSicom = Table(
    'CFG_Tag_PiSicom', metadata,
    Column('TAGPI_ID', Integer, nullable=False),
    Column('TAGPI_CODIGO', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TAGPI_DESCRIPCION', String(1024, 'SQL_Latin1_General_CP1_CI_AS'))
)


class CFGTerminal(Base):
    __tablename__ = 'CFG_Terminal'

    IdTerminal = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False)
    IdNivelVoltaje = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False, index=True)
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT, nullable=False)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))

    CFG_Empresa = relationship('CFGEmpresa')
    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGTipoBarra(Base):
    __tablename__ = 'CFG_TipoBarra'

    IdTipoBarra = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Descripcion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False)
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT, nullable=False)
    FechaUltimaModificacion = Column(DateTime)
    UsuarioModificador = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))


class CFGTipoCombustible(Base):
    __tablename__ = 'CFG_TipoCombustible'

    IdTipoCombustible = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Descripcion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdTipoGeneracion = Column(ForeignKey('CFG_TipoGeneracion.IdTipoGeneracion'), nullable=False)
    IdTipoTecnologia = Column(ForeignKey('CFG_TipoTecnologia.IdTipoTecnologia'), nullable=False)
    FechaCreacion = Column(DateTime, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(Date, server_default=text("(getdate())"))
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))

    CFG_TipoGeneracion = relationship('CFGTipoGeneracion')
    CFG_TipoTecnologia = relationship('CFGTipoTecnologia')


class CFGTipoCompensador(Base):
    __tablename__ = 'CFG_TipoCompensador'

    IdTipoCompensador = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaUltimaActualizacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    Estado = Column(BIT)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaInactivacion = Column(DateTime)


class CFGTipoEmpresa(Base):
    __tablename__ = 'CFG_TipoEmpresa'

    IdTipoEmpresa = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Descripcion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreador = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    Estado = Column(BIT)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaInactivacion = Column(DateTime)
    UsuarioModificador = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))


class CFGTipoGeneracion(Base):
    __tablename__ = 'CFG_TipoGeneracion'

    IdTipoGeneracion = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Descripcion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioUltimaActualizacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))


class CFGTipoIndisponibilidad(Base):
    __tablename__ = 'CFG_TipoIndisponibilidad'

    IdTipoIndisponibilidad = Column(Integer, primary_key=True)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False)


class CFGTipoLTC(Base):
    __tablename__ = 'CFG_TipoLTC'

    IdTipoLTC = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False)
    UsuarioCreador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaUltimaModificacion = Column(DateTime)
    UsuarioModificador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Estado = Column(BIT)


class CFGTipoTAG(Base):
    __tablename__ = 'CFG_TipoTAG'

    IdTipoTAG = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaUltimaModificacion = Column(DateTime, server_default=text("(getdate())"))


class CFGTipoTecnologia(Base):
    __tablename__ = 'CFG_TipoTecnologia'

    IdTipoTecnologia = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Descripcion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdTipoGeneracion = Column(SmallInteger, nullable=False)
    UsuarioCreador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCreacion = Column(DateTime, server_default=text("(getdate())"))
    UsuarioUltimaActualizacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime)
    UsuarioInactivacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaInactivacion = Column(DateTime)
    Estado = Column(BIT)


class CFGTipoTransformador(Base):
    __tablename__ = 'CFG_TipoTransformador'

    IdTipoTransformador = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaUltimaModificacion = Column(DateTime, server_default=text("(getdate())"))
    UsuarioModificador = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))


class CFGTipoUnidad(Base):
    __tablename__ = 'CFG_TipoUnidad'

    IdTipoUnidad = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT, nullable=False)
    FechaUltimaActualizacion = Column(DateTime)


class CFGTipoUnidadNegocio(Base):
    __tablename__ = 'CFG_TipoUnidadNegocio'

    IdTipoUnidadNegocio = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    Binario = Column(Integer)
    Estado = Column(BIT)
    FechaUltimaActualizacion = Column(DateTime)
    UsuarioModificador = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))


class CFGTiposDia(Base):
    __tablename__ = 'CFG_TiposDias'

    IdTipo = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    Estado = Column(BIT, nullable=False)
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class CFGTransformador(Base):
    __tablename__ = 'CFG_Transformador'

    IdTransformador = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdSubestacion = Column(ForeignKey('CFG_SubEstacion.IdSubestacion'), nullable=False, index=True)
    IdBancoTransformador = Column(ForeignKey('CFG_BancoTransformadores.IdBancoTransformador'), index=True)
    IdNivelVoltaje = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False, index=True)
    IdTipoTransformador = Column(ForeignKey('CFG_TipoTransformador.IdTipoTransformador'), nullable=False, index=True)
    AjusteAlta = Column(Numeric(10, 2))
    AjusteBaja = Column(Numeric(10, 2))
    AjusteProt = Column(Numeric(10, 2))
    CorrNormal = Column(Numeric(10, 2))
    MVA_Emerg = Column(Numeric(10, 2))
    MVA_NominalFA = Column(Numeric(10, 2))
    MVA_NominalFOA = Column(Numeric(10, 2))
    MVA_NominalOA = Column(Numeric(10, 2))
    Num_Inductor = Column(SmallInteger)
    Num_Taps = Column(SmallInteger)
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))

    CFG_BancoTransformadore = relationship('CFGBancoTransformadore')
    CFG_Empresa = relationship('CFGEmpresa')
    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')
    CFG_SubEstacion = relationship('CFGSubEstacion')
    CFG_TipoTransformador = relationship('CFGTipoTransformador')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGUnidad(Base):
    __tablename__ = 'CFG_Unidad'

    IdUnidad = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False)
    IdUNegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False)
    IdCentral = Column(ForeignKey('CFG_Central.IdCentral'), nullable=False)
    IdGrupoGeneracion = Column(ForeignKey('CFG_GrupoGeneracion.IdGrupoGeneracion'))
    IdNivelVoltaje = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False)
    IdTipoTecnologia = Column(ForeignKey('CFG_TipoTecnologia.IdTipoTecnologia'), nullable=False)
    IdTipoCombustible = Column(ForeignKey('CFG_TipoCombustible.IdTipoCombustible'), nullable=False)
    Pot_Efectiva = Column(Numeric(10, 2))
    Pot_EfectivaReactiva = Column(Numeric(10, 2))
    Pot_instalada = Column(Numeric(10, 2))
    Pot_disponible = Column(Numeric(10, 2))
    Pot_Min_Emergencia = Column(Numeric(10, 2))
    Pot_Min = Column(Numeric(10, 2))
    Pot_Max_Emergencia = Column(Numeric(10, 2))
    Pot_Max = Column(Numeric(10, 2))
    Vel_TomaCargaNormal = Column(Numeric(10, 2))
    Vel_TomaCargaEmergencia = Column(Numeric(10, 2))
    VelocidadDescargaNormal = Column(Numeric(10, 2))
    VelocidadDescargaEmerg = Column(Numeric(10, 2))
    MaximaGeneracion = Column(Numeric(10, 2))
    MaximaAbsorcion = Column(Numeric(10, 2))
    TiempoMaximoPotenciaMinimaEmerg = Column(Numeric(10, 2))
    TiempoMaximoPotenciaMaxEmerg = Column(Numeric(10, 2))
    TiempoMaximoPotenciaMaxima = Column(Numeric(10, 2))
    TiempoMinimoOperacion = Column(Numeric(10, 2))
    TiempoMaximoOperacion = Column(Numeric(10, 2))
    TiempoFueraArranqueFrio = Column(Numeric(10, 2))
    TiempoFueraArranqueTibio = Column(Numeric(10, 2))
    TiempoFueraArranqueCaliente = Column(Numeric(10, 2))
    TiempoMinimoParada = Column(Numeric(10, 2))
    TiempoMismoSentido = Column(Numeric(10, 2))
    TiempoSentidoContrario = Column(Numeric(10, 2))
    TiempoArranqueFrio = Column(Numeric(10, 2))
    TiempoArranqueTibio = Column(Numeric(10, 2))
    TiempoArranqueCaliente = Column(Numeric(10, 2))
    TasaIndisponibilidad = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Estatismo = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    AporteRegulacionVoltaje = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    ConsumoAuxiliares = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    ArranqueSalida = Column(SmallInteger)
    CapacidadArranque = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    ReleBajaFrecuencia = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    ReleSobreFrecuencia = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    ReleBajoVoltaje = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    ReleAltoVoltaje = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    ReleVHZ = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion1 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion2 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion3 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion4 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion5 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion6 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion7 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion8 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion9 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT, nullable=False)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))
    Xi = Column(Numeric(10, 2))
    Xj = Column(Numeric(10, 2))
    IdTipoIndisponibilidad = Column(ForeignKey('CFG_TipoIndisponibilidad.IdTipoIndisponibilidad'), nullable=False)
    Informacion10 = Column(String(1000, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaInicioOpComercial = Column(DateTime)

    CFG_Central = relationship('CFGCentral')
    CFG_Empresa = relationship('CFGEmpresa')
    CFG_GrupoGeneracion = relationship('CFGGrupoGeneracion')
    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')
    CFG_TipoCombustible = relationship('CFGTipoCombustible')
    CFG_TipoIndisponibilidad = relationship('CFGTipoIndisponibilidad')
    CFG_TipoTecnologia = relationship('CFGTipoTecnologia')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGUnidadCombustible(Base):
    __tablename__ = 'CFG_UnidadCombustible'

    IdUnidadCombustible = Column(Integer, primary_key=True)
    IdTipoCombustible = Column(Integer, nullable=False)
    IdUnidad = Column(Integer, nullable=False)
    FechaInicio = Column(DateTime, nullable=False)
    FechaFin = Column(DateTime, nullable=False)
    Usuario = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaModificacion = Column(DateTime, nullable=False)


class CFGUnidadMedida(Base):
    __tablename__ = 'CFG_UnidadMedida'

    IdUnidadMedida = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Descripcion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class CFGUnidadNegocio(Base):
    __tablename__ = 'CFG_UnidadNegocio'

    IdUNegocio = Column(Integer, primary_key=True)
    IdEmpresa = Column(ForeignKey('CFG_Empresa.IdEmpresa'), nullable=False, index=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, unique=True)
    Nombre = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, index=True)
    Abreviatura = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    IdTipoUnidadNegocio = Column(ForeignKey('CFG_TipoUnidadNegocio.IdTipoUnidadNegocio'), nullable=False, server_default=text("((1))"))
    Direccion = Column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    IdCiudad = Column(ForeignKey('CFG_Ciudad.IdCiudad'), index=True)
    IdProvincia = Column(ForeignKey('CFG_Provincia.IdProvincia'), index=True)
    IdPais = Column(ForeignKey('CFG_Pais.IdPais'), index=True)
    Contacto = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Email = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Telefono = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    Telefono2 = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    Fax = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaUltimaActualizacion = Column(DateTime, server_default=text("(getdate())"))
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    Estado = Column(BIT)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))

    CFG_Ciudad = relationship('CFGCiudad')
    CFG_Empresa = relationship('CFGEmpresa')
    CFG_Pai = relationship('CFGPai')
    CFG_Provincia = relationship('CFGProvincia')
    CFG_TipoUnidadNegocio = relationship('CFGTipoUnidadNegocio')


class CFGUnidadNegocioTipoUnidad(Base):
    __tablename__ = 'CFG_UnidadNegocio_TipoUnidad'

    Row_ID = Column(BigInteger, primary_key=True)
    IdUnegocio = Column(ForeignKey('CFG_UnidadNegocio.IdUNegocio'), nullable=False, index=True)
    IdTipoUnidadNegocio = Column(ForeignKey('CFG_TipoUnidadNegocio.IdTipoUnidadNegocio'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)

    CFG_TipoUnidadNegocio = relationship('CFGTipoUnidadNegocio')
    CFG_UnidadNegocio = relationship('CFGUnidadNegocio')


class CFGUnidadTipoUnidad(Base):
    __tablename__ = 'CFG_UnidadTipoUnidad'

    Row_ID = Column(BigInteger, primary_key=True)
    IdUnidad = Column(ForeignKey('CFG_Unidad.IdUnidad'), nullable=False)
    IdTipoUnidad = Column(ForeignKey('CFG_TipoUnidad.IdTipoUnidad'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioCreacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaUltimaActualizacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))

    CFG_TipoUnidad = relationship('CFGTipoUnidad')
    CFG_Unidad = relationship('CFGUnidad')


class CFGUnidadTmp(Base):
    __tablename__ = 'CFG_Unidad_Tmp'

    IdUnidad = Column(Integer, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdEmpresa = Column(Integer, nullable=False)
    IdUNegocio = Column(Integer, nullable=False)
    IdCentral = Column(Integer, nullable=False)
    IdGrupoGeneracion = Column(Integer)
    IdNivelVoltaje = Column(Integer, nullable=False)
    IdTipoTecnologia = Column(SmallInteger, nullable=False)
    IdTipoCombustible = Column(SmallInteger, nullable=False)
    Pot_Efectiva = Column(Numeric(10, 2))
    Pot_EfectivaReactiva = Column(Numeric(10, 2))
    Pot_instalada = Column(Numeric(10, 2))
    Pot_disponible = Column(Numeric(10, 2))
    Pot_Min_Emergencia = Column(Numeric(10, 2))
    Pot_Min = Column(Numeric(10, 2))
    Pot_Max_Emergencia = Column(Numeric(10, 2))
    Pot_Max = Column(Numeric(10, 2))
    Vel_TomaCargaNormal = Column(Numeric(10, 2))
    Vel_TomaCargaEmergencia = Column(Numeric(10, 2))
    VelocidadDescargaNormal = Column(Numeric(10, 2))
    VelocidadDescargaEmerg = Column(Numeric(10, 2))
    MaximaGeneracion = Column(Numeric(10, 2))
    MaximaAbsorcion = Column(Numeric(10, 2))
    TiempoMaximoPotenciaMinimaEmerg = Column(Numeric(10, 2))
    TiempoMaximoPotenciaMaxEmerg = Column(Numeric(10, 2))
    TiempoMaximoPotenciaMaxima = Column(Numeric(10, 2))
    TiempoMinimoOperacion = Column(Numeric(10, 2))
    TiempoMaximoOperacion = Column(Numeric(10, 2))
    TiempoFueraArranqueFrio = Column(Numeric(10, 2))
    TiempoFueraArranqueTibio = Column(Numeric(10, 2))
    TiempoFueraArranqueCaliente = Column(Numeric(10, 2))
    TiempoMinimoParada = Column(Numeric(10, 2))
    TiempoMismoSentido = Column(Numeric(10, 2))
    TiempoSentidoContrario = Column(Numeric(10, 2))
    TiempoArranqueFrio = Column(Numeric(10, 2))
    TiempoArranqueTibio = Column(Numeric(10, 2))
    TiempoArranqueCaliente = Column(Numeric(10, 2))
    TasaIndisponibilidad = Column(Numeric(10, 2))
    Estatismo = Column(Numeric(10, 2))
    AporteRegulacionVoltaje = Column(Numeric(10, 2))
    ConsumoAuxiliares = Column(Numeric(10, 2))
    ArranqueSalida = Column(SmallInteger)
    CapacidadArranque = Column(Integer)
    ReleBajaFrecuencia = Column(Numeric(10, 2))
    ReleSobreFrecuencia = Column(Numeric(10, 2))
    ReleBajoVoltaje = Column(Numeric(10, 2))
    ReleAltoVoltaje = Column(Numeric(10, 2))
    ReleVHZ = Column(Numeric(10, 2))
    Informacion1 = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion2 = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion3 = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion4 = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion5 = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion6 = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion7 = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion8 = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    Informacion9 = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaAlta = Column(DateTime)
    FechaBaja = Column(DateTime)
    FechaCreacion = Column(DateTime, nullable=False)
    UsuarioCreacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT, nullable=False)
    FechaInactivacion = Column(DateTime)
    UsuarioInactivacion = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaUltimaActualizacion = Column(DateTime)
    Xi = Column(Numeric(10, 2))
    Xj = Column(Numeric(10, 2))


class CFGVoltajesMAXMIN(Base):
    __tablename__ = 'CFG_Voltajes_MAX_MIN'

    Norma_ID = Column(Integer, primary_key=True)
    Voltaje_ID = Column(ForeignKey('CFG_NivelVoltaje.IdNivelVoltaje'), nullable=False)
    Nombre = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    ValorMaximo = Column(Numeric(10, 2), nullable=False)
    ValorMinimo = Column(Numeric(10, 2), nullable=False)
    FechaInicial = Column(DateTime, nullable=False)
    FechaCaducidad = Column(DateTime)
    UsuarioCreador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    FechaActualizacion = Column(DateTime, server_default=text("(getdate())"))
    UsuarioModificador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))

    CFG_NivelVoltaje = relationship('CFGNivelVoltaje')


class CFGZona(Base):
    __tablename__ = 'CFG_Zona'

    IdZona = Column(SmallInteger, primary_key=True)
    Codigo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Nombre = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaCreacion = Column(DateTime, nullable=False)
    UsuarioCreacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Estado = Column(BIT)
    FechaActualizacion = Column(DateTime)


class DNVMedidor(Base):
    __tablename__ = 'DNV_Medidor'
    __table_args__ = (
        Index('IX_DNV_Medidor_IXPrincipal', 'TAG', 'Fecha', 'Hora', 'ValorNumerico', 'ValorCaracter'),
    )

    Row_ID = Column(BigInteger, primary_key=True)
    TAG = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    ValorNumerico = Column(Numeric(10, 2))
    ValorCaracter = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCarga = Column(DateTime, nullable=False, server_default=text("(getdate())"))


class DNVPI(Base):
    __tablename__ = 'DNV_PI'
    __table_args__ = (
        Index('IX_DNV_PI_FechaHoraVNVC', 'TAG', 'Fecha', 'Hora', 'ValorNumerico', 'ValorCaracter'),
    )

    TAG = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'), primary_key=True, nullable=False, index=True)
    FechaHora = Column(DateTime, nullable=False)
    Fecha = Column(Date, primary_key=True, nullable=False, index=True)
    Hora = Column(Time, primary_key=True, nullable=False, index=True)
    ValorNumerico = Column(Numeric(18, 2))
    ValorCaracter = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Status = Column(Integer, nullable=False)
    FechaCarga = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    TipoVista = Column(Integer, nullable=False)


class DOPDesconexione(Base):
    __tablename__ = 'DOP_Desconexiones'

    Row_ID = Column(BigInteger, primary_key=True)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    MW_Desconectado = Column(Numeric(10, 2), nullable=False)
    FechaCarga = Column(DateTime, server_default=text("(getdate())"))


class DOPDisponibilidad(Base):
    __tablename__ = 'DOP_Disponibilidad'

    Row_ID = Column(BigInteger, primary_key=True)
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    GrupoGeneracion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Unidad = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Fecha = Column(Date)
    MW_Disponible = Column(Numeric(10, 2))
    FechaCarga = Column(DateTime, server_default=text("(getdate())"))


class DOPNovedadesRelevante(Base):
    __tablename__ = 'DOP_NovedadesRelevantes'

    Row_ID = Column(BigInteger, primary_key=True)
    Fecha = Column(Date)
    Descripcion = Column(String(8000, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCarga = Column(DateTime, server_default=text("(getdate())"))
    NombreArchivo = Column(String(200, 'SQL_Latin1_General_CP1_CI_AS'))


class DPLComparador(Base):
    __tablename__ = 'DPL_Comparador'

    ROW_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Unegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Grupo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Unidad = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Precio = Column(Numeric(15, 5))
    MV_PROG = Column(Numeric(10, 2))
    MV_REAL = Column(Numeric(10, 2))
    Fecha = Column(Date)
    Hora = Column(Time)
    Desvio = Column(BIT)


class DPLCostoVariable(Base):
    __tablename__ = 'DPL_CostoVariable'

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), index=True)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), index=True)
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), index=True)
    GrupoGeneracion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), index=True)
    FechaInicio = Column(Date, index=True)
    FechaFin = Column(Date, index=True)
    Costo = Column(Numeric(15, 5))
    ConsumoComb = Column(Numeric(10, 2))
    FechaCarga = Column(DateTime, server_default=text("(getdate())"))


class DPLDespachoProgramado(Base):
    __tablename__ = 'DPL_DespachoProgramado'
    __table_args__ = (
        Index('INDX_SYSTEM_TIPOS', 'UNegocio', 'Fecha', 'Empresa', 'Central', 'Unidad', 'MV', 'Precio'),
        Index('IND_DPL_DespachoProg_FecHor', 'Fecha', 'Hora', 'Unidad', 'NumRedespacho'),
        Index('IDX_DespachoProgramado', 'Empresa', 'UNegocio', 'GrupoGeneracion', 'Central', 'Unidad', 'EsRedespacho', 'NumRedespacho', 'Fecha', 'Hora', 'HoraVigencia', 'MV', 'Precio', unique=True),
        Index('IDX_Despacho_Programado_Fecha_Hora', 'Fecha', 'Hora', 'Unidad', 'NumRedespacho')
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    GrupoGeneracion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Unidad = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    EsRedespacho = Column(BIT, nullable=False)
    NumRedespacho = Column(Integer, nullable=False)
    HoraVigencia = Column(Time, nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    MV = Column(Numeric(10, 2))
    Precio = Column(Numeric(15, 5))
    FechaCarga = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    NombreArchivo = Column(String(500, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class DPLImpexty(Base):
    __tablename__ = 'DPL_Impexties'

    Row_ID = Column(BigInteger, primary_key=True)
    Fecha = Column(Date)
    Hora = Column(Time)
    NivelVoltaje = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Tipo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Dato = Column(Numeric(10, 6))
    FechaCarga = Column(DateTime, server_default=text("(getdate())"))
    NombreArchivo = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))


t_DPL_Rendimientos = Table(
    'DPL_Rendimientos', metadata,
    Column('Row_ID', BigInteger, nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FechaInicio', Date),
    Column('FechaFin', Date),
    Column('Rendimiento', Numeric(15, 5))
)


class DPLReservaCombustible(Base):
    __tablename__ = 'DPL_ReservaCombustibles'
    __table_args__ = (
        Index('IDX_DPL_ReservaCombustible', 'Empresa', 'UNegocio', 'Central', 'Fecha', 'Combustible', 'Tipo', 'PotDisponible', 'Total', 'NombreArchivo', unique=True),
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Fecha = Column(Date, nullable=False)
    PotDisponible = Column(Numeric(10, 2))
    Combustible = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Total = Column(Numeric(18, 2))
    FechaCarga = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    NombreArchivo = Column(String(500, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Tipo = Column(Integer, nullable=False)


class DPLResultado(Base):
    __tablename__ = 'DPL_Resultado'
    __table_args__ = (
        Index('IDX_DPL_Resultado', 'Linea', 'Fecha', 'Hora', 'Transaccion', 'NombreArchivo', unique=True),
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Linea = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    Transaccion = Column(String(2, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaCarga = Column(DateTime, nullable=False)
    NombreArchivo = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class DVCompensador(Base):
    __tablename__ = 'DV_Compensador'
    __table_args__ = (
        Index('IX_DV_Compensador_Tipo_Fecha_Hora', 'TipoCompensador', 'Fecha', 'Hora', 'Row_ID', 'Empresa', 'UNegocio', 'Subestacion', 'Compensador', 'ValorOriginal', 'Color', 'UsuarioValidacion'),
        Index('IX_DV_Compensador_Tipo_Fecha', 'TipoCompensador', 'Fecha', 'Row_ID', 'Empresa', 'UNegocio', 'Subestacion', 'Compensador', 'ValorValidado', 'Color', 'Hora', 'UsuarioValidacion'),
        Index('IDX_DV_Compensador', 'TipoCompensador', 'Empresa', 'UNegocio', 'Subestacion', 'Compensador', 'Fecha', 'Hora', 'TAG', 'ValorOriginal', 'ValorValidado', 'TipoValidacion', 'Color', unique=True)
    )

    Row_ID = Column(BigInteger, primary_key=True)
    TipoCompensador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Subestacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Compensador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    TAG = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'))
    ValorOriginal = Column(Numeric(10, 2))
    ValorValidado = Column(Numeric(10, 2), nullable=False, server_default=text("((0))"))
    TipoValidacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Color = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    FechaValidacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioValidacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class DVDemanda(Base):
    __tablename__ = 'DV_Demanda'
    __table_args__ = (
        Index('IX_DemandasUNegocio', 'Tipo', 'UNegocio', 'Fecha', 'Hora', 'Demanda'),
        Index('IDX_DV_Demanda', 'Fecha', 'Empresa', 'UNegocio', 'Hora', 'Tipo', 'Demanda', 'FechaCalculo', unique=True),
        Index('IND_DEMANDA_EST', 'Tipo', 'Empresa', 'UNegocio', 'Fecha', 'Hora', 'Demanda')
    )

    Row_ID = Column(Integer, primary_key=True)
    Tipo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False, index=True)
    Hora = Column(Time, nullable=False)
    Demanda = Column(Numeric(20, 2), nullable=False)
    FechaCalculo = Column(DateTime, nullable=False, server_default=text("(getdate())"))


class DVEntrega(Base):
    __tablename__ = 'DV_Entrega'
    __table_args__ = (
        Index('IX_DV_Entrega', 'Empresa', 'UNegocio', 'Subestacion', 'Posicion', 'Fecha', 'Hora', 'Color_MV', 'Color_MVAR', 'MV_Validado', 'MVAR_Validado', unique=True),
        Index('IX_DV_Entrega_FechaTodos', 'Fecha', 'Row_ID', 'Empresa', 'UNegocio', 'Subestacion', 'Posicion', 'TAG_MV', 'TAG_MVAR', 'MV_SIMAE', 'MV_Medidor', 'MV_Agente', 'MV_Validado', 'MVAR_SIMAE', 'MVAR_Medidor', 'MVAR_Agente', 'MVAR_Validado', 'Hora', 'TipoValidacion', 'Color_MV', 'Color_MVAR', 'FechaValidacion', 'UsuarioValidacion'),
        Index('IDX_DV_Entrega_PFH', 'Posicion', 'Fecha', 'Hora', 'MV_Validado', 'MVAR_Validado'),
        Index('IX_EntregasPosicion', 'Posicion', 'Fecha', 'Hora', 'MV_Validado', 'MVAR_Validado')
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Subestacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Posicion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    TAG_MV = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'))
    TAG_MVAR = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'))
    MV_SIMAE = Column(Numeric(10, 2))
    MV_Medidor = Column(Numeric(10, 2))
    MV_Agente = Column(Numeric(10, 2))
    MV_Validado = Column(Numeric(10, 2), nullable=False, server_default=text("((0))"))
    MVAR_SIMAE = Column(Numeric(10, 2))
    MVAR_Medidor = Column(Numeric(10, 2))
    MVAR_Agente = Column(Numeric(10, 2))
    MVAR_Validado = Column(Numeric(10, 2), nullable=False, server_default=text("((0))"))
    Fecha = Column(Date, nullable=False, index=True)
    Hora = Column(Time, nullable=False)
    TipoValidacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Color_MV = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Color_MVAR = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaValidacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioValidacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class DVFact(Base):
    __tablename__ = 'DV_Fact'
    __table_args__ = (
        Index('IDX_DV_Fact', 'Empresa', 'UNegocio', 'Subestacion', 'Fact', 'Fecha', 'Hora', 'TAG', 'ValorOriginal', 'ValorValidado', 'TipoValidacion', 'Color', unique=True),
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Subestacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fact = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    TAG = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'))
    ValorOriginal = Column(Numeric(10, 2))
    ValorValidado = Column(Numeric(10, 2), nullable=False)
    TipoValidacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Color = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(DateTime, nullable=False)
    Hora = Column(Time, nullable=False)
    FechaValidacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioValidacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class DVFlujo(Base):
    __tablename__ = 'DV_Flujo'
    __table_args__ = (
        Index('IDX_DV_Flujo_LF', 'Linea', 'Fecha', 'Elemento', 'MV_Validado', 'Hora'),
        Index('IDX_DV_Flujo', 'Fecha', 'Hora', 'Elemento', 'Linea', 'SubestacionDest', 'SubestacionOri', 'UNegocio', 'Empresa', 'TipoFlujo', 'MV_Validado', 'MVAR_Validado', 'Color_MV', 'Color_MVAR', unique=True),
        Index('IDX_DV_Flujo_Consulta', 'TipoFlujo', 'Linea', 'Fecha', 'Empresa', 'UNegocio', 'SubestacionOri', 'SubestacionDest', 'Elemento', 'MV_Original', 'MV_Validado', 'MVAR_Original', 'MVAR_Validado', 'Hora'),
        Index('IDX_DV_Flujo_TLF', 'TipoFlujo', 'Linea', 'Fecha', 'Empresa', 'UNegocio', 'SubestacionOri', 'SubestacionDest', 'Elemento', 'MV_Original', 'MV_Validado', 'MVAR_Original', 'MVAR_Validado', 'Hora'),
        Index('IDX_DV_Flujo_LFT', 'Linea', 'Fecha', 'Empresa', 'SubestacionOri', 'SubestacionDest', 'Elemento', 'MV_Original', 'MV_Validado', 'MVAR_Original', 'MVAR_Validado', 'Hora'),
        Index('IX_DV_Flujo_Elmento_Fecha', 'Elemento', 'Fecha', 'Empresa', 'SubestacionOri', 'SubestacionDest', 'Linea', 'MV_Original', 'MV_Validado', 'MVAR_Original', 'MVAR_Validado', 'Hora'),
        Index('IX_DV_Flujo_Fecha', 'Fecha', 'Empresa', 'SubestacionOri', 'SubestacionDest', 'Linea', 'Elemento', 'MV_Original', 'MV_Validado', 'MVAR_Original', 'MVAR_Validado', 'Hora')
    )

    Row_ID = Column(BigInteger, primary_key=True)
    TipoFlujo = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, index=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    SubestacionOri = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    SubestacionDest = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Linea = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Elemento = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    TAG = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'))
    MV_Original = Column(Numeric(10, 2))
    MV_Validado = Column(Numeric(10, 2), nullable=False, server_default=text("((0))"))
    MVAR_Original = Column(Numeric(10, 2))
    MVAR_Validado = Column(Numeric(10, 2), nullable=False, server_default=text("((0))"))
    TipoValidacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Color_MV = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Color_MVAR = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False, index=True)
    Hora = Column(Time, nullable=False)
    FechaValidacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioValidacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Lim_OperacionContinuo = Column(Numeric(10, 2))
    MVA_NominalFOA = Column(Numeric(10, 2))


class DVGeneracion(Base):
    __tablename__ = 'DV_Generacion'
    __table_args__ = (
        Index('IDX_DV_Generacion_FCUMVH', 'Fecha', 'Central', 'Unidad', 'MV_Validado', 'Hora'),
        Index('IDX_DV_Generacion_F', 'Fecha', 'Unidad', 'MV_Validado', 'Hora'),
        Index('IDX_DV_Generacion_UF', 'Unidad', 'Fecha', 'MV_Validado', 'Hora'),
        Index('IDX_DV_Generacion', 'Empresa', 'UNegocio', 'Central', 'GrupoGeneracion', 'Unidad', 'Fecha', 'Hora', 'MV_Validado', 'MVAR_Validado', 'TipoValidacion', 'Color_MV', 'Color_MVAR', 'UsuarioValidacion', unique=True),
        Index('IX_DV_Generacion_Unidad', 'Unidad', 'Empresa', 'UNegocio', 'Central', 'GrupoGeneracion', 'MV_Validado', 'MVAR_Validado', 'Fecha', 'Hora')
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    GrupoGeneracion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Unidad = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    TAG_MV = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'))
    TAG_MVAR = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'))
    MV_SIMAE = Column(Numeric(10, 2))
    MV_Medidor = Column(Numeric(10, 2))
    MV_Agente = Column(Numeric(10, 2))
    MV_Validado = Column(Numeric(10, 2), nullable=False)
    MVAR_SIMAE = Column(Numeric(10, 2))
    MVAR_Medidor = Column(Numeric(10, 2))
    MVAR_Agente = Column(Numeric(10, 2))
    MVAR_Validado = Column(Numeric(10, 2), nullable=False)
    Fecha = Column(Date, nullable=False, index=True)
    Hora = Column(Time, nullable=False, index=True)
    TipoValidacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Color_MV = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Color_MVAR = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaValidacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioValidacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class DVInterconexion(Base):
    __tablename__ = 'DV_Interconexion'

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Linea = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Elemento = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    TAG = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'))
    PAVOriginal = Column(Numeric(10, 2))
    QAVOriginal = Column(Numeric(10, 2))
    PAV = Column(Numeric(10, 2))
    QAV = Column(Numeric(10, 2))
    SV1 = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    SV2 = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    TipoValidacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False, server_default=text("('INTERCONEXIONES')"))
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    FechaValidacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioValidacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    IdNivelVoltaje = Column(Integer)
    INTERC_AV = Column(Numeric(10, 2), nullable=False, server_default=text("((0))"))


class DVLTC(Base):
    __tablename__ = 'DV_LTC'
    __table_args__ = (
        Index('IX_DV_LTC_LTC_Fecha', 'LTC', 'Fecha', 'Empresa', 'UNegocio', 'SubEstacion', 'Transformador', 'Hora', 'Valor'),
        Index('IDX_DV_LTC', 'Empresa', 'UNegocio', 'SubEstacion', 'Transformador', 'LTC', 'Fecha', 'Hora', 'Valor', 'FechaValidacion', 'UsuarioValidacion', unique=True),
        Index('IX_DV_LTC_Fecha_Hora', 'Fecha', 'Hora', 'Empresa', 'UNegocio', 'SubEstacion', 'Transformador', 'LTC', 'Valor')
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    SubEstacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Transformador = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    LTC = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    Valor = Column(Numeric(18, 2), nullable=False)
    FechaValidacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioValidacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class DVVoltaje(Base):
    __tablename__ = 'DV_Voltaje'
    __table_args__ = (
        Index('IDX_DV_Voltaje', 'Empresa', 'UNegocio', 'SubEstacion', 'Barra', 'Fecha', 'Hora', 'ValorValidado', 'TipoValidacion', 'Color', 'LimiteSuperior', 'LimiteInferior', unique=True),
        Index('IX_DV_Voltaje_Fecha_Hora', 'Fecha', 'Hora', 'Row_ID', 'Empresa', 'UNegocio', 'SubEstacion', 'Barra', 'TAG', 'ValorOriginal', 'ValorValidado', 'TipoValidacion', 'Color', 'LimiteSuperior', 'LimiteInferior', 'FechaValidacion', 'UsuarioValidacion')
    )

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    SubEstacion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Barra = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    TAG = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'))
    ValorOriginal = Column(Numeric(10, 2))
    ValorValidado = Column(Numeric(10, 2), nullable=False)
    TipoValidacion = Column(String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Color = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    LimiteSuperior = Column(Numeric(10, 2), nullable=False)
    LimiteInferior = Column(Numeric(10, 2), nullable=False)
    Fecha = Column(Date, nullable=False)
    Hora = Column(Time, nullable=False)
    FechaValidacion = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    UsuarioValidacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


class HISTInfDemEstadistica(Base):
    __tablename__ = 'HIST_Inf_Dem_Estadisticas'

    Table_ID = Column(Integer, primary_key=True)
    Anio = Column(Integer)
    MaximoAnio = Column(Numeric(18, 4))
    NumeroMes = Column(Integer)
    Mes = Column(String(30, 'SQL_Latin1_General_CP1_CI_AS'))
    MaximoMes = Column(Numeric(18, 4))
    Dia = Column(Date)
    MaximoDia = Column(Numeric(18, 4))
    Empresa = Column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    MaximoEmpresa = Column(Numeric(18, 4))
    UNegocio = Column(String(150, 'SQL_Latin1_General_CP1_CI_AS'))
    MaximoUNegocio = Column(Numeric(18, 4))
    Hora = Column(Time)
    Demanda = Column(Numeric(18, 4))


t_LOG_AGT_CaudalesNivelesHorarios = Table(
    'LOG_AGT_CaudalesNivelesHorarios', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Embalse', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('Cau_Ent_Prom', SQL_VARIANT),
    Column('Cau_Ent_Hora', SQL_VARIANT),
    Column('Cau_Lat_Prom', SQL_VARIANT),
    Column('Cau_Turbinado', SQL_VARIANT),
    Column('Cau_Vertido', SQL_VARIANT),
    Column('Cau_Des_Fondo', SQL_VARIANT),
    Column('Nivel', SQL_VARIANT),
    Column('Cota_Descarga', SQL_VARIANT),
    Column('Altura_Neta', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('NombreFicha', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_AGT_CaudalesNivelesHorariosDiaActual = Table(
    'LOG_AGT_CaudalesNivelesHorariosDiaActual', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Embalse', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('Cau_Ent_Prom', SQL_VARIANT),
    Column('Cau_Ent_Hora', SQL_VARIANT),
    Column('Cau_Lat_Prom', SQL_VARIANT),
    Column('Cau_Turbinado', SQL_VARIANT),
    Column('Cau_Vertido', SQL_VARIANT),
    Column('Cau_Des_Fondo', SQL_VARIANT),
    Column('Nivel', SQL_VARIANT),
    Column('Cota_Descarga', SQL_VARIANT),
    Column('Altura_Neta', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('NombreFicha', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_AGT_CaudalesNivelesHorariosDiaActual_P = Table(
    'LOG_AGT_CaudalesNivelesHorariosDiaActual_P', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Embalse', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('Cau_Ent_Prom', SQL_VARIANT),
    Column('Cau_Ent_Hora', SQL_VARIANT),
    Column('Cau_Lat_Prom', SQL_VARIANT),
    Column('Cau_Turbinado', SQL_VARIANT),
    Column('Cau_Vertido', SQL_VARIANT),
    Column('Cau_Des_Fondo', SQL_VARIANT),
    Column('Nivel', SQL_VARIANT),
    Column('Cota_Descarga', SQL_VARIANT),
    Column('Altura_Neta', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('NombreFicha', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT),
    Column('RegistroId', Integer)
)


t_LOG_AGT_CaudalesNivelesHorarios_P = Table(
    'LOG_AGT_CaudalesNivelesHorarios_P', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Embalse', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('Cau_Ent_Prom', SQL_VARIANT),
    Column('Cau_Ent_Hora', SQL_VARIANT),
    Column('Cau_Lat_Prom', SQL_VARIANT),
    Column('Cau_Turbinado', SQL_VARIANT),
    Column('Cau_Vertido', SQL_VARIANT),
    Column('Cau_Des_Fondo', SQL_VARIANT),
    Column('Nivel', SQL_VARIANT),
    Column('Cota_Descarga', SQL_VARIANT),
    Column('Altura_Neta', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('NombreFicha', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT),
    Column('RegistroId', Integer)
)


t_LOG_AGT_Entrega = Table(
    'LOG_AGT_Entrega', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Subestacion', SQL_VARIANT),
    Column('Posicion', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('MV', SQL_VARIANT),
    Column('MVAR', SQL_VARIANT),
    Column('EmpresaDestino', SQL_VARIANT),
    Column('UNegocioDestino', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_AGT_Entrega_P = Table(
    'LOG_AGT_Entrega_P', metadata,
    Column('RegistroId', BigInteger),
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Subestacion', SQL_VARIANT),
    Column('Posicion', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('MV', SQL_VARIANT),
    Column('MVAR', SQL_VARIANT),
    Column('EmpresaDestino', SQL_VARIANT),
    Column('UNegocioDestino', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_AGT_Generacion = Table(
    'LOG_AGT_Generacion', metadata,
    Column('Central', SQL_VARIANT),
    Column('Unidad', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('MV', SQL_VARIANT),
    Column('MVAR', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('FechaCarga', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('NombreFicha', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_AGT_Generacion_P = Table(
    'LOG_AGT_Generacion_P', metadata,
    Column('RegistroId', BigInteger),
    Column('Central', SQL_VARIANT),
    Column('Unidad', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('MV', SQL_VARIANT),
    Column('MVAR', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('FechaCarga', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('NombreFicha', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_AGT_InformacionHidrologica = Table(
    'LOG_AGT_InformacionHidrologica', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Embalse', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('Vol_Almacenado', SQL_VARIANT),
    Column('Vol_Turbinado', SQL_VARIANT),
    Column('Vol_Vertido', SQL_VARIANT),
    Column('Vol_Des_Fondo', SQL_VARIANT),
    Column('Horas_Aper_Desfondo_dia', SQL_VARIANT),
    Column('Caudal_Prom', SQL_VARIANT),
    Column('Nivel', SQL_VARIANT),
    Column('Res_Energetica', SQL_VARIANT),
    Column('Energia_Rem_Almacenada', SQL_VARIANT),
    Column('Embalse_Destino', SQL_VARIANT),
    Column('Energia_Rem_Alm_Emb_Destino', SQL_VARIANT),
    Column('Energia_Rem_Total_Almacenada', SQL_VARIANT),
    Column('Energia_Emergencia_Emb_Destino', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('FechaCarga', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('NombreFicha', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_AGT_InformacionHidrologica_P = Table(
    'LOG_AGT_InformacionHidrologica_P', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Embalse', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('Vol_Almacenado', SQL_VARIANT),
    Column('Vol_Turbinado', SQL_VARIANT),
    Column('Vol_Vertido', SQL_VARIANT),
    Column('Vol_Des_Fondo', SQL_VARIANT),
    Column('Vol_Util', SQL_VARIANT),
    Column('Horas_Aper_Desfondo_dia', SQL_VARIANT),
    Column('Caudal_Prom', SQL_VARIANT),
    Column('Nivel', SQL_VARIANT),
    Column('Res_Energetica', SQL_VARIANT),
    Column('Energia_Rem_Almacenada', SQL_VARIANT),
    Column('Embalse_Destino', SQL_VARIANT),
    Column('Energia_Rem_Alm_Emb_Destino', SQL_VARIANT),
    Column('Energia_Rem_Total_Almacenada', SQL_VARIANT),
    Column('Energia_Emergencia_Emb_Destino', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('FechaCarga', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('NombreFicha', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT),
    Column('RegistroId', Integer)
)


t_LOG_AGT_Novedades = Table(
    'LOG_AGT_Novedades', metadata,
    Column('Central', SQL_VARIANT),
    Column('Unidad', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('Evento', SQL_VARIANT),
    Column('Causal', SQL_VARIANT),
    Column('MW', SQL_VARIANT),
    Column('Descripcion', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('FechaCarga', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('NombreFicha', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_AGT_ProducConsumGas = Table(
    'LOG_AGT_ProducConsumGas', metadata,
    Column('RegistroId', BigInteger),
    Column('Fecha', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('COD_CENTRAL', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nombre_Central', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('COD_UNIDAD', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nombre_Unidad', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Produccion_MWh', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ConsumoGas_MPCD', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Observacion', String(2048, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Usuario', String(100, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_LOG_AGT_PronosticosHidrologicos = Table(
    'LOG_AGT_PronosticosHidrologicos', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Embalse', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('FechaInicio', SQL_VARIANT),
    Column('FechaFin', SQL_VARIANT),
    Column('NSemana', SQL_VARIANT),
    Column('Cau_Pronosticado', SQL_VARIANT),
    Column('Limite_Inferior', SQL_VARIANT),
    Column('Limite_Superior', SQL_VARIANT),
    Column('Nivel_Confianza', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('FechaCarga', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('NombreFicha', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_AGT_PronosticosHidrologicos_P = Table(
    'LOG_AGT_PronosticosHidrologicos_P', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Embalse', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('FechaInicio', SQL_VARIANT),
    Column('FechaFin', SQL_VARIANT),
    Column('NSemana', SQL_VARIANT),
    Column('Cau_Pronosticado', SQL_VARIANT),
    Column('Limite_Inferior', SQL_VARIANT),
    Column('Limite_Superior', SQL_VARIANT),
    Column('Nivel_Confianza', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('FechaCarga', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('NombreFicha', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT),
    Column('RegistroId', Integer)
)


class LOGDNVPIHorario(Base):
    __tablename__ = 'LOG_DNV_PI_Horario'

    Fecha = Column(Date, primary_key=True, nullable=False)
    Hora = Column(Time, primary_key=True, nullable=False)
    Version = Column(SmallInteger, primary_key=True, nullable=False)
    TotalRegistros = Column(Integer, nullable=False)
    EstadoId = Column(SmallInteger, nullable=False)
    Observaciones = Column(String(500, 'SQL_Latin1_General_CP1_CI_AS'))
    FechaRegistro = Column(DateTime, nullable=False)
    Usuario = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


t_LOG_DPL_CostoVariable = Table(
    'LOG_DPL_CostoVariable', metadata,
    Column('RegistroId', Integer),
    Column('Usuario', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Observacion', String(500, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_LOG_DPL_DespachoProgramado = Table(
    'LOG_DPL_DespachoProgramado', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('GrupoGeneracion', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Unidad', SQL_VARIANT),
    Column('EsRedespacho', SQL_VARIANT),
    Column('NumRedespacho', SQL_VARIANT),
    Column('HoraVigencia', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('MV', SQL_VARIANT),
    Column('Precio', SQL_VARIANT),
    Column('FechaCarga', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_DPL_DespachoProgramado_P = Table(
    'LOG_DPL_DespachoProgramado_P', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('GrupoGeneracion', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Unidad', SQL_VARIANT),
    Column('EsRedespacho', SQL_VARIANT),
    Column('NumRedespacho', SQL_VARIANT),
    Column('HoraVigencia', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('MV', SQL_VARIANT),
    Column('Precio', SQL_VARIANT),
    Column('FechaCarga', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT),
    Column('RegistroId', Integer)
)


t_LOG_DPL_ReservaCombustibles = Table(
    'LOG_DPL_ReservaCombustibles', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('PotDisponible', SQL_VARIANT),
    Column('Combustible', SQL_VARIANT),
    Column('Total', SQL_VARIANT),
    Column('FechaCarga', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('Tipo', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_DPL_ReservaCombustibles_P = Table(
    'LOG_DPL_ReservaCombustibles_P', metadata,
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('PotDisponible', SQL_VARIANT),
    Column('Combustible', SQL_VARIANT),
    Column('Total', SQL_VARIANT),
    Column('FechaCarga', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('Tipo', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT),
    Column('RegistroId', Integer)
)


t_LOG_DPL_Resultado = Table(
    'LOG_DPL_Resultado', metadata,
    Column('Linea', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('Transaccion', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT)
)


t_LOG_DPL_Resultado_P = Table(
    'LOG_DPL_Resultado_P', metadata,
    Column('Linea', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('Transaccion', SQL_VARIANT),
    Column('NombreArchivo', SQL_VARIANT),
    Column('Observacion', SQL_VARIANT),
    Column('Usuario', SQL_VARIANT),
    Column('RegistroId', Integer, nullable=False)
)


t_LOG_DV_Compensador = Table(
    'LOG_DV_Compensador', metadata,
    Column('RegistroId', Integer, nullable=False),
    Column('Usuario', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Observacion', String(500, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_LOG_DV_Entrega = Table(
    'LOG_DV_Entrega', metadata,
    Column('RegistroId', Integer),
    Column('Usuario', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Observacion', String(500, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_LOG_DV_Flujo = Table(
    'LOG_DV_Flujo', metadata,
    Column('RegistroId', Integer),
    Column('Usuario', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Observacion', String(500, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_LOG_DV_Generacion = Table(
    'LOG_DV_Generacion', metadata,
    Column('RegistroId', Integer),
    Column('Usuario', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Observacion', String(500, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_LOG_DV_LTC = Table(
    'LOG_DV_LTC', metadata,
    Column('RegistroId', Integer, nullable=False),
    Column('Usuario', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Observacion', String(500, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_LOG_DV_Voltaje = Table(
    'LOG_DV_Voltaje', metadata,
    Column('RegistroId', Integer),
    Column('Usuario', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Observacion', String(500, 'SQL_Latin1_General_CP1_CI_AS'))
)


class SIOCEntrega(Base):
    __tablename__ = 'SIOC_Entregas'

    IdSiocEntregas = Column(Integer, primary_key=True)
    Nom_Unegocio = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Cod_Posicion = Column(String(35, 'SQL_Latin1_General_CP1_CI_AS'))
    Fecha = Column(Date)
    Hora = Column(Time)
    MV_Validado = Column(Numeric(18, 2))
    MVAR_Validado = Column(Numeric(18, 2))


class SIOCGeneracion(Base):
    __tablename__ = 'SIOC_Generacion'

    IdSiocGeneracion = Column(Integer, primary_key=True)
    Nomb_Emp = Column(String(35, 'SQL_Latin1_General_CP1_CI_AS'))
    Nomb_UNeg = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Cod_Cen = Column(String(5, 'SQL_Latin1_General_CP1_CI_AS'))
    Cod_Unidad = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
    Fecha = Column(Date)
    Hora = Column(Time)
    MV_Validado = Column(Numeric(18, 2))
    MVAR_Validado = Column(Numeric(18, 2))


class SIOCNivelesCaudale(Base):
    __tablename__ = 'SIOC_NivelesCaudales'

    IdSiocNivelCaudal = Column(Integer, primary_key=True)
    Empresa = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
    UNegocio = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Embalse = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
    Central = Column(String(15, 'SQL_Latin1_General_CP1_CI_AS'))
    Fecha = Column(Date)
    Caudal_Prom = Column(Numeric(18, 2))
    Nivel = Column(Numeric(18, 2))
    NIVEL_MAX = Column(Numeric(18, 2))
    NIVEL_MIN = Column(Numeric(18, 2))


class SYSEstadoValidacion(Base):
    __tablename__ = 'SYS_EstadoValidacion'

    Row_ID = Column(Integer, primary_key=True)
    IdTipoValidacion = Column(Integer, nullable=False)
    Usuario = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Fecha = Column(DateTime, nullable=False)


class SYSEstadoValidacionHistorial(Base):
    __tablename__ = 'SYS_EstadoValidacionHistorial'

    Row_ID = Column(Integer, primary_key=True)
    IdTipoValidacion = Column(Integer, nullable=False)
    HoraInicioVal = Column(DateTime, nullable=False)
    HoraFinVal = Column(DateTime, nullable=False)
    UsuarioVal = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))


t_SYS_HorarioPI = Table(
    'SYS_HorarioPI', metadata,
    Column('Tipo', Integer, nullable=False),
    Column('Hora', Integer, nullable=False),
    Column('HoraIni', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('HoraFin', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Rango', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_SYS_HorarioVistas = Table(
    'SYS_HorarioVistas', metadata,
    Column('IdTipo', Integer, nullable=False),
    Column('Descripcion', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Vista', String(20, 'SQL_Latin1_General_CP1_CI_AS'))
)


class SYSHora(Base):
    __tablename__ = 'SYS_Horas'
    __table_args__ = (
        Index('IX_SYS_Horas', 'Fecha', 'Hora'),
    )

    Row_ID = Column(Integer, primary_key=True)
    Fecha = Column(Date)
    Hora = Column(Time)


class SYSLogCargaArchivoEntrega(Base):
    __tablename__ = 'SYS_LogCargaArchivoEntrega'

    Row_ID = Column(BigInteger, primary_key=True)
    ErrorCode = Column(Integer)
    ErrorColumn = Column(Integer)
    Empresa = Column(SQL_VARIANT)
    UNegocio = Column(SQL_VARIANT)
    Subestacion = Column(SQL_VARIANT)
    Posicion = Column(SQL_VARIANT)
    Fecha = Column(SQL_VARIANT)
    Hora = Column(SQL_VARIANT)
    MV = Column(SQL_VARIANT)
    MVAR = Column(SQL_VARIANT)
    EmpresaDestino = Column(SQL_VARIANT)
    UNegocioDestino = Column(SQL_VARIANT)
    CodigoAgente = Column(SQL_VARIANT)
    FechaError = Column(DateTime, server_default=text("(getdate())"))
    NombreArchivo = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))


t_SYS_LogCargaArchivoInfoHidro = Table(
    'SYS_LogCargaArchivoInfoHidro', metadata,
    Column('Row_ID', BigInteger),
    Column('ErrorCode', Integer),
    Column('ErrorColumn', BigInteger),
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Embalse', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('Vol_Almacenado', SQL_VARIANT),
    Column('Vol_Turbinado', SQL_VARIANT),
    Column('Vol_Vertido', SQL_VARIANT),
    Column('Vol_Des_Fondo', SQL_VARIANT),
    Column('Horas_aper_Desfondo_dia', SQL_VARIANT),
    Column('Caudal_Prom', SQL_VARIANT),
    Column('Nivel', SQL_VARIANT),
    Column('Res_Energetica', SQL_VARIANT),
    Column('Energi_Rem_Almacenada', SQL_VARIANT),
    Column('Embalse_Destino', SQL_VARIANT),
    Column('Energia_Rem_Alm_Emb_Destino', SQL_VARIANT),
    Column('Energia_Rem_Total_Almacenada', SQL_VARIANT),
    Column('Energia_Emergencia_emb_destino', SQL_VARIANT),
    Column('Agente', SQL_VARIANT),
    Column('Archivo', String(100, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_SYS_LogCargaArchivoNiveles = Table(
    'SYS_LogCargaArchivoNiveles', metadata,
    Column('Row_ID', BigInteger),
    Column('ErrorCode', Integer),
    Column('ErrorColumn', Integer),
    Column('Empresa', SQL_VARIANT),
    Column('UNegocio', SQL_VARIANT),
    Column('Central', SQL_VARIANT),
    Column('Fecha', SQL_VARIANT),
    Column('Hora', SQL_VARIANT),
    Column('Cau_Ent_Prom', SQL_VARIANT),
    Column('Cau_Ent_Hora', SQL_VARIANT),
    Column('Cau_Lat_Prom', SQL_VARIANT),
    Column('Cau_Turbinado', SQL_VARIANT),
    Column('Cau_Vertido', SQL_VARIANT),
    Column('Cau_Des_Fondo', SQL_VARIANT),
    Column('Nivel', SQL_VARIANT),
    Column('Cota_Descarga', SQL_VARIANT),
    Column('Altura_Neta', SQL_VARIANT),
    Column('Archivo', String(100, 'SQL_Latin1_General_CP1_CI_AS'))
)


class SYSLogCargaArchivo(Base):
    __tablename__ = 'SYS_LogCargaArchivos'

    Row_ID = Column(BigInteger, primary_key=True)
    ErrorCode = Column(Integer)
    ErrorColumn = Column(Integer)
    Central = Column(SQL_VARIANT)
    Unidad = Column(SQL_VARIANT)
    Fecha = Column(SQL_VARIANT)
    Hora = Column(SQL_VARIANT)
    MV = Column(SQL_VARIANT)
    MVAR = Column(SQL_VARIANT)
    Agente = Column(SQL_VARIANT)
    fechaError = Column(DateTime, server_default=text("(getdate())"))
    Archivo = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))


class SYSLogValidacion(Base):
    __tablename__ = 'SYS_LogValidacion'

    Row_ID = Column(BigInteger, primary_key=True)
    Fecha = Column(DateTime, index=True, server_default=text("(getdate())"))
    TipoValidacion = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    FechaDato = Column(Date)
    HoraDato = Column(Time)
    Dato = Column(Numeric(10, 2))
    Descripcion = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    EventoBosniOriginal = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EventoAgente = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    EventoBosniReemplazo = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Color = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Usuario = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))


class SYSTipoValidacion(Base):
    __tablename__ = 'SYS_TipoValidacion'

    Row_ID = Column(BigInteger, primary_key=True)
    Tipo = Column(String(40, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)


t_TMP_AGT_CaudalesNivelesHorarios = Table(
    'TMP_AGT_CaudalesNivelesHorarios', metadata,
    Column('Empresa', Unicode(255)),
    Column('UNegocio', Unicode(255)),
    Column('Embalse', Unicode(255)),
    Column('Central', Unicode(255)),
    Column('Fecha', Unicode(255)),
    Column('Hora', Unicode(255)),
    Column('Cau_Ent_Prom', Unicode(255)),
    Column('Cau_Ent_Hora', Unicode(255)),
    Column('Cau_Lat_Prom', Unicode(255)),
    Column('Cau_Turbinado', Unicode(255)),
    Column('Cau_Vertido', Unicode(255)),
    Column('Cau_Des_Fondo', Unicode(255)),
    Column('Nivel', Unicode(255)),
    Column('Cota_Descarga', Unicode(255)),
    Column('Altura_Neta', Unicode(255)),
    Column('Agente', Unicode(255)),
    Column('NombreArchivo', Unicode(255)),
    Column('NombreFicha', Unicode(255)),
    Column('Usuario', Unicode(255))
)


t_TMP_AGT_CaudalesNivelesHorariosDiaActual = Table(
    'TMP_AGT_CaudalesNivelesHorariosDiaActual', metadata,
    Column('Empresa', Unicode(255)),
    Column('UNegocio', Unicode(255)),
    Column('Embalse', Unicode(255)),
    Column('Central', Unicode(255)),
    Column('Fecha', Unicode(255)),
    Column('Hora', Unicode(255)),
    Column('Cau_Ent_Prom', Unicode(255)),
    Column('Cau_Ent_Hora', Unicode(255)),
    Column('Cau_Lat_Prom', Unicode(255)),
    Column('Cau_Turbinado', Unicode(255)),
    Column('Cau_Vertido', Unicode(255)),
    Column('Cau_Des_Fondo', Unicode(255)),
    Column('Nivel', Unicode(255)),
    Column('Cota_Descarga', Unicode(255)),
    Column('Altura_Neta', Unicode(255)),
    Column('Agente', Unicode(255)),
    Column('NombreArchivo', Unicode(255)),
    Column('NombreFicha', Unicode(255)),
    Column('Usuario', Unicode(255))
)


class TMPAGTCaudalesNivelesHorariosDiaActualP(Base):
    __tablename__ = 'TMP_AGT_CaudalesNivelesHorariosDiaActual_P'

    Empresa = Column(Unicode(255))
    UNegocio = Column(Unicode(255))
    Embalse = Column(Unicode(255))
    Central = Column(Unicode(255))
    Fecha = Column(Unicode(255))
    Hora = Column(Unicode(255))
    Cau_Ent_Prom = Column(Unicode(255))
    Cau_Ent_Hora = Column(Unicode(255))
    Cau_Lat_Prom = Column(Unicode(255))
    Cau_Turbinado = Column(Unicode(255))
    Cau_Vertido = Column(Unicode(255))
    Cau_Des_Fondo = Column(Unicode(255))
    Nivel = Column(Unicode(255))
    Cota_Descarga = Column(Unicode(255))
    Altura_Neta = Column(Unicode(255))
    Agente = Column(Unicode(255))
    NombreArchivo = Column(Unicode(255))
    NombreFicha = Column(Unicode(255))
    Usuario = Column(Unicode(255))
    RegistroId = Column(Integer, primary_key=True)


class TMPAGTCaudalesNivelesHorariosP(Base):
    __tablename__ = 'TMP_AGT_CaudalesNivelesHorarios_P'

    Empresa = Column(Unicode(255))
    UNegocio = Column(Unicode(255))
    Embalse = Column(Unicode(255))
    Central = Column(Unicode(255))
    Fecha = Column(Unicode(255))
    Hora = Column(Unicode(255))
    Cau_Ent_Prom = Column(Unicode(255))
    Cau_Ent_Hora = Column(Unicode(255))
    Cau_Lat_Prom = Column(Unicode(255))
    Cau_Turbinado = Column(Unicode(255))
    Cau_Vertido = Column(Unicode(255))
    Cau_Des_Fondo = Column(Unicode(255))
    Nivel = Column(Unicode(255))
    Cota_Descarga = Column(Unicode(255))
    Altura_Neta = Column(Unicode(255))
    Agente = Column(Unicode(255))
    NombreArchivo = Column(Unicode(255))
    NombreFicha = Column(Unicode(255))
    Usuario = Column(Unicode(255))
    RegistroId = Column(Integer, primary_key=True)


t_TMP_AGT_Entrega = Table(
    'TMP_AGT_Entrega', metadata,
    Column('Empresa', Unicode(255)),
    Column('UNegocio', Unicode(255)),
    Column('Subestacion', Unicode(255)),
    Column('Posicion', Unicode(255)),
    Column('Fecha', Unicode(255)),
    Column('Hora', Unicode(255)),
    Column('MV', Unicode(255)),
    Column('MVAR', Unicode(255)),
    Column('EmpresaDestino', Unicode(255)),
    Column('UNegocioDestino', Unicode(255)),
    Column('CodigoAgente', Unicode(255)),
    Column('FechaCarga', Unicode(255), server_default=text("(getdate())")),
    Column('NombreArchivo', Unicode(255)),
    Column('NombreFicha', Unicode(255)),
    Column('Usuario', Unicode(255))
)


class TMPAGTEntregaP(Base):
    __tablename__ = 'TMP_AGT_Entrega_P'

    RegistroId = Column(BigInteger, primary_key=True)
    Empresa = Column(Unicode(255))
    UNegocio = Column(Unicode(255))
    Subestacion = Column(Unicode(255))
    Posicion = Column(Unicode(255))
    Fecha = Column(Unicode(255))
    Hora = Column(Unicode(255))
    MV = Column(Unicode(255))
    MVAR = Column(Unicode(255))
    EmpresaDestino = Column(Unicode(255))
    UNegocioDestino = Column(Unicode(255))
    CodigoAgente = Column(Unicode(255))
    FechaCarga = Column(Unicode(255), server_default=text("(getdate())"))
    NombreArchivo = Column(Unicode(255))
    NombreFicha = Column(Unicode(255))
    Usuario = Column(Unicode(255))


t_TMP_AGT_Generacion = Table(
    'TMP_AGT_Generacion', metadata,
    Column('Central', Unicode(255)),
    Column('Unidad', Unicode(255)),
    Column('Fecha', Unicode(255)),
    Column('Hora', Unicode(255)),
    Column('MV', Unicode(255)),
    Column('MVAR', Unicode(255)),
    Column('Agente', Unicode(255)),
    Column('FechaCarga', Unicode(255)),
    Column('NombreArchivo', Unicode(255)),
    Column('NombreFicha', Unicode(255)),
    Column('Usuario', Unicode(255))
)


class TMPAGTGeneracionP(Base):
    __tablename__ = 'TMP_AGT_Generacion_P'

    RegistroId = Column(BigInteger, primary_key=True)
    Central = Column(Unicode(255))
    Unidad = Column(Unicode(255))
    Fecha = Column(Unicode(255))
    Hora = Column(Unicode(255))
    MV = Column(Unicode(255))
    MVAR = Column(Unicode(255))
    Agente = Column(Unicode(255))
    FechaCarga = Column(Unicode(255))
    NombreArchivo = Column(Unicode(255))
    NombreFicha = Column(Unicode(255))
    Usuario = Column(Unicode(255))


t_TMP_AGT_InformacionHidrologica = Table(
    'TMP_AGT_InformacionHidrologica', metadata,
    Column('Empresa', Unicode(255)),
    Column('UNegocio', Unicode(255)),
    Column('Embalse', Unicode(255)),
    Column('Central', Unicode(255)),
    Column('Fecha', Unicode(255)),
    Column('Hora', Unicode(255)),
    Column('Vol_Almacenado', Unicode(255)),
    Column('Vol_Turbinado', Unicode(255)),
    Column('Vol_Vertido', Unicode(255)),
    Column('Vol_Des_Fondo', Unicode(255)),
    Column('Horas_Aper_Desfondo_dia', Unicode(255)),
    Column('Caudal_Prom', Unicode(255)),
    Column('Nivel', Unicode(255)),
    Column('Res_Energetica', Unicode(255)),
    Column('Energia_Rem_Almacenada', Unicode(255)),
    Column('Embalse_Destino', Unicode(255)),
    Column('Energia_Rem_Alm_Emb_Destino', Unicode(255)),
    Column('Energia_Rem_Total_Almacenada', Unicode(255)),
    Column('Energia_Emergencia_Emb_Destino', Unicode(255)),
    Column('Agente', Unicode(255)),
    Column('FechaCarga', Unicode(255)),
    Column('NombreArchivo', Unicode(255)),
    Column('NombreFicha', Unicode(255)),
    Column('Usuario', Unicode(255))
)


class TMPAGTInformacionHidrologicaP(Base):
    __tablename__ = 'TMP_AGT_InformacionHidrologica_P'

    Empresa = Column(Unicode(255))
    UNegocio = Column(Unicode(255))
    Embalse = Column(Unicode(255))
    Central = Column(Unicode(255))
    Fecha = Column(Unicode(255))
    Hora = Column(Unicode(255))
    Vol_Almacenado = Column(Unicode(255))
    Vol_Turbinado = Column(Unicode(255))
    Vol_Vertido = Column(Unicode(255))
    Vol_Des_Fondo = Column(Unicode(255))
    Vol_Util = Column(Unicode(255))
    Horas_Aper_Desfondo_dia = Column(Unicode(255))
    Caudal_Prom = Column(Unicode(255))
    Nivel = Column(Unicode(255))
    Res_Energetica = Column(Unicode(255))
    Energia_Rem_Almacenada = Column(Unicode(255))
    Embalse_Destino = Column(Unicode(255))
    Energia_Rem_Alm_Emb_Destino = Column(Unicode(255))
    Energia_Rem_Total_Almacenada = Column(Unicode(255))
    Energia_Emergencia_Emb_Destino = Column(Unicode(255))
    Agente = Column(Unicode(255))
    FechaCarga = Column(Unicode(255))
    NombreArchivo = Column(Unicode(255))
    NombreFicha = Column(Unicode(255))
    Usuario = Column(Unicode(255))
    RegistroId = Column(Integer, primary_key=True)


t_TMP_AGT_Novedades = Table(
    'TMP_AGT_Novedades', metadata,
    Column('Central', Unicode(255)),
    Column('Unidad', Unicode(255)),
    Column('Fecha', Unicode(255)),
    Column('Hora', Unicode(255)),
    Column('Evento', Unicode(255)),
    Column('Causal', Unicode(255)),
    Column('MW', Unicode(255)),
    Column('Descripcion', Unicode(255)),
    Column('Agente', Unicode(255)),
    Column('FechaCarga', Unicode(255)),
    Column('NombreArchivo', Unicode(255)),
    Column('NombreFicha', Unicode(255)),
    Column('Usuario', Unicode(255))
)


class TMPAGTProducConsumGa(Base):
    __tablename__ = 'TMP_AGT_ProducConsumGas'

    RegistroId = Column(BigInteger, primary_key=True)
    Fecha = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    COD_CENTRAL = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Nombre_Central = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    COD_UNIDAD = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Nombre_Unidad = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Produccion_MWh = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    ConsumoGas_MPCD = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Usuario = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))


t_TMP_AGT_PronosticosHidrologicos = Table(
    'TMP_AGT_PronosticosHidrologicos', metadata,
    Column('Empresa', Unicode(255)),
    Column('UNegocio', Unicode(255)),
    Column('Embalse', Unicode(255)),
    Column('Central', Unicode(255)),
    Column('FechaInicio', Unicode(255)),
    Column('FechaFin', Unicode(255)),
    Column('NSemana', Unicode(255)),
    Column('Cau_Pronosticado', Unicode(255)),
    Column('Limite_Inferior', Unicode(255)),
    Column('Limite_Superior', Unicode(255)),
    Column('Nivel_Confianza', Unicode(255)),
    Column('Agente', Unicode(255)),
    Column('FechaCarga', Unicode(255)),
    Column('NombreArchivo', Unicode(255)),
    Column('NombreFicha', Unicode(255)),
    Column('Usuario', Unicode(255))
)


class TMPAGTPronosticosHidrologicosP(Base):
    __tablename__ = 'TMP_AGT_PronosticosHidrologicos_P'

    Empresa = Column(Unicode(255))
    UNegocio = Column(Unicode(255))
    Embalse = Column(Unicode(255))
    Central = Column(Unicode(255))
    FechaInicio = Column(Unicode(255))
    FechaFin = Column(Unicode(255))
    NSemana = Column(Unicode(255))
    Cau_Pronosticado = Column(Unicode(255))
    Limite_Inferior = Column(Unicode(255))
    Limite_Superior = Column(Unicode(255))
    Nivel_Confianza = Column(Unicode(255))
    Agente = Column(Unicode(255))
    FechaCarga = Column(Unicode(255))
    NombreArchivo = Column(Unicode(255))
    NombreFicha = Column(Unicode(255))
    Usuario = Column(Unicode(255))
    RegistroId = Column(Integer, primary_key=True)


class TMPBOSNIHorasOperada(Base):
    __tablename__ = 'TMP_BOSNI_HorasOperadas'

    IdUnidad = Column(Integer, primary_key=True, nullable=False)
    FechaHoraDato = Column(DateTime, primary_key=True, nullable=False)
    HorasOperadas = Column(Numeric(18, 4))


t_TMP_CFG_TAG = Table(
    'TMP_CFG_TAG', metadata,
    Column('IdTAG', Integer, nullable=False),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Descripcion', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdOrigenTAG', SmallInteger, nullable=False),
    Column('IdTipoTAG', SmallInteger, nullable=False),
    Column('FechaCreacion', DateTime, nullable=False),
    Column('UsuarioCreacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Estado', BIT),
    Column('FechaInactivacion', DateTime),
    Column('UsuarioInactivacion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FechaUltimaModificacion', DateTime),
    Column('Prioridad', Integer, nullable=False)
)


class TMPCaudalesHistorico(Base):
    __tablename__ = 'TMP_Caudales_Historicos'

    Row_Id = Column(Integer, primary_key=True)
    Embalse = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Anio = Column(Integer)
    Mes = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Valor_Promedio = Column(Numeric(18, 2))


class TMPCuencasPeriodo(Base):
    __tablename__ = 'TMP_Cuencas_Periodos'

    Row_ID = Column(Integer, primary_key=True)
    Cuenca = Column(String(10, 'SQL_Latin1_General_CP1_CI_AS'))
    Periodo = Column(String(10, 'SQL_Latin1_General_CP1_CI_AS'))
    Mes = Column(Integer)
    NombreMes = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Anio = Column(Integer)
    CodEliminar = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))


t_TMP_DPL_CostoVariable = Table(
    'TMP_DPL_CostoVariable', metadata,
    Column('RegistroId', Integer),
    Column('Empresa', Unicode(250)),
    Column('UNegocio', Unicode(250)),
    Column('Central', Unicode(250)),
    Column('GrupoGeneracion', Unicode(250)),
    Column('FechaInicio', Unicode(250)),
    Column('FechaFin', Unicode(250)),
    Column('Costo', Unicode(250)),
    Column('ConsumoComb', Unicode(250)),
    Column('Usuario', String(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_TMP_DPL_DespachoProgramado = Table(
    'TMP_DPL_DespachoProgramado', metadata,
    Column('Empresa', Unicode(255)),
    Column('UNegocio', Unicode(255)),
    Column('GrupoGeneracion', Unicode(255)),
    Column('Central', Unicode(255)),
    Column('Unidad', Unicode(255)),
    Column('EsRedespacho', Unicode(255)),
    Column('NumRedespacho', Unicode(255)),
    Column('HoraVigencia', Unicode(255)),
    Column('Fecha', Unicode(255)),
    Column('Hora', Unicode(255)),
    Column('MV', Unicode(255)),
    Column('Precio', Unicode(255)),
    Column('FechaCarga', Unicode(255)),
    Column('NombreArchivo', Unicode(255)),
    Column('Usuario', Unicode(255))
)


class TMPDPLDespachoProgramadoP(Base):
    __tablename__ = 'TMP_DPL_DespachoProgramado_P'

    Empresa = Column(Unicode(255))
    UNegocio = Column(Unicode(255))
    GrupoGeneracion = Column(Unicode(255))
    Central = Column(Unicode(255))
    Unidad = Column(Unicode(255))
    EsRedespacho = Column(Unicode(255))
    NumRedespacho = Column(Unicode(255))
    HoraVigencia = Column(Unicode(255))
    Fecha = Column(Unicode(255))
    Hora = Column(Unicode(255))
    MV = Column(Unicode(255))
    Precio = Column(Unicode(255))
    FechaCarga = Column(Unicode(255))
    NombreArchivo = Column(Unicode(255))
    Usuario = Column(Unicode(255))
    RegistroId = Column(Integer, primary_key=True)


t_TMP_DPL_ReservaCombustibles = Table(
    'TMP_DPL_ReservaCombustibles', metadata,
    Column('Empresa', Unicode(255)),
    Column('UNegocio', Unicode(255)),
    Column('Central', Unicode(255)),
    Column('Fecha', Unicode(255)),
    Column('PotDisponible', Unicode(255)),
    Column('Combustible', Unicode(255)),
    Column('Total', Unicode(255)),
    Column('FechaCarga', Unicode(255)),
    Column('NombreArchivo', Unicode(255)),
    Column('Tipo', Unicode(255)),
    Column('Usuario', Unicode(255))
)


class TMPDPLReservaCombustiblesP(Base):
    __tablename__ = 'TMP_DPL_ReservaCombustibles_P'

    Empresa = Column(Unicode(255))
    UNegocio = Column(Unicode(255))
    Central = Column(Unicode(255))
    Fecha = Column(Unicode(255))
    PotDisponible = Column(Unicode(255))
    Combustible = Column(Unicode(255))
    Total = Column(Unicode(255))
    FechaCarga = Column(Unicode(255))
    NombreArchivo = Column(Unicode(255))
    Tipo = Column(Unicode(255))
    Usuario = Column(Unicode(255))
    RegistroId = Column(Integer, primary_key=True)


t_TMP_DPL_Resultado = Table(
    'TMP_DPL_Resultado', metadata,
    Column('Linea', Unicode(255)),
    Column('Fecha', Unicode(255)),
    Column('Hora', Unicode(255)),
    Column('Transaccion', Unicode(255)),
    Column('NombreArchivo', Unicode(255)),
    Column('Usuario', Unicode(255))
)


class TMPDPLResultadoP(Base):
    __tablename__ = 'TMP_DPL_Resultado_P'

    Linea = Column(Unicode(255))
    Fecha = Column(Unicode(255))
    Hora = Column(Unicode(255))
    Transaccion = Column(Unicode(255))
    NombreArchivo = Column(Unicode(255))
    Usuario = Column(Unicode(255))
    RegistroId = Column(Integer, primary_key=True)


t_TMP_DV_Compensador = Table(
    'TMP_DV_Compensador', metadata,
    Column('RegistroId', Integer, nullable=False),
    Column('TipoCompensador', String(250, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Empresa', String(250, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UNegocio', String(250, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Subestacion', String(250, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Compensador', String(250, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorValidado', String(250, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TipoValidacion', String(250, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', String(250, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Hora', String(250, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Usuario', String(250, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_TMP_DV_Entrega = Table(
    'TMP_DV_Entrega', metadata,
    Column('RegistroId', BigInteger, nullable=False),
    Column('Empresa', Unicode(250)),
    Column('UNegocio', Unicode(250)),
    Column('Subestacion', Unicode(250)),
    Column('Posicion', Unicode(250)),
    Column('MV_Validado', Unicode(250)),
    Column('MVAR_Validado', Unicode(250)),
    Column('Fecha', Unicode(250)),
    Column('Hora', Unicode(250)),
    Column('Usuario', Unicode(250))
)


class TMPDVFlujo(Base):
    __tablename__ = 'TMP_DV_Flujo'

    RegistroId = Column(Integer, primary_key=True)
    TipoFlujo = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    Empresa = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    UNegocio = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    SubestacionOri = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    SubestacionDest = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    Linea = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    Elemento = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    MV_Validado = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    MVAR_Validado = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    TipoValidacion = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    Fecha = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    Hora = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))
    Usuario = Column(String(250, 'SQL_Latin1_General_CP1_CI_AS'))


t_TMP_DV_Generacion = Table(
    'TMP_DV_Generacion', metadata,
    Column('RegistroId', BigInteger, nullable=False),
    Column('Empresa', Unicode(250)),
    Column('Unegocio', Unicode(250)),
    Column('Central', Unicode(250)),
    Column('Grupogeneracion', Unicode(250)),
    Column('Unidad', Unicode(250)),
    Column('Fecha', Unicode(250)),
    Column('Hora', Unicode(250)),
    Column('MV_Validado', Unicode(250)),
    Column('MVAR_Validado', Unicode(250)),
    Column('Usuario', Unicode(250))
)


t_TMP_DV_LTC = Table(
    'TMP_DV_LTC', metadata,
    Column('RegistroId', BigInteger, nullable=False),
    Column('Empresa', Unicode(250)),
    Column('UNegocio', Unicode(250)),
    Column('Subestacion', Unicode(250)),
    Column('Transformador', Unicode(250)),
    Column('LTC', Unicode(250)),
    Column('Fecha', Unicode(250)),
    Column('Hora', Unicode(250)),
    Column('Valor', Unicode(250)),
    Column('Usuario', Unicode(250))
)


t_TMP_DV_Voltaje = Table(
    'TMP_DV_Voltaje', metadata,
    Column('RegistroId', BigInteger, nullable=False),
    Column('Empresa', Unicode(250)),
    Column('Unegocio', Unicode(250)),
    Column('SubEstacion', Unicode(250)),
    Column('Barra', Unicode(250)),
    Column('ValorValidado', Unicode(250)),
    Column('Fecha', Unicode(250)),
    Column('Hora', Unicode(250)),
    Column('Usuario', Unicode(250))
)


class TMPDespachoProgramado(Base):
    __tablename__ = 'TMP_DespachoProgramado'

    Row_ID = Column(BigInteger, primary_key=True)
    Empresa = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    UNegocio = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    GrupoGeneracion = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Central = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Unidad = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    EsRedespacho = Column(BIT)
    NumRedespacho = Column(Integer)
    HoraVigencia = Column(Time)
    Fecha = Column(Date)
    Hora = Column(Time)
    MV = Column(Numeric(10, 2))
    Precio = Column(Numeric(15, 5))
    FechaCarga = Column(DateTime)
    NombreArchivo = Column(String(500, 'SQL_Latin1_General_CP1_CI_AS'))


t_TMP_GENSYSTEM_Hidro = Table(
    'TMP_GENSYSTEM_Hidro', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('idTipoGeneracion', Integer),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nombre', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', Date),
    Column('Energia', Numeric(20, 4)),
    Column('PotMax', Numeric(19, 4)),
    Column('Anio', Integer),
    Column('Mes', Integer)
)


t_TMP_GENSYSTEM_Term = Table(
    'TMP_GENSYSTEM_Term', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', Date),
    Column('Energia', Numeric(20, 4)),
    Column('PotMax', Numeric(19, 4)),
    Column('Anio', Integer),
    Column('Mes', Integer)
)


class TMPHISTORICODEMANDA(Base):
    __tablename__ = 'TMP_HISTORICO_DEMANDAS'

    ID_HIST_DEM = Column(Integer, primary_key=True)
    AÑO = Column(Integer, nullable=False)
    ENERGIA = Column(Numeric(18, 1), nullable=False)
    CRECIM_ENERG = Column(Numeric(18, 1), nullable=False)
    POTENCIA = Column(Numeric(18, 1), nullable=False)
    CRECIM_POT = Column(Numeric(18, 1), nullable=False)


class TMPHISTPOTPROMDIA(Base):
    __tablename__ = 'TMP_HIST_POTPROMDIA'

    ID = Column(BigInteger, primary_key=True)
    Fecha = Column(Date, nullable=False)
    Central = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Unidad = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'), nullable=False)
    Pot_Prom_Dia = Column(Numeric(10, 2))


class TMPHISDEMMENSUAL(Base):
    __tablename__ = 'TMP_HIS_DEM_MENSUAL'

    ID_HIST_DEM = Column(Integer, primary_key=True)
    AÑO = Column(Integer, nullable=False)
    MES = Column(Integer, nullable=False)
    ENERGIA = Column(Numeric(18, 5), nullable=False)
    CRECIM_ENERG = Column(Numeric(18, 5), nullable=False)
    POTENCIA = Column(Numeric(18, 5), nullable=False)
    CRECIM_POT = Column(Numeric(18, 5), nullable=False)


class TMPPromediosCaudalesHistorico(Base):
    __tablename__ = 'TMP_Promedios_CaudalesHistoricos'

    Row_Id = Column(Integer, primary_key=True)
    Mes = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Embalse = Column(String(20, 'SQL_Latin1_General_CP1_CI_AS'))
    Qmax = Column(Numeric(18, 2))
    Qprom = Column(Numeric(18, 2))
    Qmin = Column(Numeric(18, 2))


t_TMP_System_Dem = Table(
    'TMP_System_Dem', metadata,
    Column('Table_ID', Integer),
    Column('Tipo', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cod_Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nom_Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cod_UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nom_UNegocio', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', Date, index=True),
    Column('Energia', Numeric(20, 2)),
    Column('PotMax', Numeric(20, 2))
)


t_TMP_System_Embalse = Table(
    'TMP_System_Embalse', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nom_Empresa', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nom_UNegocio', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Embalse', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nom_Embalse', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', Date, index=True),
    Column('Hora', Time),
    Column('Vol_Almacenado', Numeric(10, 2)),
    Column('Vol_Turbinado', Numeric(10, 2)),
    Column('Vol_Vertido', Numeric(10, 2)),
    Column('Vol_Des_Fondo', Numeric(10, 2)),
    Column('Horas_Aper_Desfondo_dia', Numeric(10, 2)),
    Column('Caudal_Prom', Numeric(10, 2)),
    Column('Nivel', Numeric(10, 2)),
    Column('Res_Energetica', Numeric(10, 2)),
    Column('Energia_Rem_Almacenada', Numeric(10, 2)),
    Column('Embalse_Destino', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Energia_Rem_Alm_Emb_Destino', Numeric(10, 2)),
    Column('Energia_Rem_Total_Almacenada', Numeric(10, 2)),
    Column('Energia_Emergencia_Emb_Destino', Numeric(10, 2)),
    Column('CaudalEntradaProm', Numeric(20, 2)),
    Column('CaudalEntradaHora', Numeric(20, 2)),
    Column('CaudalLateralProm', Numeric(20, 2)),
    Column('CaudalTurbinado', Numeric(20, 2)),
    Column('CaudalVertido', Numeric(20, 2)),
    Column('CaudalDesFondo', Numeric(20, 2)),
    Column('Nivel_Prom', Numeric(20, 2)),
    Column('CotaDescarga', Numeric(20, 2)),
    Column('AlturaNeta', Numeric(20, 2))
)


t_TMP_System_Gen = Table(
    'TMP_System_Gen', metadata,
    Column('IdTipoGen', Integer),
    Column('Cod_TipoGen', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nom_TipoGen', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cod_Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nom_Empresa', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cod_Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nom_UNegocio', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cod_Ele', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nom_Ele', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', Date, index=True),
    Column('Energia', Numeric(20, 4)),
    Column('PotenciaMax', Numeric(19, 4))
)


class TMPSystemGenRedespacho(Base):
    __tablename__ = 'TMP_System_Gen_Redespachos'

    ROW_ID = Column(Integer, primary_key=True)
    Empresa = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreEmpresa = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    UNegocio = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreUNegocio = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Central = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreCentral = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Unidad = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreUnidad = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    CodigoTG = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreTG = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    CodigoTT = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreTT = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    CodigoTC = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreTC = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Fecha = Column(Date)
    NumRedespacho = Column(Integer)
    MV = Column(Numeric(18, 2))
    Precio_Prom = Column(Numeric(18, 2))


class TMPSystemGenTipo(Base):
    __tablename__ = 'TMP_System_Gen_Tipos'

    ROW_ID = Column(Integer, primary_key=True)
    Empresa = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreEmpresa = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    UNegocio = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreUnegocio = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Central = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreCentral = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Elemento = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    Fecha = Column(Date, index=True)
    CodigoTG = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreTG = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    CodigoTT = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreTT = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    CodigoTC = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    NombreTC = Column(String(100, 'SQL_Latin1_General_CP1_CI_AS'))
    Energia = Column(Numeric(18, 4))
    Color = Column(String(50, 'SQL_Latin1_General_CP1_CI_AS'))
    MV_Programado = Column(Numeric(18, 4))
    Precio_Prom = Column(Numeric(18, 2))


t_TMP_System_Perdidas_Energia = Table(
    'TMP_System_Perdidas_Energia', metadata,
    Column('Fecha', Date, index=True),
    Column('MWH_Demanda', Numeric(20, 2)),
    Column('MWH_Exportacion', Numeric(20, 2)),
    Column('MWH_Generacion', Numeric(20, 2))
)


t_TMP_System_Perdidas_Potencia = Table(
    'TMP_System_Perdidas_Potencia', metadata,
    Column('Fecha', Date, index=True),
    Column('Hora', Time),
    Column('MW_Generacion', Numeric(20, 2)),
    Column('MW_Demanda', Numeric(20, 2)),
    Column('MW_Exportacion', Numeric(20, 2)),
    Column('DeePerdidas', Numeric(18, 4)),
    Column('HoraDeePerdidas', Time)
)


t_TMP_System_Perdidas_Potencia_Ext = Table(
    'TMP_System_Perdidas_Potencia_Ext', metadata,
    Column('Fecha', Date, index=True),
    Column('Hora', Time),
    Column('Nom_Unegocio', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Exportacion', Numeric(20, 2))
)


class Sysdiagram(Base):
    __tablename__ = 'sysdiagrams'
    __table_args__ = (
        Index('UK_principal_name', 'principal_id', 'name', unique=True),
    )

    name = Column(Unicode(128), nullable=False)
    principal_id = Column(Integer, nullable=False)
    diagram_id = Column(Integer, primary_key=True)
    version = Column(Integer)
    definition = Column(LargeBinary)


t_vBarrasDNV = Table(
    'vBarrasDNV', metadata,
    Column('IdEmpresa', Integer),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdUNegocio', Integer),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdSubestacion', Integer),
    Column('SubEstacion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdBarra', Integer),
    Column('Barra', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdNivelVoltaje', Integer),
    Column('NivelVoltaje', Numeric(10, 2)),
    Column('IdTAG', Integer),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Prioridad', Integer),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('FechaHora', DateTime, nullable=False),
    Column('Voltaje', Numeric(10, 2), nullable=False),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Calidad', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_vCalificacionByTipoBOSNI = Table(
    'vCalificacionByTipoBOSNI', metadata,
    Column('TPB_EVENTO_ID', Integer, nullable=False),
    Column('ITM_ID', Integer, nullable=False),
    Column('ITM_NOMBRE', String(64, 'SQL_Latin1_General_CP850_CS_AS'), nullable=False),
    Column('TPB_EVENTO_PROC', Integer)
)


t_vCapacitor = Table(
    'vCapacitor', metadata,
    Column('Row_ID', BigInteger, nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreEmpresa', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Emp_FechaAlta', DateTime),
    Column('Emp_FechaBaja', DateTime),
    Column('TipoCompensador', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreUNegocio', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UN_FechaAlta', DateTime),
    Column('UN_FechaBaja', DateTime),
    Column('Subestacion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreSubestacion', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Sub_FechaAlta', DateTime),
    Column('Sub_FechaBaja', DateTime),
    Column('Compensador', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreCompensador', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Com_FechaAlta', DateTime),
    Column('Com_FechaBaja', DateTime),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorOriginal', Numeric(10, 2)),
    Column('ValorValidado', Numeric(10, 2), nullable=False),
    Column('TipoValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('FechaValidacion', DateTime, nullable=False),
    Column('UsuarioValidacion', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_vCompensadoresDNV = Table(
    'vCompensadoresDNV', metadata,
    Column('IdEmpresa', Integer, nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUNegocio', Integer, nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdSubestacion', Integer, nullable=False),
    Column('SubEstacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdCompensador', Integer, nullable=False),
    Column('Compensador', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Tipo', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Capacidad', Numeric(20, 2)),
    Column('IdTAG', Integer),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Prioridad', Integer),
    Column('FechaHora', DateTime),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Estado', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AV', Numeric(10, 2))
)


t_vDespachoProgramado = Table(
    'vDespachoProgramado', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Pot_Min', Numeric(10, 2), nullable=False),
    Column('Pot_Efectiva', Numeric(10, 2), nullable=False),
    Column('Pot_Disponible', Numeric(10, 2), nullable=False),
    Column('Pot_Instalada', Numeric(10, 2), nullable=False),
    Column('Pot_Max', Numeric(10, 2), nullable=False),
    Column('EsRedespacho', BIT, nullable=False),
    Column('NumRedespacho', Integer, nullable=False),
    Column('HoraVigencia', Time, nullable=False),
    Column('MV', Numeric(10, 2)),
    Column('Precio', Numeric(15, 5)),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('Xi', Numeric(10, 2), nullable=False),
    Column('Xj', Numeric(10, 2), nullable=False),
    Column('TipoGeneracion', SmallInteger, nullable=False)
)


t_vDespachoProgramadoOriginal = Table(
    'vDespachoProgramadoOriginal', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Pot_Min', Numeric(10, 2)),
    Column('EsRedespacho', BIT, nullable=False),
    Column('NumRedespacho', Integer, nullable=False),
    Column('HoraVigencia', Time, nullable=False),
    Column('MV', Numeric(10, 2)),
    Column('Precio', Numeric(15, 5)),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('Xi', Numeric(10, 2)),
    Column('Xj', Numeric(10, 2))
)


t_vDespachoProgramado_Interconexion = Table(
    'vDespachoProgramado_Interconexion', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdUnegocio', Integer, nullable=False),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Linea', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Voltaje_Linea', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UNegocio_Alias', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Uneg_NombreDest', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EsRedespacho', BIT),
    Column('NumRedespacho', Integer),
    Column('HoraVigencia', Time),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('MV', Numeric(10, 2)),
    Column('Precio', Numeric(15, 5))
)


t_vELEMENTO_TAG = Table(
    'vELEMENTO_TAG', metadata,
    Column('ELEMENTO_ID', Integer, nullable=False),
    Column('ELEMENTO_CODIGO', String(20, 'SQL_Latin1_General_CP850_CS_AS'), nullable=False),
    Column('ELEMENTO_NOMBRE', String(100, 'SQL_Latin1_General_CP850_CS_AS'), nullable=False),
    Column('ELEMENTO_ESTADO', Integer),
    Column('ELEMENTO_FECHACREACION', DateTime, nullable=False),
    Column('ELEMENTO_TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TAG_PRIORIDAD', Integer),
    Column('TAG_ESTADO', BIT),
    Column('TAG_ORIGEN', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ELEMENTO_TAG_FECHA_ASOCIACION', DateTime),
    Column('ELEMENTO_TAG_USUARIOASOCIACION', String(20, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vEntregasDNV = Table(
    'vEntregasDNV', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SubEstacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdPosicion', Integer, nullable=False),
    Column('Posicion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TipoPosicion', Integer, nullable=False),
    Column('EMS_TAG_PAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EMS_Prioridad_TAG_PAV', Integer),
    Column('EMS_ValorCaracter_PAV', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EMS_PAV', Numeric(10, 2)),
    Column('EMS_TAG_PAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EMS_Prioridad_TAG_PAQ', Integer),
    Column('EMS_PAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('EMS_TAG_QAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EMS_Prioridad_TAG_QAV', Integer),
    Column('EMS_ValorCaracter_QAV', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EMS_QAV', Numeric(10, 2)),
    Column('EMS_TAG_QAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EMS_Prioridad_TAG_QAQ', Integer),
    Column('EMS_QAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('EMS_Fecha', Date),
    Column('EMS_Hora', Time),
    Column('ION_TAG_PAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ION_Prioridad_TAG_PAV', Integer),
    Column('ION_ValorCaracter_PAV', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ION_PAV', Numeric(10, 2)),
    Column('ION_TAG_PAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ION_Prioridad_TAG_PAQ', Integer),
    Column('ION_PAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ION_TAG_QAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ION_Prioridad_TAG_QAV', Integer),
    Column('ION_ValorCaracter_QAV', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ION_QAV', Numeric(10, 2)),
    Column('ION_TAG_QAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ION_Prioridad_TAG_QAQ', Integer),
    Column('ION_QAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ION_Fecha', Date),
    Column('ION_Hora', Time),
    Column('CodigoAgente', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AGENTE_MV', Numeric(10, 2)),
    Column('AGENTE_MVAR', Numeric(10, 2)),
    Column('AGENTE_Fecha', Date),
    Column('AGENTE_Hora', Time)
)


t_vEventoTipoGeneracionBOSNI = Table(
    'vEventoTipoGeneracionBOSNI', metadata,
    Column('TPB_EVENTO_ID', Integer, nullable=False),
    Column('TPB_EVENTO_NOMBRE', String(80, 'SQL_Latin1_General_CP850_CS_AS'), nullable=False)
)


t_vExportacion = Table(
    'vExportacion', metadata,
    Column('IdEmpresa', Integer, nullable=False),
    Column('Emp_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Emp_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Emp_FechaAlta', DateTime),
    Column('Emp_FechaBaja', DateTime),
    Column('IdUNegocio', Integer, nullable=False),
    Column('UN_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UN_Nombre', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UN_FechaAlta', DateTime),
    Column('UN_FechaBaja', DateTime),
    Column('IdSubOri', Integer, nullable=False),
    Column('SEOri_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEOri_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEOri_FechaAlta', DateTime),
    Column('SEOri_FechaBaja', DateTime),
    Column('IdSubDest', Integer, nullable=False),
    Column('SEDest_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEDest_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEDest_FechaAlta', DateTime),
    Column('SEDest_FechaBaja', DateTime),
    Column('Linea', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Lin_FechaAlta', DateTime),
    Column('Lin_FechaBaja', DateTime),
    Column('IdNivelVoltaje', Integer, nullable=False),
    Column('NV_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NV_FechaAlta', DateTime),
    Column('NV_FechaBaja', DateTime),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('MV_Original', Numeric(38, 2)),
    Column('MV_Validado', Numeric(38, 2)),
    Column('MVAR_Original', Numeric(38, 2)),
    Column('MVAR_Validado', Numeric(38, 2))
)


t_vExportacionLinea = Table(
    'vExportacionLinea', metadata,
    Column('IdEmpresa', Integer, nullable=False),
    Column('Emp_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Emp_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUNegocio', Integer, nullable=False),
    Column('UN_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UN_Nombre', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdSubOri', Integer, nullable=False),
    Column('SEOri_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEOri_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdSubDest', Integer, nullable=False),
    Column('SEDest_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEDest_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Linea', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NV_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('MV_Original', Numeric(38, 2)),
    Column('MV_Validado', Numeric(38, 2)),
    Column('MVAR_Original', Numeric(38, 2)),
    Column('MVAR_Validado', Numeric(38, 2))
)


t_vFlujoCircuito = Table(
    'vFlujoCircuito', metadata,
    Column('Row_ID', BigInteger, nullable=False),
    Column('TipoFlujo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Emp_FechaAlta', DateTime),
    Column('Emp_FechaBaja', DateTime),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UNeg_FechaAlta', DateTime),
    Column('UNeg_FechaBaja', DateTime),
    Column('SubestacionOri', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('SubestacionDest', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Linea', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Lin_FechaAlta', DateTime),
    Column('Lin_FechaBaja', DateTime),
    Column('Elemento', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cir_FechaAlta', DateTime),
    Column('Cir_FechaBaja', DateTime),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('MV_Original', Numeric(10, 2)),
    Column('MV_Validado', Numeric(10, 2)),
    Column('MVAR_Original', Numeric(10, 2)),
    Column('MVAR_Validado', Numeric(10, 2)),
    Column('TipoValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Color_MV', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Color_MVAR', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('FechaValidacion', DateTime),
    Column('UsuarioValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vFlujoCircuitoDNV = Table(
    'vFlujoCircuitoDNV', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('F1_SubEstacionOrigen', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('F1_SUbEstacionDestino', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('linea', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Circuito', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('F1_TAG_PAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorCaracter_PAV1', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PAV1', Numeric(18, 2)),
    Column('F1_TAG_PAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PAQ1', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('F1_TAG_QAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QAV1', Numeric(18, 2)),
    Column('F1_TAG_QAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QAQ1', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('F2_SubEstacionOrigen', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('F2_SubEstacionDestino', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('F2_TAG_PAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PAV2', Numeric(18, 2)),
    Column('F2_TAG_PAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PAQ2', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('F2_TAG_QAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QAV2', Numeric(18, 2)),
    Column('F2_TAG_QAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QAQ2', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Fecha', Date),
    Column('Hora', Time)
)


t_vFlujoTrafoDNV = Table(
    'vFlujoTrafoDNV', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SubEstacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Transformador', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TAG_PAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('P_AV', Numeric(10, 2)),
    Column('TAG_PAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TAG_QAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Q_AV', Numeric(10, 2)),
    Column('TAG_QAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Estado', BIT),
    Column('Prioridad', Integer)
)


t_vFlujoTransformador = Table(
    'vFlujoTransformador', metadata,
    Column('Row_ID', BigInteger, nullable=False),
    Column('TipoFlujo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('NombreEmpresa', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Emp_FechaAlta', DateTime),
    Column('Emp_FechaBaja', DateTime),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('NombreUNegocio', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UNeg_FechaAlta', DateTime),
    Column('UNeg_FechaBaja', DateTime),
    Column('Subestacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('NombreSubestacion', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Sub_FechaAlta', DateTime),
    Column('Sub_FechaBaja', DateTime),
    Column('Elemento', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('NombreTrafo', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Tra_FechaAlta', DateTime),
    Column('Tra_FechaBaja', DateTime),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('MV_Original', Numeric(10, 2)),
    Column('MV_Validado', Numeric(10, 2), nullable=False),
    Column('MVAR_Original', Numeric(10, 2)),
    Column('MVAR_Validado', Numeric(10, 2), nullable=False),
    Column('TipoValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MV', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MVAR', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('FechaValidacion', DateTime, nullable=False),
    Column('UsuarioValidacion', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_vFlujoTransformadorDNV = Table(
    'vFlujoTransformadorDNV', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SubEstacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Transformador', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TAG_PAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('P_AV', Numeric(18, 2)),
    Column('TAG_PAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TAG_QAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Q_AV', Numeric(18, 2)),
    Column('TAG_QAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('QAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Estado', BIT),
    Column('Prioridad', Integer)
)


t_vGeneracion = Table(
    'vGeneracion', metadata,
    Column('Row_ID', BigInteger, nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('NombreEmpresa', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('NombreUNegocio', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('NombreCentral', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('NombreGrupoGeneracion', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Embalse', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreEmbalse', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TipoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreTipoGeneracion', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TipoTecnologia', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreTipoTecnologia', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TipoCombustible', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreTipoCombustible', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TAG_MV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TAG_MVAR', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('MV_SIMAE', Numeric(10, 2)),
    Column('MV_Medidor', Numeric(10, 2)),
    Column('MV_Agente', Numeric(10, 2)),
    Column('MV_Validado', Numeric(10, 2), nullable=False),
    Column('MVAR_SIMAE', Numeric(10, 2)),
    Column('MVAR_Medidor', Numeric(10, 2)),
    Column('MVAR_Agente', Numeric(10, 2)),
    Column('MVAR_Validado', Numeric(10, 2), nullable=False),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('TipoValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MV', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MVAR', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaValidacion', DateTime, nullable=False),
    Column('UsuarioValidacion', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_vGeneracionAGT = Table(
    'vGeneracionAGT', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('MV', Numeric(10, 2)),
    Column('MVAR', Numeric(10, 2)),
    Column('Agente', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', Date),
    Column('Hora', Time)
)


t_vGeneracionBOSNI = Table(
    'vGeneracionBOSNI', metadata,
    Column('UNIDAD_ID', Integer),
    Column('UNIDAD_CODIGO', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UNIDAD_NOMBRE', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EVENTO_ID', BigInteger, nullable=False),
    Column('EVENTO_CLASE', Integer, nullable=False),
    Column('TPB_EVENTO_ID', Integer),
    Column('TPB_EVENTO_NOMBRE', String(80, 'SQL_Latin1_General_CP850_CS_AS')),
    Column('TPB_CALIF_ID', Integer),
    Column('TPB_CALIF_CODIGO', String(8, 'SQL_Latin1_General_CP850_CS_AS')),
    Column('TPB_CALIF_NOMBRE', String(64, 'SQL_Latin1_General_CP850_CS_AS')),
    Column('EVENTO_FECHA_HORA', DateTime, nullable=False),
    Column('EVENTO_FECHA', Date),
    Column('EVENTO_HORA', Time)
)


t_vGeneracionBOSNI_Interconexion = Table(
    'vGeneracionBOSNI_Interconexion', metadata,
    Column('IdUNegocio', Integer, nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nombre', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('EVENTO_ID', BigInteger, nullable=False),
    Column('TPB_EVENTO_ID', Integer, nullable=False),
    Column('TPB_EVENTO_NOMBRE', String(80, 'SQL_Latin1_General_CP850_CS_AS'), nullable=False),
    Column('TPB_CALIF_ID', Integer),
    Column('TPB_CALIF_NOMBRE', String(64, 'SQL_Latin1_General_CP850_CS_AS')),
    Column('EVENTO_FECHAHORA', DateTime, nullable=False),
    Column('NIVELVOLTAJE_ID', Integer),
    Column('EMPRESA_ID', Integer),
    Column('EVENTO_DTL_PODER', Numeric(10, 2)),
    Column('EVENTO_FECHA', Date),
    Column('EVENTO_HORA', Time)
)


t_vGeneracionDNV = Table(
    'vGeneracionDNV', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdUnidad', Integer),
    Column('EMS_Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Pot_Min', Numeric(10, 2)),
    Column('EMS_Tag_PAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Prioridad', Integer),
    Column('EMS_PAV', Numeric(10, 2)),
    Column('EMS_PAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('EMS_Tag_QAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('EMS_QAV', Numeric(10, 2)),
    Column('EMS_QAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Fecha_EMS', Date),
    Column('Hora_EMS', Time),
    Column('ION_Tag_PAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ION_Tag_QAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ION_PAV', Numeric(10, 2)),
    Column('ION_PAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ION_QAV', Numeric(10, 2)),
    Column('ION_QAQ', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Fecha_ION', Date),
    Column('Hora_ION', Time),
    Column('Agente', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('AGENTE_PAV', Numeric(10, 2)),
    Column('AGENTE_QAV', Numeric(10, 2)),
    Column('Fecha_AGENTE', Date),
    Column('Hora_AGENTE', Time),
    Column('TAGMV_CENTRAL', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CENTRAL_MV', Numeric(10, 2)),
    Column('TAGMVAR_CENTRAL', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CENTRAL_MVAR', Numeric(10, 2))
)


t_vGeneracionDNVTagMedBaj = Table(
    'vGeneracionDNVTagMedBaj', metadata,
    Column('IdUnidad', Integer),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Tag_PAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Prioridad_P', Integer),
    Column('P_AV', Numeric(10, 2)),
    Column('Tag_PAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('P_AQ', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Tag_QAV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Prioridad_Q', Integer),
    Column('Q_AV', Numeric(10, 2)),
    Column('Tag_QAQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Q_AQ', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Fecha', Date),
    Column('Hora', Time)
)


t_vGeneracionEMS_AQ_P = Table(
    'vGeneracionEMS_AQ_P', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Pot_Min', Numeric(10, 2)),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorNumerico', Numeric(18, 2)),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Prioridad', Integer, nullable=False)
)


t_vGeneracionEMS_AQ_Q = Table(
    'vGeneracionEMS_AQ_Q', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Pot_Min', Numeric(10, 2)),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorNumerico', Numeric(18, 2)),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Prioridad', Integer, nullable=False)
)


t_vGeneracionEMS_AV_P = Table(
    'vGeneracionEMS_AV_P', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Pot_Min', Numeric(10, 2)),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorNumerico', Numeric(18, 2)),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Prioridad', Integer, nullable=False)
)


t_vGeneracionEMS_AV_Q = Table(
    'vGeneracionEMS_AV_Q', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Pot_Min', Numeric(10, 2)),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorNumerico', Numeric(18, 2)),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Prioridad', Integer, nullable=False)
)


t_vGeneracionHidro = Table(
    'vGeneracionHidro', metadata,
    Column('IdEmpresa', Integer, nullable=False),
    Column('Cod_Emp', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_Emp', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_Emp', DateTime),
    Column('FechaBaja_Emp', DateTime),
    Column('IdUNegocio', Integer, nullable=False),
    Column('Cod_UNeg', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_UNeg', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_UNeg', DateTime),
    Column('FechaBaja_UNeg', DateTime),
    Column('IdCentral', Integer, nullable=False),
    Column('Cod_Cen', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_Central', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_Cen', DateTime),
    Column('FechaBaja_Cen', DateTime),
    Column('IdGrupoGeneracion', Integer, nullable=False),
    Column('Cod_GG', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_GG', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_GG', DateTime),
    Column('FechaBaja_GG', DateTime),
    Column('Cod_Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_Unidad', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_Uni', DateTime),
    Column('FechaBaja_Uni', DateTime),
    Column('IdTipoGeneracion', Integer, nullable=False),
    Column('Cod_TipoGen', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Des_TipoGen', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FechaAlta_TipoGen', DateTime, nullable=False),
    Column('FechaBaja_TipoGen', DateTime),
    Column('IdTipoTecnologia', SmallInteger, nullable=False),
    Column('Cod_TipoTec', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Des_TipoTec', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_TipoTec', DateTime),
    Column('FechaBaja_TipoTec', DateTime),
    Column('Row_ID', BigInteger, nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TAG_MV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TAG_MVAR', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('MV_SIMAE', Numeric(10, 2)),
    Column('MV_Medidor', Numeric(10, 2)),
    Column('MV_Agente', Numeric(10, 2)),
    Column('MV_Validado', Numeric(10, 2), nullable=False),
    Column('MVAR_SIMAE', Numeric(10, 2)),
    Column('MVAR_Medidor', Numeric(10, 2)),
    Column('MVAR_Agente', Numeric(10, 2)),
    Column('MVAR_Validado', Numeric(10, 2), nullable=False),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('TipoValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MV', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MVAR', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaValidacion', DateTime, nullable=False),
    Column('UsuarioValidacion', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_vGeneracionION_AQ_P = Table(
    'vGeneracionION_AQ_P', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Pot_Min', Numeric(10, 2)),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorNumerico', Numeric(18, 2)),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Prioridad', Integer, nullable=False)
)


t_vGeneracionION_AQ_Q = Table(
    'vGeneracionION_AQ_Q', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Pot_Min', Numeric(10, 2)),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorNumerico', Numeric(18, 2)),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Prioridad', Integer, nullable=False)
)


t_vGeneracionION_AV_P = Table(
    'vGeneracionION_AV_P', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Pot_Min', Numeric(10, 2)),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorNumerico', Numeric(18, 2)),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Prioridad', Integer, nullable=False)
)


t_vGeneracionION_AV_Q = Table(
    'vGeneracionION_AV_Q', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Pot_Min', Numeric(10, 2)),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorNumerico', Numeric(18, 2)),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Prioridad', Integer, nullable=False)
)


t_vGeneracionRenovable = Table(
    'vGeneracionRenovable', metadata,
    Column('IdEmpresa', Integer, nullable=False),
    Column('Cod_Emp', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUNegocio', Integer, nullable=False),
    Column('Cod_UNeg', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdCentral', Integer, nullable=False),
    Column('Cod_Cen', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_Central', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Cod_Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_Unidad', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdTipoGeneracion', Integer, nullable=False),
    Column('Cod_TipoGen', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Des_TipoGen', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdTipoTecnologia', SmallInteger, nullable=False),
    Column('Cod_TipoTec', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Des_TipoTec', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdTipoCombustible', SmallInteger, nullable=False),
    Column('Cod_TipoComb', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Des_TipoComb', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Row_ID', BigInteger, nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TAG_MV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TAG_MVAR', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('MV_SIMAE', Numeric(10, 2)),
    Column('MV_Medidor', Numeric(10, 2)),
    Column('MV_Agente', Numeric(10, 2)),
    Column('MV_Validado', Numeric(10, 2), nullable=False),
    Column('MVAR_SIMAE', Numeric(10, 2)),
    Column('MVAR_Medidor', Numeric(10, 2)),
    Column('MVAR_Agente', Numeric(10, 2)),
    Column('MVAR_Validado', Numeric(10, 2), nullable=False),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('TipoValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MV', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MVAR', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaValidacion', DateTime, nullable=False),
    Column('UsuarioValidacion', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_vGeneracionTermica = Table(
    'vGeneracionTermica', metadata,
    Column('IdEmpresa', Integer, nullable=False),
    Column('Cod_Emp', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_Emp', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUNegocio', Integer, nullable=False),
    Column('Cod_UNeg', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_UNeg', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdCentral', Integer, nullable=False),
    Column('Cod_Cen', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_Central', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Cod_Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_Unidad', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdTipoGeneracion', Integer, nullable=False),
    Column('Cod_TipoGen', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Des_TipoGen', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdTipoTecnologia', SmallInteger, nullable=False),
    Column('Cod_TipoTec', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Des_TipoTec', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdTipoCombustible', SmallInteger, nullable=False),
    Column('Cod_TipoComb', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Des_TipoComb', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Row_ID', BigInteger, nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TAG_MV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TAG_MVAR', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('MV_SIMAE', Numeric(10, 2)),
    Column('MV_Medidor', Numeric(10, 2)),
    Column('MV_Agente', Numeric(10, 2)),
    Column('MV_Validado', Numeric(10, 2), nullable=False),
    Column('MVAR_SIMAE', Numeric(10, 2)),
    Column('MVAR_Medidor', Numeric(10, 2)),
    Column('MVAR_Agente', Numeric(10, 2)),
    Column('MVAR_Validado', Numeric(10, 2), nullable=False),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('TipoValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MV', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MVAR', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaValidacion', DateTime, nullable=False),
    Column('UsuarioValidacion', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_vGeneracionTermicaRenovable = Table(
    'vGeneracionTermicaRenovable', metadata,
    Column('IdEmpresa', Integer, nullable=False),
    Column('Cod_Emp', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_Emp', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_Emp', DateTime),
    Column('FechaBaja_Emp', DateTime),
    Column('IdUNegocio', Integer, nullable=False),
    Column('Cod_UNeg', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_UNeg', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_UNeg', DateTime),
    Column('FechaBaja_UNeg', DateTime),
    Column('IdCentral', Integer, nullable=False),
    Column('Cod_Cen', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_Central', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_Cen', DateTime),
    Column('FechaBaja_Cen', DateTime),
    Column('IdUnidad', Integer, nullable=False),
    Column('Cod_Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nomb_Unidad', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_Unidad', DateTime),
    Column('FechaBaja_Unidad', DateTime),
    Column('IdTipoGeneracion', Integer, nullable=False),
    Column('Cod_TipoGen', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Des_TipoGen', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_TipoGen', DateTime, nullable=False),
    Column('FechaBaja_TipoGen', DateTime),
    Column('IdTipoTecnologia', SmallInteger, nullable=False),
    Column('Cod_TipoTec', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Des_TipoTec', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_TipoTec', DateTime),
    Column('FechaBaja_TipoTec', DateTime),
    Column('IdTipoCombustible', SmallInteger, nullable=False),
    Column('Cod_TipoComb', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Des_TipoComb', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaAlta_TipoComb', DateTime),
    Column('FechaBaja_TipoComb', DateTime),
    Column('Row_ID', BigInteger, nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TAG_MV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TAG_MVAR', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('MV_SIMAE', Numeric(10, 2)),
    Column('MV_Medidor', Numeric(10, 2)),
    Column('MV_Agente', Numeric(10, 2)),
    Column('MV_Validado', Numeric(10, 2), nullable=False),
    Column('MVAR_SIMAE', Numeric(10, 2)),
    Column('MVAR_Medidor', Numeric(10, 2)),
    Column('MVAR_Agente', Numeric(10, 2)),
    Column('MVAR_Validado', Numeric(10, 2), nullable=False),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('TipoValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MV', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color_MVAR', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('FechaValidacion', DateTime, nullable=False),
    Column('UsuarioValidacion', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_vGeneracion_Central_P = Table(
    'vGeneracion_Central_P', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Prioridad', Integer, nullable=False),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CENTRAL_MV', Numeric(18, 2)),
    Column('FechaP', Date),
    Column('HoraP', Time),
    Column('FechaG', Date),
    Column('HoraG', Time)
)


t_vGeneracion_Central_Q = Table(
    'vGeneracion_Central_Q', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Central', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('GrupoGeneracion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUnidad', Integer, nullable=False),
    Column('Unidad', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Prioridad', Integer, nullable=False),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('CENTRAL_MV', Numeric(18, 2)),
    Column('FechaP', Date),
    Column('HoraP', Time),
    Column('FechaG', Date),
    Column('HoraG', Time)
)


t_vImportExport = Table(
    'vImportExport', metadata,
    Column('IdEmpresa', Integer, nullable=False),
    Column('Emp_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Emp_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Emp_FechaAlta', DateTime),
    Column('Emp_FechaBaja', DateTime),
    Column('IdUNegocio', Integer, nullable=False),
    Column('UN_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UN_Nombre', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UN_FechaAlta', DateTime),
    Column('UN_FechaBaja', DateTime),
    Column('IdSubOri', Integer, nullable=False),
    Column('SEOri_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEOri_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEOri_FechaAlta', DateTime),
    Column('SEOri_FechaBaja', DateTime),
    Column('IdSubDest', Integer, nullable=False),
    Column('SEDest_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEDest_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEDest_FechaAlta', DateTime),
    Column('SEDest_FechaBaja', DateTime),
    Column('Linea', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Circuito', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Lin_FechaAlta', DateTime),
    Column('Lin_FechaBaja', DateTime),
    Column('Cir_Nombre', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('NumCircuito', SmallInteger, nullable=False),
    Column('Cir_FechaAlta', DateTime),
    Column('Cir_FechaBaja', DateTime),
    Column('IdNivelVoltaje', Integer, nullable=False),
    Column('NV_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NV_FechaAlta', DateTime),
    Column('NV_FechaBaja', DateTime),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('MV_Original', Numeric(10, 2)),
    Column('MV_Validado', Numeric(10, 2)),
    Column('MVAR_Original', Numeric(10, 2)),
    Column('MVAR_Validado', Numeric(10, 2)),
    Column('Color_MV', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Color_MVAR', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FechaValidacion', DateTime),
    Column('UsuarioValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TipoValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vImportacion = Table(
    'vImportacion', metadata,
    Column('IdEmpresa', Integer, nullable=False),
    Column('Emp_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Emp_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Emp_FechaAlta', DateTime),
    Column('Emp_FechaBaja', DateTime),
    Column('IdUNegocio', Integer, nullable=False),
    Column('UN_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UN_Nombre', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UN_FechaAlta', DateTime),
    Column('UN_FechaBaja', DateTime),
    Column('IdSubOri', Integer, nullable=False),
    Column('SEOri_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEOri_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEOri_FechaAlta', DateTime),
    Column('SEOri_FechaBaja', DateTime),
    Column('IdSubDest', Integer, nullable=False),
    Column('SEDest_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEDest_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEDest_FechaAlta', DateTime),
    Column('SEDest_FechaBaja', DateTime),
    Column('Linea', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Lin_FechaAlta', DateTime),
    Column('Lin_FechaBaja', DateTime),
    Column('IdNivelVoltaje', Integer, nullable=False),
    Column('NV_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NV_FechaAlta', DateTime),
    Column('NV_FechaBaja', DateTime),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('MV_Original', Numeric(38, 2)),
    Column('MV_Validado', Numeric(38, 2)),
    Column('MVAR_Original', Numeric(38, 2)),
    Column('MVAR_Validado', Numeric(38, 2))
)


t_vImportacionLinea = Table(
    'vImportacionLinea', metadata,
    Column('IdEmpresa', Integer, nullable=False),
    Column('Emp_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Emp_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdUNegocio', Integer, nullable=False),
    Column('UN_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UN_Nombre', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdSubOri', Integer, nullable=False),
    Column('SEOri_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEOri_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('IdSubDest', Integer, nullable=False),
    Column('SEDest_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SEDest_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Linea', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NV_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('MV_Original', Numeric(38, 2)),
    Column('MV_Validado', Numeric(38, 2)),
    Column('MVAR_Original', Numeric(38, 2)),
    Column('MVAR_Validado', Numeric(38, 2))
)


t_vInterconexionDNV = Table(
    'vInterconexionDNV', metadata,
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SubestacionOrigen', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SubestacionDestino', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Linea', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Circuito', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PAV', Numeric(10, 2), nullable=False),
    Column('QAV', Numeric(10, 2), nullable=False),
    Column('SV1', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SV2', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Estado', BIT),
    Column('Prioridad', Integer),
    Column('IdNivelVoltaje', Integer, nullable=False),
    Column('INTERC_AV', Numeric(10, 2), nullable=False)
)


t_vLTC = Table(
    'vLTC', metadata,
    Column('CodigoEmpresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreEmpresa', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Emp_FechaAlta', DateTime),
    Column('Emp_FechaBaja', DateTime),
    Column('CodigoUNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreUNegocio', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UN_FechaAlta', DateTime),
    Column('UN_FechaBaja', DateTime),
    Column('CodigoSubestacion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreSubestacion', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Sub_FechaAlta', DateTime),
    Column('Sub_FechaBaja', DateTime),
    Column('CodigoTrafo', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreTrafo', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Tra_FechaAlta', DateTime),
    Column('Tra_FechaBaja', DateTime),
    Column('CodigoLTC', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreLTC', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LTC_FechaAlta', DateTime),
    Column('LTC_FechaBaja', DateTime),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('Valor', Numeric(18, 2), nullable=False)
)


t_vLTC_AV = Table(
    'vLTC_AV', metadata,
    Column('EMPRESA_CODIGO', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('EMPRESA_NOMBRE', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UNEGOCIO_CODIGO', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UNEGOCIO_NOMBRE', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SUBESTACION_CODIGO', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('SUBESTACION_NOMBRE', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('LTC_CODIGO', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('LTC_NOMBRE', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TRAFO_CODIGO', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TRAFO_NOMBRE', String(100, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('LTC_ESTADO', BIT, nullable=False),
    Column('LTC_TAG_AV', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LTC_AV', Numeric(10, 2)),
    Column('TAG_ESTADO', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FechaHora', DateTime),
    Column('Fecha', Date),
    Column('Hora', Time)
)


t_vPosicion_Generacion_H = Table(
    'vPosicion_Generacion_H', metadata,
    Column('IdPosicion', Integer, nullable=False),
    Column('Posicion_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TipoPosicion', Integer, nullable=False),
    Column('GeneracionMV', Numeric(38, 2)),
    Column('GeneracionMVAR', Numeric(38, 2)),
    Column('Fecha', Date),
    Column('Hora', Time)
)


t_vPosicion_Generacion_T = Table(
    'vPosicion_Generacion_T', metadata,
    Column('IdPosicion', Integer, nullable=False),
    Column('Posicion_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('TipoPosicion', Integer, nullable=False),
    Column('GeneracionMV', Numeric(38, 2)),
    Column('GeneracionMVAR', Numeric(38, 2)),
    Column('Fecha', Date),
    Column('Hora', Time)
)


t_vPotencia_Importacion = Table(
    'vPotencia_Importacion', metadata,
    Column('IdEmpresa', Integer),
    Column('Emp_Codigo', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Emp_Nombre', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdUNegocio', Integer),
    Column('Cod_Unegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Nom_Unegocio', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdLinea', Integer, nullable=False),
    Column('Cod_Lin', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Nom_Lin', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Sistema', String(128, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Cod_NV', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdNivelVoltaje', Integer),
    Column('MV', Numeric(38, 2)),
    Column('Fecha', Date),
    Column('Hora', Time)
)


t_vReactor = Table(
    'vReactor', metadata,
    Column('Row_ID', BigInteger, nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreEmpresa', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Emp_FechaAlta', DateTime),
    Column('Emp_FechaBaja', DateTime),
    Column('TipoCompensador', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreUNegocio', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UN_FechaAlta', DateTime),
    Column('UN_FechaBaja', DateTime),
    Column('Subestacion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreSubestacion', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Sub_FechaAlta', DateTime),
    Column('Sub_FechaBaja', DateTime),
    Column('Compensador', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreCompensador', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Com_FechaAlta', DateTime),
    Column('Com_FechaBaja', DateTime),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorOriginal', Numeric(10, 2)),
    Column('ValorValidado', Numeric(10, 2), nullable=False),
    Column('TipoValidacion', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Color', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('FechaValidacion', DateTime, nullable=False),
    Column('UsuarioValidacion', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_vTAG = Table(
    'vTAG', metadata,
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_vTAG_Voltaje = Table(
    'vTAG_Voltaje', metadata,
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False)
)


t_vTransData_Demanda = Table(
    'vTransData_Demanda', metadata,
    Column('Tipo', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('Demanda', Numeric(20, 2)),
    Column('FechaCalculo', DateTime)
)


t_vUnidadPQ = Table(
    'vUnidadPQ', metadata,
    Column('IdEmpresa', Integer),
    Column('EMPRESA', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdUNegocio', Integer),
    Column('UNEGOCIO', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdCentral', Integer),
    Column('CENTRAL', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdGrupoGeneracion', Integer),
    Column('GRUPOGENERACION', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('IdUnidad', Integer),
    Column('UNIDAD', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('FechaHora', DateTime, nullable=False),
    Column('Fecha', Date, nullable=False),
    Column('Hora', Time, nullable=False),
    Column('PotenciaActiva', Numeric(10, 2)),
    Column('ValorCaracter', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('TAGQ', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('PotenciaReactiva', Numeric(10, 2)),
    Column('ValorCaracterQ', String(50, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Calidad', String(50, 'SQL_Latin1_General_CP1_CI_AS'))
)


t_vVoltaje = Table(
    'vVoltaje', metadata,
    Column('Row_ID', BigInteger),
    Column('Empresa', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreEmpresa', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Emp_FechaAlta', DateTime),
    Column('Emp_FechaBaja', DateTime),
    Column('UNegocio', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreUNegocio', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('UN_FechaAlta', DateTime),
    Column('UN_FechaBaja', DateTime),
    Column('SubEstacion', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreSubestacion', String(100, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Sub_FechaAlta', DateTime),
    Column('Sub_FechaBaja', DateTime),
    Column('Barra', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('NombreBarra', String(50, 'SQL_Latin1_General_CP1_CI_AS'), nullable=False),
    Column('Bar_FechaAlta', DateTime),
    Column('Bar_FechaBaja', DateTime),
    Column('TAG', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('ValorOriginal', Numeric(10, 2)),
    Column('ValorValidado', Numeric(10, 2)),
    Column('TipoValidacion', String(75, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('Color', String(20, 'SQL_Latin1_General_CP1_CI_AS')),
    Column('LimiteSuperior', Numeric(10, 2)),
    Column('LimiteInferior', Numeric(10, 2)),
    Column('Fecha', Date),
    Column('Hora', Time),
    Column('FechaValidacion', DateTime),
    Column('UsuarioValidacion', String(50, 'SQL_Latin1_General_CP1_CI_AS'))
)
