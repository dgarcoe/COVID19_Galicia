import os
from datetime import date

os.system('python3 ./update_data.py')
os.system('python3 ./update_graphs.py')

print('Pushing data to repo')
os.system('git commit -a -m "Uploaded data '+str(date.today())+'"')
os.system('git push')
