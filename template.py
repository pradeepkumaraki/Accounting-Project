import PySimpleGUI as sg      
from beautifultable import BeautifulTable

table = BeautifulTable()
table.column_headers = ["Creditor_Name", "Credited_Amount", "Available_Balance","Purpose","Person_Authorized","Date","Transaction_Id"]

tab2_layout = [sg.PopupYesNo('PopupYesNo')]	

event, values  = sg.Window('Everything bagel', auto_size_text=True, default_element_size=(40, 1)).Layout(tab2_layout).Read()   

print(event, values) 