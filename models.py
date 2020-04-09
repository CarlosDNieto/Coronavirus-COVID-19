"""
This module is for classes and methods that we will need.

We need 2 classes:
	- country
	- Timecountries_series
"""

import pandas as pd
import numpy as np

country_column = 'Country/Region'
drop_cols = ['Lat','Long','Province/State']

class TimeSeries:

	def __init__(self, data, country_name=None):

		# fix the columns with dates
		df = data.copy()
		df.drop(drop_cols, axis=1, inplace=True)
		cols = df.columns.to_list()	
		date_cols = [date.split()[0] for date in list(map(str,pd.to_datetime(cols[1:])))]
		cols[1:] = date_cols
		df.rename(dict(zip(df.columns.to_list(),cols)),axis=1, inplace=True)
		df.sort_values(by=country_column,inplace=True)
		df.index=df[country_column]
		df.drop(country_column,axis=1,inplace=True)

		# unique contries list ordered alphabetically.
		countries_list = list(df.index.unique())
		countries_list.sort()


		self.country_name = country_name

		# if the user throws a country_name name
		if country_name != None:

			# check if country name is a string or a list
			if type(country_name)==str:

				# verify if its a valid country
				if country_name in countries_list:

					self.country_name = country_name

					df = df[df.index==self.country_name].groupby(country_column).sum()
					df.replace({0:np.nan},inplace=True)
					df.dropna(axis=1,inplace=True)					

					self.data = df

				# if country not valid
				else:
					err = """
Please enter a valid country_name.

valid country names: {}
					""".format(countries_list)
					print(err)
					raise

			# If it is a list
			elif type(country_name)==list:

				# check if all are valid countries
				if all(i in countries_list for i in country_name):
					self.country_name = country_name

					# get all countries series of values
					countries_series = []
					for i in range(len(country_name)):
						countries_series.append(
							df[df.index==self.country_name[i]].groupby(country_column).sum()
							)

					# consolidate series in a df
					df = pd.concat(countries_series)
					df.replace({0:np.nan},inplace=True)
					df.dropna(axis=1,inplace=True,thresh=1)

					self.data = df

				else:
					err = """
Please enter a valid country_name.

valid country names: {}
					""".format(countries_list)
					print(err)
					raise

		else:
			self.data = df.groupby(country_column).sum()



	## Methods ##

	def get_data_frame(self, transpose=False):
		"""
		Gets data frame of Time Series.
		"""
		if transpose:
			df = self.data.copy()
			return df.transpose()

		else:
			df = self.data.copy()
			return df

	def get_last_update_date(self):
		"""
		Gets last update date of the time series
		"""
		df = self.data.copy()
		dates = pd.to_datetime(df.columns.to_list())
		max_date = str(dates.max()).split()[0]
		return max_date

	def get_last_values(self):
		"""
		"""
		df = self.data.copy()
		last_date = self.get_last_update_date()
		last_values = df[last_date]
		return last_values

	def get_diff(self,percentages=False):
		"""
		"""
		if percentages:
			df = self.data.copy()
			df = df.diff(axis=1)/df
			return df.dropna(axis=1,thresh=1)

		else:
			df = self.data.copy()
			return df.diff(axis=1).dropna(axis=1,thresh=1)