var mysql = require('mysql')
var connection = mysql.createPool({
  connectionLimit : 10,
  host: 'localhost',
  database: 'hyphenation',
  user: 'hyphenation',
  password: 'hyphenation',
  multipleStatements: true,
});

module.exports = connection
