import HyphenateText, { SOFT_HYPHEN, SOFT_HYPHEN_REGEX } from './hyphenateText'

/**
 * Applies hyphenation to the text of a DOM element.
 * If no arguments are passed, is applied to the entire document.
 */
const HyphenateDOM = (element, options) => {
  if (!element) {
    element = document.body
  }

  const run = async() => {
    // console.log(element)
    const text = await HyphenateText(GetText(element), options)
    ApplyText(element, text)


    if (process.env.NODE_ENV === 'development') {
      // console.log(text.replace(SOFT_HYPHEN_REGEX, '-'))

      if (text.replace(SOFT_HYPHEN_REGEX, '') !== GetText(element)) {
        console.log(GetText(element))
        console.warn(text)
        throw new Error('Text did not match up')

      }
    }
  }

  /* Run if or when DOM is ready */
  if (
    document.readyState === "complete" ||
    document.readyState === "loaded" ||
    document.readyState === "interactive"
  ) {
    run()
  } else {
    document.addEventListener('DOMContentLoaded', run, false);
  }
}
export default HyphenateDOM


const GetText = (element) => {
  let out = ''
  const Traverse = (input) => {
    if (Array.isArray(input)) {
      return input.map(Traverse)
    } else if (input && input.childNodes) {
      for (var j = 0; j < input.childNodes.length; j++) {
        var node = input.childNodes[j];
        if (['SCRIPT', 'STYLE', 'CODE'].includes(node.nodeName)) continue;
        if (node.nodeType === Node.TEXT_NODE) {
          var nodeText = node.nodeValue;
          out += nodeText + '\n'
        } else {
          Traverse(node)
        }
      }
    }
  }
  Traverse(element)
  return out.replace(SOFT_HYPHEN_REGEX, '')
}

const ApplyText = (element, text) => {
  let cur_index = 0
  if (!text) {
    console.error('No text received')
    return
  }

  const indexesWithHyphenation = []
  let j = 0
  text.split(SOFT_HYPHEN_REGEX).forEach((str, index) => {
    j += str.length
    if (j !== text.length) {
      indexesWithHyphenation.push(j)
    }
  })
  // console.log(text.split(SOFT_HYPHEN_REGEX))
  // console.log(indexesWithHyphenation)

  const outputTextWithoutHypenations = text.replace(SOFT_HYPHEN_REGEX, '');
  const Traverse = (input) => {
    if (Array.isArray(input)) {
      return input.map(Traverse)
    } else if (input && input.childNodes) {
      for (var j = 0; j < input.childNodes.length; j++) {
        var node = input.childNodes[j];
        if (['SCRIPT', 'STYLE', 'CODE'].includes(node.nodeName)) continue;
        if (node.nodeType === Node.TEXT_NODE) {
          var nodeText = node.nodeValue.replace(SOFT_HYPHEN_REGEX, '');

          // console.log(`matching \n"${nodeText}" with \n"${outputTextWithoutHypenations.slice(cur_index, cur_index + nodeText.length)}"`)
          if (
            nodeText === outputTextWithoutHypenations.slice(cur_index, cur_index + nodeText.length)
          ) {
            // console.log(cur_index)
            // console.log(indexesWithHyphenation)
            var nodeTextSplit = nodeText.split('')
            let out = ''
            for (let i = 0; i < nodeTextSplit.length; i++) {
              out += nodeTextSplit[i]
              if (indexesWithHyphenation.includes(cur_index + i + 1)) {
                out += SOFT_HYPHEN
                // out += '-'
              }
            }
            // console.log('"'+out+'"')
            input.replaceChild(document.createTextNode(out), node);
          }
          /* Plus one since we've added a newline break in the first function */
          cur_index += nodeText.length + 1
        } else {
          Traverse(node)
        }
      }
    }
  }
  Traverse(element)
}
