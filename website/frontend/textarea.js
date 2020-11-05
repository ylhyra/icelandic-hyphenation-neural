import React from 'react'
import HyphenateText from 'core/hyphenateText'
import copy from 'clipboard-copy'

const options = {
  best: {
    min_left_letters: 3,
    min_right_letters: 3,
    min_word_length: 6,
    min_subword_length: 4,
    min_subword_length_for_secondary_splits: 14,
  },
  next_best: {
    min_left_letters: 3,
    min_right_letters: 3,
    min_word_length: 6,
    min_subword_length: 3,
    min_subword_length_for_secondary_splits: 8,
  },
}

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: '',
      hyphenated: '',
      message: '',
      option: 'unicode',
      // options: options.best
    }
  }
  handleTextareaChange = e => {
    this.timer && clearTimeout(this.timer)
    this.setState({ message: 'Hleð...', text: e.target.value })
    this.timer = setTimeout(this.hyphenate, 500);
  }
  hyphenate = async() => {
    try {
      const hyphenated = await HyphenateText(this.state.text, this.state.options)
      this.setState({ hyphenated, message: null })
      this.copy(hyphenated)
    } catch (e) {
      this.setState({ message: '<b>Villa</b>: Náði ekki að sækja líkan! :(' })
    }
  }
  updateOption = e => {
    this.setState({ option: e.target.value });
    this.copy(this.state.hyphenated)
  }
  updateSensitivity = e => {
    this.setState({ options: options[e.target.value] }, this.hyphenate)
  }
  copy = text => {
    this.setState({ message: null })
    /* Timeout to make the transition obvious to the reader */
    if (text && text.indexOf('\u00AD') > 0) {
      setTimeout(() => {
        let textToCopy = text
        if (this.state.option === 'html') {
          textToCopy = text.replace(/\u00AD/g, '&shy;')
        } else if (this.state.option === 'css') {
          textToCopy = text.replace(/\u00AD/g, '<span class="unselectable">&shy;</span>')
        }
        copy(textToCopy, { message: '' })
        this.setState({ message: 'Textinn með mjúkum bandstrikum hefur verið vistaður í klippiborðið þitt. Þú getur nú límt <i>(e. paste)</i> textann hvert sem er.' })
      }, 200)
    }
  }
  render = () => {
    return <div>
      <textarea onChange={this.handleTextareaChange} placeholder="Skrifaðu texta..."/>
      {this.state.hyphenated && (
        <div>
          {this.state.option === 'unicode' && <div className="output" dangerouslySetInnerHTML={{__html: StyledUnicode(this.state.hyphenated)}}/>}
          {this.state.option === 'html' && <div className="output" dangerouslySetInnerHTML={{__html: HTML(this.state.hyphenated)}}/>}
          {this.state.option === 'css' && <div className="output" dangerouslySetInnerHTML={{__html: CSS(this.state.hyphenated)}}/>}
          {/* <div className="options">
            Hamur: {' '}
            <select onChange={this.updateSensitivity}>
              <option value="best">Aðeins bestu orðskiptingarnar, bara mjög löng orð (gott fyrir texta á netinu)</option>
              <option value="next_best">Bestu og næstbestu orðskiptingarnar (hentar betur ef texti þarf að komsat fyrir í mjóum dálkum)</option>
            </select>
          </div> */}
          <div className="options">
            Hvernig bandstrik má bjóða þér?{' '}
            <select onChange={this.updateOption}>
              <option value="unicode">Mjúk bandstrik</option>
              <option value="html">Mjúk bandstrik í HTML</option>
            </select>
            {this.state.option === 'html' && <div>Sjá <a href="https://github.com/egilll/icelandic-hyphenation/blob/master/docs/Ekki_l%C3%ADma.md#readme">leiðbeiningar um notkun á vefsíðum</a>.</div>}
          </div>
        </div>
      )}
      {this.state.message && <div className="clipboard" dangerouslySetInnerHTML={{__html: this.state.message}}/> }
    </div>
  }
}

const StyledUnicode = (input) => {
  return input
    .replace(/>/g, '&gt;')
    .replace(/</g, '&lt;')
    .replace(/\u00AD/g, '<span class="shy"><span>&shy;</span></span>')

}
const HTML = (input) => {
  return input
    .replace(/>/g, '&gt;')
    .replace(/</g, '&lt;')
    .replace(/\u00AD/g, '<span class="red">&amp;shy;</span>')
}
export default App
