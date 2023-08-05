import sqlalchemy
from bamboo_lib.connectors.models import BaseDriver
from data_catapult.database.postgres import PostgresDriver as CatapultPgd


class PostgresDriver(BaseDriver):
    TYPE = 'Postgres Bulk Write Driver'

    def __init__(self, **kwargs):
        super(PostgresDriver, self).__init__(**kwargs)
        self.engine = sqlalchemy.create_engine(self.uri)

    def write_df(self, table_name, df, **kwargs):
        pgd = CatapultPgd(self.engine)
        schema_name = kwargs.get("schema", "public")
        dtype = kwargs.get("dtype", None)
        return pgd.to_sql(df, schema_name, table_name, dtype)

    def add_pk(self, *args):
        pgd = CatapultPgd(self.engine)
        return pgd.add_pk(*args)
