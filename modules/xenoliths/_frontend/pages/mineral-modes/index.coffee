Spine = require "spine"
d3 = require "d3"
template = require "./template.html"

tabulate = (el, data, columns) ->
  columns = (k for k of data[0])
  table = d3.select(el)
    .append("table")
  thead = table.append("thead")
  tbody = table.append("tbody")
  # append the header row
  thead.append("tr")
    .selectAll("th")
      .data(columns)
      .enter()
        .append("th")
          .text (column) -> column

  # create a row for each object in the data
  rows = tbody.selectAll("tr")
    .data(data)
    .enter()
      .append("tr")
  # create a cell in each row for each column
  cells = rows.selectAll("td")
    .data (row) ->
      columns.map (column) ->
        column: column
        value: row[column]
    .enter()
      .append("td")
        .html (d) -> d.value
  table

class MineralModes extends Spine.Controller
  constructor: ->
    super
    @$el.html template
    d3.json "/api/modes", (err, d)=>
      @setupData(d.data)

  setupData: (@data)->
    tabulate "#left", @data.map (d)->
      f =
        id: d.id
        complete: "#{Math.round(d.complete*100)}%"
      for key, val of d.modes
        f[key] = "#{Math.round(val*100)}%"
      f

module.exports = MineralModes
