import os

def ask(q):
  os.system('clear')
  print(q)
  print('--------------------')
  a = input(' ')
  print('--------------------')
  return(a)

ask('test')
