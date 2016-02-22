Client = require 'pg-native'
types = require 'pg-types'
utils = require 'pg/lib/utils'

conString = "postgres://localhost/xenoliths_flask"

c = new Client types: types

module.exports = (sql, data)->
  c.connectSync conString
  prepared = data.map utils.prepareValue
  return c.querySync sql, prepared
