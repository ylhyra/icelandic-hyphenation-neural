<h1 align="center">Hyphenation <br/>neural network <br/>for Icelandic <br/>🇮🇸</h1>

This is a JavaScript-based neural network recognizes word boundaries in Icelandic [compound words](https://en.wikipedia.org/wiki/Compound_(linguistics)) and nested compound words. By default it hyphenates on “*aðfangadags–kvöld*” rather than “*aðfanga–dagskvöld*”, which can in many situations aid the reader to parse the word. Optionally, more frequent hyphenation points (“*að·fanga·dags·kvöld*”) can be returned.

Use it online [here](http://hyphenation.ylhyra.is/).

## Documentation

This program adds [soft hyphens](https://en.wikipedia.org/wiki/Soft_hyphen) to text. It can run in the browser or Node.js with the use of [TensorFlow.js](https://www.tensorflow.org/js). The program is 700kB gzipped. Initialization takes about 2 seconds but the hyphenation itself is quick. Hyphenation should be applied to text during a pre-processing step rather than being applied by end-users.

**In the browser:**

```html
<script type="text/javascript" src="https://cdn.jsdelivr.net/gh/ylhyra/icelandic-hyphenation-neural/build/core.js"></script>

<script type="text/javascript">

/* Example 1: Hyphenate text */
IcelandicHyphenation
  .HyphenateText('forsætisráðherra')
  .then(text => {
    console.log(text);
  })

/* Example 2: Add hyphenation to a DOM element */
var element = document.getElementById('root')
IcelandicHyphenation.HyphenateElement(element)

</script>
```

**In Node.js:**

```js
const IcelandicHyphenation = require('icelandic-hyphenation-neural')

const text = await IcelandicHyphenation.HyphenateText('forsætisráðherra')
```

### Configuration

- `min_word_length`
  - Only hyphenate words that are this long.
  - Default: 6.
- `min_left_letters`
  - Hyphenation must be at least this many letters from the left edge of the word.
  - Default:  3.
- `min_right_letters`  
  - Hyphenation must be at least this many letters from the right edge of the word.
  - Default: 3.
- `min_subword_length`
  - A sub-word is a word inside the longer word, the subwords in "*sjávar–líf–fræði*" are *sjávar*, *líf*, *fræði* and *líffræði*. This particular option only applies to words in the middle, so here *líf*. If `min_subword_length` is set to 3, the hyphenation can be "*sjávar–líf–fræði*" (if the below option regarding secondary splits is also set low), if it's more than that it will be "*sjávar–líffræði*".
  - Default: 3.
- `min_subword_length_for_secondary_splits`
  - In the word "*for|sætis**·**ráð|herra**–**sumar**·**bú|staðurinn*", primary splits are marked with "**–**", secondary splits are marked with "**·**", and tertiary splits are marked with "|". Here we have two sub-words: "forsætis**·**ráðherra" and "sumar**·**bústaðurinn". These words are too long still and we usually want to split them even further. If `min_subword_length_for_secondary_splits` is 16 or less, our hyphenated output will be "*forsætis–ráðherra–sumar–bústaðurinn*". If it is more than 16, the hyphenated output will be "*forsætisráðherra–sumarbústaðurinn*".
  - Default: 8
- `model_base_url`
  - Default:

**Examples:**


```js
/* Returns „ó-ánægð með ís-búðina“ */
const text = await IcelandicHyphenation.HyphenateText('óánægð með ísbúðina', {
  min_left_letters: 1,
})
```

### Methods

- HyphenateText(input, options)
  - Returns a promise. Returns text with hyphenations.
- HyphenateDOM(element, options)
  - Adds hyphenation directly to element. Returns nothing.

## Usage notes

- [Preventing hyphens from being copied](https://github.com/egilll/do-not-copy-hyphens#readme)

## Credits

- Built upon the [HypheNN-de](https://github.com/msiemens/HypheNN-de) project by [Markus Siemens](https://github.com/msiemens) <small>([MIT](https://opensource.org/licenses/MIT))</small>.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

You can suggest improvements by using the [issue tracker](https://github.com/egilll/icelandic-hyphenation/issues/new) or by [contacting me](mailto:egill@egill.xyz).
