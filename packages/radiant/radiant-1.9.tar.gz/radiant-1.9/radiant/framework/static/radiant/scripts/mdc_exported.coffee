$(document).ready ->

    #drawer = new mdc.drawer.MDCTemporaryDrawer(document.querySelector('.mdc-drawer--temporary'));
    #document.querySelector('.menu').addEventListener('click', () => drawer.open = true);


    topAppBarElement = document.querySelector(".mdc-top-app-bar");
    topAppBar = new mdc.topAppBar.MDCTopAppBar(topAppBarElement);


    #$(document).on "click", ".menu", (event) ->

    $(".mdc-top-app-bar").on "MDCTopAppBar:nav", (event) ->


        if document.querySelector(".mdc-drawer--persistent")
            drawer = new mdc.drawer.MDCPersistentDrawer(document.querySelector(".mdc-drawer"))
            drawer.open = true


        if document.querySelector(".mdc-drawer--temprary")
            drawer = new mdc.drawer.MDCTemporaryDrawer(document.querySelector(".mdc-drawer"))
            drawer.open = true


        if document.querySelector(".mdc-drawer--permanent")
            drawer = new mdc.drawer.MDCPermanentDrawer(document.querySelector(".mdc-drawer"))
            drawer.open = true

