window.onload = function() {
    var currURL = document.URL.split('/').slice(-1)[0].split('#')[0];
    var selector = `nav#nav > ul > li > a[href="${currURL}"]`;
    var active = document.querySelector(selector);

    if (active == null)
        var active = document.querySelector('nav#nav > ul > li > a');

    active.parentNode.className = "active";
}