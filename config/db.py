from sqlalchemy import create_engine, MetaData
# Crear el motor de conexión
engine = create_engine("mysql+pymysql://andrew1:843cb920@www.db4free.net/database_daw")
con = engine.connect()
# Crear un objeto MetaData
meta = MetaData()
