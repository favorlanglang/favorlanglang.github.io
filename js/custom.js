window.onload = function() {
    var selector = `nav#nav > ul > li > a[href="${document.URL.split('/').slice(-1)[0]}"]`
    var active = document.querySelector(selector);

    if (active == null)
        var active = document.querySelector('nav#nav > ul > li > a');

    active.parentNode.className = "active";
}