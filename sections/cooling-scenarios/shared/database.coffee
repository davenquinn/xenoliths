Promise = require 'bluebird'
pgp = require('pg-promise')(promiseLib: Promise)

conString = "postgres://localhost/xenoliths_flask"

module.exports =
  db: pgp conString
  storedProcedure: (fn)->
    new pgp.QueryFile fn, minify: true


