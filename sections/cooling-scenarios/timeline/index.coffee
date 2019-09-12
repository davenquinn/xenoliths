_ = require 'underscore'
d3 = require 'd3'
require 'd3-selection-multi'
fs = require 'fs'
path = require 'path'
Promise = require 'bluebird'
require './main.styl'

modelColors = require '../shared/colors'
{subductionTypeClasses} = require '../shared/util'
{db, storedProcedure} = require '../shared/database'
axes = require 'd3-plot-area/src'
plotArea = require './plot-area'
ageLabels = require './age-labels'
legend = require './legend'
underplatingScale = require './underplating-scale'
yaml = require 'js-yaml'
fs = require 'fs'

ff = 'font-family': 'Helvetica Neue Light'

_ = fs.readFileSync "#{__dirname}/../scenarios.yaml"
scenarios = yaml.safeLoad _

dpi = 96
sz = width: dpi*6.5, height: dpi*4

fn = path.join __dirname,'query.sql'
sql = storedProcedure fn

getData = (scenario)->
  db.query(sql, [scenario.name])
    .then (d)->
      d.id = scenario.name
      d.title = scenario.title
      d.subtitle = scenario.subtitle or null
      d.limits = [
        d3.min d, (a)->a.trange[0]
        d3.max d, (a)->a.trange[1]]
      d.axSize = d.limits[1]-d.limits[0]
      console.log d
      return d

spacing = 350
spacingBottom = 100
offsY = 0

__makeOuterAxes = (data)->
  outerAxes = axes()
    .size sz
    .margin
      right: 0.4*dpi
      left: 0.15*dpi
      top: 0.32*dpi
      bottom: 0.4*dpi
  outerAxes.scale.x
    .domain [80,0]

  outerAxes.scale.y
    .domain [0, d3.sum(data,(d)->d.axSize)+2*spacing+spacingBottom]
  outerAxes.axes.x()
    .label 'Time before present (Ma)'
    .labelOffset 22
    .tickSize 4

  outerAxes.axes.y('right')
    .label 'Temperature (°C)'
    .labelOffset 30
    .despine()

  vscale = outerAxes.scale.y
  scaleDelta = (d)->vscale(0)-vscale(d)

  outerAxes.scaleDelta = scaleDelta
  outerAxes

createProfileDividers = (lineGenerator, color)->
  (d)->
    profiles = d.profile.map (a,i)->
      profile: a
      trange: [d.lower[i],d.upper[i]]
      time: d.time[i]

    profiles = profiles.filter (a)->a.profile

    sel = d3.select @
      .selectAll 'path'
      .data profiles

    sel.enter()
      .append 'path'
      .attrs
        stroke: modelColors(d).alpha(0.5).css()
        d: (d)->
          t = d.trange.map (a)->[d.time,a]
          lineGenerator(t)

 alpha = "ABCDEF"

createAxes = (outerAxes)->
  (data, i)->
    # Sort the dataset for predictability
    data.sort (a,b)->a.time[0] < b.time[0]

    el = d3.select @

    axsize =
      width: outerAxes.plotArea.size().width
      height: outerAxes.scaleDelta(data.axSize)

    ax = axes()
      .size axsize
      .position x: 0, y: offsY
      .margin 0
    ax.scale.x = outerAxes.scale.x
    ax.scale.y.domain data.limits

    ax.axes.y('right')
      .tickPadding 5
      .tickSize 3
      .ticks Math.floor(data.axSize/200)
      .tickFormat d3.format("i")
      .tickSizeOuter 0

    el.call ax
    offsY += axsize.height + outerAxes.scaleDelta(spacing)

    plt =  ax.plotArea()
    bkg = plt.append 'g'

    sel = plt
      .selectAll 'g.model-run'
      .data data

    enter = sel.enter()
      .append 'g'
        .attrs
          class: (d)->
            cls = "model-run #{d.name}"
            cls += subductionTypeClasses(d)
            return cls
        .each plotArea(ax)

    #enter.append 'g'
    #  .attrs class: 'profile'
    #  .each createProfileDividers(ax.line())

    h = "<tspan class='subfig-index'>#{alpha[i]}</tspan>
         <tspan>#{data.title}</tspan>"
    if data.subtitle?
      h += " <tspan class='subtitle'>#{data.subtitle}</tspan>"
    # Add title
    plt.append 'text'
      .html h
      .attrs
        class: 'title'
        x: if i == 0 then 2*dpi else 0
        dy: 10

    if data.id == 'forearc'
      labels = ageLabels(ax)
      #bkg.call labels.connectingLine(data)
      enter.each labels
      el.call labels.axisLabel(ax.scale.x(70)-30,104)

      el.append "text"
        .html "
          <tspan>Underplating at cessation</tspan>
          <tspan x=0 dy=8>of subduction</tspan>"
        .attrs
          class: 'axis-description'
          transform: "translate(#{ax.scale.x(30)} 164)"
          'text-anchor': 'start'
          fill: modelColors.scales.forearc(40)

      el.append "text"
        .html "
          <tspan>Cretaceous–Paleogene stalled-slab scenarios
          <tspan>do not correspond to a</tspan>
          <tspan x=0 dy=8>clear driver of underplating but share basic model structure
          with <tspan class='bold'>C</tspan></tspan>"
        .attrs
          class: 'axis-description'
          transform: "translate(#{ax.scale.x(70)} 187)"
          'text-anchor': 'start'
          fill: modelColors.scales.forearc(80)

    if data.id == 'farallon'
      enter
        .filter (d,c)->
          c==0
        .each ageLabels(ax)

      el.append "text"
        .html "
          <tspan>Rollback underplating after impact of</tspan>
          <tspan x=0 dy=8>Shatsky-conjugate LIP</tspan>"
        .attrs
          class: 'axis-description'
          transform: "translate(#{ax.scale.x(73)} 300)"
          'text-anchor': 'start'
          fill: modelColors.scales.farallon(160)

    if data.id != 'forearc'
      k = if data.id == 'farallon' then 80 else 30
      s = underplatingScale(ax)
        .label "Asthenosphere held at #{k} km"
      plt.append('g').call s

    if i == 1
      plt.append 'text'
        .text 'Monterey Plate'
        .attrs
          class: 'annotation monterey-plate'
          fill: modelColors.scales.forearc(30)
          transform: (d)->
            x = ax.scale.x(10)
            y = ax.scale.y(1340)
            "translate(#{x},#{y}) rotate(5)"

setupElement = (el, data)->
    g = el
      .attrs sz
      .append 'g'
      .attr 'class', 'outer'

    outerAxes = __makeOuterAxes(data)
    g.call outerAxes

    plt = outerAxes.plotArea()
    plt.selectAll 'g.axes'
      .data data
      .enter().append 'g'
        .attrs class: 'axes'
        .each createAxes(outerAxes)

    plt.call legend

func = (el_, opts, callback)->
  el = d3.select(el_).append 'svg'
  Promise.map scenarios, getData, concurrency: 1
    .then (data)->setupElement(el, data)
    .finally callback

module.exports = func
