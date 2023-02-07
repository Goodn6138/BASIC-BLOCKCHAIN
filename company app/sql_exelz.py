import numpy as np
import pandas as pd
import hashlib
import sqlite3

conn =sqlite3.connect(':memory:')

path = r'C:\Users\user\Downloads\SOROJAPA 10 06 2022.xlsx'
df = pd.read_excel(path)
df.to_sql(name = 'poop' , con = conn)
