import os
import glob
import pandas as pd
from pathlib import Path
import csv

repo_path = Path(os.getcwd()).parent

data_folder_path = repo_path / 'data'

os.chdir(data_folder_path)

extension = 'csv'

all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

print(all_filenames)
data_list = []

for file in all_filenames:
    with open(file, encoding='utf-8', errors='replace', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        for lines in reader:
            data_list.append(lines)

data = pd.DataFrame(data_list)
data.to_csv('cover_letters.csv', index=False, encoding = 'utf-8-sig', header=['text'])
