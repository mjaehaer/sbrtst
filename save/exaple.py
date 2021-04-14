from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph
connection = "mysql://root:@127.0.0.1/newuspd?charset=utf8"

# connects = "postgresql://postgres:875543@localhost:5432/newbase"

# create the pydot graph object by autoloading all tables via a bound metadata object
graph = create_schema_graph(
   metadata=MetaData(connection),
   show_datatypes=False,   # The image would get nasty big if we'd show the datatypes
   show_indexes=False,     # ditto for indexes
   rankdir='LR',           # From left to right (instead of top to bottom)
   concentrate=False       # Don't try to join the relation lines together
)
graph.write_png('dbschema.png') # write out the file