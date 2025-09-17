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


def fetch_records(table_name, columns, where_params=None):
    if '*' in columns:
        select_clause = "*"
    else:
        # Join the list of column names into a comma-separated string
        select_clause = ", ".join(columns)

    query = f"SELECT {select_clause} FROM {table_name}"

    if where_params:
        where_clauses = [f"{key} = :{key}" for key in where_params.keys()]
        query += " WHERE " + " AND ".join(where_clauses)

    results = []
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(query, where_params or {})
            colnames = [desc[0].lower() for desc in cursor.description]
            for row in cursor.fetchall():
                results.append(dict(zip(colnames, row)))

    except oracledb.DatabaseError as e:
        return False

    return results


def run_update_query(sql_query, params):
    with db_connection.cursor() as cursor:
        try:
            cursor.execute(sql_query, params)
            rows_updated = cursor.rowcount
            connection.commit()
            print(f"✅ Successfully updated {rows_updated} row(s).")
            
        except oracledb.Error as e:
            error_obj, = e.args
            connection.rollback()
            rows_updated = -1 
        finally:
            return rows_updated


