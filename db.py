from logger import logger
from database_config import dev_db_config

db_pool = DatabaseManager(dev_db_config)
db_connection = db_connection.get_connection()


def add_validation_request(headers, data):
    columns = [
        "GROUP_NAME",
        "SRC_ASOF",
        "SRC_DATASET_ID",
        "SRC_SCHEMA",
        "TGET_ASOF",
        "TGT_DATASET_ID",
        "TGT_SCHEMA",
        "TABLE_NAME",
        "REQUESTED_BY",
        "STATUS"
    ]

    try:
        insert_query, data_to_insert = generate_insert_query("data_comp_request_master", "DATA_COMP_REQUEST_MASTER_SEQ", columns, data)
        with db_connection.cursor() as cursor:
            cursor.execute(insert_query, data_to_insert)
        db_connection.commit()
        print("Data inserted successfully")
    except oracledb.Error as e:
        print("Error inserting data:", e)
        return False
    
    return True


def generate_insert_query(table_name, sequence_name, columns, data):
    """
    Generates a safe Oracle INSERT query with named placeholders.

    Args:
        columns (list): A list of column names.
        data (dict): A dictionary of data where keys match the column names.

    Returns:
        tuple: A tuple containing the query string and the data dictionary.
    """
    # Create the column part of the query: "(ID, GROUP_NAME, ...)"
    id_column = "ID"
    all_columns_str = f"{id_column}, {', '.join(columns)}"

    # The sequence's .NEXTVAL is used for the ID, not a placeholder.
    placeholders = ", ".join(f":{col}" for col in columns)
    all_values_str = f"{sequence_name}.NEXTVAL, {', '.join(placeholders)}"

    # Construct the final query string
    query = f"INSERT INTO {table_name} ({all_columns_str}) VALUES ({all_values_str})"

    return query, data


