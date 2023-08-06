from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *

from gsheetsdb import connect

conn = connect()
result = conn.execute('SELECT * FROM "https://docs.google.com/spreadsheets/d/1_rN3lm0R_bU3NemO0s9pbFkY5LQPcuy1pscv8ZXPtg8/edit?usp=sharing" LIMIT 0')
print(list(result))
print(result.description)

result = conn.execute('SELECT * FROM "https://docs.google.com/spreadsheets/d/1_rN3lm0R_bU3NemO0s9pbFkY5LQPcuy1pscv8ZXPtg8/edit?headers=1#gid=0"')
for row in result:
    print(row)

result = conn.execute('SELECT * FROM "https://docs.google.com/spreadsheets/d/1_rN3lm0R_bU3NemO0s9pbFkY5LQPcuy1pscv8ZXPtg8/edit?headers=2#gid=1077884006"')
for row in result:
    print(row)

result = conn.execute('SELECT * FROM "https://docs.google.com/spreadsheets/d/1_rN3lm0R_bU3NemO0s9pbFkY5LQPcuy1pscv8ZXPtg8/edit?headers=2&gid=1077884006"')
for row in result:
    print(row)


engine = create_engine('gsheets://docs.google.com/spreadsheets/d/1AAqVVSpGeyRZyrr4n--fb_IxhLwwKtLbjfu4h6MyyYA/edit#gid=0') 

