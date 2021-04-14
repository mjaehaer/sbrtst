import psycopg2
from contextlib import closing
import urllib.parse,sys

str = sys.argv[1]
fragment = urllib.parse.urlparse(str).fragment
print(dict(urllib.parse.parse_qsl(fragment)))

with closing(psycopg2.connect(
    database="newbase", 
    user="postgres", 
    password="875543", 
    host="127.0.0.1", 
    port="5432")) as conn:
    with conn.cursor() as cursor:
        cursor.execute('''
        SELECT * FROM information_schema.key_column_usage where constraint_catalog = 'newbase' and constraint_name like '%fkey'
        ''')
        for row in cursor:
            print(row)
            print(type(row))

