import time
import pandas as pd

df = pd.read_csv('/Users/shuchitaprakash/coding1/job_data2.csv')


# Create a pandas DataFrame from the extracted data
df = pd.read_csv('/Users/shuchitaprakash/coding1/job_data2.csv')

# Creating new dataframe 
new_DF= df.copy()

# coverting data types
columns_to_convert = ['job_titles', 'employer', 'Country' , 'Region' ,'Job_Type' , 'job link']

new_DF[columns_to_convert] = new_DF[columns_to_convert].astype(pd.StringDtype())
#new_DF['Region'] = new_DF['Region'].astype(pd.StringDtype())
new_DF['Creation date'] = pd.to_datetime(new_DF['Creation date'])
new_DF.info() # prints schema
#print(new_DF)


# Transformation on extracted data


# Split the "Country" column based on ':' and expand into two columns
new_DF[['CountryName', 'Region']] = new_DF['Country'].str.split(':', expand=True)

# Drop the original "Country" column from the new DataFrame
new_DF.drop('Country', axis=1, inplace=True)

# Flatten Region column
new_DF = new_DF.assign(Region=new_DF['Region'].str.split(', ')).explode('Region')

# indexing based of columns job_titles, region
new_DF['Index'] = new_DF.groupby(['Region', 'job_titles']).cumcount() + 1
new_DF.index.name = 'JobId'
new_DF.drop('Index', axis=1, inplace=True)

#new_DF['job link'] = new_DF['job link'].str[0]
#new_DF['job link'] = new_DF['job link'].str.join(', ')
new_DF['job link'] = new_DF['job link'].str.extract(r"'([^']*)'")

new_DF['Region'] = new_DF['Region'].str.strip()

# Print the new DataFrame
#print(new_DF)
#new_DF.to_csv("Country.csv", index=True)
#new_DF.to_csv("Country.csv")
#new_DF.info()

# Analysing

df_totalJobs = new_DF[['job_titles','Creation date' ,'Region']]
df_totalJobs = df_totalJobs.groupby('Region').size().reset_index(name='count')

#df_totalJobs = df_totalJobs.groupby(['Region', 'job_titles']).size().reset_index(name='count')

# Sort the data frame by "Creation date"
#df_totalJobs = df_totalJobs.sort_values('Creation date')

print(df_totalJobs)
df_totalJobs.info()
df_totalJobs.to_csv("Sorted.csv")



