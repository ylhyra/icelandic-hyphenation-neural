const defaultConfig = {
  min_left_letters: 3,
  min_right_letters: 3,
  min_word_length: 6,
  min_subword_length: 3,
  secondary_splits_if_subword_is_at_minimum_X_length: 8,
  verbose: true,
  debug: process.env.NODE_ENV !== 'production',
  model_base_url: process.env.NODE_ENV === 'production' ? "https://cdn.jsdelivr.net/gh/ylhyra/icelandic-hyphenation-neural/build" : "http://localhost:9500",
}
// const url = document.currentScript ? document.currentScript:''

export default defaultConfig


export const MAJOR_HYPHENATION_INDICATOR_VALUE = 1
export const MINOR_HYPHENATION_INDICATOR_VALUE = 0.55
export const MORPHEME_BREAK_INDICATOR_VALUE = 0.1
