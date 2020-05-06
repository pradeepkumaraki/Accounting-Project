import PySimpleGUI as sg  
import sqlite3
from sqlite3 import Error
from beautifultable import BeautifulTable

#l = ['1','2','3']

def get_credit_transactions():
	con = sql_connect()
	cur = con.cursor()
	cur.execute("SELECT Name,Balance,Description,Transact FROM Credits WHERE Balance>0")
	rows = cur.fetchall()
	credits = {}
	for row in rows:
		row = list(map(str,row))
		key = " ".join(row[:-1])
		credits[key] = row[-1]
	con.close()
	return credits

def get_transaction_id():
	import string
	import random
	x = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
	return x

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def show_credits(conn,start_date,end_date):
	cur = conn.cursor()
	if(start_date != '' and end_date !=''):
		sql_query = "SELECT * FROM Credits WHERE date(Date)>='{}' AND date(Date)<='{}'".format(start_date,end_date)
	else:
		sql_query = "SELECT * FROM Credits"
	print(sql_query)
	cur.execute(sql_query)
	rows = cur.fetchall()
	table = BeautifulTable()
	table.column_headers = ["Creditor_Name", "Credited_Amount", "Available_Balance","Purpose","Person_Authorized","Date","Transaction_Id"]
	for row in rows:
		row = list(map(str,row))
		table.append_row(row)
	sg.Print(table)
		#sg.PopupScrolled(row)

def show_debits(conn,start_date,end_date):
	cur = conn.cursor()
	if(start_date != '' and end_date !=''):
		sql_query = "SELECT * FROM Debits WHERE date(Date)>='{}' AND date(Date)<='{}'".format(start_date,end_date)
	else:
		sql_query = "SELECT * FROM Debits"
	cur.execute(sql_query)
	rows = cur.fetchall()
	table = BeautifulTable()
	table.column_headers = ["Debitor_Name", "Debited_Amount","Purpose","Person_Authorized","Date","Credit_Id","Transaction_Id"]
	for row in rows:
		row = list(map(str,row))
		table.append_row(row)
	sg.Print(table)
		#sg.PopupScrolled(row)

def show_all_transactions(conn,start_date,end_date):
	cur = conn.cursor()
	if(start_date != '' and end_date !=''):
		sql_query = "SELECT * FROM Credits WHERE date(Date)>='{}' AND date(Date)<='{}'".format(start_date,end_date)
	else:
		sql_query = "SELECT * FROM Credits"
	#print(sql_query)
	cur.execute(sql_query)
	credit_rows = cur.fetchall()
	if(start_date != '' and end_date !=''):
		sql_query = "SELECT * FROM Debits WHERE date(Date)>='{}' AND date(Date)<='{}'".format(start_date,end_date)
	else:
		sql_query = "SELECT * FROM Debits"
	cur.execute(sql_query)
	debit_rows = cur.fetchall()
	table = BeautifulTable()
	temp_list=[]
	#print(credit_rows)
	#print(debit_rows)
	table.column_headers = ["Transaction_Type", "Name","Credited_Amount","Available_Balance","Debited Amount","Purpose","Person_Authorized","Date","Credit_Id","Transaction_Id"]
	for row in credit_rows:
		row = list(map(str,row))
		temp = ["Credit"]
		temp.extend(row[:3])
		temp.extend([" "])
		temp.extend(row[3:])
		temp.extend([" "])
		temp_list.append(tuple([row[5],temp]))
		#print(temp_list)

	for row in debit_rows:
		row = list(map(str,row))
		temp = ["Debit"]
		temp.extend([row[0]])
		temp.extend([" "," "])
		temp.extend(row[1:])
		temp_list.append(tuple([row[4],temp]))
		print(temp_list)
#"""
	temp_list.sort()
	for i in range(len(temp_list)):
		table.append_row(temp_list[i][1])
	sg.Print(table)
#"""
def credit_transaction(conn, values):
	sql_query = "INSERT INTO Credits (Name, Amount, Balance, Description, Certified_name,Date,Transact) VALUES ('{}','{}','{}','{}','{}','{}','{}');".format(values['creditor_name'],values['credit_amount'],values['credit_amount'],values['credit_purpose'],values['credit_authority'],values['credit_date'],values['credit_id'])
	#print("sql_query\n",sql_query)
	conn.execute(sql_query)
	conn.commit()

def debit_transaction(conn, values):
	sql_query = "INSERT INTO Debits (Name,Amount,Description,Certified_name,Date,Credit_Transact,Debit_Transact) VALUES ('{}','{}','{}','{}','{}','{}','{}');".format(values['debit_name'],values['debit_amount'],values['debit_purpose'],values['debit_authority'],values['debit_date'],values['debit_creditid'],values['debit_id'])
	#print(sql_query)
	conn.execute(sql_query)
	credit_sql_query = "UPDATE Credits SET Balance = Balance - {} WHERE Transact= '{}'".format(values['debit_amount'],values['debit_creditid'])
	print(credit_sql_query)
	conn.execute(credit_sql_query)
	conn.commit()


 
def sql_connect():
    database = "/home/aki/accounting_project/sample.db"

    # create a database connection
    conn = create_connection(database)

    conn.execute('''CREATE TABLE IF NOT EXISTS Credits 
            (Name STRING(50) NOT NULL, 
             Amount DECIMAL NOT NULL,
             Balance DECIMAL NOT NULL,
            Description STRING(50) NOT NULL,
            Certified_name STRING(50) NOT NULL,
            Date DATETIME NOT NULL, 
            Transact STRING(50) PRIMARY KEY NOT NULL)''')


    conn.execute('''CREATE TABLE IF NOT EXISTS Debits 
            (Name STRING(50) NOT NULL,
             Amount DECIMAL NOT NULL, 
            Description STRING(50) NOT NULL,
            Certified_name STRING(50) NOT NULL,
            Date DATE NOT NULL,
            Credit_Transact STRING(50)	 NOT NULL, 
            Debit_Transact STRING(50) PRIMARY KEY NOT NULL,
            FOREIGN KEY (Credit_Transact) REFERENCES Credits (Transact) 
  ON UPDATE CASCADE
  ON DELETE CASCADE)''')

    conn.execute('''CREATE TABLE IF NOT EXISTS logs 
            (Name STRING(50) NOT NULL,
             Amount DECIMAL NOT NULL, 
            Description STRING(50) NOT NULL,
            Certified_name STRING(50) NOT NULL,
            Date DATETIME NOT NULL, 
            Transact INTEGER  NOT NULL,
            Action STRING(50) NOT NULL)''')

    return conn

tab1_layout = [[sg.Text('Accounting - Ledger', size=(30, 1), font=("Helvetica", 25), text_color='blue')],      
   [sg.Text('Creditors Name')],      
   [sg.InputText(key='creditor_name')],  
   [sg.Text('Amount being Credited')],
   [sg.InputText(key = 'credit_amount')],
   [sg.Text('Purpose of giving amount')],
   [sg.InputText(key = 'credit_purpose')],
   [sg.Text('Person authorising the Credit amount')],
   [sg.InputText(default_text="Chandra Shekar", key='credit_authority')],
   [sg.Text('Date')],
   [sg.InputText(key='credit_date'),sg.CalendarButton(button_text="calendar", target = "credit_date")],
   [sg.Button('Credit', button_color=('white', 'green')),sg.Button('Exit')]]

credits = get_credit_transactions()
creds = list(credits.keys())
#print("creds",creds)

tab2_layout = [[sg.Text('Accounting - Ledger', size=(30, 1), font=("Helvetica", 25), text_color='blue')],      
   [sg.Text("Debitor's Name")],      
   [sg.InputText(key='debit_name')],  
   [sg.Text('Amount being Debited')],
   [sg.InputText(key = 'debit_amount')],
   [sg.Text('Purpose of giving amount')],
   [sg.InputText(key = 'debit_purpose')],
   [sg.Text('Person authorising the debit amount')],
   [sg.InputText(default_text="Chandra Shekar", key='debit_authority')],
   [sg.Text('Date')],
   [sg.InputText(key='debit_date'),sg.CalendarButton(button_text="calendar", target = "debit_date")],
   [sg.Text('Select transaction where to debit from')],
   [sg.Listbox(values=creds, key="debit_creditid", size=(40,8))],
   #[sg.Listbox(values=l, key="debit_creditid", size=(30, 6))],
   [sg.Button('Debit',button_color=('white', 'green')),sg.Button('Exit')]]

tab3_layout = [[sg.Text('Accounting - Ledger', size=(30, 1), font=("Helvetica", 25), text_color='blue')],           
   [sg.InputText(key='start_date'),sg.CalendarButton(button_text="Start Date", target = "start_date")],
   [sg.InputText(key='end_date'),sg.CalendarButton(button_text="End Date", target = "end_date")],
   [sg.Button('Show Credits', button_color=('white', 'green')),sg.Button('Show Debits', button_color=('white', 'green')),sg.Button('Show All', button_color=('white', 'green')),sg.Button('Exit')]]

tab4_layout = []

layout = [[sg.TabGroup([[sg.Tab('Credit', tab1_layout), sg.Tab('Debit', tab2_layout),sg.Tab('Report', tab3_layout),sg.Tab('Summary', tab4_layout)]])]] 

#event, values  = sg.Window('Everything bagel', auto_size_text=True, default_element_size=(40, 1)).Layout(layout).Read()   

window = sg.Window('Accounting System', auto_size_text=True, default_element_size=(40, 1)).Layout(layout)  

while True:                 # Event Loop  
  event, values = window.Read()  
  print(event, values)
  con = sql_connect()
  if event is None or event == 'Exit':
  	break  
  if event == 'Credit':
  	credit_values = {}
  	credit_values['creditor_name'] = values['creditor_name']
  	credit_values['credit_date'] = values['credit_date'].split(" ")[0]
  	credit_values['credit_authority'] = values['credit_authority']
  	credit_values['credit_purpose'] = values['credit_purpose']
  	credit_values['credit_amount'] = values['credit_amount']
  	credit_values['credit_id'] = get_transaction_id()
  	try:
  		credit_transaction(con, credit_values)
  	except Exception as e:
  		print(e)
  if event == 'Debit':
  	debit_values = {}
  	debit_values['debit_name'] = values['debit_name']
  	debit_values['debit_date'] = values['debit_date'].split(" ")[0]
  	debit_values['debit_authority'] = values['debit_authority']
  	debit_values['debit_purpose'] = values['debit_purpose']
  	debit_values['debit_amount'] = values['debit_amount']
  	debit_values['debit_id'] = get_transaction_id()
  	#credits = get_credit_transactions()
  	#print(credits)
  	#print(values['debit_creditid']	)
  	debit_values['debit_creditid']  = credits[values['debit_creditid'][0]]
  	try:
  		debit_transaction(con, debit_values)
  	except Exception as e:
  		print(e)

  if event == "Show Credits":
  	start_date = values["start_date"].split(" ")[0]
  	end_date = values["end_date"].split(" ")[0]
  	show_credits(con,start_date,end_date)

  if event == "Show Debits":
  	start_date = values["start_date"].split(" ")[0]
  	end_date = values["end_date"].split(" ")[0]
  	show_debits(con,start_date,end_date)
  if(event=="Show All"):
  	start_date = values["start_date"].split(" ")[0]
  	end_date = values["end_date"].split(" ")[0]
  	show_all_transactions(con,start_date,end_date)

    
con.close()
window.Close()
#print(event, values) 

#"""
