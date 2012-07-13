/*
 Live.js - One script closer to Designing in the Browser
 Written for Handcraft.com by Martin Kool (@mrtnkl).

 Version 4.
 Recent change: Made stylesheet and mimetype checks case insensitive.

 http://livejs.com
 http://livejs.com/license (MIT)
 @livejs

 Include live.js#css to monitor css changes only.
 Include live.js#js to monitor js changes only.
 Include live.js#html to monitor html changes only.
 Mix and match to monitor a preferred combination such as live.js#html,css

 By default, just include live.js to monitor all css, js and html changes.

 Live.js can also be loaded as a bookmarklet. It is best to only use it for CSS then,
 as a page reload due to a change in html or css would not re-include the bookmarklet.
 To monitor CSS and be notified that it has loaded, include it as: live.js#css,notify
 */
(function () {

    var resources = {},
        currentLinkElements = {},
        oldLinkElements = {},
        interval = 1000,
        loaded = false,
        active = { "css":0, "js":0 },
        app = null,
        page_type_id = null,
        changesAPI = null,
        listAPI = null;

    var Live = {

        // performs a cycle per interval
        heartbeat:function () {
            if (document.body) {
                // make sure all resources are loaded on first activation
                if (!loaded) Live.loadResources();
                Live.checkForChanges();
            }
        },

        // loads all local css and js resources upon first activation
        loadResources:function () {
            changesAPI = app.root + app.api_root + "assets/changed/"
            listAPI = app.root + app.api_root + "assets/list/"
            resources = app.state_info.loaded_assets;
            // add rule for morphing between old and new css files
            var head = document.getElementsByTagName("head")[0],
                style = document.createElement("style"),
                rule = "transition: all .3s ease-out;"
            var css = [".livejs-loading * { ", rule, " -webkit-", rule, "-moz-", rule, "-o-", rule, "}"].join('');
            style.setAttribute("type", "text/css");
            head.appendChild(style);
            style.styleSheet ? style.styleSheet.cssText = css : style.appendChild(document.createTextNode(css));

            var documentLinks = document.getElementsByTagName("link")
            var linksMap = {};
            var linkMatcher = /stylesheet/i
            for (var i = 0, len = documentLinks.length; i < len; i++) {
                var documentLink = documentLinks[i];
                var href = documentLink.getAttribute("href", 2);
                var rel = documentLink.getAttribute("rel");
                if (rel.match(linkMatcher)) {
                    linksMap[href] = documentLink;
                }
            }

            var cssPacks = app.state_info.loaded_assets.css;
            for (var packName in cssPacks) {
                var linksUrl = cssPacks[packName];
                var currentLinks = currentLinkElements[packName] = {}
                for (var i = 0, len = linksUrl.length; i < len; i++) {
                    var linkUrl = linksUrl[i];
                    var linkElement = linksMap[linkUrl];
                    if (linkElement) {
                        currentLinks[linkUrl] = linkElement;
                    }
                }
            }

            // yep
            loaded = true;
        },

        // check all tracking resources for changes
        checkForChanges:function () {
            if (!active.js && !active.css) {
                setTimeout(Live.heartbeat, interval);
                return;
            }

            $.getJSON(changesAPI + page_type_id, function (data) {
                if (active.js) {
                    if (data.js.length > 0) {
                        Live.refreshResource("js");
                    }
                }
                if (active.css) {
                    for (var i = 0, len = data.css.length; i < len; i++) {
                        Live.refreshResource("css", data.css[i]);
                    }
                }
            });
        },

        // act upon a changed url of certain content type
        refreshResource:function (type, name) {
            switch (type.toLowerCase()) {
                // css files can be reloaded dynamically by replacing the link element
                case "css":
                    $.getJSON(listAPI + page_type_id, function (data) {
                        setTimeout(Live.heartbeat, 10);
                        oldLinkElements[name] = currentLinkElements[name];
                        var link, html, head, next;
                        for (var linkUrl in currentLinkElements[name]) {
                            link = currentLinkElements[name][linkUrl],
                                html = document.body.parentNode,
                                head = link.parentNode,
                                next = link.nextSibling
                            break;
                        }
                        var cssPacks = data.css;
                        for (var packName in cssPacks) {
                            var linksUrl = cssPacks[packName];
                            var currentLinks = currentLinkElements[packName] = {}
                            for (var i = 0, len = linksUrl.length; i < len; i++) {
                                var
                                    linkUrl = linksUrl[i],
                                    newLink = document.createElement("link");

                                html.className = html.className.replace(/\s*livejs\-loading/gi, '') + ' livejs-loading';
                                newLink.setAttribute("type", "text/css");
                                newLink.setAttribute("rel", "stylesheet");
                                newLink.setAttribute("href", linkUrl);
                                next ? head.insertBefore(newLink, next) : head.appendChild(newLink);
                                currentLinks[linkUrl] = newLink;
                            }

                        }
                        // schedule removal of the old link
                        Live.removeoldLinkElements();
                    });
                    break;

                // check if an html resource is our current url, then reload
                case "html":
                    break;

                // local javascript changes cause a reload as well
                case "js":
                    document.location.reload();
            }
        },

        // removes the old stylesheet rules only once the new one has finished loading
        removeoldLinkElements:function () {
            var pending = 0;
            for (var name in oldLinkElements) {
                var oldLinks = oldLinkElements[name];
                var currentLinks = currentLinkElements[name];
                for (var url in oldLinks) {
                    // if this sheet has any cssRules, delete the old link
                    try {
                        var
                            oldLink = oldLinks[url],
                            html = document.body.parentNode;
                        oldLink.parentNode.removeChild(oldLink);
                        delete oldLinks[url];
                        setTimeout(function () {
                            html.className = html.className.replace(/\s*livejs\-loading/gi, '');
                        }, 100);
                    } catch (e) {
                        pending++;
                    }
                    if (pending) setTimeout(Live.removeoldLinkElements, 50);
                }
            }
        }
    };

    /*
     // start listening
     if (document.location.protocol != "file:") {
     if (!window.liveJsLoaded)
     Live.heartbeat();

     window.liveJsLoaded = true;
     }
     else if (window.console)
     console.log("Live.js doesn't support the file protocol. It needs http.");
     */
    if (!window.$){
        return;
    }
    $(function () {
        app = window.app;
        if (!app)
            return
        page_type_id = app.state_info.current_page;

        function assetLoaded() {
            var assetTemplate = "<tr> <th colspan='2'><%= type %></th> </tr> <% _.each(_.keys(assets[type]), function(id){ var i = 0; _.each(assets[type][id], function(url){ %> <tr> <% if(i === 0) { %><td><%= id %></td> <% }else{ %> <td>&nbsp;</td> <% } %> <td><%= url %></td> </tr> <% i+=1; }); }); %> ";
            var template = _.template(assetTemplate);
            var $tbody = $("#pDebugAssetTable tbody")

            var html = "";
            html += template({assets:app.state_info.loaded_assets, type:'js'})
            html += template({assets:app.state_info.loaded_assets, type:'css'})

            $tbody.html(html);
        }

        function setCookie(c_name, value) {
            document.cookie = c_name + "=" + value;
        }

        function getCookie(c_name) {
            var i, x, y, ARRcookies = document.cookie.split(";");
            for (i = 0; i < ARRcookies.length; i++) {
                x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
                y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
                x = x.replace(/^\s+|\s+$/g, "");
                if (x == c_name) {
                    return unescape(y);
                }
            }
        }

        var cookiePrefix = "borobudur.live."
        var $form = $("form#pDebugAssetLive");
        var all = {"js":null, "css":null}
        for (var name in all) {
            var $checkbox = $("[name='" + name + "']", $form);
            var cookieVal = getCookie(cookiePrefix + name)
            $checkbox.attr("checked", cookieVal)
            var checked = $checkbox.attr("checked");
            active[name] = checked;

            $checkbox.change(function () {
                var checked = $(this).attr("checked");
                var name = $(this).attr("name");
                active[name] = checked;
                setCookie(cookiePrefix + name, checked, 20);
            });
        }
        assetLoaded();

        Live.heartbeat();
    });
})();
