from logger import logger
from database_config import dev_db_config

db_pool = DatabaseManager(dev_db_config)
db_connection = db_connection.get_connection()


def add_validation_request(headers, data):
    columns = [
        ID,
        GROUP_NAME,
        SRC_ASOF,
        SRC_DATASET_ID,
        SRC_SCHEMA,
        TGET_ASOF,
        TGT_DATASET_ID,
        TGT_SCHEMA,
        TABLE_NAME,
        REQUESTED_BY,
        CREATE_TS
    ]

    try:
        insert_query, data_to_insert = generate_insert_query("data_cmp_", columns, data)
        with db_connection.cursor() as cursor:
            cursor.execute(insert_query, data_to_insert)
        connection.commit()
        print("Data inserted successfully")
    except oracledb.Error as e:
        print("Error inserting data:", e)
    
    return True


def generate_insert_query(table_name, columns, data):
    """
    Generates a safe Oracle INSERT query with named placeholders.

    Args:
        columns (list): A list of column names.
        data (dict): A dictionary of data where keys match the column names.

    Returns:
        tuple: A tuple containing the query string and the data dictionary.
    """
    # Create the column part of the query: "(ID, GROUP_NAME, ...)"
    column_names = ", ".join(columns)

    # Create the placeholders part of the query: "(:ID, :GROUP_NAME, ...)"
    # The ":" prefix is the standard for named placeholders in many Oracle drivers
    placeholders = ", ".join(f":{col}" for col in columns)

    # Construct the final query string
    query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

    return query, data


