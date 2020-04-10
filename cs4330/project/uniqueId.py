import string, random
import MySQLdb as sql


# Function to get random id, and check its uniqueness
def getUniqueId(table_name, key, cursor, length):
    new_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    s = f"SELECT * FROM {table_name} where {key} = '{new_id}'"
    cursor.execute(s)
    res = cursor.fetchone()
    while res is not None and len(res) > 0:  # ID collision
        new_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        s = f"SELECT * FROM {table_name} where {key} = '{new_id}'"
        cursor.execute(s)
        res = cursor.fetchone()
    return new_id
