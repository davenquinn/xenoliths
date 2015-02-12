###*
Classy - classy classes for JavaScript

:copyright: (c) 2011 by Armin Ronacher.
:license: BSD.
###
createClasses = ->
  usesSuper = (obj) ->
    not probe_super or /\B\$super\b/.test(obj.toString())

  # helper function to set the attribute of something to a value or
  #     removes it if the value is undefined.
  setOrUnset = (obj, key, value) ->
    if value is `undefined`
      delete obj[key]
    else
      obj[key] = value
    return

  # gets the own property of an object
  getOwnProperty = (obj, name) ->
    (if Object::hasOwnProperty.call(obj, name) then obj[name] else `undefined`)

  # instanciate a class without calling the constructor
  cheapNew = (cls) ->
    disable_constructor = true
    rv = new cls
    disable_constructor = false
    rv
  CLASSY_VERSION = "1.4"
  context = this
  old = context.Class
  disable_constructor = false
  probe_super = (->
    $super()
    return
  ).toString().indexOf("$super") > 0

  # the base class we export
  Class = ->


  # restore the global Class name and pass it to a function.  This allows
  #     different versions of the classy library to be used side by side and
  #     in combination with other libraries.
  Class.$noConflict = ->
    try
      setOrUnset context, "Class", old
    catch e

      # fix for IE that does not support delete on window
      context.Class = old
    Class


  # what version of classy are we using?
  Class.$classyVersion = CLASSY_VERSION

  # extend functionality
  Class.$extend = (properties) ->
    super_prototype = @::

    # disable constructors and instanciate prototype.  Because the
    #       prototype can't raise an exception when created, we are safe
    #       without a try/finally here.
    prototype = cheapNew(this)

    # copy all properties of the includes over if there are any
    if properties.__include__
      i = 0
      n = properties.__include__.length

      while i isnt n
        mixin = properties.__include__[i]
        for name of mixin
          value = getOwnProperty(mixin, name)
          prototype[name] = mixin[name]  if value isnt `undefined`
        ++i

    # copy class vars from the superclass
    properties.__classvars__ = properties.__classvars__ or {}
    if prototype.__classvars__
      for key of prototype.__classvars__
        continue

    # copy all properties over to the new prototype
    for name of properties
      value = getOwnProperty(properties, name)
      continue  if name is "__include__" or value is `undefined`
      prototype[name] = (if typeof value is "function" and usesSuper(value) then ((meth, name) ->
        ->
          old_super = getOwnProperty(this, "$super")
          @$super = super_prototype[name]
          try
            return meth.apply(this, arguments)
          finally
            setOrUnset this, "$super", old_super
          return
      )(value, name) else value)

    # dummy constructor
    rv = ->
      return  if disable_constructor
      proper_this = (if context is this then cheapNew(arguments.callee) else this)
      proper_this.__init__.apply proper_this, arguments  if proper_this.__init__
      proper_this.$class = rv
      proper_this


    # copy all class vars over of any
    for key of properties.__classvars__
      value = getOwnProperty(properties.__classvars__, key)
      rv[key] = value  if value isnt `undefined`

    # copy prototype and constructor over, reattach $extend and
    #       return the class
    rv:: = prototype
    rv.constructor = rv
    rv.$extend = Class.$extend
    rv.$withData = Class.$withData
    rv


  # instanciate with data functionality
  Class.$withData = (data) ->
    rv = cheapNew(this)
    for key of data
      value = getOwnProperty(data, key)
      rv[key] = value  if value isnt `undefined`
    rv

  Class

  # export the class
module.exports = createClasses()
