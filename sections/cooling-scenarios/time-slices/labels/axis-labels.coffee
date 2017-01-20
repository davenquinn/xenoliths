setupWidths = (data)->
  it = 0
  data.map (d)->
    sz = d.ax.node().getBBox()
    v = sz.x-it+2
    it += v+sz.width
    d.loc =
      width: sz.width
      'margin-left': v
    return d

existsFilter = (f)->(d)->f(d)?

createLabels = (tag, data, accessor)->
  # Setup basic labels for a tag type and accessor function
  (el)->
    __data = setupWidths(data.filter(existsFilter(accessor)))
    sel = el.selectAll tag
      .data __data
      .enter()
      .append tag
      .html accessor
      .styles (d)->d.loc

module.exports =
  axisTitles: createLabels
