# Writeup for AlpacaHack 2100
<img width="1840" height="730" alt="image" src="https://github.com/user-attachments/assets/473f7813-ed5e-45fe-9bc8-357a3cfab4fd" />


問題文には、
```
🦙 < フラグは Daily AlpacaHack の 2100年1月 のカレンダーにあるパカ
```
と書いてあるので、2100年1月のカレンダーを見に行きます。

Daily AlpacaHack のカレンダーは「次の月」ボタンを押せば、次の月に進めます。

<img width="304" height="64" alt="image" src="https://github.com/user-attachments/assets/0ce5aa5f-6cd2-4262-a37d-ac8d6d33f427" />


単純にこのボタンを約75年分、つまり900回くらい押し続けていけばひとまずは解けそうですが、何かしらの病気になりそうです。

何か効率的に解く方法はないでしょうか？

ここでボタンの遷移先のURLを見ると、 https://alpacahack.com/daily?month=2026-01 のようになっています。
実際、押すとそのページに遷移します。

どうやら `month` に指定された年月のカレンダーが表示されるようです。

では、このクエリ文字列 `month=2026-01` を `month=2100-01` に変えてみるとどうでしょうか？

実際飛んでみると、2100年1月のカレンダーが表示され、11日から17日にフラグが細切れに配置されていました。

<img width="1197" height="1073" alt="image" src="https://github.com/user-attachments/assets/a7aaecf9-dd27-4b18-8263-09d7757a2abb" />


これらを結合するとフラグです。これで健康的に解けました。

Flag: `Alpaca{brought_AGI_to_humanity..._yes,_Alpaca_Gentle_Intelligence.}`
