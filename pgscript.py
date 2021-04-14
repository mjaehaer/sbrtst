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

query_columns = '''
	SELECT table_schema,
       table_name,
       column_name
from information_schema.columns
where table_schema not in ('information_schema', 'pg_catalog')
order by table_schema, 
         table_name,
         ordinal_position;
'''
query_fk = '''
SELECT
	tc.constraint_schema,
	tc.table_name,
	kcu.column_name,
	rc.constraint_schema,
	ccu.table_name AS references_table,
	ccu.column_name AS references_field
	

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
columns = []
fk = []
tblViews = []

with closing(psycopg2.connect(database = database, user = username, password = password, host = hostname, port = port)) as conn:
	with conn.cursor() as cursor:
		cursor.execute(query_columns)
		for row in cursor:
			columns.append(row)

tables_1 = []
tables_2 = []
with closing(psycopg2.connect(database = database, user = username, password = password, host = hostname, port = port)) as conn:
	with conn.cursor() as cursor:
		cursor.execute(query_fk)
		for row in cursor:
			fk.append(list(row))
			tables_1.append(list((row[0],row[1])))
			tables_2.append(list((row[3],row[4])))

for i in tables_1:
	for t in columns:
		if i[0] in t[0] and i[1] in t[1]:
			if t[2] not in i:
				i.append(t[2])

for i in tables_2:
	for t in columns:
		if i[0] in t[0] and i[1] in t[1]:
			if t[2] not in i:
				i.append(t[2])

for x in tables_1:
	if x in tables_1:
		tables_1.remove(x)
# print(fk)
with closing(psycopg2.connect(database = database, user = username, password = password, host = hostname, port = port)) as conn:
	with conn.cursor() as cursor:
		cursor.execute(query_views)
		for row in cursor:
			tblViews.append(row)
# print(tblViews)			
print('tblViews \n')
simple_table(tables_1,tables_2, fk, tblViews)
print("pdf_saved")