var express = require('express')
var app = express()
import compression from 'compression'
import path from 'path'
import HyphenateText from 'core/text'
import bodyParser from 'body-parser'
import cors from 'cors'
import frontpage from 'website/frontend/frontpage.html.js'

app.use(compression({}))
// app.use('/robots.txt', express.static(path.join(__dirname, './../public/robots.txt')))
app.use('/css.css', express.static(path.join(__dirname, './../frontend/css.css')))
app.use('/script.js', cors(), express.static(path.join(__dirname, './../../build/website.js')))
app.use('/plugin.js', cors(), express.static(path.join(__dirname, './../../build/plugin.js')))
app.use('/plugin.js.map', cors(), express.static(path.join(__dirname, './../../build/plugin.js.map')))
app.use('/model/', cors(), express.static(path.join(__dirname, './../../build/model/')))

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.all('/', cors(), (req, res) => {
  res.send(frontpage({
    text: req.body.text,
  }))
})

// app.all('/api', cors(), (req, res) => {
//   res.setHeader('X-Robots-Tag', 'noindex')
//
//   // const text = req.query['text'] || req.query['texti'] || req.query['t'] || req.body.text || req.body.texti
//   //
//   // /* Hard limit on number of characters, 40 thousand */
//   // if (text.length > 40000) {
//   //   return res.status(413).json({ error: 'Payload is over 40,000 characters' })
//   // }
//   //
//   // HyphenateText(text, hyphenation => {
//   //   res.send(hyphenation)
//   // })
// })

app.listen(9500)
