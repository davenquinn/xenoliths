const Visualizer = require('figment-ui').default;

const vz = new Visualizer({buildDir: `${__dirname}/build`});

vz.task('textures.pdf', '../sections/textures/generate/index.coffee')
  .task('model-time-slices.pdf', '../sections/cooling-scenarios/time-slices/index.coffee')
  .task('model-comparison.pdf', '../sections/cooling-scenarios/comparison/index.coffee')
  .task('model-timeline.pdf', '../sections/cooling-scenarios/timeline/index.coffee');

module.exports = vz
