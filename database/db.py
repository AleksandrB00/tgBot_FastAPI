from models import *

db.bind(provider='postgres', user='postgres', password='postgres', host='localhost', database='postgres')
db.generate_mapping(create_tables=True)
