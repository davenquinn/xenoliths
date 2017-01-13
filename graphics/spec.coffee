{Printer} = require 'pdf-printer'
printer = new Printer buildDir: "#{__dirname}/build"

printer
  #.task 'textures.pdf', '../sections/textures/generate'
  #.task 'modal-mineralogy.pdf', '../sections/modal-mineralogy/generate'
  .task 'model-timeline.pdf', '../sections/cooling-scenarios/timeline'

module.exports = printer
