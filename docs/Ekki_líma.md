# Notkun mjúkra bandstrika á vefsíðum

Mjúk bandstrik eru hluti af textanum og fljóta með þegar texti er klipptur-og-límdur. Þessi hegðun er ekki alltaf æskileg þar sem ósýnileg bandstrikin geta þvælst fyrir þegar maður setur textann inn í Excel eða forritunarskrár.

Koma má í veg fyrir að mjúk bandstrik fljóti með með því að hlaða eftirfarandi skriftu á vefsíðunni þinni:
```html
<script type="text/javascript" src="https://cdn.jsdelivr.net/gh/egilll/do-not-copy-hyphens/dist/index.js"></script>
```

Ef þú notar NodeJS er hægt að sækja skriftuna með `npm install do-not-copy-hyphens --save` og hlaða henni svo inn með:
```js
require('do-not-copy-hyphens')
```
