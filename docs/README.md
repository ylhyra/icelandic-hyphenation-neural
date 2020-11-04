# Hyphenation neural network for Icelandic 🇮🇸

This is a JavaScript-based neural network recognizes word boundaries in Icelandic [compound words](https://en.wikipedia.org/wiki/Compound_(linguistics)) and nested compound words. By default it hyphenates on “*aðfangadags–kvöld*” rather than “*aðfanga–dagskvöld*”, allowing the reader to parse words with more ease. Optionally, more frequent hyphenation points (“*að·fanga·dags·kvöld*”) can be returned.

Use it online [here](http://hyphenation.ylhyra.is/).

#

```html
<script type="text/javascript" src="https://cdn.jsdelivr.net/gh/ylhyra/icelandic-hyphenation-neural/build/core.js"></script>
<script type="text/javascript">
IcelandicHyphenation.config.model_url = "https://cdn.jsdelivr.net/gh/ylhyra/icelandic-hyphenation-neural/build/model/mode.json"
var output = IcelandicHyphenation.text('virkilega langur texti')
</script>
```


## Documentation

* [Preventing hyphens from being copied](https://github.com/egilll/do-not-copy-hyphens#readme)

## Credits

* Built upon the [HypheNN-de](https://github.com/msiemens/HypheNN-de) project by [Markus Siemens](https://github.com/msiemens) <small>([MIT](https://opensource.org/licenses/MIT))</small>.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

You can suggest improvements by using the [issue tracker](https://github.com/egilll/icelandic-hyphenation/issues/new) or by [contacting me](mailto:egill@egill.xyz).
