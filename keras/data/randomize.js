const path = require('path')
const fs = require('fs')
const { shuffle } = require('underscore')

const file = path.resolve(__dirname, `wordlist.txt`)
let data = shuffle((fs.readFileSync(file, 'utf8')).split('\n'))
fs.writeFileSync(file, data.join('\n'), function () {})
