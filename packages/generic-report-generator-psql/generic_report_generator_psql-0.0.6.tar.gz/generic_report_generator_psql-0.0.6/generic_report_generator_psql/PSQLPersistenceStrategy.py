from sqlformat import ResultPersistenceStrategy
from sqlformat.helper import sql_helper
from sqlformat import SQLStatement


class PSQLPersistenceStrategy(ResultPersistenceStrategy):
    def __init__(self,
                 create_table_statement: str,
                 schema: str,
                 buffer_prefix: str,
                 fixed_buffer_id: str):
        """
        :param create_table_statement: Result structure in SQL CREATE Table format
        :param schema: The result buffer will be created on
        :param buffer_prefix: The buffer table name prefix usually is application name
        :param fixed_buffer_id: The buffer table id
        """
        super().__init__()
        _validate_create_table_statement(create_table_statement)
        self.create_table_statement = create_table_statement
        self.schema = schema
        self.buffer_prefix = buffer_prefix
        self.fixed_buffer_id = fixed_buffer_id

    def _init_buffer(self):
        return sql_helper.split_statements(self.create_table_statement.format(
            __schema__=self.schema,
            __temp_table__=self.temp_table_name
        ))

    def _flush_buffer(self):
        # Work around for Database that didn't support flush table to local file.
        self.buffer_destination = "{}.{}".format(self.schema, self.temp_table_name)
        return [SQLStatement("")]

    @property
    def temp_table_name(self):
        return "{}_{}".format(
            self.buffer_prefix.lower().replace('-', '_'),
            str(self.fixed_buffer_id).lower().replace('-', '_')
        )

    def change_buffer_id(self):
        self.buffer_id = self.fixed_buffer_id

    @property
    def extra_procedure_variables(self):
        return {
            "__schema__": self.schema,
            "__temp_table__": self.temp_table_name
        }


def _validate_create_table_statement(create_table_statement):
    is_statement_valid = "{__schema__}.{__temp_table__}" in create_table_statement
    if not is_statement_valid:
        raise Exception('Table name must be {__schema__}.{__temp_table__}')
    return True
