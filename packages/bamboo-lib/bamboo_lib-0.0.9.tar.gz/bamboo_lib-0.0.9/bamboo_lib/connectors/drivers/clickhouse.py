from bamboo_lib.connectors.models import BaseDriver
from data_catapult.database.clickhouse import ClickhouseDriver as CatapultCd


class ClickhouseDriver(BaseDriver):
    TYPE = 'Clickhouse Bulk Write Driver'

    def __init__(self, **kwargs):
        super(ClickhouseDriver, self).__init__(**kwargs)
        self.settings = {
            "host": kwargs.get("host", "localhost"),
            "port": int(kwargs.get("port", 9000)),
            "database": kwargs.get("database", "default"),
            "user": kwargs.get("user", "default"),
            "password": kwargs.get("password", "")
        }

    def write_df(self, table_name, df, **kwargs):
        pgd = CatapultCd(**self.settings)
        # TODO support for schema names and explicit dtypes
        # dtype = kwargs.get("dtype", None)
        pk = kwargs.get("pk", None)
        return pgd.ingest(df, table_name, if_exists="append", pk=pk)
