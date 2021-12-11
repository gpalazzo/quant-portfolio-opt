import re
from typing import Any, Dict, Optional, List
import os

import pandas as pd
from sqlalchemy.exc import NoSuchModuleError

from kedro.io.core import AbstractDataSet, DataSetError


KNOWN_PIP_INSTALL = {
    "psycopg2": "psycopg2",
    "mysqldb": "mysqlclient",
    "cx_Oracle": "cx_Oracle",
}

DRIVER_ERROR_MESSAGE = """
A module/driver is missing when connecting to your SQL server. SQLDataSet
 supports SQLAlchemy drivers. Please refer to
 https://docs.sqlalchemy.org/en/13/core/engines.html#supported-databases
 for more information.
\n\n
"""


def _find_known_drivers(module_import_error: ImportError) -> Optional[str]:
    """Looks up known keywords in a ``ModuleNotFoundError`` so that it can
    provide better guideline for the user.

    Args:
        module_import_error: Error raised while connecting to a SQL server.

    Returns:
        Instructions for installing missing driver. An empty string is
        returned in case error is related to an unknown driver.

    """

    # module errors contain string "No module name 'module_name'"
    # we are trying to extract module_name surrounded by quotes here
    res = re.findall(r"'(.*?)'", str(module_import_error.args[0]).lower())

    # in case module import error does not match our expected pattern
    # we have no recommendation
    if not res:
        return None

    missing_module = res[0]

    if KNOWN_PIP_INSTALL.get(missing_module):
        return (
            "You can also try installing missing driver with\n"
            "\npip install {}".format(KNOWN_PIP_INSTALL.get(missing_module))
        )

    return None


def _get_missing_module_error(import_error: ImportError) -> DataSetError:
    missing_module_instruction = _find_known_drivers(import_error)

    if missing_module_instruction is None:
        return DataSetError(
            f"{DRIVER_ERROR_MESSAGE}Loading failed with error:\n\n{str(import_error)}"
        )

    return DataSetError(f"{DRIVER_ERROR_MESSAGE}{missing_module_instruction}")


def _get_sql_alchemy_missing_error() -> DataSetError:
    return DataSetError(
        "The SQL dialect in your connection is not supported by "
        "SQLAlchemy. Please refer to "
        "https://docs.sqlalchemy.org/en/13/core/engines.html#supported-databases "
        "for more information."
    )


class CustomSQLQueryDataSet(AbstractDataSet):
    """``SQLQueryDataSet`` loads data from a provided SQL query. It
    uses ``pandas.DataFrame`` internally, so it supports all allowed
    pandas options on ``read_sql_query``. Since Pandas uses SQLAlchemy behind
    the scenes, when instantiating ``SQLQueryDataSet`` one needs to pass
    a compatible connection string either in ``credentials`` (see the example
    code snippet below) or in ``load_args``. Connection string formats supported
    by SQLAlchemy can be found here:
    https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls

    It does not support save method so it is a read only data set.
    To save data to a SQL server use ``SQLTableDataSet``.


    Example:
    ::

        >>> from kedro.extras.datasets.pandas import SQLQueryDataSet
        >>> import pandas as pd
        >>>
        >>> data = pd.DataFrame({"col1": [1, 2], "col2": [4, 5],
        >>>                      "col3": [5, 6]})
        >>> sql = "SELECT * FROM table_a"
        >>> credentials = {
        >>>     "con": "postgresql://scott:tiger@localhost/test"
        >>> }
        >>> data_set = SQLQueryDataSet(sql=sql,
        >>>                            credentials=credentials)
        >>>
        >>> sql_data = data_set.load()
        >>>

    """

    def __init__(
        self, sql: str, credentials: Dict[str, Any], load_args: Dict[str, Any] = None
    ) -> None:
        """Creates a new ``SQLQueryDataSet``.

        Args:
            sql: The sql query statement.
            credentials: A dictionary with a ``SQLAlchemy`` connection string.
                Users are supposed to provide the connection string 'con'
                through credentials. It overwrites `con` parameter in
                ``load_args`` and ``save_args`` in case it is provided. To find
                all supported connection string formats, see here:
                https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls
            load_args: Provided to underlying pandas ``read_sql_query``
                function along with the connection string.
                To find all supported arguments, see here:
                https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_sql_query.html
                To find all supported connection string formats, see here:
                https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls

        Raises:
            DataSetError: When either ``sql`` or ``con`` parameters is emtpy.
        """

        if not sql:
            raise DataSetError(
                "`sql` argument cannot be empty. Please provide a sql query"
            )

        if not (credentials and "con" in credentials and credentials["con"]):
            raise DataSetError(
                "`con` argument cannot be empty. Please "
                "provide a SQLAlchemy connection string."
            )

        default_load_args = {}  # type: Dict[str, Any]

        self._load_args = (
            {**default_load_args, **load_args}
            if load_args is not None
            else default_load_args
        )

        self._load_args["sql"] = sql
        self._load_args["con"] = credentials["con"]

    def _describe(self) -> Dict[str, Any]:
        load_args = self._load_args.copy()
        del load_args["sql"]
        del load_args["con"]
        return dict(sql=self._load_args["sql"], load_args=load_args)

    def _parse_query_source(self) -> List[str]:
        query_source = self._load_args["sql"].split(" ")[-1]
        return query_source.split(".")

    def _load(self) -> pd.DataFrame:
        try:
            database, schema, table = self._parse_query_source()
            self._load_args["con"] = self._load_args["con"].replace(
                os.getenv("PGSQL_DATABASE"), database
            )
            return pd.read_sql_query(**self._load_args)
        except ImportError as import_error:
            raise _get_missing_module_error(import_error) from import_error
        except NoSuchModuleError as exc:
            raise _get_sql_alchemy_missing_error() from exc

    def _save(self, data: pd.DataFrame) -> None:
        database, schema, table = self._parse_query_source()
        _con = self._load_args["con"].replace(os.getenv("PGSQL_DATABASE"), database)
        data.to_sql(table, _con, if_exists="replace", index=False)
