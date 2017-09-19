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


  lenTotal = mergedData.length

  x.domain [0,lenTotal]

  temperature = xScale()
    .range [0,thermometers.length-1].map(x)
    .domain thermometers

  depletion = xScale()
    .range [4,lenTotal].map(x)
    .domain depletionTypes

  tscale = y.copy().domain [920,1120]
  dscale = y.copy()
    .domain [0,20]
    .range [innerSize.height, 100]

  ax = svg.append 'g.axes'

  tax = d3.axisLeft(tscale)
    .ticks 5
    .tickSize 3
    .tickFormat d3.format('.0f')

  ax.append 'g.y.axis.temperature'
    .call tax

  tax = d3.axisRight(dscale)
    .ticks 5
    .tickSize 3
    .tickFormat d3.format('.0f')

  ax.append 'g.y.axis.depletion'
    .call tax
    .translate [innerSize.width,0]


  xAx = ax.append 'g.x'
    .translate [0,innerSize.height]

  xt = xAx.append 'g.axis.temperature'
    .call d3.axisBottom(temperature)

  xd = xAx.append 'g.axis.depletion'
    .call d3.axisBottom(depletion)

  tdata = thermometers.map (d,i)->
    accessor = (level=0)->
      (v)->
        a = v.temperature[d]
        T = a.n + a.s*level
        tscale(T)

    loc = temperature(d)
    label = tnames[i]
    {accessor, loc, label}

  ddata = depletionTypes.map (d,i)->
    accessor = (level=0)->(v)->
      dscale(v.depletion[d])
    loc = depletion(d)
    label = dnames[i]
    {accessor, loc, label}

  dataTypes = tdata.concat(ddata)

  dataAtProbability = (d,level=0)->(v,i)->
    return v.accessor(level)(d)

  lineData = (d)->
    _ = d3.line()
      .x (v)->v.loc
      .y dataAtProbability(d,0)
    _(dataTypes)

  agen = (level)->(d)->
    _ = d3.area()
      .x (v)->v.loc
      .y0 dataAtProbability(d,level)
      .y1 dataAtProbability(d,-level)
    _(dataTypes)

  buildData = (d,i)->
    el = d3.select @
    console.log d

    el.append 'path'
      .at
        d: lineData
        'stroke': d.color
        'stroke-width': 2
        'fill': 'transparent'

    el.append 'path'
      .attrs
        d: agen(1)
        fill: d.color
        'fill-opacity': 0.1

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
