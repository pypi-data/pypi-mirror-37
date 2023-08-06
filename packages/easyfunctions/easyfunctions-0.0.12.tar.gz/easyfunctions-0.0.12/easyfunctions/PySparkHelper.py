import pandas as pd
import numpy as np
import re
from pyspark.sql.types import *

class PySparkHelper:


	def __init__(self):
		pass



	def convertTypes(self, type_in):

		pattern_datetime = re.compile('.*datetime.*')

		if type_in == 'int64':
			return IntegerType()
		elif type_in == 'float64':
			return FloatType()
		elif type_in == 'bool':
			return BooleanType()
		elif type_in in ['object','string']:
			return StringType()
		elif re.match(pattern=pattern_datetime, string=type_in):
			return TimestampType()
		else:
			return StringType()



	def toPySparkDf(self, context, df_in):
		list_of_cols = []

		for i in df_in.columns:
			new_struct_field = StructField(i, self.convertTypes(str(df_in[i].dtype)), True)
			list_of_cols.append(new_struct_field)
	    
		DfSchema = StructType(list_of_cols)

		return context.createDataFrame(df_in,schema=DfSchema)
