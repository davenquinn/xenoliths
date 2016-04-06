module.exports = (ax)->
  (el)->
    el.append 'text'
      .attr
        class: 'oc-age'
        x: (d)->ax.scale.x(d.time[0])
        y: (d)->ax.scale.y(d.lower[0])
        dy: -2
        dx: -10
        'font-size': 6
        'font-family': 'Helvetica Neue Light Italic'
      .text (d)->
        n = d.start_time - d.subduction_time
        "#{n} Myr"

