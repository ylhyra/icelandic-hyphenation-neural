import React from 'react'
import ReactDOM from 'react-dom'
import Textarea from './textarea'

ReactDOM.render(
  <div>
    <h1>
      Íslenskar orð&shy;skiptingar
    </h1>
    <div className="subtitle">
      Orðskipti&shy;vél sem tekur tillit<br/> til sam&shy;skeyttra orða
    </div>
    <Textarea/>
    <div className="paragraph">
      Þessi vél bætir inn <b>mjúkum bandstrikum</b> <i>(e. soft hyphens)</i> þar sem við á. Bandstrikin eru ósýnileg, en gefa tölvum vísbendingar um hvar best sé að skipta orði.
    </div>
    <div className="paragraph">
      Samsett íslensk orð eru flestum orðskipti&shy;vélum ofviða. Hér er reynt eftir fremsta megni að skipta samsettum orðum eftir merkingar&shy;bútum frekar en hljóð&shy;bútum.
    </div>
    <div className="paragraph">
      Hægt er að nota útkomuna úr þessari vél hvar sem er, í ritvinnsluforritum eða á netinu.
    </div>

    <div className="paragraph">
      Sendið upplýsingar um villur <a href="mailto:egill@egill.xyz">hingað</a>. Orð geta verið tvíræð og því reynir vélin frekar að gæta hófs við orðskiptingar.
    </div>

    <div className="paragraph small-gray">
      <a href="https://github.com/egilll/icelandic-hyphenation/blob/master/docs/README-is.md#readme"><span>Um verkefnið</span></a> – <a href="https://github.com/egilll/icelandic-hyphenation/blob/master/docs/API-is.md#readme"><span>Api</span> {'🐒'}</a>
    </div>

  </div>, document.getElementById('root'));
