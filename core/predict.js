import * as tf from '@tensorflow/tfjs';
// import * as tf from '@tensorflow/tfjs-core';
// import '@tensorflow/tfjs-backend-webgl';
// import { loadLayersModel } from '@tensorflow/tfjs-layers'

import { GetOptions } from './config'
export const chars = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'á', 'æ', 'é', 'í', 'ð', 'ó', 'ö', 'ú', 'ý', 'þ']
const number_of_possible_letters = chars.length
const WINDOW_SIZE = 22;
const padding = new Array(WINDOW_SIZE / 2 - 1).fill(0);
let model
export const cache = {}





/**
 * Input is an array of lowercase words
 *
 * Output an object showing hyphenation point likelihood
 *   { "word": [0,0,1] }
 */
export const predict = async(array_of_words, options) => {
  options = GetOptions(options)

  if (array_of_words.length === 0) return cache;
  const startTime = new Date();

  if (!model) {
    model = await tf.loadLayersModel(`${options.model_base_url || ''}/model/model.json`)
  }
  const startTime2 = new Date();

  const processed = []
  array_of_words.forEach(word => {
    let word_int = word.split('').map(char => chars.indexOf(char))
    word_int = [...padding, ...word_int, ...padding]
    for (let i = 0; i <= word_int.length - WINDOW_SIZE; i++) {
      const Window = word_int.slice(i, i + WINDOW_SIZE)
      let j = []
      for (let e = 0; e < Window.length; e++) {
        let one_hot = new Array(number_of_possible_letters).fill(0)
        one_hot[Window[e]] = 1
        j.push(one_hot)
      }
      processed.push(j)
    }
  })

  if (processed.length === 0) {
    return cache
  }

  const predicted = await model.predict(tf.tensor(processed)).data()

  let current_index = 0
  array_of_words.forEach(word => {
    const out = []
    const word_spit = word.split('')
    word_spit.forEach((letter, index) => {
      if (index + 1 < word_spit.length) {
        if (predicted[current_index] > 0)
          out.push(predicted[current_index])
        else
          out.push(0)
        current_index++
      }
    })
    cache[word] = out
  })

  if (options.verbose) {
    console.log(`Hyphenation for ${array_of_words.length} words done in ${Math.round(new Date() - startTime2)} ms (loading model took ${Math.round(startTime2-startTime)} ms)`)
  }

  options.debug && console.log(cache)

  return cache
}

console.log('haha')
