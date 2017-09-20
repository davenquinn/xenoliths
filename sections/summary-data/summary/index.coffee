d3 = require 'd3-jetpack/build/d3v4+jetpack'
{readFileSync} = require 'fs'
{annotation} = require 'd3-svg-annotation'
conventions = require 'd3-conventions'
require './main.styl'

getJSON = (fn)->
  d = readFileSync require.resolve fn
  JSON.parse d.toString()

dpi = 72
sz = width: dpi*6.5, height: dpi*3
margin = {
  left: 0.4*dpi
  bottom: 0.38*dpi
  right: 0.5*dpi
  top: 0.05*dpi
}

data = getJSON "./temperature-summary.json"
depletionData = getJSON "./depletion-summary.json"

mergedData = for d in data
  temperature = d.core
  {id, color} = d
  depletion = depletionData.find (v)->v.sample_id == id
  {temperature, depletion, id, color}

xScale = ->
  d3.scaleBand()
    .paddingInner 0.6

thermometers = ['bkn','ca_opx_corr','ta98','ree']
tnames = ['BKN','Ca-in-Opx','TA98','HREE']
depletionTypes = ['Al2O3', 'MgO', 'ree']
dnames = ["Al<tspan class='sub'>2</tspan>O<tspan class='sub'>3</tspan>", 'MgO','REE']

module.exports = (el, callback)->
  console.log mergedData
  {size, innerSize, transform, x, y} = conventions { sz..., margin... }


  #innerSize.width -= 2*innerMargin

  svg = d3.select(el)
    .append 'svg'
    .attr 'height', size.height
    .attr 'width', size.width
    .append 'g'
    .attr 'transform', transform


  lenTotal = mergedData.length

  x.domain [0,lenTotal]

  temperature = xScale()
    .rangeRound [0,thermometers.length-1].map(x)
    .domain thermometers


  depletion = xScale()
    .range [4,lenTotal].map(x)
    .domain depletionTypes

  tscale = y.copy().domain [920,1120]
  dscale = y.copy()
    .domain [0,20]

  tdata = thermometers.map (id,i)->
    accessor = (level=0)->
      (v)->
        a = v.temperature[id]
        T = a.n + a.s*level
        tscale(T)

    scale = temperature
    loc = temperature(id)
    label = tnames[i]
    {id, accessor, loc, label, scale}

  ddata = depletionTypes.map (id,i)->
    accessor = (level=0)->(v)->
      dscale(v.depletion[id])
    scale = depletion
    loc = depletion(id)
    label = dnames[i]
    {id, accessor, loc, label, scale}

  dataTypes = tdata.concat(ddata)

  dataAtProbability = (d,level=0)->(v,i)->
    return v.accessor(level)(d)

  xLocs = (point)->
    {scale, loc} = point
    start = loc
    end = start+scale.bandwidth()
    {start,end}

  lineData = (d)->
    y = dataAtProbability(d,0)
    arr = []
    for pt in dataTypes
      {start,end} = xLocs(pt)
      y_ = y(pt)
      arr.push [start, y_]
      arr.push [end,y_]
    d3.line()(arr)

  agen = (level)->(d)->
    area = d3.area()
      .x (v)->v.x
      .y0 (v)->v.y0
      .y1 (v)->v.y1

    upper = dataAtProbability(d,level)
    lower = dataAtProbability(d,-level)
    arr = []
    for pt in dataTypes
      y0 = upper(pt)
      y1 = lower(pt)
      {start,end} = xLocs(pt)
      arr.push { x: start, y0, y1}
      arr.push { x: end, y0, y1}
    area(arr)

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

  ### Build axes ###

  ax = svg.append 'g.axes'

  tax = d3.axisLeft(tscale)
    .ticks 5
    .tickSize 3
    .tickFormat d3.format('.0f')

  ax.append 'g.y.axis.temperature'
    .call tax
    .append 'text.label'
      .text 'Temperature (°C)'
      .attrs 'transform': "translate(-20,#{innerSize.height/2}) rotate(-90)"

  tax = d3.axisRight(dscale)
    .ticks 5
    .tickSize 3
    .tickFormat d3.format('.0f')

  ax.append 'g.y.axis.depletion'
    .call tax
    .translate [innerSize.width,0]


  xAx = ax.append 'g.x'
    .translate [0,innerSize.height]

  sel = ax.append 'g.backdrop'
    .selectAll 'g.system'
    .data dataTypes
    .enter()

  s = sel.append 'g.system'
    .translate (d)->[d.loc,0]

  s.append 'rect.backdrop'
    .at
      width: (d)->d.scale.bandwidth()
      height: innerSize.height
      y: 0

  s.append 'text.system-label'
   .translate (d)->
      [d.scale.bandwidth()/2, innerSize.height+4]
   .html (d)->d.label

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
