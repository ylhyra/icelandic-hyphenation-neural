<h1 align="center">Hyphenation <br/>neural network <br/>for Icelandic <br/>🇮🇸</h1>

This is a JavaScript-based neural network recognizes word boundaries in Icelandic [compound words](https://en.wikipedia.org/wiki/Compound_(linguistics)) and nested compound words. By default it hyphenates on “*aðfangadags–kvöld*” rather than “*aðfanga–dagskvöld*”, which can in many situations aid the reader to parse the word. Optionally, more frequent hyphenation points (“*að·fanga·dags·kvöld*”) can be returned.

Use it online [here](http://hyphenation.ylhyra.is/).

## Documentation

This program adds [soft hyphens](https://en.wikipedia.org/wiki/Soft_hyphen) to text. It can run in the browser or Node.js with the use of [TensorFlow.js](https://www.tensorflow.org/js). The program is 700kB gzipped. Initialization takes about 2 seconds but the hyphenation itself is quick. Hyphenation should be applied to text during a pre-processing step rather than being applied by end-users.





```html
<script type="text/javascript" src="https://cdn.jsdelivr.net/gh/ylhyra/icelandic-hyphenation-neural/build/core.js"></script>
<script type="text/javascript">
IcelandicHyphenation
  .HyphenateText('virkilega langur texti')
  .then(text => {
    console.log(text);
  })
</script>
```


## Usage notes

* [Preventing hyphens from being copied](https://github.com/egilll/do-not-copy-hyphens#readme)

## Credits

* Built upon the [HypheNN-de](https://github.com/msiemens/HypheNN-de) project by [Markus Siemens](https://github.com/msiemens) <small>([MIT](https://opensource.org/licenses/MIT))</small>.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

You can suggest improvements by using the [issue tracker](https://github.com/egilll/icelandic-hyphenation/issues/new) or by [contacting me](mailto:egill@egill.xyz).
