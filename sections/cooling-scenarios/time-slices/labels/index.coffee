d3 = require 'd3'
require 'd3-selection-multi'
_ = require 'underscore'

fs = require 'fs'

{axisTitles} = require './axis-labels'

addSantaLuciaConstraint = (scenario)->
  ly = scenario.layout
  # Add P-T constraints
  ax = ly.axes()[1]
  g = ax.plotArea().append 'g'

  g.datum {T: 715, z: 25}
  g.attrs
    class: 'constraint'
    transform: (d)->
      "translate(#{ax.scale.x(d.T)},#{ax.scale.y(d.z)})"
  g.append 'circle'
    .attrs
      r: 3
      fill: '#444'
  g.append 'foreignObject'
    .attrs
      x: 5
      y: -10
    .append 'xhtml:div'
      .text 'Santa Lucia'
      .attrs class: 'santa-lucia-label'

f = d3.format('.0f')

v = [30,65]
axisProfileLabels = (d,j)->
  sel = d3.select(@).selectAll 'g.data'

  sel.filter (d,i)->
      i == 0 or i >= sel.size()-2
    .each (d,i)->
      el = d3.select @
      u = el.select('use')
      t = "#{f(d.time)} Ma"

      createText = (t, opts={})->
        el.append 'text'
          .attrs
            fill: u.attr('stroke')
            dy: opts.dy or if i != 0 then -2 else 8
          .append 'textPath'
          .text t
          .attrs
            'xlink:href': u.attr('href')

      offs1 = v[j]-4*i**0.8
      createText(t)
        .attrs startOffset: "#{offs1}%"

      offs = 55-10*i**0.8
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
