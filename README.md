# forswitches-deob
Deobfuscates useless forswitches

```js
for ($._Ce = 0; $._Ce < 4; $._Ce += 1) {
    switch ($._Ce) {
        case 3:
            try {
                n.zfgformats = n.zfgformats || [];
            } catch (n) {}
            break;
        case 1:
            var t = n.document.documentElement.dataset.fp;
            break;
        case 2:
            n[t] = n[t] || [];
            break;
        case 0:
            if (!n.document.documentElement.dataset.fp) {
                n.document.documentElement.dataset.fp = f.random().toString(36).slice(2);
            }
            break;
    }
}
```

## To

```js
if (!n.document.documentElement.dataset.fp) {
    n.document.documentElement.dataset.fp = f.random().toString(36).slice(2);
}
var t = n.document.documentElement.dataset.fp;
n[t] = n[t] || [];
try {
    n.zfgformats = n.zfgformats || [];
} catch (n) {}
```
