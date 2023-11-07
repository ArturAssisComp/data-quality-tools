import os
import subprocess
from dbfread import DBF
import csv

dbf2csv_path = os.path.join(__file__, 'dbf2csv.exe')

output_path = str(input('Enter the path for csv outputs:')).replace('\\', '/')
if not output_path:
    output_path = './csv'
for dirpath, _, filenames in os.walk('.'):
    for filename in filenames:
        print(f'Processing {filename}')
        current_filename = os.path.join(dirpath, filename)
        extension = os.path.basename(current_filename).split('.')[-1].lower()
        if extension == 'dbc':
            dbf_filepath = current_filename.replace('.dbc', '.dbf')
            subprocess.Popen([os.path.join(dbf2csv_path), current_filename, dbf_filepath])
        elif extension == 'dbf':
            dbf_filepath = current_filename
        else:
            continue

        table=DBF(dbf_filepath, encoding='iso.8859.1')
        csv_filepath = output_path + '/' +  os.path.basename(dbf_filepath).replace('.dbf', '.csv')
        with open(csv_filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(table.field_names)
            for record in table:
                writer.writerow(list(record.values()))
