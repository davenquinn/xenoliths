{Printer} = require 'pdf-printer'

printer = new Printer
  buildDir: "#{__dirname}/build"

printer
  #.task 'textures.pdf', '../sections/textures/generate'
  .task 'model-comparison.pdf', '../sections/cooling-scenarios/comparison'
  .task 'model-timeline.pdf', '../sections/cooling-scenarios/timeline'
  .task 'model-time-slices.pdf', '../sections/cooling-scenarios/time-slices'
module.exports = printer
