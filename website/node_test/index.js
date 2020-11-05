/*
export NODE_PATH=. && node -r esm website/node_test/index.js
*/
import HyphenateText from 'core/hyphenateText'

const main = async() => {
  const text = HyphenateText('vinsæll', {
    model_url: `file:///${__dirname}/../`
  })
  console.log(text)
}
main()
