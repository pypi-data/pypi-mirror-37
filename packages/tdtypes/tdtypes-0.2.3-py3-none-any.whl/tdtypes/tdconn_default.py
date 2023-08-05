"Default Teradata connection functions"

__author__ = "Paresh Adhia"
__copyright__ = "Copyright 2016-2017, Paresh Adhia"

from teradata.api import *

def dbconn_args(parser):
	"add an optional argument to passed argparse object to enable supplying ODBC connection string"
	import os

	defdsn = os.environ.get('TDCONN')
	parser.add_argument("--tdconn", default=defdsn, required=(defdsn is None), help="Connection string")


def dbconnect(*args, **kargs):
	"returns raw database connection"
	from teradata.tdodbc import connect
	return connect(driver='Teradata', **{k:v for k, v in [a.split('=') for a in args[0].tdconn.split(';')]})
