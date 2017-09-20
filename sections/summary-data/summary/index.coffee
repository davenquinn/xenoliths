d3 = require 'd3-jetpack/build/d3v4+jetpack'
{readFileSync} = require 'fs'
{annotation} = require 'd3-svg-annotation'
conventions = require 'd3-conventions'
require './main.styl'

marginInner = 10
dpi = 96
sz = width: dpi*6.5, height: dpi*2.5
margin = {
  left: 0.4*dpi+marginInner
  bottom: 0.38*dpi
  right: 0.55*dpi+marginInner
  top: 0.05*dpi
}

data = require "./temperature-summary.json"
depletionData = require "./depletion-summary.json"
spinelCrData = require "./spinel-cr.json"

mergedData = for d in data
  temperature = d.core
  {id, color} = d
  depletion = depletionData.find (v)->v.sample_id == id
  depletion["hree"] = depletion["ree"]
  spinel = spinelCrData[id]
  {temperature, depletion, id, color, spinel}

xScale = ->
  d3.scaleBand()
    .paddingInner 0.6

thermometers = ['bkn','ca_opx_corr','ta98','ree']
tnames = ['BKN','Ca-in-Opx','TA98','REE']
depletionTypes = ['spinel_cr','Al2O3', 'MgO', 'hree']
dnames = [
  "<tspan dy=2>Spinel</tspan><tspan x=0 dy=12>Cr#</tspan>",
  "Al<tspan class='sub'>2</tspan>O<tspan class='sub'>3</tspan>",
  'MgO','HREE']

module.exports = (el, callback)->
  {size, innerSize,
   transform, x, y} = conventions { sz..., margin... }


  #innerSize.width -= 2*innerMargin

  svg = d3.select(el)
    .append 'svg'
    .attr 'height', size.height
    .attr 'width', size.width
    .append 'g'
    .attr 'transform', transform

  tscale = y.copy().domain [920,1120]
  dscale = y.copy()
    .domain [0,30]

  tdata = thermometers.map (id,i)->
    accessor = (level=0)->
      (v)->
        a = v.temperature[id]
        T = a.n + a.s*level
        tscale(T)

    label = tnames[i]
    {id, accessor, label}

  tdata.push {id: 'spacer'}

  ddata = depletionTypes.map (id,i)->
    if id == "spinel_cr"
      accessor = (level=0)->(v)->
        {cr_number, cr_number_std} = v.spinel
        dscale(cr_number+level*cr_number_std)
    else
      accessor = (level=0)->(v)->
        dscale(v.depletion[id])
    label = dnames[i]
    {id, accessor, label}

  dataTypes = tdata.concat(ddata)

  xScale = d3.scaleBand()
    .paddingInner 0.6
    .domain dataTypes.map (d)->d.id
    .range [0,innerSize.width]

  dataAtProbability = (d,level=0)->(v,i)->
    return v.accessor(level)(d)

  xLocs = (point)->
    {id} = point
    console.log id
    loc = xScale(id)
    console.log loc
    start = loc
    end = start+xScale.bandwidth()
    {start,end}

  lineData = (d)->
    y = dataAtProbability(d,0)
    arr = []
    for pt in dataTypes
      continue unless pt.accessor?
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
      continue unless pt.accessor?
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

    el.append 'path'
      .attrs
        d: agen(2)
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
    .translate [-marginInner,0]
    .append 'text.label'
      .text 'Temperature (°C)'
      .attrs 'transform': "translate(-20,#{innerSize.height/2}) rotate(-90)"

  tax = d3.axisRight(dscale)
    .ticks 5
    .tickSize 3
    .tickPadding 6
    .tickFormat d3.format('.0f')

  ax.append 'g.y.axis.depletion'
    .call tax
    .translate [innerSize.width+marginInner,0]
    .append 'text.label'
      .attrs 'transform': "translate(30,#{innerSize.height/2}) rotate(90)" 
      .tspans  ['Depletion degree (%)','Spinel Cr#'], 10

  xAx = ax.append 'g.x'
    .translate [0,innerSize.height]

  back = ax.append 'g.backdrop'

  _ = ["Thermometer","Modeled depletion"]
  v = dataTypes.map (d)->d.id
  ids = [v[0],v[6]]
  back.appendMany _, 'text.system-type-label'
    .html (d,i)->d
    .translate (v,i)->[xScale(ids[i]),innerSize.height+25]

  realDataTypes = dataTypes.filter (d)-> d.id != "spacer"

  sel = back.selectAll 'g.system'
    .data realDataTypes
    .enter()

  s = sel.append 'g.system'
    .translate (d)->[xScale(d.id),0]

  s.append 'rect.backdrop'
    .at
      width: (d)->xScale.bandwidth()
      height: innerSize.height
      y: 0

  s.append 'text.system-label'
   .translate (d)->
      [xScale.bandwidth()/2, innerSize.height+10]
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
