import threading
from threading import Thread, Semaphore, Lock
from time import sleep
import sys

controle = 0
caldeirao = []
mutex = Semaphore(1)
finaliza = 0
lock1 = Lock()
lock2 = Lock()
lock3 = Lock()


def canibal():
   global controle
   global caldeirao
   global finaliza
   nomeThread = threading.currentThread().getName()
   contador = 0

   while True:
      if controle == 0:
         if finaliza == 1:
            sleep(4)
            print('{} comeu {} pedacos...'.format(nomeThread, contador))
            sys.exit()
         elif len(caldeirao) == 0:
            controle = 1
         else:
            mutex.acquire()
            print('{} se servindo... '.format(nomeThread))
            caldeirao.pop()
            contador += 1
            sleep(1)
            mutex.release()
            print('{} comendo...'.format(nomeThread))
            sleep(3)
      if controle == 1:
          if nomeThread == 'canibal 1':
              print('{} dormindo...'.format(nomeThread))
              lock1.acquire()
          if nomeThread == 'canibal 2':
              print('{} dormindo...'.format(nomeThread))
              lock2.acquire()
          if nomeThread == 'canibal 3':
              print('{} dormindo...'.format(nomeThread))
              lock3.acquire()

def cozinheiro():
   global controle
   global caldeirao
   global finaliza
   global dormeCanibal
   contador = 0
   dorme = 0
   while True:
      mutex.acquire()
      if finaliza == 1:
         sleep(2)
         print('\ncozinheiro encheu o caldeirao {} vezes...'.format(contador))
         sys.exit()
      if controle == 1:
         print('cozinheiro preparando...')
         sleep(5)
         for i in range(5):
            caldeirao.append(i)
         controle = 0
         dorme = 0
         contador += 1
         lock1.release()
         lock2.release()
         lock3.release()
      if dorme == 0:
         print('cozinheiro dormindo...')
         dorme = 1
      mutex.release()

def finalizar():
   global finaliza
   sleep(120)
   finaliza = 1

controlador = Thread(target=finalizar)
canibal1 = Thread(target=canibal, name='canibal 1')
canibal2 = Thread(target=canibal, name='canibal 2')
canibal3 = Thread(target=canibal, name='canibal 3')
cozinheiro = Thread(target=cozinheiro, name='cozinheiro')
print('====== PROBLEMA DO JANTAR DOS CANIBAIS ======')
print('Obs: Duracao do programa e de 120s \n')
sleep(1)
canibal1.start()
canibal2.start()
canibal3.start()
cozinheiro.start()
controlador.start()

