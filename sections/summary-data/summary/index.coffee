d3 = require 'd3-jetpack/build/d3v4+jetpack'
{readFileSync} = require 'fs'
{annotation} = require 'd3-svg-annotation'
conventions = require 'd3-conventions'
require './main.styl'

getJSON = (fn)->
  d = readFileSync require.resolve fn
  JSON.parse d.toString()

data = getJSON "./temperature-summary.json"
depletionData = getJSON "./depletion-summary.json"

mergedData = for d in data
  temperature = d.core
  {id, color} = d
  depletion = depletionData.find (v)->v.sample_id == id
  {temperature, depletion, id, color}

xScale = ->
  d3.scaleBand()
    .paddingInner 40
    .paddingOuter 20

thermometers = ['bkn','ca_opx_corr','ta98','ree']
tnames = ['BKN','Ca-in-Opx','TA98','REE']
depletionTypes = ['Al2O3', 'MgO', 'ree']
dnames = ['Al<sub>2</sub>O<sub>3</sub>', 'MgO','REE']

module.exports = (el, callback)->
  console.log mergedData
  {size, innerSize, transform, x, y} = conventions {
    width: 500, height: 500, margin: 20}

  svg = d3.select(el)
    .append 'svg'
    .attr 'height', size.height
    .attr 'width', size.width
    .append 'g'
    .attr 'transform', transform

  splitPoint = 6/10


  temperature = xScale()
    .range [0,splitPoint].map(x)
    .domain thermometers

  depletion = xScale()
    .range [splitPoint,1].map(x)
    .domain depletionTypes

  ax = svg.append 'g.axes'
    .attr 'transform', "translate(0,#{innerSize.height})"

  xt = ax.append 'g.x.axis.temperature'
    .call d3.axisBottom(temperature)

  xd = ax.append 'g.x.axis.depletion'
    .call d3.axisBottom(depletion)

  tscale = y.copy().domain [920,1120]
  dscale = y.copy().domain [0,30]

  tdata = thermometers.map (d,i)->
    accessor = (v)->v.temperature[d].n
    scale = tscale
    loc = temperature(d)
    label = tnames[i]
    {accessor, scale, loc, label}

  ddata = depletionTypes.map (d,i)->
    accessor = (v)->v.depletion[d]
    scale = dscale
    loc = depletion(d)
    label = dnames[i]
    {accessor, scale, loc, label}

  dataTypes = tdata.concat(ddata)

  buildData = (d,i)->
    el = d3.select @
    console.log d

    lineData = d3.line()
      .x (v)->v.loc
      .y (v,i)->
        {accessor, scale} = v
        y = scale accessor(d)
        console.log y
        return y

    el.append 'path'
      .at
        d: lineData(dataTypes)
        'stroke': d.color
        'stroke-width': 2
        'fill': 'transparent'

  ### Plot data ###
  sel = svg.append 'g'
    .attr 'class', 'data'
    .selectAll 'g.sample'
    .data mergedData
    .enter()

  sel.append 'g'
    .attr 'class', 'sample'
    .each buildData

  callback()
