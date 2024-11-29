import streamlit as st
import mysql.connector
from click import password_option
from streamlit import button

mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='project'

)
def add_customer(name, phno, password, balance):
    a=mydb.cursor()
    query='insert into customer(cname,phno,password,balance) values(%s,%s,%s,%s)'
    a.execute(query,(name,phno,password,balance))
    mydb.commit()

    a.execute('select cid,cname,phno,password,balance from customer where phno=%s',(phno,))
    b=a.fetchall()
    st.success(f'customer_id={b[0][0]} \n'
               f'customer_name={b[0][1]}\n'
               f'customer_phno={b[0][2]}\n'
               f'customer_password={b[0][3]}\n'
               f'customer_balance={b[0][4]}\n')
    st.success('CUSTOMER ADDED SUCCESSFULLY')




st.header('WELCOME TO THE ABCD BANK')
menu=['ADD THE CUSTOMER','WITHDRAW THE MONEY','DEPOSIT','VIEW BALANCE','PASSWORD CHANGE']
option=st.selectbox('option',menu)
if option=='ADD THE CUSTOMER':
    name = st.text_input('NAME')
    phno = st.number_input('PHNO', min_value=0)
    password = st.text_input('PASSWORD',type='password')
    balance = st.number_input('BALANCE', min_value=1000)
    button = st.button('CREATE')
    if button:
        add_customer(name, phno, password, balance)

elif option=='WITHDRAW THE MONEY':
    cid=st.number_input('CID',min_value=0,format='%d')
    password=st.text_input('PASSWORD',type='password')
    amount=st.number_input('AMOUNT',min_value=0,format='%d')
    if st.button('WITHDRAW'):
        a=mydb.cursor()
        a.execute('select cid,password,balance from customer where cid=%s',(cid,))
        b=a.fetchall()
        if password==b[0][1] and cid == b[0][0]:
            if amount<=b[0][2]:
                s=mydb.cursor()
                s.execute(f'update customer set balance=balance-{amount} where cid={cid}')
                mydb.commit()
                st.success('withdraw successfully')
            else:
                st.error('insufficient balance')
elif option=='DEPOSIT':
    cid=st.number_input('CID',min_value=0)
    password=st.text_input('PASSWORD',type='password')
    amount=st.number_input('AMOUNT',min_value=0,format='%d')
    if st.button('DEPOSIT'):
        a=mydb.cursor()
        a.execute('select cid,password from customer where cid=%s',(cid,))
        b=a.fetchall()
        if password==b[0][1] and cid==b[0][0]:
            a.execute(f'update customer set balance=balance+{amount} where cid={cid}')
            mydb.commit()
            st.success(f'{amount}deposit successfully')
        else:
            st.success(f'{amount}not deposited')
elif option=='VIEW BALANCE':
    cid=st.number_input('CID',min_value=0)
    password=st.text_input('PASSWORD',type='password')
    if st.button('VIEW'):
        a = mydb.cursor()
        a.execute('select cid,password,balance from customer where cid=%s', (cid,))
        b = a.fetchall()
        if password == b[0][1] and cid == b[0][0]:
            st.success(f'{ b[0][2]} ')
        else:
            print('invalid data')

elif option=='PASSWORD CHANGE':
    cid=st.number_input('CID',min_value=0)
    password=st.text_input(' OLD PASSWORD',type='password')
    new_password = st.text_input('NEW PASSWORD', type='password')
    if st.button('VIEW'):
        a = mydb.cursor()
        a.execute('select cid,password,balance from customer where cid=%s', (cid,))
        b = a.fetchall()
        if password == b[0][1] and cid == b[0][0]:
            a.execute(f'update customer set password={new_password} where cid={cid}')
            mydb.commit()
            st.success('successfully CHANGED')
        else:
            print('invalid data')

