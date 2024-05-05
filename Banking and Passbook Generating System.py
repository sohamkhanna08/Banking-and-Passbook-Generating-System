import mysql.connector
from datetime import date
from tabulate import tabulate

def account_status(acno):
  conn = mysql.connector.connect(host='localhost', database='bankproject', user='root', password='1234')
  cursor = conn.cursor()
  sql ="select status,balance from customer where acno ='{}';".format(acno)
  result = cursor.execute(sql)
  result = cursor.fetchone()
  conn.commit()
  conn.close()
  return result

def deposit_amount():
    conn = mysql.connector.connect(host='localhost', database='bankproject', user='root', password='1234')
    cursor = conn.cursor()
    clear()
    acno = input('Enter account No : ')
    amount = input('Enter amount : ')
    today = date.today()
    result = account_status(acno)
    if result[0]== 'active':
      sql1 ="update customer set balance = balance+{} where acno = '{}' and status='active';".format(amount,acno)
      sql2 ="insert into transaction (amount,type,acno,dot) values('{}','Deposit','{}','{}');".format(amount,acno,str(today))
      cursor.execute(sql2)
      cursor.execute(sql1)
      conn.commit()
      print('\n\nAmount Deposited')
    else:
      print('\nClosed or Suspended Account.... ')
    wait= input('\n\nPress any key to continue.... ')
    conn.close()

def withdraw_amount():
    conn = mysql.connector.connect(host='localhost', database='bankproject', user='root', password='1234')
    cursor = conn.cursor()
    clear()
    acno = input('Enter account No : ')
    amount = input('Enter amount : ')
    today = date.today()
    result = account_status(acno)
    if result[0] == 'active' and int(result[1])>=int(amount):
      sql1 = "update customer set balance = balance-'{}' where acno = '{}' and status='active';".format(amount,acno)
      sql2 = "insert into transaction(amount,type,acno,dot) values('{}','withdraw','{}','{}');".format(amount,acno,str(today))
      cursor.execute(sql2)
      cursor.execute(sql1)
      conn.commit()
      print('\n\nAmount Withdrawn')
    else:
      print('\n\nClosed or Suspended Account Or Insufficient amount')
    wait = input('\n\n\n Press any key to continue....')
    conn.close()

def transaction_menu():
    while True:
      clear()
      print('Transaction Menu :-')
      print("\n1. Deposit Amount")
      print('\n2. WithDraw Amount')
      print('\n3. Back to Main Menu')
      print('\n\n')
      choice = int(input('Enter your choice : '))
      if choice == 1:
        deposit_amount()
      if choice == 2:
        withdraw_amount()
      if choice == 3:
        break

def search_menu():
    conn = mysql.connector.connect(host='localhost', database='bankproject', user='root', password='1234')
    cursor = conn.cursor()
    while True:
      clear()
      print('Search Menu :-')
      print("\n1. Account No")
      print('\n2. Aadhar Card')
      print('\n3. Phone No')
      print('\n4. Email')
      print('\n5. Name')
      print('\n6. Back to Main Menu')
      choice = int(input('\n\nEnter your choice : '))
      field_name=''
      if choice == 1:
        field_name ='acno'
      if choice == 2:
        field_name ='aadhar_no'
      if choice == 3:
        field_name = 'phone'
      if choice == 4:
        field_name = 'email'
      if choice == 5:
        field_name = 'name'
      if choice == 6:
        break
      msg ="Enter {} : ".format(field_name)
      value = input(msg)
      if field_name=='acno':
        sql = "select * from customer where {} ={} ;".format(field_name,value)
      else:
        sql = "select * from customer where {} like '{}%';".format(field_name,value)
      cursor.execute(sql)
      records = cursor.fetchall()
      n=len(records)
      clear()
      print('Search Result for',field_name,value,':-')
      print('-'*120)
      print(tabulate(records,headers=['Acc No','Name','Address','Phone','Email','Aadhar No','Acc Type','Status','Balance'], tablefmt = 'psql'))
      if(n<=0):
        print('\n')
        print(field_name, value,'does not exist')
      wait = input('\n\n\nPress any key to continue....')
    conn.commit()
    conn.close()
    wait=input('\n\n\nPress any key to continue....')
   
def daily_report():
   clear()   
   conn = mysql.connector.connect(host='localhost', database='bankproject', user='root', password='1234')
   today = date.today()
   cursor = conn.cursor()
   sql = "select * from transaction where dot='{}';".format(str(today))
   cursor.execute(sql)
   records = cursor.fetchall()
   clear()
   print('Daily Report :',today)
   print('-'*120)
   print(tabulate(records,headers=['Tid','Date of Transaction','Amount','Type','Acc No'],tablefmt='psql'))
   conn.close()
   wait = input('\n\n\nPress any key to continue....')

def monthly_report():
   clear()
   conn = mysql.connector.connect(host='localhost', database='bankproject', user='root', password='1234')
   today = date.today()
   cursor = conn.cursor()
   sql = 'select tid,dot,amount,type,acno from transaction t where month(dot)="' + \
       str(today).split('-')[1]+'";'
   cursor.execute(sql)
   records = cursor.fetchall()
   clear()
   print('Monthly Report :', str(today).split('-')[1], '-', str(today).split('-')[0])
   print('-'*120)
   print(tabulate(records,headers=['Tid','Date of Transaction','Amount','Type','Acc No'],tablefmt='psql'))
   conn.close()
   wait = input('\n\n\n Press any key to continue....')

def account_details():
    clear()
    acno = input('Enter account no :')
    conn = mysql.connector.connect(host='localhost', database='bankproject', user='root', password='1234')
    cursor = conn.cursor()
    sql ="select * from customer where acno ='{}';".format(acno)
    sql1 = "select tid,dot,amount,type from transaction t where t.acno='{}';".format(acno)
    cursor.execute(sql)
    result = cursor.fetchone()
    clear()
    print('Account Details :-')
    print('-'*100)
    print('Account No :',result[0])
    print('Customer Name :',result[1])
    print('Address :',result[2])
    print('Phone NO :',result[3])
    print('Email ID :',result[4])
    print('Aadhar No :',result[5])
    print('Account Type :',result[6])
    print('Account Status :',result[7])
    print('Current Balance :',result[8])
    print('-'*100)
    cursor.execute(sql1)
    results = cursor.fetchall()
    for result in results:
        print(result[0], result[1], result[2], result[3])
    conn.commit()
    conn.close()
    wait=input('\n\n\nPress any key to continue.....')

def report_menu():
    while True:
      clear()
      print('Report Menu :-')
      print("\n1.  Daily Report")
      print('\n2.  Monthly Report')
      print('\n3.  Back to Main Menu')
      choice = int(input('\n\nEnter your choice : '))
      if choice == 1:
        daily_report()
      if choice == 2:
        monthly_report()
      if choice == 3:
        break

def add_account():
    conn = mysql.connector.connect(host='localhost', database='bankproject', user='root', password='1234')
    cursor = conn.cursor()
    acno = input('Enter account number :')
    name = input('Enter Name :')
    addr = input('Enter address ')
    phone = input('Enter Phone no :')
    email = input('Enter Email :')
    aadhar = input('Enter AAdhar no :')
    actype = input('Account Type (saving/current ) :')
    balance = input('Enter opening balance :')
    status = input('Enter Status :')
    sql = "insert into customer values ({} , '{}' , '{}' , {} , '{}' , {} , '{}' , '{}' , {});".format(acno,name,addr,phone,email,aadhar,actype,status,balance)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    print('New customer added successfully')

def modify_account():
    conn = mysql.connector.connect(host='localhost', database='bankproject', user='root', password='1234')
    cursor = conn.cursor()
    acno = input('Enter customer Account No :')
    print('\n\nModify screen :-')
    print('\n 1.  Customer Name')
    print('\n 2.  Customer Address')
    print('\n 3.  Customer Phone No')
    print('\n 4.  Customer Email ID')
    choice = int(input('\n\nWhat do you want to change ? '))
    new_data = input('Enter New value :')
    field_name=''
    if choice == 1:
       field_name = 'name'
    if choice == 2:
       field_name = 'address'
    if choice == 3:
       field_name = 'phone'
    if choice == 4:
       field_name = 'email'
    sql ="update customer set {} = '{}' where acno={};".format(field_name,new_data,acno) 
    cursor.execute(sql)
    conn.commit()
    print('Customer Information modified..')

def close_account():
    conn = mysql.connector.connect(host='localhost', database='bankproject', user='root', password='1234')
    cursor = conn.cursor()
    acno = input('Enter customer Account No :')
    sql ="update customer set status='close' where acno ='{}';".format(acno)
    cursor.execute(sql)
    conn.commit()
    print('Account closed')

def clear():
  for _ in range(55):
     print()

def main_menu():
    while True:
      clear()
      print('Main Menu :-')
      print("\n1. Add Account")
      print('\n2. Modify Account')
      print('\n3. Close Account')
      print('\n4. Transaction Menu')
      print('\n5. Search Menu')
      print('\n6. Report Menu')
      print('\n7. Account Details')
      print('\n8. Close application')
      print('\n\n')
      choice = int(input('Enter your choice : '))
      if choice == 1:
        add_account()
      if choice == 2:
        modify_account()
      if choice == 3:
        close_account()
      if choice == 4:
        transaction_menu()
      if choice == 5:
        search_menu()
      if choice == 6:
        report_menu()
      if choice == 7:
        account_details()  
      if choice == 8:
        break

main_menu()
