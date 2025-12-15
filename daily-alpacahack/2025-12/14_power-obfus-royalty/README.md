# Writeup for power_obfus_royalty

`power_obfus_royalty.ps1` という名前の PowerShell スクリプトが与えられます。

中身を見ると、

```
$Buf = & ([CHAr]73+[ChaR]101+[CHAr]88) ([chaR]82+[ChaR]69+[chAr]97+[CHar]68+[CHar]45+[CHAr]72+[CHAr]111+[CHar]115+[CHAR]84+[chAR]32+[Char]40+[cHAR]91+[cHAR]99+[char]72+[cHAr]65+[ChAR]82+[ChAR]93+[CHAr]55+[CHaR]48+[CHaR]43+[cHAR]91+[chAR]67+[CHAr]104+[cHaR]65+[ChAr]114+[Char]93+[CHar]55+[CHAr]54+[CHAr]43+[cHAr]91+[cHAr]99+[cHAR]72+[ChAr]65+[ChaR]114+[Char]93+[ChaR]54(省略)
```

となっています。長かったので省略しています。

ファイル名に `obfus` とあることからも難読化されているようです。

`[Char]数値` がたくさんありますが、これは `Char` 型にキャストする構文で、例えば `[Char]73` は `I` を表します。

まずは、これを復元して整えるスクリプトを書きます:

```python
import re

data = open("distfiles/power_obfus_royalty.ps1", "r").read()

pattern = r'\[[cC][hH][aA][rR]\]\d+'

for _ in range(2):
    matches = re.findall(pattern, data)

    for match in matches:
        num = int(re.search(r'\d+', match).group())
        char = chr(num)
        data = data.replace(match, f'"{char}"')

    data = data.replace('"+"', "")

print(data)
```

復元後も `[Char]数値` が残っていたり `"+"` の結合があったりで、それらも整えています。

これを実行すると以下のようになります:

```
$ python transform1.py
$Buf = & ("IeX") ("REaD-HosT ("FLAG")")
IF (& ("IEX") ("iex ("(`$BUf).ComparETo(("TSGLIVE{1nv0k3_3xpr35510"+[CHaR"+(powershell.exe -executionpolicy bypass -enc aQBlAHgAIAAoAGkAZQB4ACAAKABbAGMASABhA(省略)WwBjAGgAYQByAF0AMwA0ACkAKQA=)+0r_p0w3r5h3ll_0bfu5ca710n}"))")")) {& ("ieX") ("wriTe-OUtpUt ("Wrong...")")} ElSE {& ("ieX") ("WrItE-ouTput ("Correct!!!")")}
```

ここで、`powershell.exe` に渡されている Base64 文字列は長かったので省略しています。

この時点で、以下のことがわかります:
- `Read-Host` でユーザー入力が `$Buf` に格納されそう
- この `$Buf` と `TSGLIVE{1nv0k3_3xpr35510` + (`[CHaR` + `powershell.exe -executionpolicy bypass -enc (Base64 文字列)`) + `0r_p0w3r5h3ll_0bfu5ca710n}` が比較されていそう
- `Wrong`, `Correct` と文字列があることから、フラグチェッカーっぽい

そこで、まず Base64 文字列をデコードすると、

```
i\x00e\x00x\x00 \x00(\x00i\x00e\x00x\x00 \x00(\x00[\x00c\x00H\x00a\x00r\x00]\x003\x004\x00+\x00[\x00C\x00H(省略)
```

という結果が得られます。

`\x00` がたくさんありますが、これは UTF-16 でエンコードされた文字列のようです。デコードすると、

```
iex (iex ([cHar]34+[CHar]101+[chAR]99+[CHar]104+[char]111+[ChAR]32+[CHaR]93+[cHar]49+(省略)
```

という結果が得られます。

これもさらに先程と同様に `[Char](数値)` を元に戻していきましょう。

次のスクリプトを実行します:

```python
import base64
import re

encoded_command = "aQBlAHgAIAAoAGkAZQB4ACAAKA(省略)F0AMwA0ACkAKQA="
command = base64.b64decode(encoded_command).decode('utf-16le')


pattern = r'\[[cC][hH][aA][rR]\]\d+'

for _ in range(2):
    matches = re.findall(pattern, command)

    for match in matches:
        num = int(re.search(r'\d+', match).group())
        char = chr(num)
        command = command.replace(match, f'"{char}"')

    command = command.replace('"+"', "")

print(command)
```

これを実行すると、

```
$ python transform2.py
iex (iex (""echo ]110+"_15_an_1mp0r7an7_f3a7ur3_f"""))
```

となりました。この結果からフラグは次のようになりそうです:

`TSGLIVE{1nv0k3_3xpr35510` + `[CHaR]110` + `_15_an_1mp0r7an7_f3a7ur3_f` + `0r_p0w3r5h3ll_0bfu5ca710n}`

これらを結合するとフラグが求まりました。

Flag: `TSGLIVE{1nv0k3_3xpr35510n_15_an_1mp0r7an7_f3a7ur3_f0r_p0w3r5h3ll_0bfu5ca710n}`
