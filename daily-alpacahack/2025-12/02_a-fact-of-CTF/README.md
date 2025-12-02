# Writeup for a fact of CTF

>AlpacaHack で一番最初に完成したものの難易度調整により出題されなかった幻の問題 （運営コメント）

`output.txt` からフラグを逆算するのがゴールです。

`chall.py` の出力は例えば、`FLAG` が `ABC` だとすると、

```
$ python
>>> ord('A')
65
>>> ord('B')
66
>>> ord('C')
67
```
であることから、

$$2^{65} \times 3^{66} \times 5^{67}$$

すなわち `77257885956581530904801604508822500000000000000000000000000000000000000000000000000000000000000000` となります。

では、出力の値からフラグを逆算するにはどうすればいいでしょうか？

素因数分解ができたら解くことが出来そうです。

Pythonで以下のプログラムを実行します（`x`は出力の値、`primes`は`chall.py`にある素数）:

```
for p in primes:
    if x % p == 0:
        exp = 0
        while x % p == 0:
            x //= p
            exp += 1
        print(chr(exp), end='')
```

これでフラグが出力されます。

Flag: `Alpaca{prime_factorization_solves_everything}`
