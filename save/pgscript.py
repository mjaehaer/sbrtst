from urllib.parse import urlparse
import psycopg2
import sys
from contextlib import closing
from test import simple_table

# result = urlparse(sys.argv[1])
result = urlparse("postgresql://postgres:875543@localhost:5432/newbase")

username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

query_tables = '''
SELECT schemaname,tablename
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema';	
'''

query_columns = '''
	SELECT table_schema,
       table_name,
       -- ordinal_position as position,
       column_name
       -- data_type,
       -- case when character_maximum_length is not null
       --      then character_maximum_length
       --      else numeric_precision end as max_length,
       -- is_nullable
       -- column_default as default_value
from information_schema.columns
where table_schema not in ('information_schema', 'pg_catalog')
order by table_schema, 
         table_name,
         ordinal_position;
'''

query_fk = '''
SELECT
	ccu.table_name AS references_table,
	ccu.column_name AS references_field,
	tc.table_name,
	kcu.column_name  

FROM information_schema.table_constraints tc

LEFT JOIN information_schema.key_column_usage kcu
 ON tc.constraint_catalog = kcu.constraint_catalog
 AND tc.constraint_schema = kcu.constraint_schema
 AND tc.constraint_name = kcu.constraint_name

LEFT JOIN information_schema.referential_constraints rc
 ON tc.constraint_catalog = rc.constraint_catalog
 AND tc.constraint_schema = rc.constraint_schema
 AND tc.constraint_name = rc.constraint_name

LEFT JOIN information_schema.constraint_column_usage ccu
 ON rc.unique_constraint_catalog = ccu.constraint_catalog
 AND rc.unique_constraint_schema = ccu.constraint_schema
 AND rc.unique_constraint_name = ccu.constraint_name

WHERE lower(tc.constraint_type) in ('foreign key')
'''

query_views = '''
	SELECT u.view_schema as schema_name,
	u.view_name,
	u.table_schema as referenced_table_schema,
	u.table_name as referenced_table_name
	from information_schema.view_table_usage u
	join information_schema.views v 
	on u.view_schema = v.table_schema
	and u.view_name = v.table_name
	where u.table_schema not in ('information_schema', 'pg_catalog')
	order by u.view_schema,
	u.view_name;
'''
tables = []
columns = []
fk = []
tblViews = []

with closing(psycopg2.connect(database = database, user = username, password = password, host = hostname, port = port)) as conn:
	with conn.cursor() as cursor:
		cursor.execute(query_tables)
		for row in cursor:
			tables.append(row)

print('tables \n')

with closing(psycopg2.connect(database = database, user = username, password = password, host = hostname, port = port)) as conn:
	with conn.cursor() as cursor:
		cursor.execute(query_columns)
		for row in cursor:
			columns.append(row)
print('columns \n')

with closing(psycopg2.connect(database = database, user = username, password = password, host = hostname, port = port)) as conn:
	with conn.cursor() as cursor:
		cursor.execute(query_fk)
		for row in cursor:
			fk.append(row)
print('fk \n')

with closing(psycopg2.connect(database = database, user = username, password = password, host = hostname, port = port)) as conn:
	with conn.cursor() as cursor:
		cursor.execute(query_views)
		for row in cursor:
			tblViews.append(row)
print('tblViews \n')

simple_table(tables,columns,fk,tblViews)