# Hyphenation neural network for Icelandic 🇮🇸

This neural network recognizes word boundaries in Icelandic [compound words](https://en.wikipedia.org/wiki/Compound_(linguistics)) and nested compound words. By default it hyphenates on “*aðfangadags–kvöld*” rather than “*aðfanga–dagskvöld*”, allowing the reader to parse words with more ease. Optionally, more frequent hyphenation points (“*að·fanga·dags·kvöld*”) can be returned

The program runs in a browser.

## Documentation

* [Preventing hyphens from being copied](https://github.com/egilll/do-not-copy-hyphens#readme)

## Credits

* Built upon the [HypheNN-de](https://github.com/msiemens/HypheNN-de) project by [Markus Siemens](https://github.com/msiemens) <small>([MIT](https://opensource.org/licenses/MIT))</small>.

## License

* Code: [MIT](https://opensource.org/licenses/MIT)
* Trained network: [CC0](https://creativecommons.org/publicdomain/zero/1.0/)

Use it online [here](https://ordskipting.egill.xyz/). You can suggest improvements by using the [issue tracker](https://github.com/egilll/icelandic-hyphenation/issues/new) or by [contacting me](mailto:egill@egill.xyz).
