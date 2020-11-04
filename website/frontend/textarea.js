import React from 'react'
import HyphenateText from 'core/text'
import copy from 'clipboard-copy'

class App extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      text: '',
      hyphenated: '',
      message: '',
      option: 'unicode',
    }
  }
  handleChange = async e => {
    const hyphenated = await HyphenateText(e.target.value)

    // get(e.target.value, hyphenated => {
      this.setState({ hyphenated, message: null })
      this.copy(hyphenated)
    // }, message => {
    //   this.setState({ message })
    // })
  }
  updateOption = e => {
    this.setState({ option: e.target.value });
    this.copy(this.state.hyphenated)
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
      <textarea onChange={this.handleChange} placeholder="Skrifaðu texta..."/>
      {this.state.message && <div className="clipboard" dangerouslySetInnerHTML={{__html: this.state.message}}/> }
      {this.state.hyphenated && (
        <div>
          {this.state.option === 'unicode' && <div className="output" dangerouslySetInnerHTML={{__html: StyledUnicode(this.state.hyphenated)}}/>}
          {this.state.option === 'html' && <div className="output" dangerouslySetInnerHTML={{__html: HTML(this.state.hyphenated)}}/>}
          {this.state.option === 'css' && <div className="output" dangerouslySetInnerHTML={{__html: CSS(this.state.hyphenated)}}/>}
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
