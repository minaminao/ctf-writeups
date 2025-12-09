# Writeup for Emojify

https://alpacahack.com/daily/challenges/emojify


サーバーにアクセスすると次のようなサービスがあり、

![](assets/image.png)

例えば、プレースホルダーに従って `pizza` と入力すると、

![](assets/image-1.png)

超ビッグなピザの絵文字が表示されます。

フラグは、`secret` サービスにあるが、 `compose.yaml` を見ると外部から直接アクセスすることはできません。

なので内部からアクセスする必要があり、その方法を探っていきます。

`frontend` サービスでは以下のコードで動いており、

```js
import express from "express";
import fs from "node:fs";

const waf = (path) => {
  if (typeof path !== "string") throw new Error("Invalid types");
  if (!path.startsWith("/")) throw new Error("Invalid 1");
  if (!path.includes("emoji")) throw new Error("Invalid 2");
  return path;
};

express()
  .get("/", (req, res) => res.type("html").send(fs.readFileSync("index.html")))
  .get("/api", async (req, res) => {
    try {
      const path = waf(req.query.path);
      const url = new URL(path, "http://backend:3000");
      const emoji = await fetch(url).then((r) => r.text());
      res.send(emoji);
    } catch (err) {
      res.send(err.message);
    }
  })
  .listen(3000);
```

例えば、`pizza` を送信すると、この `/api` が呼ばれます。
具体的には `/api?path=/emoji/pizza` へのリクエストが走ります。

そして、`const url = new URL(path, "http://backend:3000");` によって `path` と `http://backend:3000` が結合されているようです。

MDN のドキュメントで `URL` について調べると、以下のような記述があります（[ref](https://developer.mozilla.org/ja/docs/Web/API/URL/URL)）:

>`new URL(url, base)`
>
>`base` (省略可)
>文字列で、`url` が相対参照の場合に使用するベース URL を表します。 指定されなかった場合、既定値は `undefined` です。

つまり、`url` が相対参照でない場合は、`base` は無視され、そのまま `url` が使用されそうです。
これを用いて、`secret` サービスに宛先を向けることができそうだとわかります。

しかし、例えば `http://secret:1337/flag` を入力しても、`waf` 関数の `if (!path.startsWith("/")) throw new Error("Invalid 1");` ルールによって先頭が `/` から始まらなければ弾かれます。

ここで、さらに MDN のドキュメントを読んでいくと、以下の使用法が示されています:

```
new URL("//foo.com", "https://example.com");
// => 'https://foo.com/' (see relative URLs)
```

つまり、URLスキーマを省略した `//secret:1337/flag` でも動作し、これで `waf` の `/` から始まらなければならないルールは守ることができます。

次に `if (!path.includes("emoji")) throw new Error("Invalid 2");` ルールを守らなければいけません。
これは、例えばクエリ文字列 `?emoji` をつければパスできます。

よって、 `/api?path=//secret:1337/flag?emoji` にアクセスすることでフラグが得られました。

Flag: `Alpaca{Sup3r_Speci4l_Rar3_Flag}`

（頭文字を取ると `SSRF` になっている！）
