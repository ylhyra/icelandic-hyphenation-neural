const path = require('path')
const fs = require('fs')
const { shuffle } = require('underscore')
const LineByLineReader = require('line-by-line')

const file = path.resolve(__dirname, `wordlist.txt`)
let data = [] //shuffle((fs.readFileSync(file, 'utf8')).split('\n'))


var lr = new LineByLineReader(file)
lr.on('error', (err) => {
  console.log(err)
})
var count = 0

lr.on('line', async(line) => {
  data.push(line)
  count++
  if(count%1000000 === 0){
    console.log(count)
  }
});

lr.on('end', () => {
  console.log('LOADED')
  data = shuffle(data)
  fs.writeFileSync(file, '', function () {})

  for (let i = 0; i < data.length; i += 100000) {
    fs.appendFileSync(file, data.slice(i, i + 100000).join('\n'), function () {})
  }
  process.exit()
})
