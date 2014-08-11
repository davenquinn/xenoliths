$ = require("jquery")
Pages = require("../pages")

setPage = (page)->
    $(".page").remove()
    console.log(page)
    $("body").append(page)
    page.attr("class","page")
    page.afterAttach()

module.exports =
    "": ->
        console.log "Homepage"
        setPage(new Pages.Home)
    "/map": ->
        console.log "Map page"
        setPage(new Pages.Map)
