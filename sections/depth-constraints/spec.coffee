printer = new Printer buildDir: "#{__dirname}/build"
printer.task 'ca-ol-pressures.temp.pdf', './add-xenoliths-area'
module.exports = printer
