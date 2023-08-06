
########################################################################
class RDNT


    #----------------------------------------------------------------------
    open_url: (url_) ->

        console.log("open: #{url_}")

        $.get
            data: {"url": url_}
            url: "/rdnt/open_url/"
            success: (response) ->

                if not response.success
                    alert("Error opening #{url_}")



$(document).ready ->

    RDNT = new RDNT()


    $(document).on "click", ".RDNT-open_url", (event) ->
        event.preventDefault()
        url = $(@).attr("href")
        RDNT.open_url(url)


    #$(document).on "click", ".RDNT-ignore_link", (event) ->
        #event.preventDefault()
        ##event.stopPropagation()


