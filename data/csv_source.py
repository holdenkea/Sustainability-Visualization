import pandas as pd
import os

# path to file's directory
current_dir = os.path.dirname(__file__)

# building full path to csv
csv_path = os.path.join(current_dir, 'normalized_data4.csv')

# load csv
df = pd.read_csv(csv_path)

# change this to a dash callback later to update the data from the database (maybe)