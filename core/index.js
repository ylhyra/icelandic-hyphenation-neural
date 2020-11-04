import HyphenateDOM from './hyphenateDOM'
import HyphenateText from './hyphenateText'

// setTimeout(()=>{
//   DOM()
// },300)

if (window) {
  window.IcelandicHyphenation = {
    HyphenateText,
    HyphenateDOM,
  }
}
