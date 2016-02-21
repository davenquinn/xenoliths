pg = require 'pg'

conString = "postgres://localhost/xenoliths_flask"

module.exports = ->
  args = Array.apply(null, arguments)
  callback = args.pop()
  sql = args[0]
  data = args[1]

  pg.connect conString, (err, client, done) ->
    if err
      callback(err)
      return
    client.query sql, data, (err, result) ->
      callback(err, result)
      done()
