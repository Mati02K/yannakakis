import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from yannakakis.db import Database
from yannakakis.yannakakis import Yannakakis
from yannakakis.jobdataset.JobQuery1A import JobQuery1A
import numpy as np

# Read the CSV files
# movie_info_idx = pd.read_csv('imdb dataset/movie_info_idx.csv')
# info_type = pd.read_csv('imdb dataset/info_type.csv')


# Connect to the database and load the job dataset params
db = Database()
job = JobQuery1A()

# Load tables from the database
tables = {
    table_name: db.fetch_table_from_db(table_name, columns, db.connection)
    for table_name, columns in job.columns.items()
}

#  {'left': 'title', 'right': 'movie_info_idx', 'left_key': 'id', 'right_key': 'movie_id'}

movie_companies = tables['movie_companies']
title = tables['title']

movie_id = []
for i in movie_companies:
    movie_id.append(i['movie_id'])

id = []
for i in title:
    id.append(i['id'])

# if 112 in movie_id:
#     print("Yes it is present")

# company_type_id = [1, 2]
# frequency = [5, 17811]
job = ['1A', '5B', '5C']
python = [1.263460, 7.656614, 5.559874]
postgre = [0.280, 4.126, 0.836]

plt.figure(figsize=(10, 6))
sns.barplot(x = job, y = postgre, color='red')
#sns.histplot(movie_id)
#sns.histplot(movie_id, shrink=0.9, bins=np.arange(min(movie_id) - 0.5, max(movie_id) + 1.5, 1))
# Set the x-axis ticks and labels
# plt.xticks(np.arange(min(movie_id), max(movie_id)+1, 1))
# plt.ylim(0, 5000)  # Set specific y-axis range
# plt.xlim(0, 115)
plt.title('POSTGRESQL Implementation (Time performance)')
plt.xlabel('Job Queries')
plt.ylabel('Time (in seconds)')

plt.tight_layout()
plt.show()



# Plot scatter plot for info_type_id and id directly
# plt.figure(figsize=(10, 6))
# sns.scatterplot(x=info_type_id, y=id)
# plt.title('Scatter Plot of info_type_id vs id')
# plt.xlabel('info_type_id from movie_info_idx')
# plt.ylabel('id from info_type')
# plt.show()

# Create a correlation matrix with both columns
# data = pd.DataFrame({'info_type_id': movie_info_idx['info_type_id'], 'id': info_type['id']})
# correlation_matrix = data.corr()

# # Plot heatmap
# plt.figure(figsize=(8, 6))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
# plt.title('Correlation Heatmap')
# plt.show()



'''
        self.join_tree = [
        {"left": "company_type", "right": "movie_companies", "left_key": "id", "right_key": "company_type_id"},
        {"left": "movie_companies", "right": "title", "left_key": "movie_id", "right_key": "id"},
        {"left": "title", "right": "movie_info_idx", "left_key": "id", "right_key": "movie_id"},
        {"left": "movie_companies", "right": "movie_info_idx", "left_key": "movie_id", "right_key": "movie_id"},
        {"left": "movie_info_idx", "right": "info_type", "left_key": "info_type_id", "right_key": "id"}
        ]
'''