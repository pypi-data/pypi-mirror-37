#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright 2018 QIWIAPI
# Written by: * StiNeR 1776 
# https://github.com/stoner1776/QIWIAPI/


# This script is designed for fast and anonymous transactions.
# For full-fledged anonymous use of this script  you need to - 
# Connect to the  network TOR,  as  well as a  white  account.
# All rights reserved. THE MIT LICENSE.

from QIWIAPI import * 
from time import sleep
log ='''
    ____ _ __    __ _             _
   /___ (_) / /\ \ (_) __ _ _ __ (_)
  //  / / \ \/  \/ / |/ _` | '_ \| |      
 / \_/ /| |\  /\  /| | (_| | |_) | |    
 \___,_\|_| \/  \/ |_|\__,_| .__/|_|          
===========================|_|=======    
[version: 5.0] /..Fast translations 
                     and anonymity../
'''
print(log)
def user_info():
  global token,api
  token=input('Enter token: ') 
  api = QApi(token=token, phone="") 
  try: 
    print('Balance:',api.balance) 
  except:
    print('Error check!')
    return user_info()
user_info()
acc=input('Phone: +')
com=input('Comment: ') 
t=input('Mod id? ')
if t == 'y':
  print (api.full_balance)
  id = input('Id: ')
else:
    id='643'
def pay_info():
  try:
    api.pay(account=acc, amount=input('Pay: '), comment=com, acc_id=id, currency='643') 
  except:
    print('Error pay!')
    return pay_info()
pay_info()
print(api.balance)
print('Successfull!')
def user_exit():
	try:
		enter=input('Please press [Enter] to exit ')
		log2 ='''
    ______       _  __    ___ _______________
   / __/ /____  / |/ /__ / _ <  /_  /_  / __/
  _\ \/ __/ _ \/    / -_) , _/ / / / / / _ \ 
 /___/\__/\___/_/|_/\__/_/|_/_/ /_/ /_/\___/ 
==============www.stoner1776.pro=============
'''
		print(log2)
	except:
		print('Error')
		return user_exit()
user_exit()
