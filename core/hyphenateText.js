import { predict, chars } from './predict'
import { GetOptions, MAJOR_HYPHENATION_INDICATOR_VALUE, MINOR_HYPHENATION_INDICATOR_VALUE } from './config'
export const SOFT_HYPHEN = '\u00AD'
// export const SOFT_HYPHEN = '-'
export const SOFT_HYPHEN_REGEX = /\u00AD/g
const icelandic_letters = chars.join('')
const latin_letters = 'a-zA-Z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u024F'
const other_hyphens = '\\-\\–'
const matchable_adjacent_to_spaces = `(?:[^${latin_letters}${other_hyphens}]+?)?`
const spacesAndAdjacentPunctuation = new RegExp(`(${matchable_adjacent_to_spaces}\\s+?${matchable_adjacent_to_spaces})`, 'g')
const fullyIcelandicString = new RegExp(`^[${icelandic_letters}]+$`, 'i')
// const spaces = ' \u00A0' /* Space and nbsp */

/**
 * Hyphenates raw paragraphs of text
 */
const HyphenateText = async(text, options, setMessage) => {
  options = GetOptions(options)

  try {
    /* Remove any previous soft hyphens */
    text = text.replace(SOFT_HYPHEN_REGEX, '')

    const allStringsInDocument = []
    const wordsToHyphenate = []
    const icelandicRegex = new RegExp(`([${icelandic_letters}]{${options.min_word_length},})`, 'i')

    text
      /* Split on spaces and adjacent non-Latin (which includes punctuation) */
      .split(spacesAndAdjacentPunctuation)
      .forEach(string => {
        if (
          /* Short words */
          string.length < options.min_word_length ||
          /* Spaces */
          /\s/.test(string) ||
          /* Other strings that don't include Icelandic */
          !(new RegExp(`[${icelandic_letters}]{${options.min_word_length}}`, 'i')).test(string)
        ) {
          allStringsInDocument.push({ string })
          return;
        }
        /* Fully Icelandic string */
        if (fullyIcelandicString.test(string)) {
          if (!wordsToHyphenate.includes(string.toLowerCase())) {
            wordsToHyphenate.push(string.toLowerCase())
          }
          allStringsInDocument.push({ string, toHyphenate: string.toLowerCase() })
          return;
        }
        /* Icelandic mixed with other */
        const split = string.split(icelandicRegex)
        split.forEach((item, index) => {
          if (index % 2 !== 0 || item.length < options.min_word_length) {
            allStringsInDocument.push({ string: item })
          } else {
            if (!wordsToHyphenate.includes(item.toLowerCase())) {
              wordsToHyphenate.push(item.toLowerCase())
            }
            allStringsInDocument.push({ string: item, toHyphenate: item.toLowerCase() })
          }
        })
      })

    const prediction = await predict(wordsToHyphenate, options)

    // if (config.debug) {
    //   let debug = []
    //   for (let word in prediction) {
    //     debug.push(prediction[word])
    //   }
    //   console.log(debug.join(', '))
    // }
    // console.log(prediction)
    // console.log(allStringsInDocument)
    return allStringsInDocument.map(item => {
      if (!item.toHyphenate) return item.string;
      const hyphenation = prediction[item.toHyphenate]
      if (!hyphenation.find(i => i > MINOR_HYPHENATION_INDICATOR_VALUE - 0.2)) return item.string;

      const areThereAnyMajorHyphenations = hyphenation.find(i => i > MAJOR_HYPHENATION_INDICATOR_VALUE - 0.2)

      let sorted = hyphenation.map((value, index) => {
        if (value > MINOR_HYPHENATION_INDICATOR_VALUE - 0.2) {
          return { value, index }
        }
        return null
      }).filter(Boolean).sort((a, b) => b.value - a.value)

      let chosen = []
      sorted.forEach(item => {
        if (chosen.find(c => Math.abs(item.index - c.index) < options.min_subword_length)) return;
        if (
          item.value > MAJOR_HYPHENATION_INDICATOR_VALUE - 0.2 ||
          !areThereAnyMajorHyphenations
        ) {
          return chosen.push(item)
        }

        //   const closestToLeft =
        //   const closestToRight =
        //
        // !chosen.find(c => Math.abs(item.index - c.index) <= config.min_subword_length_for_secondary_splits)
      })

      let out = ''
      const split = item.string.split('')
      for (let i = 0; i < split.length; i++) {
        out += split[i]
        if (i + 1 < options.min_left_letters ||
          item.string.length - i - 1 < options.min_right_letters
        ) continue;
        const value = (chosen.find(c => c.index === i) || {}).value
        if (value > MAJOR_HYPHENATION_INDICATOR_VALUE - 0.2) {
          out += SOFT_HYPHEN
        } else if (value > MINOR_HYPHENATION_INDICATOR_VALUE - 0.2) {
          out += SOFT_HYPHEN
        }
      }
      return out
    }).join('')

  } catch (error) {
    console.log(error)
  }
}

export default HyphenateText
