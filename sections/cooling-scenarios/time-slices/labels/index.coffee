d3 = require 'd3'
require 'd3-selection-multi'
_ = require 'underscore'
yaml = require "js-yaml"

fs = require 'fs'

f = fs.readFileSync __dirname+'/constraint-labels.yaml'
labelData = yaml.load f


{axisTitles} = require './axis-labels'

makeConstraint = (scale)->(d,i)->
  g = d3.select @
  g.attrs
    class: 'constraint'
    transform: "translate(#{scale.x(d.T)},#{scale.y(d.z)})"
  g.append 'rect'
    .attrs
      x: -2
      y: -2
      width: 4
      height: 4
      fill: '#888'
  g.append 'foreignObject'
    .attrs d.attrs
    .append 'xhtml:div'
      .text d.text
      .attrs class: d.class

addSantaLuciaConstraint = (scenario)->
  ly = scenario.layout

  axes = ly.axes()

  # Add P-T constraints
  sel = axes[1]
    .plotArea()
    .selectAll 'g.constraint'
    .data labelData

  sel.enter()
    .append 'g'
    .each makeConstraint(axes[1].scale)

f = d3.format('.0f')

v = [30,65]
axisProfileLabels = (d,j)->
  sel = d3.select(@).selectAll 'g.data'

  sel.filter (d,i)->
      i == 0 or i >= sel.size()-3
    .each (d,i)->
      el = d3.select @
      u = el.select('use')
      t = "#{f(d.time)} Ma"

      createText = (t, opts={})->
        el.append 'text'
          .styles fill: u.attr('stroke')
          .attrs
            dy: opts.dy or if i != 0 then -2 else 8
          .append 'textPath'
          .html t
          .attrs
            'xlink:href': u.attr('href')

      offs1 = v[j]-4-i**0.3

      createText(t)
        .attrs startOffset: "#{offs1}%"

      offs = 40-4*i**0.3
      if j == 0
        t = "#{f(d.start_time-d.time)} Myr"
        createText(t)
          .attrs
            startOffset: "#{offs}%"
            class: 'oc-age'

      if i == 0 and j == 0
        #t = "Time of\nsubduction"
        #t.split('\n').forEach (t,i)->
          #createText(t, dy: 16+7*i)
            #.attrs
              #startOffset: "#{offs1}%"
              #class: 'label'

        t = "Age of\noceanic crust"
        t.split('\n').forEach (t,i)->
          createText(t, dy: 16+7*i)
            .attrs
              startOffset: "#{offs}%"
              class: 'oc-age label'

      if i == 0
        val = if j==0 then "start" else "end"
        t = "<tspan>T</tspan><tspan class='label-subscript'>#{val}</tspan>"
        t.split('\n').forEach (t,i)->
          createText(t, dy: 16+7*i)
            .attrs
              startOffset: "#{offs1}%"
              class: 'label timestep'


addProfileLabels = (el)->
  axes = el.selectAll 'g.axis'
    .data [true,true,false]
    .filter (d)->d
    .each axisProfileLabels


titles =
  initial: "Underplating"
  'underplating-started': "Underplating"
  'before-subduction': "Subduction"
  final: "Final"

createAgeLabels = (axes, slices)->
  # prepare data
  data = _.zip(axes,slices)
    .map (d)->{ax: d[0], slice: d[1]}

  for d in data
    i = d.slice.id
    if i of titles
      d.title = titles[i]
    d.age = d.slice.age

    if i == 'final'
      d.age = "1.65 Ma"

  (el)->
    el.append 'div'
      .attrs class: 'axis-labels'
      .call axisTitles('h2', data, (d)->d.title)

    el.append 'div'
      .attrs class: 'age-labels'
      .call axisTitles('h3', data, (d)->d.age)

module.exports =
  santaLuciaConstraint: addSantaLuciaConstraint
  createAgeLabels: createAgeLabels
  profileLabels: addProfileLabels
