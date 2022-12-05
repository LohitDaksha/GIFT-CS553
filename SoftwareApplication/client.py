import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import copy


sbox = {0:1, 1:10, 2:4, 3:12, 4:6, 5:15, 6:3, 7:9, 8:2, 9:13, 10:11, 11:7, 12:5, 13:0, 14:8, 15:14}

def SubCells(state):
  state_ = ['0' for i in range(64)]
  for i in range(0,64,4):
    inter = state[i+3] + state[i+2] + state[i+1] + state[i]
    sin = eval('0b' + ''.join(inter))
    sout = sbox[sin]
    out = list('0' * (4 - len(bin(sout)[2:])) + bin(sout)[2:])
    state_[i], state_[i+1], state_[i+2], state_[i+3] = out[3], out[2], out[1], out[0]
  return copy.deepcopy(state_)

def PermBits(state):
  state_ = ['0' for i in range(64)]
  for i in range(64):
    pos = 4 * (i // 16) + 16 * ((3 * ((i % 16) // 4) + (i % 4)) % 4) + (i % 4)
    state_[pos] = state[i]
  return copy.deepcopy(state_)

def RC_LFSR(lfsr):
  lfsr_ = ['0' for i in range(6)]
  lfsr_[1:6] = lfsr[:5]
  lfsr_[0] =  bin(int(lfsr[5]) ^ int(lfsr[4]) ^ 1)[2:]
  return copy.deepcopy(lfsr_)

def key_update(key):
  key_ = ['0' for i in range(128)]
  key_[16*0:16*1] = key[16*2:16*3]
  key_[16*1:16*2] = key[16*3:16*4]
  key_[16*2:16*3] = key[16*4:16*5]
  key_[16*3:16*4] = key[16*5:16*6]
  key_[16*4:16*5] = key[16*6:16*7]
  key_[16*5:16*6] = key[16*7:16*8]
  key_[16*6:16*7] = key[4:16] + key[0:4]
  key_[16*7:16*8] = key[30:32] + key[16:30]
  return copy.deepcopy(key_)

def AddRoundKey(state, key, lfsr):
  state_ = copy.deepcopy(state)
  for i in range(16):
    state_[4*i] = bin(int(state[4*i]) ^ int(key[i]))[2:]
    state_[4*i+1] = bin(int(state[4*i+1]) ^ int(key[16+i]))[2:]
  for i in range(6):
    state_[4*i+3] = bin(int(state[4*i+3]) ^ int(lfsr[i]))[2:]
  state_[63] = bin(int(state[63]) ^ 1)[2:]
  return copy.deepcopy(state_)

lfsr_ = ['1','0','0','0','0','0']

def One_Round_GIFT(state):
  global lfsr_
  global key_
  state_ = state
  state_ = SubCells(state_)
  state_ = PermBits(state_)
  state_ = AddRoundKey(state_, key_, lfsr_)
  lfsr_ = RC_LFSR(lfsr_)
  key_ = key_update(key_)
  return copy.deepcopy(state_)

def Full_GIFT(plaintxt, key):
  global lfsr_
  global key_
  key_ = key
  state = plaintxt
  for i in range(28):
    state = One_Round_GIFT(state)
  return copy.deepcopy(state)

def encrypt(plaintxt, key):
  global lfsr_
  global key_
  plaintxt = bin(eval('0x' + str(input("Enter message you want to encrypt (in hexadecimal)"))))[2:]
  plaintxt = list('0' * (64 - len(plaintxt)) + plaintxt)
  key = bin(eval('0x' + str(input("Enter the key (in hexadecimal)"))))[2:]
  key = list('0' * (128 - len(key)) + key)
  ciphrtxt = Full_GIFT(plaintxt, key)
  ciphrtxt = ciphrtxt[::-1]
  ciphrtxt = hex(eval('0b' + ''.join(ciphrtxt)))[2:]
  ciphrtxt = '0' * (16 - len(ciphrtxt)) + ciphrtxt
  print(ciphrtxt)

init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]

client_color = random.choice(colors)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 
separator_token = "<SEP>" 

s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")


name = input("Enter your name: ")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        message
        print("\n" + message)


t = Thread(target=listen_for_messages)

t.daemon = True

t.start()

Key='0'*32
while True:

    to_send =  input('Type your message here:\n\t')

    if to_send.lower() == 'q':
        break
    
    to_send_=''
    C=''
    for c in to_send:
        to_send_+=(2-len(hex(ord(c))[2:]))*'0'+hex(ord(c))[2:]
    
    to_send=''
    for _ in range(len(to_send_)//16):
        to_send+=encrypt(to_send_[16*_:min(16*(_+1), len(to_send_))], Key)
    

    
    
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"

    s.send(to_send)


s.close()