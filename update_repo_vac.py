import os
from datetime import date

os.system('python3 ./update_data_vac.py')
os.system('python3 ./update_graphs_vac.py')

print('Pushing data to repo')
os.system('git commit -a -m "Uploaded vaccination data '+str(date.today())+'"')
os.system('git push')
