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

santaLuciaConstraint = (scenario)->
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

axisProfileLabels = (d,j)->
  sel = d3.select(@).selectAll 'g.data'
  v = [30,65]
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

__upl__ = (type)->(d,j)->
  if type == 'farallon'
    text = ['None',"6 Myr",'Instantaneous']
    indices = [0,3,4]
    labelIx = 0
    labelY = 16
    dy = [8,-3,5.5]
  else
    text = ['Instantaneous', "6 Myr"]
    indices = [0,3]
    labelIx = 1
    labelY = -26
    dy = [8,-3]

  sel = d3.select(@).selectAll 'g.data'
  sel.filter (d,i)->
      indices.includes i
    .each (d,i)->
      el = d3.select @
      u = el.select('use')

      createText = (t, opts={})->
        el.append 'text'
          .styles fill: u.attr('stroke')
          .attrs
            dy: opts.dy or if i != 0 then -3 else 8
          .append 'textPath'
          .html t
          .attrs
            'xlink:href': u.attr('href')

      offs = null
      if type == 'farallon'
        offs = 68-4*i**0.3
        if i == 2
          offs = 72
      else
        offs = 12+4*i**0.3

      te = text[i]
      t_ = createText(te, dy: dy[i])
        .attrs
          startOffset: "#{offs}%"
          class: 'slab-window-age'

      if type == 'farallon' and i == 2
        t_.style 'font-size', '0.55em'


      return unless i == labelIx
      t = "Duration of\nslab window\nheating"
      t.split('\n').forEach (t,i)->
        createText(t, dy: labelY+7*i)
          .attrs
            startOffset: "#{offs}%"
            class: 'slab-window-age label'
          .styles 'text-align': 'middle'

underplatingProfileLabels = (type)->(el)->
  if type == 'shallow'
    data = [false,true,false]
  else
    data = [false, false, false, true, false]
  axes = el.selectAll 'g.axis'
    .data data
    .filter (d)->d
    .each __upl__(type)


profileLabels = (el)->
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

underplatingConstraint = (scenario)->
  ## Eventually this should become labels of ages

module.exports = {
  santaLuciaConstraint
  createAgeLabels
  profileLabels
  underplatingConstraint
  underplatingProfileLabels
}
