# Writeup for AlpacaHack 2100
<img width="920" height="365" alt="image" src="https://gist.github.com/user-attachments/assets/80052254-7e2e-4e9c-b07c-1c1123478038" />

問題文には、
```
🦙 < フラグは Daily AlpacaHack の 2100年1月 のカレンダーにあるパカ
```
と書いてあるので、2100年1月のカレンダーを見に行きます。

Daily AlpacaHack のカレンダーは「次の月」ボタンを押せば、次の月に進めます。

<img width="304" height="64" alt="image" src="https://gist.github.com/user-attachments/assets/4c062191-62df-42cc-a854-2149cfd7b5ba" />

単純にこのボタンを約75年分、つまり900回くらい押し続けていけばひとまずは解けそうですが、何かしらの病気になりそうです。

何か効率的に解く方法はないでしょうか？

ここでボタンの遷移先のURLを見ると、 https://alpacahack.com/daily?month=2026-01 のようになっています。
実際、押すとそのページに遷移します。

どうやら `month` に指定された年月のカレンダーが表示されるようです。

では、このクエリ文字列 `month=2026-01` を `month=2100-01` に変えてみるとどうでしょうか？

実際飛んでみると、2100年1月のカレンダーが表示され、11日から17日にフラグが細切れに配置されていました。

<img width="1197" height="1073" alt="image" src="https://gist.github.com/user-attachments/assets/0d293e4c-d149-4a54-b2fe-229031e29506" />

これらを結合するとフラグです。これで健康的に解けました。

Flag: `Alpaca{brought_AGI_to_humanity..._yes,_Alpaca_Gentle_Intelligence.}`
