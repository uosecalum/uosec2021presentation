from pwn import *
import sys

context.log_level="critical"
target = "uosec.canihax.com"
port = 5000


solution = []
guess = False
while True:
    r = remote(target, port)
    # chomp banner
    r.recvline()
    if guess:
        guess = False
        # try solution
        r.sendline("".join(solution).encode('utf-8'))
        try:
            recv = r.recvline_contains(b'flag')
            if recv:
                print(recv.decode('utf-8').strip('\r'))
                sys.exit(0)
        except EOFError:
            pass
    r.sendline(''.join(solution).encode('utf-8')+chr(0).encode('utf-8'))
    resp = r.recvuntil(b'.', drop=True).decode("ascii").split(' ')[-1]
    solution.append(chr(0 - int(resp)))
    guess = True
