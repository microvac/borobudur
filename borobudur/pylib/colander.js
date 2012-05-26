/* Zepto v1.0rc1 - polyfill zepto event detect fx ajax form touch - zeptojs.com/license */
(function(a){String.prototype.trim===a&&(String.prototype.trim=function(){return this.replace(/^\s+/,"").replace(/\s+$/,"")}),Array.prototype.reduce===a&&(Array.prototype.reduce=function(b){if(this===void 0||this===null)throw new TypeError;var c=Object(this),d=c.length>>>0,e=0,f;if(typeof b!="function")throw new TypeError;if(d==0&&arguments.length==1)throw new TypeError;if(arguments.length>=2)f=arguments[1];else do{if(e in c){f=c[e++];break}if(++e>=d)throw new TypeError}while(!0);while(e<d)e in c&&(f=b.call(a,f,c[e],e,c)),e++;return f})})();var Zepto=function(){function A(a){return v.call(a)=="[object Function]"}function B(a){return a instanceof Object}function C(b){var c,d;if(v.call(b)!=="[object Object]")return!1;d=A(b.constructor)&&b.constructor.prototype;if(!d||!hasOwnProperty.call(d,"isPrototypeOf"))return!1;for(c in b);return c===a||hasOwnProperty.call(b,c)}function D(a){return a instanceof Array}function E(a){return typeof a.length=="number"}function F(b){return b.filter(function(b){return b!==a&&b!==null})}function G(a){return a.length>0?[].concat.apply([],a):a}function H(a){return a.replace(/::/g,"/").replace(/([A-Z]+)([A-Z][a-z])/g,"$1_$2").replace(/([a-z\d])([A-Z])/g,"$1_$2").replace(/_/g,"-").toLowerCase()}function I(a){return a in i?i[a]:i[a]=new RegExp("(^|\\s)"+a+"(\\s|$)")}function J(a,b){return typeof b=="number"&&!k[H(a)]?b+"px":b}function K(a){var b,c;return h[a]||(b=g.createElement(a),g.body.appendChild(b),c=j(b,"").getPropertyValue("display"),b.parentNode.removeChild(b),c=="none"&&(c="block"),h[a]=c),h[a]}function L(b,d){return d===a?c(b):c(b).filter(d)}function M(a,b,c,d){return A(b)?b.call(a,c,d):b}function N(a,b,d){var e=a%2?b:b.parentNode;e?e.insertBefore(d,a?a==1?e.firstChild:a==2?b:null:b.nextSibling):c(d).remove()}function O(a,b){b(a);for(var c in a.childNodes)O(a.childNodes[c],b)}var a,b,c,d,e=[],f=e.slice,g=window.document,h={},i={},j=g.defaultView.getComputedStyle,k={"column-count":1,columns:1,"font-weight":1,"line-height":1,opacity:1,"z-index":1,zoom:1},l=/^\s*<(\w+|!)[^>]*>/,m=[1,3,8,9,11],n=["after","prepend","before","append"],o=g.createElement("table"),p=g.createElement("tr"),q={tr:g.createElement("tbody"),tbody:o,thead:o,tfoot:o,td:p,th:p,"*":g.createElement("div")},r=/complete|loaded|interactive/,s=/^\.([\w-]+)$/,t=/^#([\w-]+)$/,u=/^[\w-]+$/,v={}.toString,w={},x,y,z=g.createElement("div");return w.matches=function(a,b){if(!a||a.nodeType!==1)return!1;var c=a.webkitMatchesSelector||a.mozMatchesSelector||a.oMatchesSelector||a.matchesSelector;if(c)return c.call(a,b);var d,e=a.parentNode,f=!e;return f&&(e=z).appendChild(a),d=~w.qsa(e,b).indexOf(a),f&&z.removeChild(a),d},x=function(a){return a.replace(/-+(.)?/g,function(a,b){return b?b.toUpperCase():""})},y=function(a){return a.filter(function(b,c){return a.indexOf(b)==c})},w.fragment=function(b,d){d===a&&(d=l.test(b)&&RegExp.$1),d in q||(d="*");var e=q[d];return e.innerHTML=""+b,c.each(f.call(e.childNodes),function(){e.removeChild(this)})},w.Z=function(a,b){return a=a||[],a.__proto__=arguments.callee.prototype,a.selector=b||"",a},w.isZ=function(a){return a instanceof w.Z},w.init=function(b,d){if(!b)return w.Z();if(A(b))return c(g).ready(b);if(w.isZ(b))return b;var e;if(D(b))e=F(b);else if(C(b))e=[c.extend({},b)],b=null;else if(m.indexOf(b.nodeType)>=0||b===window)e=[b],b=null;else if(l.test(b))e=w.fragment(b.trim(),RegExp.$1),b=null;else{if(d!==a)return c(d).find(b);e=w.qsa(g,b)}return w.Z(e,b)},c=function(a,b){return w.init(a,b)},c.extend=function(c){return f.call(arguments,1).forEach(function(d){for(b in d)d[b]!==a&&(c[b]=d[b])}),c},w.qsa=function(a,b){var c;return a===g&&t.test(b)?(c=a.getElementById(RegExp.$1))?[c]:e:a.nodeType!==1&&a.nodeType!==9?e:f.call(s.test(b)?a.getElementsByClassName(RegExp.$1):u.test(b)?a.getElementsByTagName(b):a.querySelectorAll(b))},c.isFunction=A,c.isObject=B,c.isArray=D,c.isPlainObject=C,c.inArray=function(a,b,c){return e.indexOf.call(b,a,c)},c.trim=function(a){return a.trim()},c.uuid=0,c.map=function(a,b){var c,d=[],e,f;if(E(a))for(e=0;e<a.length;e++)c=b(a[e],e),c!=null&&d.push(c);else for(f in a)c=b(a[f],f),c!=null&&d.push(c);return G(d)},c.each=function(a,b){var c,d;if(E(a)){for(c=0;c<a.length;c++)if(b.call(a[c],c,a[c])===!1)return a}else for(d in a)if(b.call(a[d],d,a[d])===!1)return a;return a},c.fn={forEach:e.forEach,reduce:e.reduce,push:e.push,indexOf:e.indexOf,concat:e.concat,map:function(a){return c.map(this,function(b,c){return a.call(b,c,b)})},slice:function(){return c(f.apply(this,arguments))},ready:function(a){return r.test(g.readyState)?a(c):g.addEventListener("DOMContentLoaded",function(){a(c)},!1),this},get:function(b){return b===a?f.call(this):this[b]},toArray:function(){return this.get()},size:function(){return this.length},remove:function(){return this.each(function(){this.parentNode!=null&&this.parentNode.removeChild(this)})},each:function(a){return this.forEach(function(b,c){a.call(b,c,b)}),this},filter:function(a){return c([].filter.call(this,function(b){return w.matches(b,a)}))},add:function(a,b){return c(y(this.concat(c(a,b))))},is:function(a){return this.length>0&&w.matches(this[0],a)},not:function(b){var d=[];if(A(b)&&b.call!==a)this.each(function(a){b.call(this,a)||d.push(this)});else{var e=typeof b=="string"?this.filter(b):E(b)&&A(b.item)?f.call(b):c(b);this.forEach(function(a){e.indexOf(a)<0&&d.push(a)})}return c(d)},eq:function(a){return a===-1?this.slice(a):this.slice(a,+a+1)},first:function(){var a=this[0];return a&&!B(a)?a:c(a)},last:function(){var a=this[this.length-1];return a&&!B(a)?a:c(a)},find:function(a){var b;return this.length==1?b=w.qsa(this[0],a):b=this.map(function(){return w.qsa(this,a)}),c(b)},closest:function(a,b){var d=this[0];while(d&&!w.matches(d,a))d=d!==b&&d!==g&&d.parentNode;return c(d)},parents:function(a){var b=[],d=this;while(d.length>0)d=c.map(d,function(a){if((a=a.parentNode)&&a!==g&&b.indexOf(a)<0)return b.push(a),a});return L(b,a)},parent:function(a){return L(y(this.pluck("parentNode")),a)},children:function(a){return L(this.map(function(){return f.call(this.children)}),a)},siblings:function(a){return L(this.map(function(a,b){return f.call(b.parentNode.children).filter(function(a){return a!==b})}),a)},empty:function(){return this.each(function(){this.innerHTML=""})},pluck:function(a){return this.map(function(){return this[a]})},show:function(){return this.each(function(){this.style.display=="none"&&(this.style.display=null),j(this,"").getPropertyValue("display")=="none"&&(this.style.display=K(this.nodeName))})},replaceWith:function(a){return this.before(a).remove()},wrap:function(a){return this.each(function(){c(this).wrapAll(c(a)[0].cloneNode(!1))})},wrapAll:function(a){return this[0]&&(c(this[0]).before(a=c(a)),a.append(this)),this},unwrap:function(){return this.parent().each(function(){c(this).replaceWith(c(this).children())}),this},clone:function(){return c(this.map(function(){return this.cloneNode(!0)}))},hide:function(){return this.css("display","none")},toggle:function(b){return(b===a?this.css("display")=="none":b)?this.show():this.hide()},prev:function(){return c(this.pluck("previousElementSibling"))},next:function(){return c(this.pluck("nextElementSibling"))},html:function(b){return b===a?this.length>0?this[0].innerHTML:null:this.each(function(a){var d=this.innerHTML;c(this).empty().append(M(this,b,a,d))})},text:function(b){return b===a?this.length>0?this[0].textContent:null:this.each(function(){this.textContent=b})},attr:function(c,d){var e;return typeof c=="string"&&d===a?this.length==0||this[0].nodeType!==1?a:c=="value"&&this[0].nodeName=="INPUT"?this.val():!(e=this[0].getAttribute(c))&&c in this[0]?this[0][c]:e:this.each(function(a){if(this.nodeType!==1)return;if(B(c))for(b in c)this.setAttribute(b,c[b]);else this.setAttribute(c,M(this,d,a,this.getAttribute(c)))})},removeAttr:function(a){return this.each(function(){this.nodeType===1&&this.removeAttribute(a)})},prop:function(b,c){return c===a?this[0]?this[0][b]:a:this.each(function(a){this[b]=M(this,c,a,this[b])})},data:function(b,c){var d=this.attr("data-"+H(b),c);return d!==null?d:a},val:function(b){return b===a?this.length>0?this[0].value:a:this.each(function(a){this.value=M(this,b,a,this.value)})},offset:function(){if(this.length==0)return null;var a=this[0].getBoundingClientRect();return{left:a.left+window.pageXOffset,top:a.top+window.pageYOffset,width:a.width,height:a.height}},css:function(c,d){if(d===a&&typeof c=="string")return this.length==0?a:this[0].style[x(c)]||j(this[0],"").getPropertyValue(c);var e="";for(b in c)typeof c[b]=="string"&&c[b]==""?this.each(function(){this.style.removeProperty(H(b))}):e+=H(b)+":"+J(b,c[b])+";";return typeof c=="string"&&(d==""?this.each(function(){this.style.removeProperty(H(c))}):e=H(c)+":"+J(c,d)),this.each(function(){this.style.cssText+=";"+e})},index:function(a){return a?this.indexOf(c(a)[0]):this.parent().children().indexOf(this[0])},hasClass:function(a){return this.length<1?!1:I(a).test(this[0].className)},addClass:function(a){return this.each(function(b){d=[];var e=this.className,f=M(this,a,b,e);f.split(/\s+/g).forEach(function(a){c(this).hasClass(a)||d.push(a)},this),d.length&&(this.className+=(e?" ":"")+d.join(" "))})},removeClass:function(b){return this.each(function(c){if(b===a)return this.className="";d=this.className,M(this,b,c,d).split(/\s+/g).forEach(function(a){d=d.replace(I(a)," ")}),this.className=d.trim()})},toggleClass:function(b,d){return this.each(function(e){var f=M(this,b,e,this.className);(d===a?!c(this).hasClass(f):d)?c(this).addClass(f):c(this).removeClass(f)})}},["width","height"].forEach(function(b){c.fn[b]=function(d){var e,f=b.replace(/./,function(a){return a[0].toUpperCase()});return d===a?this[0]==window?window["inner"+f]:this[0]==g?g.documentElement["offset"+f]:(e=this.offset())&&e[b]:this.each(function(a){var e=c(this);e.css(b,M(this,d,a,e[b]()))})}}),n.forEach(function(a,b){c.fn[a]=function(){var a=c.map(arguments,function(a){return B(a)?a:w.fragment(a)});if(a.length<1)return this;var d=this.length,e=d>1,f=b<2;return this.each(function(c,g){for(var h=0;h<a.length;h++){var i=a[f?a.length-h-1:h];O(i,function(a){a.nodeName!=null&&a.nodeName.toUpperCase()==="SCRIPT"&&(!a.type||a.type==="text/javascript")&&window.eval.call(window,a.innerHTML)}),e&&c<d-1&&(i=i.cloneNode(!0)),N(b,g,i)}})},c.fn[b%2?a+"To":"insert"+(b?"Before":"After")]=function(b){return c(b)[a](this),this}}),w.Z.prototype=c.fn,w.camelize=x,w.uniq=y,c.zepto=w,c}();window.Zepto=Zepto,"$"in window||(window.$=Zepto),function(a){function f(a){return a._zid||(a._zid=d++)}function g(a,b,d,e){b=h(b);if(b.ns)var g=i(b.ns);return(c[f(a)]||[]).filter(function(a){return a&&(!b.e||a.e==b.e)&&(!b.ns||g.test(a.ns))&&(!d||f(a.fn)===f(d))&&(!e||a.sel==e)})}function h(a){var b=(""+a).split(".");return{e:b[0],ns:b.slice(1).sort().join(" ")}}function i(a){return new RegExp("(?:^| )"+a.replace(" "," .* ?")+"(?: |$)")}function j(b,c,d){a.isObject(b)?a.each(b,d):b.split(/\s/).forEach(function(a){d(a,c)})}function k(b,d,e,g,i,k){k=!!k;var l=f(b),m=c[l]||(c[l]=[]);j(d,e,function(c,d){var e=i&&i(d,c),f=e||d,j=function(a){var c=f.apply(b,[a].concat(a.data));return c===!1&&a.preventDefault(),c},l=a.extend(h(c),{fn:d,proxy:j,sel:g,del:e,i:m.length});m.push(l),b.addEventListener(l.e,j,k)})}function l(a,b,d,e){var h=f(a);j(b||"",d,function(b,d){g(a,b,d,e).forEach(function(b){delete c[h][b.i],a.removeEventListener(b.e,b.proxy,!1)})})}function p(b){var c=a.extend({originalEvent:b},b);return a.each(o,function(a,d){c[a]=function(){return this[d]=m,b[a].apply(b,arguments)},c[d]=n}),c}function q(a){if(!("defaultPrevented"in a)){a.defaultPrevented=!1;var b=a.preventDefault;a.preventDefault=function(){this.defaultPrevented=!0,b.call(this)}}}var b=a.zepto.qsa,c={},d=1,e={};e.click=e.mousedown=e.mouseup=e.mousemove="MouseEvents",a.event={add:k,remove:l},a.proxy=function(b,c){if(a.isFunction(b)){var d=function(){return b.apply(c,arguments)};return d._zid=f(b),d}if(typeof c=="string")return a.proxy(b[c],b);throw new TypeError("expected function")},a.fn.bind=function(a,b){return this.each(function(){k(this,a,b)})},a.fn.unbind=function(a,b){return this.each(function(){l(this,a,b)})},a.fn.one=function(a,b){return this.each(function(c,d){k(this,a,b,null,function(a,b){return function(){var c=a.apply(d,arguments);return l(d,b,a),c}})})};var m=function(){return!0},n=function(){return!1},o={preventDefault:"isDefaultPrevented",stopImmediatePropagation:"isImmediatePropagationStopped",stopPropagation:"isPropagationStopped"};a.fn.delegate=function(b,c,d){var e=!1;if(c=="blur"||c=="focus")a.iswebkit?c=c=="blur"?"focusout":c=="focus"?"focusin":c:e=!0;return this.each(function(f,g){k(g,c,d,b,function(c){return function(d){var e,f=a(d.target).closest(b,g).get(0);if(f)return e=a.extend(p(d),{currentTarget:f,liveFired:g}),c.apply(f,[e].concat([].slice.call(arguments,1)))}},e)})},a.fn.undelegate=function(a,b,c){return this.each(function(){l(this,b,c,a)})},a.fn.live=function(b,c){return a(document.body).delegate(this.selector,b,c),this},a.fn.die=function(b,c){return a(document.body).undelegate(this.selector,b,c),this},a.fn.on=function(b,c,d){return c==undefined||a.isFunction(c)?this.bind(b,c):this.delegate(c,b,d)},a.fn.off=function(b,c,d){return c==undefined||a.isFunction(c)?this.unbind(b,c):this.undelegate(c,b,d)},a.fn.trigger=function(b,c){return typeof b=="string"&&(b=a.Event(b)),q(b),b.data=c,this.each(function(){"dispatchEvent"in this&&this.dispatchEvent(b)})},a.fn.triggerHandler=function(b,c){var d,e;return this.each(function(f,h){d=p(typeof b=="string"?a.Event(b):b),d.data=c,d.target=h,a.each(g(h,b.type||b),function(a,b){e=b.proxy(d);if(d.isImmediatePropagationStopped())return!1})}),e},"focusin focusout load resize scroll unload click dblclick mousedown mouseup mousemove mouseover mouseout change select keydown keypress keyup error".split(" ").forEach(function(b){a.fn[b]=function(a){return this.bind(b,a)}}),["focus","blur"].forEach(function(b){a.fn[b]=function(a){if(a)this.bind(b,a);else if(this.length)try{this.get(0)[b]()}catch(c){}return this}}),a.Event=function(a,b){var c=document.createEvent(e[a]||"Events"),d=!0;if(b)for(var f in b)f=="bubbles"?d=!!b[f]:c[f]=b[f];return c.initEvent(a,d,!0,null,null,null,null,null,null,null,null,null,null,null,null),c}}(Zepto),function(a){function b(a){var b=this.os={},c=this.browser={},d=a.match(/WebKit\/([\d.]+)/),e=a.match(/(Android)\s+([\d.]+)/),f=a.match(/(iPad).*OS\s([\d_]+)/),g=!f&&a.match(/(iPhone\sOS)\s([\d_]+)/),h=a.match(/(webOS|hpwOS)[\s\/]([\d.]+)/),i=h&&a.match(/TouchPad/),j=a.match(/Kindle\/([\d.]+)/),k=a.match(/Silk\/([\d._]+)/),l=a.match(/(BlackBerry).*Version\/([\d.]+)/);if(c.webkit=!!d)c.version=d[1];e&&(b.android=!0,b.version=e[2]),g&&(b.ios=b.iphone=!0,b.version=g[2].replace(/_/g,".")),f&&(b.ios=b.ipad=!0,b.version=f[2].replace(/_/g,".")),h&&(b.webos=!0,b.version=h[2]),i&&(b.touchpad=!0),l&&(b.blackberry=!0,b.version=l[2]),j&&(b.kindle=!0,b.version=j[1]),k&&(c.silk=!0,c.version=k[1]),!k&&b.android&&a.match(/Kindle Fire/)&&(c.silk=!0)}b.call(a,navigator.userAgent),a.__detect=b}(Zepto),function(a,b){function l(a){return a.toLowerCase()}function m(a){return d?d+a:l(a)}var c="",d,e,f,g={Webkit:"webkit",Moz:"",O:"o",ms:"MS"},h=window.document,i=h.createElement("div"),j=/^((translate|rotate|scale)(X|Y|Z|3d)?|matrix(3d)?|perspective|skew(X|Y)?)$/i,k={};a.each(g,function(a,e){if(i.style[a+"TransitionProperty"]!==b)return c="-"+l(a)+"-",d=e,!1}),k[c+"transition-property"]=k[c+"transition-duration"]=k[c+"transition-timing-function"]=k[c+"animation-name"]=k[c+"animation-duration"]="",a.fx={off:d===b&&i.style.transitionProperty===b,cssPrefix:c,transitionEnd:m("TransitionEnd"),animationEnd:m("AnimationEnd")},a.fn.animate=function(b,c,d,e){return a.isObject(c)&&(d=c.easing,e=c.complete,c=c.duration),c&&(c/=1e3),this.anim(b,c,d,e)},a.fn.anim=function(d,e,f,g){var h,i={},l,m=this,n,o=a.fx.transitionEnd;e===b&&(e=.4),a.fx.off&&(e=0);if(typeof d=="string")i[c+"animation-name"]=d,i[c+"animation-duration"]=e+"s",o=a.fx.animationEnd;else{for(l in d)j.test(l)?(h||(h=[]),h.push(l+"("+d[l]+")")):i[l]=d[l];h&&(i[c+"transform"]=h.join(" ")),!a.fx.off&&typeof d=="object"&&(i[c+"transition-property"]=Object.keys(d).join(", "),i[c+"transition-duration"]=e+"s",i[c+"transition-timing-function"]=f||"linear")}return n=function(b){if(typeof b!="undefined"){if(b.target!==b.currentTarget)return;a(b.target).unbind(o,arguments.callee)}a(this).css(k),g&&g.call(this)},e>0&&this.bind(o,n),setTimeout(function(){m.css(i),e<=0&&setTimeout(function(){m.each(function(){n.call(this)})},0)},0),this},i=null}(Zepto),function($){function triggerAndReturn(a,b,c){var d=$.Event(b);return $(a).trigger(d,c),!d.defaultPrevented}function triggerGlobal(a,b,c,d){if(a.global)return triggerAndReturn(b||document,c,d)}function ajaxStart(a){a.global&&$.active++===0&&triggerGlobal(a,null,"ajaxStart")}function ajaxStop(a){a.global&&!--$.active&&triggerGlobal(a,null,"ajaxStop")}function ajaxBeforeSend(a,b){var c=b.context;if(b.beforeSend.call(c,a,b)===!1||triggerGlobal(b,c,"ajaxBeforeSend",[a,b])===!1)return!1;triggerGlobal(b,c,"ajaxSend",[a,b])}function ajaxSuccess(a,b,c){var d=c.context,e="success";c.success.call(d,a,e,b),triggerGlobal(c,d,"ajaxSuccess",[b,c,a]),ajaxComplete(e,b,c)}function ajaxError(a,b,c,d){var e=d.context;d.error.call(e,c,b,a),triggerGlobal(d,e,"ajaxError",[c,d,a]),ajaxComplete(b,c,d)}function ajaxComplete(a,b,c){var d=c.context;c.complete.call(d,b,a),triggerGlobal(c,d,"ajaxComplete",[b,c]),ajaxStop(c)}function empty(){}function mimeToDataType(a){return a&&(a==htmlType?"html":a==jsonType?"json":scriptTypeRE.test(a)?"script":xmlTypeRE.test(a)&&"xml")||"text"}function appendQuery(a,b){return(a+"&"+b).replace(/[&?]{1,2}/,"?")}function serializeData(a){isObject(a.data)&&(a.data=$.param(a.data)),a.data&&(!a.type||a.type.toUpperCase()=="GET")&&(a.url=appendQuery(a.url,a.data))}function serialize(a,b,c,d){var e=$.isArray(b);$.each(b,function(b,f){d&&(b=c?d:d+"["+(e?"":b)+"]"),!d&&e?a.add(f.name,f.value):(c?$.isArray(f):isObject(f))?serialize(a,f,c,b):a.add(b,f)})}var jsonpID=0,isObject=$.isObject,document=window.document,key,name,rscript=/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,scriptTypeRE=/^(?:text|application)\/javascript/i,xmlTypeRE=/^(?:text|application)\/xml/i,jsonType="application/json",htmlType="text/html",blankRE=/^\s*$/;$.active=0,$.ajaxJSONP=function(a){var b="jsonp"+ ++jsonpID,c=document.createElement("script"),d=function(){$(c).remove(),b in window&&(window[b]=empty),ajaxComplete("abort",e,a)},e={abort:d},f;return a.error&&(c.onerror=function(){e.abort(),a.error()}),window[b]=function(d){clearTimeout(f),$(c).remove(),delete window[b],ajaxSuccess(d,e,a)},serializeData(a),c.src=a.url.replace(/=\?/,"="+b),$("head").append(c),a.timeout>0&&(f=setTimeout(function(){e.abort(),ajaxComplete("timeout",e,a)},a.timeout)),e},$.ajaxSettings={type:"GET",beforeSend:empty,success:empty,error:empty,complete:empty,context:null,global:!0,xhr:function(){return new window.XMLHttpRequest},accepts:{script:"text/javascript, application/javascript",json:jsonType,xml:"application/xml, text/xml",html:htmlType,text:"text/plain"},crossDomain:!1,timeout:0},$.ajax=function(options){var settings=$.extend({},options||{});for(key in $.ajaxSettings)settings[key]===undefined&&(settings[key]=$.ajaxSettings[key]);ajaxStart(settings),settings.crossDomain||(settings.crossDomain=/^([\w-]+:)?\/\/([^\/]+)/.test(settings.url)&&RegExp.$2!=window.location.host);var dataType=settings.dataType,hasPlaceholder=/=\?/.test(settings.url);if(dataType=="jsonp"||hasPlaceholder)return hasPlaceholder||(settings.url=appendQuery(settings.url,"callback=?")),$.ajaxJSONP(settings);settings.url||(settings.url=window.location.toString()),serializeData(settings);var mime=settings.accepts[dataType],baseHeaders={},protocol=/^([\w-]+:)\/\//.test(settings.url)?RegExp.$1:window.location.protocol,xhr=$.ajaxSettings.xhr(),abortTimeout;settings.crossDomain||(baseHeaders["X-Requested-With"]="XMLHttpRequest"),mime&&(baseHeaders.Accept=mime,mime.indexOf(",")>-1&&(mime=mime.split(",",2)[0]),xhr.overrideMimeType&&xhr.overrideMimeType(mime));if(settings.contentType||settings.data&&settings.type.toUpperCase()!="GET")baseHeaders["Content-Type"]=settings.contentType||"application/x-www-form-urlencoded";settings.headers=$.extend(baseHeaders,settings.headers||{}),xhr.onreadystatechange=function(){if(xhr.readyState==4){clearTimeout(abortTimeout);var result,error=!1;if(xhr.status>=200&&xhr.status<300||xhr.status==304||xhr.status==0&&protocol=="file:"){dataType=dataType||mimeToDataType(xhr.getResponseHeader("content-type")),result=xhr.responseText;try{dataType=="script"?(1,eval)(result):dataType=="xml"?result=xhr.responseXML:dataType=="json"&&(result=blankRE.test(result)?null:JSON.parse(result))}catch(e){error=e}error?ajaxError(error,"parsererror",xhr,settings):ajaxSuccess(result,xhr,settings)}else ajaxError(null,"error",xhr,settings)}};var async="async"in settings?settings.async:!0;xhr.open(settings.type,settings.url,async);for(name in settings.headers)xhr.setRequestHeader(name,settings.headers[name]);return ajaxBeforeSend(xhr,settings)===!1?(xhr.abort(),!1):(settings.timeout>0&&(abortTimeout=setTimeout(function(){xhr.onreadystatechange=empty,xhr.abort(),ajaxError(null,"timeout",xhr,settings)},settings.timeout)),xhr.send(settings.data?settings.data:null),xhr)},$.get=function(a,b){return $.ajax({url:a,success:b})},$.post=function(a,b,c,d){return $.isFunction(b)&&(d=d||c,c=b,b=null),$.ajax({type:"POST",url:a,data:b,success:c,dataType:d})},$.getJSON=function(a,b){return $.ajax({url:a,success:b,dataType:"json"})},$.fn.load=function(a,b){if(!this.length)return this;var c=this,d=a.split(/\s/),e;return d.length>1&&(a=d[0],e=d[1]),$.get(a,function(a){c.html(e?$(document.createElement("div")).html(a.replace(rscript,"")).find(e).html():a),b&&b.call(c)}),this};var escape=encodeURIComponent;$.param=function(a,b){var c=[];return c.add=function(a,b){this.push(escape(a)+"="+escape(b))},serialize(c,a,b),c.join("&").replace("%20","+")}}(Zepto),function(a){a.fn.serializeArray=function(){var b=[],c;return a(Array.prototype.slice.call(this.get(0).elements)).each(function(){c=a(this);var d=c.attr("type");this.nodeName.toLowerCase()!="fieldset"&&!this.disabled&&d!="submit"&&d!="reset"&&d!="button"&&(d!="radio"&&d!="checkbox"||this.checked)&&b.push({name:c.attr("name"),value:c.val()})}),b},a.fn.serialize=function(){var a=[];return this.serializeArray().forEach(function(b){a.push(encodeURIComponent(b.name)+"="+encodeURIComponent(b.value))}),a.join("&")},a.fn.submit=function(b){if(b)this.bind("submit",b);else if(this.length){var c=a.Event("submit");this.eq(0).trigger(c),c.defaultPrevented||this.get(0).submit()}return this}}(Zepto),function(a){function d(a){return"tagName"in a?a:a.parentNode}function e(a,b,c,d){var e=Math.abs(a-b),f=Math.abs(c-d);return e>=f?a-b>0?"Left":"Right":c-d>0?"Up":"Down"}function h(){g=null,b.last&&(b.el.trigger("longTap"),b={})}function i(){g&&clearTimeout(g),g=null}var b={},c,f=750,g;a(document).ready(function(){var j,k;a(document.body).bind("touchstart",function(e){j=Date.now(),k=j-(b.last||j),b.el=a(d(e.touches[0].target)),c&&clearTimeout(c),b.x1=e.touches[0].pageX,b.y1=e.touches[0].pageY,k>0&&k<=250&&(b.isDoubleTap=!0),b.last=j,g=setTimeout(h,f)}).bind("touchmove",function(a){i(),b.x2=a.touches[0].pageX,b.y2=a.touches[0].pageY}).bind("touchend",function(a){i(),b.isDoubleTap?(b.el.trigger("doubleTap"),b={}):b.x2&&Math.abs(b.x1-b.x2)>30||b.y2&&Math.abs(b.y1-b.y2)>30?(b.el.trigger("swipe")&&b.el.trigger("swipe"+e(b.x1,b.x2,b.y1,b.y2)),b={}):"last"in b&&(b.el.trigger("tap"),c=setTimeout(function(){c=null,b.el.trigger("singleTap"),b={}},250))}).bind("touchcancel",function(){c&&clearTimeout(c),g&&clearTimeout(g),g=c=null,b={}})}),["swipe","swipeLeft","swipeRight","swipeUp","swipeDown","doubleTap","tap","singleTap","longTap"].forEach(function(b){a.fn[b]=function(a){return this.bind(b,a)}})}(Zepto);//     Underscore.js 1.3.3
//     (c) 2009-2012 Jeremy Ashkenas, DocumentCloud Inc.
//     Underscore is freely distributable under the MIT license.
//     Portions of Underscore are inspired or borrowed from Prototype,
//     Oliver Steele's Functional, and John Resig's Micro-Templating.
//     For all details and documentation:
//     http://documentcloud.github.com/underscore

(function() {

  // Baseline setup
  // --------------

  // Establish the root object, `window` in the browser, or `global` on the server.
  var root = this;

  // Save the previous value of the `_` variable.
  var previousUnderscore = root._;

  // Establish the object that gets returned to break out of a loop iteration.
  var breaker = {};

  // Save bytes in the minified (but not gzipped) version:
  var ArrayProto = Array.prototype, ObjProto = Object.prototype, FuncProto = Function.prototype;

  // Create quick reference variables for speed access to core prototypes.
  var slice            = ArrayProto.slice,
      unshift          = ArrayProto.unshift,
      toString         = ObjProto.toString,
      hasOwnProperty   = ObjProto.hasOwnProperty;

  // All **ECMAScript 5** native function implementations that we hope to use
  // are declared here.
  var
    nativeForEach      = ArrayProto.forEach,
    nativeMap          = ArrayProto.map,
    nativeReduce       = ArrayProto.reduce,
    nativeReduceRight  = ArrayProto.reduceRight,
    nativeFilter       = ArrayProto.filter,
    nativeEvery        = ArrayProto.every,
    nativeSome         = ArrayProto.some,
    nativeIndexOf      = ArrayProto.indexOf,
    nativeLastIndexOf  = ArrayProto.lastIndexOf,
    nativeIsArray      = Array.isArray,
    nativeKeys         = Object.keys,
    nativeBind         = FuncProto.bind;

  // Create a safe reference to the Underscore object for use below.
  var _ = function(obj) { return new wrapper(obj); };

  // Export the Underscore object for **Node.js**, with
  // backwards-compatibility for the old `require()` API. If we're in
  // the browser, add `_` as a global object via a string identifier,
  // for Closure Compiler "advanced" mode.
  if (typeof exports !== 'undefined') {
    if (typeof module !== 'undefined' && module.exports) {
      exports = module.exports = _;
    }
    exports._ = _;
  } else {
    root['_'] = _;
  }

  // Current version.
  _.VERSION = '1.3.3';

  // Collection Functions
  // --------------------

  // The cornerstone, an `each` implementation, aka `forEach`.
  // Handles objects with the built-in `forEach`, arrays, and raw objects.
  // Delegates to **ECMAScript 5**'s native `forEach` if available.
  var each = _.each = _.forEach = function(obj, iterator, context) {
    if (obj == null) return;
    if (nativeForEach && obj.forEach === nativeForEach) {
      obj.forEach(iterator, context);
    } else if (obj.length === +obj.length) {
      for (var i = 0, l = obj.length; i < l; i++) {
        if (i in obj && iterator.call(context, obj[i], i, obj) === breaker) return;
      }
    } else {
      for (var key in obj) {
        if (_.has(obj, key)) {
          if (iterator.call(context, obj[key], key, obj) === breaker) return;
        }
      }
    }
  };

  // Return the results of applying the iterator to each element.
  // Delegates to **ECMAScript 5**'s native `map` if available.
  _.map = _.collect = function(obj, iterator, context) {
    var results = [];
    if (obj == null) return results;
    if (nativeMap && obj.map === nativeMap) return obj.map(iterator, context);
    each(obj, function(value, index, list) {
      results[results.length] = iterator.call(context, value, index, list);
    });
    if (obj.length === +obj.length) results.length = obj.length;
    return results;
  };

  // **Reduce** builds up a single result from a list of values, aka `inject`,
  // or `foldl`. Delegates to **ECMAScript 5**'s native `reduce` if available.
  _.reduce = _.foldl = _.inject = function(obj, iterator, memo, context) {
    var initial = arguments.length > 2;
    if (obj == null) obj = [];
    if (nativeReduce && obj.reduce === nativeReduce) {
      if (context) iterator = _.bind(iterator, context);
      return initial ? obj.reduce(iterator, memo) : obj.reduce(iterator);
    }
    each(obj, function(value, index, list) {
      if (!initial) {
        memo = value;
        initial = true;
      } else {
        memo = iterator.call(context, memo, value, index, list);
      }
    });
    if (!initial) throw new TypeError('Reduce of empty array with no initial value');
    return memo;
  };

  // The right-associative version of reduce, also known as `foldr`.
  // Delegates to **ECMAScript 5**'s native `reduceRight` if available.
  _.reduceRight = _.foldr = function(obj, iterator, memo, context) {
    var initial = arguments.length > 2;
    if (obj == null) obj = [];
    if (nativeReduceRight && obj.reduceRight === nativeReduceRight) {
      if (context) iterator = _.bind(iterator, context);
      return initial ? obj.reduceRight(iterator, memo) : obj.reduceRight(iterator);
    }
    var reversed = _.toArray(obj).reverse();
    if (context && !initial) iterator = _.bind(iterator, context);
    return initial ? _.reduce(reversed, iterator, memo, context) : _.reduce(reversed, iterator);
  };

  // Return the first value which passes a truth test. Aliased as `detect`.
  _.find = _.detect = function(obj, iterator, context) {
    var result;
    any(obj, function(value, index, list) {
      if (iterator.call(context, value, index, list)) {
        result = value;
        return true;
      }
    });
    return result;
  };

  // Return all the elements that pass a truth test.
  // Delegates to **ECMAScript 5**'s native `filter` if available.
  // Aliased as `select`.
  _.filter = _.select = function(obj, iterator, context) {
    var results = [];
    if (obj == null) return results;
    if (nativeFilter && obj.filter === nativeFilter) return obj.filter(iterator, context);
    each(obj, function(value, index, list) {
      if (iterator.call(context, value, index, list)) results[results.length] = value;
    });
    return results;
  };

  // Return all the elements for which a truth test fails.
  _.reject = function(obj, iterator, context) {
    var results = [];
    if (obj == null) return results;
    each(obj, function(value, index, list) {
      if (!iterator.call(context, value, index, list)) results[results.length] = value;
    });
    return results;
  };

  // Determine whether all of the elements match a truth test.
  // Delegates to **ECMAScript 5**'s native `every` if available.
  // Aliased as `all`.
  _.every = _.all = function(obj, iterator, context) {
    var result = true;
    if (obj == null) return result;
    if (nativeEvery && obj.every === nativeEvery) return obj.every(iterator, context);
    each(obj, function(value, index, list) {
      if (!(result = result && iterator.call(context, value, index, list))) return breaker;
    });
    return !!result;
  };

  // Determine if at least one element in the object matches a truth test.
  // Delegates to **ECMAScript 5**'s native `some` if available.
  // Aliased as `any`.
  var any = _.some = _.any = function(obj, iterator, context) {
    iterator || (iterator = _.identity);
    var result = false;
    if (obj == null) return result;
    if (nativeSome && obj.some === nativeSome) return obj.some(iterator, context);
    each(obj, function(value, index, list) {
      if (result || (result = iterator.call(context, value, index, list))) return breaker;
    });
    return !!result;
  };

  // Determine if a given value is included in the array or object using `===`.
  // Aliased as `contains`.
  _.include = _.contains = function(obj, target) {
    var found = false;
    if (obj == null) return found;
    if (nativeIndexOf && obj.indexOf === nativeIndexOf) return obj.indexOf(target) != -1;
    found = any(obj, function(value) {
      return value === target;
    });
    return found;
  };

  // Invoke a method (with arguments) on every item in a collection.
  _.invoke = function(obj, method) {
    var args = slice.call(arguments, 2);
    return _.map(obj, function(value) {
      return (_.isFunction(method) ? method || value : value[method]).apply(value, args);
    });
  };

  // Convenience version of a common use case of `map`: fetching a property.
  _.pluck = function(obj, key) {
    return _.map(obj, function(value){ return value[key]; });
  };

  // Return the maximum element or (element-based computation).
  _.max = function(obj, iterator, context) {
    if (!iterator && _.isArray(obj) && obj[0] === +obj[0]) return Math.max.apply(Math, obj);
    if (!iterator && _.isEmpty(obj)) return -Infinity;
    var result = {computed : -Infinity};
    each(obj, function(value, index, list) {
      var computed = iterator ? iterator.call(context, value, index, list) : value;
      computed >= result.computed && (result = {value : value, computed : computed});
    });
    return result.value;
  };

  // Return the minimum element (or element-based computation).
  _.min = function(obj, iterator, context) {
    if (!iterator && _.isArray(obj) && obj[0] === +obj[0]) return Math.min.apply(Math, obj);
    if (!iterator && _.isEmpty(obj)) return Infinity;
    var result = {computed : Infinity};
    each(obj, function(value, index, list) {
      var computed = iterator ? iterator.call(context, value, index, list) : value;
      computed < result.computed && (result = {value : value, computed : computed});
    });
    return result.value;
  };

  // Shuffle an array.
  _.shuffle = function(obj) {
    var shuffled = [], rand;
    each(obj, function(value, index, list) {
      rand = Math.floor(Math.random() * (index + 1));
      shuffled[index] = shuffled[rand];
      shuffled[rand] = value;
    });
    return shuffled;
  };

  // Sort the object's values by a criterion produced by an iterator.
  _.sortBy = function(obj, val, context) {
    var iterator = _.isFunction(val) ? val : function(obj) { return obj[val]; };
    return _.pluck(_.map(obj, function(value, index, list) {
      return {
        value : value,
        criteria : iterator.call(context, value, index, list)
      };
    }).sort(function(left, right) {
      var a = left.criteria, b = right.criteria;
      if (a === void 0) return 1;
      if (b === void 0) return -1;
      return a < b ? -1 : a > b ? 1 : 0;
    }), 'value');
  };

  // Groups the object's values by a criterion. Pass either a string attribute
  // to group by, or a function that returns the criterion.
  _.groupBy = function(obj, val) {
    var result = {};
    var iterator = _.isFunction(val) ? val : function(obj) { return obj[val]; };
    each(obj, function(value, index) {
      var key = iterator(value, index);
      (result[key] || (result[key] = [])).push(value);
    });
    return result;
  };

  // Use a comparator function to figure out at what index an object should
  // be inserted so as to maintain order. Uses binary search.
  _.sortedIndex = function(array, obj, iterator) {
    iterator || (iterator = _.identity);
    var low = 0, high = array.length;
    while (low < high) {
      var mid = (low + high) >> 1;
      iterator(array[mid]) < iterator(obj) ? low = mid + 1 : high = mid;
    }
    return low;
  };

  // Safely convert anything iterable into a real, live array.
  _.toArray = function(obj) {
    if (!obj)                                     return [];
    if (_.isArray(obj))                           return slice.call(obj);
    if (_.isArguments(obj))                       return slice.call(obj);
    if (obj.toArray && _.isFunction(obj.toArray)) return obj.toArray();
    return _.values(obj);
  };

  // Return the number of elements in an object.
  _.size = function(obj) {
    return _.isArray(obj) ? obj.length : _.keys(obj).length;
  };

  // Array Functions
  // ---------------

  // Get the first element of an array. Passing **n** will return the first N
  // values in the array. Aliased as `head` and `take`. The **guard** check
  // allows it to work with `_.map`.
  _.first = _.head = _.take = function(array, n, guard) {
    return (n != null) && !guard ? slice.call(array, 0, n) : array[0];
  };

  // Returns everything but the last entry of the array. Especcialy useful on
  // the arguments object. Passing **n** will return all the values in
  // the array, excluding the last N. The **guard** check allows it to work with
  // `_.map`.
  _.initial = function(array, n, guard) {
    return slice.call(array, 0, array.length - ((n == null) || guard ? 1 : n));
  };

  // Get the last element of an array. Passing **n** will return the last N
  // values in the array. The **guard** check allows it to work with `_.map`.
  _.last = function(array, n, guard) {
    if ((n != null) && !guard) {
      return slice.call(array, Math.max(array.length - n, 0));
    } else {
      return array[array.length - 1];
    }
  };

  // Returns everything but the first entry of the array. Aliased as `tail`.
  // Especially useful on the arguments object. Passing an **index** will return
  // the rest of the values in the array from that index onward. The **guard**
  // check allows it to work with `_.map`.
  _.rest = _.tail = function(array, index, guard) {
    return slice.call(array, (index == null) || guard ? 1 : index);
  };

  // Trim out all falsy values from an array.
  _.compact = function(array) {
    return _.filter(array, function(value){ return !!value; });
  };

  // Return a completely flattened version of an array.
  _.flatten = function(array, shallow) {
    return _.reduce(array, function(memo, value) {
      if (_.isArray(value)) return memo.concat(shallow ? value : _.flatten(value));
      memo[memo.length] = value;
      return memo;
    }, []);
  };

  // Return a version of the array that does not contain the specified value(s).
  _.without = function(array) {
    return _.difference(array, slice.call(arguments, 1));
  };

  // Produce a duplicate-free version of the array. If the array has already
  // been sorted, you have the option of using a faster algorithm.
  // Aliased as `unique`.
  _.uniq = _.unique = function(array, isSorted, iterator) {
    var initial = iterator ? _.map(array, iterator) : array;
    var results = [];
    // The `isSorted` flag is irrelevant if the array only contains two elements.
    if (array.length < 3) isSorted = true;
    _.reduce(initial, function (memo, value, index) {
      if (isSorted ? _.last(memo) !== value || !memo.length : !_.include(memo, value)) {
        memo.push(value);
        results.push(array[index]);
      }
      return memo;
    }, []);
    return results;
  };

  // Produce an array that contains the union: each distinct element from all of
  // the passed-in arrays.
  _.union = function() {
    return _.uniq(_.flatten(arguments, true));
  };

  // Produce an array that contains every item shared between all the
  // passed-in arrays. (Aliased as "intersect" for back-compat.)
  _.intersection = _.intersect = function(array) {
    var rest = slice.call(arguments, 1);
    return _.filter(_.uniq(array), function(item) {
      return _.every(rest, function(other) {
        return _.indexOf(other, item) >= 0;
      });
    });
  };

  // Take the difference between one array and a number of other arrays.
  // Only the elements present in just the first array will remain.
  _.difference = function(array) {
    var rest = _.flatten(slice.call(arguments, 1), true);
    return _.filter(array, function(value){ return !_.include(rest, value); });
  };

  // Zip together multiple lists into a single array -- elements that share
  // an index go together.
  _.zip = function() {
    var args = slice.call(arguments);
    var length = _.max(_.pluck(args, 'length'));
    var results = new Array(length);
    for (var i = 0; i < length; i++) results[i] = _.pluck(args, "" + i);
    return results;
  };

  // If the browser doesn't supply us with indexOf (I'm looking at you, **MSIE**),
  // we need this function. Return the position of the first occurrence of an
  // item in an array, or -1 if the item is not included in the array.
  // Delegates to **ECMAScript 5**'s native `indexOf` if available.
  // If the array is large and already in sort order, pass `true`
  // for **isSorted** to use binary search.
  _.indexOf = function(array, item, isSorted) {
    if (array == null) return -1;
    var i, l;
    if (isSorted) {
      i = _.sortedIndex(array, item);
      return array[i] === item ? i : -1;
    }
    if (nativeIndexOf && array.indexOf === nativeIndexOf) return array.indexOf(item);
    for (i = 0, l = array.length; i < l; i++) if (i in array && array[i] === item) return i;
    return -1;
  };

  // Delegates to **ECMAScript 5**'s native `lastIndexOf` if available.
  _.lastIndexOf = function(array, item) {
    if (array == null) return -1;
    if (nativeLastIndexOf && array.lastIndexOf === nativeLastIndexOf) return array.lastIndexOf(item);
    var i = array.length;
    while (i--) if (i in array && array[i] === item) return i;
    return -1;
  };

  // Generate an integer Array containing an arithmetic progression. A port of
  // the native Python `range()` function. See
  // [the Python documentation](http://docs.python.org/library/functions.html#range).
  _.range = function(start, stop, step) {
    if (arguments.length <= 1) {
      stop = start || 0;
      start = 0;
    }
    step = arguments[2] || 1;

    var len = Math.max(Math.ceil((stop - start) / step), 0);
    var idx = 0;
    var range = new Array(len);

    while(idx < len) {
      range[idx++] = start;
      start += step;
    }

    return range;
  };

  // Function (ahem) Functions
  // ------------------

  // Reusable constructor function for prototype setting.
  var ctor = function(){};

  // Create a function bound to a given object (assigning `this`, and arguments,
  // optionally). Binding with arguments is also known as `curry`.
  // Delegates to **ECMAScript 5**'s native `Function.bind` if available.
  // We check for `func.bind` first, to fail fast when `func` is undefined.
  _.bind = function bind(func, context) {
    var bound, args;
    if (func.bind === nativeBind && nativeBind) return nativeBind.apply(func, slice.call(arguments, 1));
    if (!_.isFunction(func)) throw new TypeError;
    args = slice.call(arguments, 2);
    return bound = function() {
      if (!(this instanceof bound)) return func.apply(context, args.concat(slice.call(arguments)));
      ctor.prototype = func.prototype;
      var self = new ctor;
      var result = func.apply(self, args.concat(slice.call(arguments)));
      if (Object(result) === result) return result;
      return self;
    };
  };

  // Bind all of an object's methods to that object. Useful for ensuring that
  // all callbacks defined on an object belong to it.
  _.bindAll = function(obj) {
    var funcs = slice.call(arguments, 1);
    if (funcs.length == 0) funcs = _.functions(obj);
    each(funcs, function(f) { obj[f] = _.bind(obj[f], obj); });
    return obj;
  };

  // Memoize an expensive function by storing its results.
  _.memoize = function(func, hasher) {
    var memo = {};
    hasher || (hasher = _.identity);
    return function() {
      var key = hasher.apply(this, arguments);
      return _.has(memo, key) ? memo[key] : (memo[key] = func.apply(this, arguments));
    };
  };

  // Delays a function for the given number of milliseconds, and then calls
  // it with the arguments supplied.
  _.delay = function(func, wait) {
    var args = slice.call(arguments, 2);
    return setTimeout(function(){ return func.apply(null, args); }, wait);
  };

  // Defers a function, scheduling it to run after the current call stack has
  // cleared.
  _.defer = function(func) {
    return _.delay.apply(_, [func, 1].concat(slice.call(arguments, 1)));
  };

  // Returns a function, that, when invoked, will only be triggered at most once
  // during a given window of time.
  _.throttle = function(func, wait) {
    var context, args, timeout, throttling, more, result;
    var whenDone = _.debounce(function(){ more = throttling = false; }, wait);
    return function() {
      context = this; args = arguments;
      var later = function() {
        timeout = null;
        if (more) func.apply(context, args);
        whenDone();
      };
      if (!timeout) timeout = setTimeout(later, wait);
      if (throttling) {
        more = true;
      } else {
        result = func.apply(context, args);
      }
      whenDone();
      throttling = true;
      return result;
    };
  };

  // Returns a function, that, as long as it continues to be invoked, will not
  // be triggered. The function will be called after it stops being called for
  // N milliseconds. If `immediate` is passed, trigger the function on the
  // leading edge, instead of the trailing.
  _.debounce = function(func, wait, immediate) {
    var timeout;
    return function() {
      var context = this, args = arguments;
      var later = function() {
        timeout = null;
        if (!immediate) func.apply(context, args);
      };
      if (immediate && !timeout) func.apply(context, args);
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  };

  // Returns a function that will be executed at most one time, no matter how
  // often you call it. Useful for lazy initialization.
  _.once = function(func) {
    var ran = false, memo;
    return function() {
      if (ran) return memo;
      ran = true;
      return memo = func.apply(this, arguments);
    };
  };

  // Returns the first function passed as an argument to the second,
  // allowing you to adjust arguments, run code before and after, and
  // conditionally execute the original function.
  _.wrap = function(func, wrapper) {
    return function() {
      var args = [func].concat(slice.call(arguments, 0));
      return wrapper.apply(this, args);
    };
  };

  // Returns a function that is the composition of a list of functions, each
  // consuming the return value of the function that follows.
  _.compose = function() {
    var funcs = arguments;
    return function() {
      var args = arguments;
      for (var i = funcs.length - 1; i >= 0; i--) {
        args = [funcs[i].apply(this, args)];
      }
      return args[0];
    };
  };

  // Returns a function that will only be executed after being called N times.
  _.after = function(times, func) {
    if (times <= 0) return func();
    return function() {
      if (--times < 1) { return func.apply(this, arguments); }
    };
  };

  // Object Functions
  // ----------------

  // Retrieve the names of an object's properties.
  // Delegates to **ECMAScript 5**'s native `Object.keys`
  _.keys = nativeKeys || function(obj) {
    if (obj !== Object(obj)) throw new TypeError('Invalid object');
    var keys = [];
    for (var key in obj) if (_.has(obj, key)) keys[keys.length] = key;
    return keys;
  };

  // Retrieve the values of an object's properties.
  _.values = function(obj) {
    return _.map(obj, _.identity);
  };

  // Return a sorted list of the function names available on the object.
  // Aliased as `methods`
  _.functions = _.methods = function(obj) {
    var names = [];
    for (var key in obj) {
      if (_.isFunction(obj[key])) names.push(key);
    }
    return names.sort();
  };

  // Extend a given object with all the properties in passed-in object(s).
  _.extend = function(obj) {
    each(slice.call(arguments, 1), function(source) {
      for (var prop in source) {
        obj[prop] = source[prop];
      }
    });
    return obj;
  };

  // Return a copy of the object only containing the whitelisted properties.
  _.pick = function(obj) {
    var result = {};
    each(_.flatten(slice.call(arguments, 1)), function(key) {
      if (key in obj) result[key] = obj[key];
    });
    return result;
  };

  // Fill in a given object with default properties.
  _.defaults = function(obj) {
    each(slice.call(arguments, 1), function(source) {
      for (var prop in source) {
        if (obj[prop] == null) obj[prop] = source[prop];
      }
    });
    return obj;
  };

  // Create a (shallow-cloned) duplicate of an object.
  _.clone = function(obj) {
    if (!_.isObject(obj)) return obj;
    return _.isArray(obj) ? obj.slice() : _.extend({}, obj);
  };

  // Invokes interceptor with the obj, and then returns obj.
  // The primary purpose of this method is to "tap into" a method chain, in
  // order to perform operations on intermediate results within the chain.
  _.tap = function(obj, interceptor) {
    interceptor(obj);
    return obj;
  };

  // Internal recursive comparison function.
  function eq(a, b, stack) {
    // Identical objects are equal. `0 === -0`, but they aren't identical.
    // See the Harmony `egal` proposal: http://wiki.ecmascript.org/doku.php?id=harmony:egal.
    if (a === b) return a !== 0 || 1 / a == 1 / b;
    // A strict comparison is necessary because `null == undefined`.
    if (a == null || b == null) return a === b;
    // Unwrap any wrapped objects.
    if (a._chain) a = a._wrapped;
    if (b._chain) b = b._wrapped;
    // Invoke a custom `isEqual` method if one is provided.
    if (a.isEqual && _.isFunction(a.isEqual)) return a.isEqual(b);
    if (b.isEqual && _.isFunction(b.isEqual)) return b.isEqual(a);
    // Compare `[[Class]]` names.
    var className = toString.call(a);
    if (className != toString.call(b)) return false;
    switch (className) {
      // Strings, numbers, dates, and booleans are compared by value.
      case '[object String]':
        // Primitives and their corresponding object wrappers are equivalent; thus, `"5"` is
        // equivalent to `new String("5")`.
        return a == String(b);
      case '[object Number]':
        // `NaN`s are equivalent, but non-reflexive. An `egal` comparison is performed for
        // other numeric values.
        return a != +a ? b != +b : (a == 0 ? 1 / a == 1 / b : a == +b);
      case '[object Date]':
      case '[object Boolean]':
        // Coerce dates and booleans to numeric primitive values. Dates are compared by their
        // millisecond representations. Note that invalid dates with millisecond representations
        // of `NaN` are not equivalent.
        return +a == +b;
      // RegExps are compared by their source patterns and flags.
      case '[object RegExp]':
        return a.source == b.source &&
               a.global == b.global &&
               a.multiline == b.multiline &&
               a.ignoreCase == b.ignoreCase;
    }
    if (typeof a != 'object' || typeof b != 'object') return false;
    // Assume equality for cyclic structures. The algorithm for detecting cyclic
    // structures is adapted from ES 5.1 section 15.12.3, abstract operation `JO`.
    var length = stack.length;
    while (length--) {
      // Linear search. Performance is inversely proportional to the number of
      // unique nested structures.
      if (stack[length] == a) return true;
    }
    // Add the first object to the stack of traversed objects.
    stack.push(a);
    var size = 0, result = true;
    // Recursively compare objects and arrays.
    if (className == '[object Array]') {
      // Compare array lengths to determine if a deep comparison is necessary.
      size = a.length;
      result = size == b.length;
      if (result) {
        // Deep compare the contents, ignoring non-numeric properties.
        while (size--) {
          // Ensure commutative equality for sparse arrays.
          if (!(result = size in a == size in b && eq(a[size], b[size], stack))) break;
        }
      }
    } else {
      // Objects with different constructors are not equivalent.
      if ('constructor' in a != 'constructor' in b || a.constructor != b.constructor) return false;
      // Deep compare objects.
      for (var key in a) {
        if (_.has(a, key)) {
          // Count the expected number of properties.
          size++;
          // Deep compare each member.
          if (!(result = _.has(b, key) && eq(a[key], b[key], stack))) break;
        }
      }
      // Ensure that both objects contain the same number of properties.
      if (result) {
        for (key in b) {
          if (_.has(b, key) && !(size--)) break;
        }
        result = !size;
      }
    }
    // Remove the first object from the stack of traversed objects.
    stack.pop();
    return result;
  }

  // Perform a deep comparison to check if two objects are equal.
  _.isEqual = function(a, b) {
    return eq(a, b, []);
  };

  // Is a given array, string, or object empty?
  // An "empty" object has no enumerable own-properties.
  _.isEmpty = function(obj) {
    if (obj == null) return true;
    if (_.isArray(obj) || _.isString(obj)) return obj.length === 0;
    for (var key in obj) if (_.has(obj, key)) return false;
    return true;
  };

  // Is a given value a DOM element?
  _.isElement = function(obj) {
    return !!(obj && obj.nodeType == 1);
  };

  // Is a given value an array?
  // Delegates to ECMA5's native Array.isArray
  _.isArray = nativeIsArray || function(obj) {
    return toString.call(obj) == '[object Array]';
  };

  // Is a given variable an object?
  _.isObject = function(obj) {
    return obj === Object(obj);
  };

  // Is a given variable an arguments object?
  _.isArguments = function(obj) {
    return toString.call(obj) == '[object Arguments]';
  };
  if (!_.isArguments(arguments)) {
    _.isArguments = function(obj) {
      return !!(obj && _.has(obj, 'callee'));
    };
  }

  // Is a given value a function?
  _.isFunction = function(obj) {
    return toString.call(obj) == '[object Function]';
  };

  // Is a given value a string?
  _.isString = function(obj) {
    return toString.call(obj) == '[object String]';
  };

  // Is a given value a number?
  _.isNumber = function(obj) {
    return toString.call(obj) == '[object Number]';
  };

  // Is a given object a finite number?
  _.isFinite = function(obj) {
    return _.isNumber(obj) && isFinite(obj);
  };

  // Is the given value `NaN`?
  _.isNaN = function(obj) {
    // `NaN` is the only value for which `===` is not reflexive.
    return obj !== obj;
  };

  // Is a given value a boolean?
  _.isBoolean = function(obj) {
    return obj === true || obj === false || toString.call(obj) == '[object Boolean]';
  };

  // Is a given value a date?
  _.isDate = function(obj) {
    return toString.call(obj) == '[object Date]';
  };

  // Is the given value a regular expression?
  _.isRegExp = function(obj) {
    return toString.call(obj) == '[object RegExp]';
  };

  // Is a given value equal to null?
  _.isNull = function(obj) {
    return obj === null;
  };

  // Is a given variable undefined?
  _.isUndefined = function(obj) {
    return obj === void 0;
  };

  // Has own property?
  _.has = function(obj, key) {
    return hasOwnProperty.call(obj, key);
  };

  // Utility Functions
  // -----------------

  // Run Underscore.js in *noConflict* mode, returning the `_` variable to its
  // previous owner. Returns a reference to the Underscore object.
  _.noConflict = function() {
    root._ = previousUnderscore;
    return this;
  };

  // Keep the identity function around for default iterators.
  _.identity = function(value) {
    return value;
  };

  // Run a function **n** times.
  _.times = function (n, iterator, context) {
    for (var i = 0; i < n; i++) iterator.call(context, i);
  };

  // Escape a string for HTML interpolation.
  _.escape = function(string) {
    return (''+string).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;').replace(/\//g,'&#x2F;');
  };

  // If the value of the named property is a function then invoke it;
  // otherwise, return it.
  _.result = function(object, property) {
    if (object == null) return null;
    var value = object[property];
    return _.isFunction(value) ? value.call(object) : value;
  };

  // Add your own custom functions to the Underscore object, ensuring that
  // they're correctly added to the OOP wrapper as well.
  _.mixin = function(obj) {
    each(_.functions(obj), function(name){
      addToWrapper(name, _[name] = obj[name]);
    });
  };

  // Generate a unique integer id (unique within the entire client session).
  // Useful for temporary DOM ids.
  var idCounter = 0;
  _.uniqueId = function(prefix) {
    var id = idCounter++;
    return prefix ? prefix + id : id;
  };

  // By default, Underscore uses ERB-style template delimiters, change the
  // following template settings to use alternative delimiters.
  _.templateSettings = {
    evaluate    : /<%([\s\S]+?)%>/g,
    interpolate : /<%=([\s\S]+?)%>/g,
    escape      : /<%-([\s\S]+?)%>/g
  };

  // When customizing `templateSettings`, if you don't want to define an
  // interpolation, evaluation or escaping regex, we need one that is
  // guaranteed not to match.
  var noMatch = /.^/;

  // Certain characters need to be escaped so that they can be put into a
  // string literal.
  var escapes = {
    '\\': '\\',
    "'": "'",
    'r': '\r',
    'n': '\n',
    't': '\t',
    'u2028': '\u2028',
    'u2029': '\u2029'
  };

  for (var p in escapes) escapes[escapes[p]] = p;
  var escaper = /\\|'|\r|\n|\t|\u2028|\u2029/g;
  var unescaper = /\\(\\|'|r|n|t|u2028|u2029)/g;

  // Within an interpolation, evaluation, or escaping, remove HTML escaping
  // that had been previously added.
  var unescape = function(code) {
    return code.replace(unescaper, function(match, escape) {
      return escapes[escape];
    });
  };

  // JavaScript micro-templating, similar to John Resig's implementation.
  // Underscore templating handles arbitrary delimiters, preserves whitespace,
  // and correctly escapes quotes within interpolated code.
  _.template = function(text, data, settings) {
    settings = _.defaults(settings || {}, _.templateSettings);

    // Compile the template source, taking care to escape characters that
    // cannot be included in a string literal and then unescape them in code
    // blocks.
    var source = "__p+='" + text
      .replace(escaper, function(match) {
        return '\\' + escapes[match];
      })
      .replace(settings.escape || noMatch, function(match, code) {
        return "'+\n_.escape(" + unescape(code) + ")+\n'";
      })
      .replace(settings.interpolate || noMatch, function(match, code) {
        return "'+\n(" + unescape(code) + ")+\n'";
      })
      .replace(settings.evaluate || noMatch, function(match, code) {
        return "';\n" + unescape(code) + "\n;__p+='";
      }) + "';\n";

    // If a variable is not specified, place data values in local scope.
    if (!settings.variable) source = 'with(obj||{}){\n' + source + '}\n';

    source = "var __p='';" +
      "var print=function(){__p+=Array.prototype.join.call(arguments, '')};\n" +
      source + "return __p;\n";

    var render = new Function(settings.variable || 'obj', '_', source);
    if (data) return render(data, _);
    var template = function(data) {
      return render.call(this, data, _);
    };

    // Provide the compiled function source as a convenience for build time
    // precompilation.
    template.source = 'function(' + (settings.variable || 'obj') + '){\n' +
      source + '}';

    return template;
  };

  // Add a "chain" function, which will delegate to the wrapper.
  _.chain = function(obj) {
    return _(obj).chain();
  };

  // The OOP Wrapper
  // ---------------

  // If Underscore is called as a function, it returns a wrapped object that
  // can be used OO-style. This wrapper holds altered versions of all the
  // underscore functions. Wrapped objects may be chained.
  var wrapper = function(obj) { this._wrapped = obj; };

  // Expose `wrapper.prototype` as `_.prototype`
  _.prototype = wrapper.prototype;

  // Helper function to continue chaining intermediate results.
  var result = function(obj, chain) {
    return chain ? _(obj).chain() : obj;
  };

  // A method to easily add functions to the OOP wrapper.
  var addToWrapper = function(name, func) {
    wrapper.prototype[name] = function() {
      var args = slice.call(arguments);
      unshift.call(args, this._wrapped);
      return result(func.apply(_, args), this._chain);
    };
  };

  // Add all of the Underscore functions to the wrapper object.
  _.mixin(_);

  // Add all mutator Array functions to the wrapper.
  each(['pop', 'push', 'reverse', 'shift', 'sort', 'splice', 'unshift'], function(name) {
    var method = ArrayProto[name];
    wrapper.prototype[name] = function() {
      var wrapped = this._wrapped;
      method.apply(wrapped, arguments);
      var length = wrapped.length;
      if ((name == 'shift' || name == 'splice') && length === 0) delete wrapped[0];
      return result(wrapped, this._chain);
    };
  });

  // Add all accessor Array functions to the wrapper.
  each(['concat', 'join', 'slice'], function(name) {
    var method = ArrayProto[name];
    wrapper.prototype[name] = function() {
      return result(method.apply(this._wrapped, arguments), this._chain);
    };
  });

  // Start chaining a wrapped Underscore object.
  wrapper.prototype.chain = function() {
    this._chain = true;
    return this;
  };

  // Extracts the result from a wrapped and chained object.
  wrapper.prototype.value = function() {
    return this._wrapped;
  };

}).call(this);
//     Backbone.js 0.9.2

//     (c) 2010-2012 Jeremy Ashkenas, DocumentCloud Inc.
//     Backbone may be freely distributed under the MIT license.
//     For all details and documentation:
//     http://backbonejs.org

(function(){

  // Initial Setup
  // -------------

  // Save a reference to the global object (`window` in the browser, `global`
  // on the server).
  var root = this;

  // Save the previous value of the `Backbone` variable, so that it can be
  // restored later on, if `noConflict` is used.
  var previousBackbone = root.Backbone;

  // Create a local reference to slice/splice.
  var slice = Array.prototype.slice;
  var splice = Array.prototype.splice;

  // The top-level namespace. All public Backbone classes and modules will
  // be attached to this. Exported for both CommonJS and the browser.
  var Backbone;
  if (typeof exports !== 'undefined') {
    Backbone = exports;
  } else {
    Backbone = root.Backbone = {};
  }

  // Current version of the library. Keep in sync with `package.json`.
  Backbone.VERSION = '0.9.2';

  // Require Underscore, if we're on the server, and it's not already present.
  var _ = root._;
  if (!_ && (typeof require !== 'undefined')) _ = require('underscore');

  // For Backbone's purposes, jQuery, Zepto, or Ender owns the `$` variable.
  var $ = root.jQuery || root.Zepto || root.ender;

  // Set the JavaScript library that will be used for DOM manipulation and
  // Ajax calls (a.k.a. the `$` variable). By default Backbone will use: jQuery,
  // Zepto, or Ender; but the `setDomLibrary()` method lets you inject an
  // alternate JavaScript library (or a mock library for testing your views
  // outside of a browser).
  Backbone.setDomLibrary = function(lib) {
    $ = lib;
  };

  // Runs Backbone.js in *noConflict* mode, returning the `Backbone` variable
  // to its previous owner. Returns a reference to this Backbone object.
  Backbone.noConflict = function() {
    root.Backbone = previousBackbone;
    return this;
  };

  // Turn on `emulateHTTP` to support legacy HTTP servers. Setting this option
  // will fake `"PUT"` and `"DELETE"` requests via the `_method` parameter and
  // set a `X-Http-Method-Override` header.
  Backbone.emulateHTTP = false;

  // Turn on `emulateJSON` to support legacy servers that can't deal with direct
  // `application/json` requests ... will encode the body as
  // `application/x-www-form-urlencoded` instead and will send the model in a
  // form param named `model`.
  Backbone.emulateJSON = false;

  // Backbone.Events
  // -----------------

  // Regular expression used to split event strings
  var eventSplitter = /\s+/;

  // A module that can be mixed in to *any object* in order to provide it with
  // custom events. You may bind with `on` or remove with `off` callback functions
  // to an event; trigger`-ing an event fires all callbacks in succession.
  //
  //     var object = {};
  //     _.extend(object, Backbone.Events);
  //     object.on('expand', function(){ alert('expanded'); });
  //     object.trigger('expand');
  //
  var Events = Backbone.Events = {

    // Bind one or more space separated events, `events`, to a `callback`
    // function. Passing `"all"` will bind the callback to all events fired.
    on: function(events, callback, context) {

      var calls, event, node, tail, list;
      if (!callback) return this;
      events = events.split(eventSplitter);
      calls = this._callbacks || (this._callbacks = {});

      // Create an immutable callback list, allowing traversal during
      // modification.  The tail is an empty object that will always be used
      // as the next node.
      while (event = events.shift()) {
        list = calls[event];
        node = list ? list.tail : {};
        node.next = tail = {};
        node.context = context;
        node.callback = callback;
        calls[event] = {tail: tail, next: list ? list.next : node};
      }

      return this;
    },

    // Remove one or many callbacks. If `context` is null, removes all callbacks
    // with that function. If `callback` is null, removes all callbacks for the
    // event. If `events` is null, removes all bound callbacks for all events.
    off: function(events, callback, context) {
      var event, calls, node, tail, cb, ctx;

      // No events, or removing *all* events.
      if (!(calls = this._callbacks)) return;
      if (!(events || callback || context)) {
        delete this._callbacks;
        return this;
      }

      // Loop through the listed events and contexts, splicing them out of the
      // linked list of callbacks if appropriate.
      events = events ? events.split(eventSplitter) : _.keys(calls);
      while (event = events.shift()) {
        node = calls[event];
        delete calls[event];
        if (!node || !(callback || context)) continue;
        // Create a new list, omitting the indicated callbacks.
        tail = node.tail;
        while ((node = node.next) !== tail) {
          cb = node.callback;
          ctx = node.context;
          if ((callback && cb !== callback) || (context && ctx !== context)) {
            this.on(event, cb, ctx);
          }
        }
      }

      return this;
    },

    // Trigger one or many events, firing all bound callbacks. Callbacks are
    // passed the same arguments as `trigger` is, apart from the event name
    // (unless you're listening on `"all"`, which will cause your callback to
    // receive the true name of the event as the first argument).
    trigger: function(events) {
      var event, node, calls, tail, args, all, rest;
      if (!(calls = this._callbacks)) return this;
      all = calls.all;
      events = events.split(eventSplitter);
      rest = slice.call(arguments, 1);

      // For each event, walk through the linked list of callbacks twice,
      // first to trigger the event, then to trigger any `"all"` callbacks.
      while (event = events.shift()) {
        if (node = calls[event]) {
          tail = node.tail;
          while ((node = node.next) !== tail) {
            node.callback.apply(node.context || this, rest);
          }
        }
        if (node = all) {
          tail = node.tail;
          args = [event].concat(rest);
          while ((node = node.next) !== tail) {
            node.callback.apply(node.context || this, args);
          }
        }
      }

      return this;
    }

  };

  // Aliases for backwards compatibility.
  Events.bind   = Events.on;
  Events.unbind = Events.off;

  // Backbone.Model
  // --------------

  // Create a new model, with defined attributes. A client id (`cid`)
  // is automatically generated and assigned for you.
  var Model = Backbone.Model = function(attributes, options) {
    var defaults;
    attributes || (attributes = {});
    if (options && options.parse) attributes = this.parse(attributes);
    if (defaults = getValue(this, 'defaults')) {
      attributes = _.extend({}, defaults, attributes);
    }
    if (options && options.collection) this.collection = options.collection;
    this.attributes = {};
    this._escapedAttributes = {};
    this.cid = _.uniqueId('c');
    this.changed = {};
    this._silent = {};
    this._pending = {};
    this.set(attributes, {silent: true});
    // Reset change tracking.
    this.changed = {};
    this._silent = {};
    this._pending = {};
    this._previousAttributes = _.clone(this.attributes);
    this.initialize.apply(this, arguments);
  };

  // Attach all inheritable methods to the Model prototype.
  _.extend(Model.prototype, Events, {

    // A hash of attributes whose current and previous value differ.
    changed: null,

    // A hash of attributes that have silently changed since the last time
    // `change` was called.  Will become pending attributes on the next call.
    _silent: null,

    // A hash of attributes that have changed since the last `'change'` event
    // began.
    _pending: null,

    // The default name for the JSON `id` attribute is `"id"`. MongoDB and
    // CouchDB users may want to set this to `"_id"`.
    idAttribute: 'id',

    // Initialize is an empty function by default. Override it with your own
    // initialization logic.
    initialize: function(){},

    // Return a copy of the model's `attributes` object.
    toJSON: function(options) {
      return _.clone(this.attributes);
    },

    // Get the value of an attribute.
    get: function(attr) {
      return this.attributes[attr];
    },

    // Get the HTML-escaped value of an attribute.
    escape: function(attr) {
      var html;
      if (html = this._escapedAttributes[attr]) return html;
      var val = this.get(attr);
      return this._escapedAttributes[attr] = _.escape(val == null ? '' : '' + val);
    },

    // Returns `true` if the attribute contains a value that is not null
    // or undefined.
    has: function(attr) {
      return this.get(attr) != null;
    },

    // Set a hash of model attributes on the object, firing `"change"` unless
    // you choose to silence it.
    set: function(key, value, options) {
      var attrs, attr, val;

      // Handle both
      if (_.isObject(key) || key == null) {
        attrs = key;
        options = value;
      } else {
        attrs = {};
        attrs[key] = value;
      }

      // Extract attributes and options.
      options || (options = {});
      if (!attrs) return this;
      if (attrs instanceof Model) attrs = attrs.attributes;
      if (options.unset) for (attr in attrs) attrs[attr] = void 0;

      // Run validation.
      if (!this._validate(attrs, options)) return false;

      // Check for changes of `id`.
      if (this.idAttribute in attrs) this.id = attrs[this.idAttribute];

      var changes = options.changes = {};
      var now = this.attributes;
      var escaped = this._escapedAttributes;
      var prev = this._previousAttributes || {};

      // For each `set` attribute...
      for (attr in attrs) {
        val = attrs[attr];

        // If the new and current value differ, record the change.
        if (!_.isEqual(now[attr], val) || (options.unset && _.has(now, attr))) {
          delete escaped[attr];
          (options.silent ? this._silent : changes)[attr] = true;
        }

        // Update or delete the current value.
        options.unset ? delete now[attr] : now[attr] = val;

        // If the new and previous value differ, record the change.  If not,
        // then remove changes for this attribute.
        if (!_.isEqual(prev[attr], val) || (_.has(now, attr) != _.has(prev, attr))) {
          this.changed[attr] = val;
          if (!options.silent) this._pending[attr] = true;
        } else {
          delete this.changed[attr];
          delete this._pending[attr];
        }
      }

      // Fire the `"change"` events.
      if (!options.silent) this.change(options);
      return this;
    },

    // Remove an attribute from the model, firing `"change"` unless you choose
    // to silence it. `unset` is a noop if the attribute doesn't exist.
    unset: function(attr, options) {
      (options || (options = {})).unset = true;
      return this.set(attr, null, options);
    },

    // Clear all attributes on the model, firing `"change"` unless you choose
    // to silence it.
    clear: function(options) {
      (options || (options = {})).unset = true;
      return this.set(_.clone(this.attributes), options);
    },

    // Fetch the model from the server. If the server's representation of the
    // model differs from its current attributes, they will be overriden,
    // triggering a `"change"` event.
    fetch: function(options) {
      options = options ? _.clone(options) : {};
      var model = this;
      var success = options.success;
      options.success = function(resp, status, xhr) {
        if (!model.set(model.parse(resp, xhr), options)) return false;
        if (success) success(model, resp);
      };
      options.error = Backbone.wrapError(options.error, model, options);
      return (this.sync || Backbone.sync).call(this, 'read', this, options);
    },

    // Set a hash of model attributes, and sync the model to the server.
    // If the server returns an attributes hash that differs, the model's
    // state will be `set` again.
    save: function(key, value, options) {
      var attrs, current;

      // Handle both `("key", value)` and `({key: value})` -style calls.
      if (_.isObject(key) || key == null) {
        attrs = key;
        options = value;
      } else {
        attrs = {};
        attrs[key] = value;
      }
      options = options ? _.clone(options) : {};

      // If we're "wait"-ing to set changed attributes, validate early.
      if (options.wait) {
        if (!this._validate(attrs, options)) return false;
        current = _.clone(this.attributes);
      }

      // Regular saves `set` attributes before persisting to the server.
      var silentOptions = _.extend({}, options, {silent: true});
      if (attrs && !this.set(attrs, options.wait ? silentOptions : options)) {
        return false;
      }

      // After a successful server-side save, the client is (optionally)
      // updated with the server-side state.
      var model = this;
      var success = options.success;
      options.success = function(resp, status, xhr) {
        var serverAttrs = model.parse(resp, xhr);
        if (options.wait) {
          delete options.wait;
          serverAttrs = _.extend(attrs || {}, serverAttrs);
        }
        if (!model.set(serverAttrs, options)) return false;
        if (success) {
          success(model, resp);
        } else {
          model.trigger('sync', model, resp, options);
        }
      };

      // Finish configuring and sending the Ajax request.
      options.error = Backbone.wrapError(options.error, model, options);
      var method = this.isNew() ? 'create' : 'update';
      var xhr = (this.sync || Backbone.sync).call(this, method, this, options);
      if (options.wait) this.set(current, silentOptions);
      return xhr;
    },

    // Destroy this model on the server if it was already persisted.
    // Optimistically removes the model from its collection, if it has one.
    // If `wait: true` is passed, waits for the server to respond before removal.
    destroy: function(options) {
      options = options ? _.clone(options) : {};
      var model = this;
      var success = options.success;

      var triggerDestroy = function() {
        model.trigger('destroy', model, model.collection, options);
      };

      if (this.isNew()) {
        triggerDestroy();
        return false;
      }

      options.success = function(resp) {
        if (options.wait) triggerDestroy();
        if (success) {
          success(model, resp);
        } else {
          model.trigger('sync', model, resp, options);
        }
      };

      options.error = Backbone.wrapError(options.error, model, options);
      var xhr = (this.sync || Backbone.sync).call(this, 'delete', this, options);
      if (!options.wait) triggerDestroy();
      return xhr;
    },

    // Default URL for the model's representation on the server -- if you're
    // using Backbone's restful methods, override this to change the endpoint
    // that will be called.
    url: function() {
      var base = getValue(this, 'urlRoot') || getValue(this.collection, 'url') || urlError();
      if (this.isNew()) return base;
      return base + (base.charAt(base.length - 1) == '/' ? '' : '/') + encodeURIComponent(this.id);
    },

    // **parse** converts a response into the hash of attributes to be `set` on
    // the model. The default implementation is just to pass the response along.
    parse: function(resp, xhr) {
      return resp;
    },

    // Create a new model with identical attributes to this one.
    clone: function() {
      return new this.constructor(this.attributes);
    },

    // A model is new if it has never been saved to the server, and lacks an id.
    isNew: function() {
      return this.id == null;
    },

    // Call this method to manually fire a `"change"` event for this model and
    // a `"change:attribute"` event for each changed attribute.
    // Calling this will cause all objects observing the model to update.
    change: function(options) {
      options || (options = {});
      var changing = this._changing;
      this._changing = true;

      // Silent changes become pending changes.
      for (var attr in this._silent) this._pending[attr] = true;

      // Silent changes are triggered.
      var changes = _.extend({}, options.changes, this._silent);
      this._silent = {};
      for (var attr in changes) {
        this.trigger('change:' + attr, this, this.get(attr), options);
      }
      if (changing) return this;

      // Continue firing `"change"` events while there are pending changes.
      while (!_.isEmpty(this._pending)) {
        this._pending = {};
        this.trigger('change', this, options);
        // Pending and silent changes still remain.
        for (var attr in this.changed) {
          if (this._pending[attr] || this._silent[attr]) continue;
          delete this.changed[attr];
        }
        this._previousAttributes = _.clone(this.attributes);
      }

      this._changing = false;
      return this;
    },

    // Determine if the model has changed since the last `"change"` event.
    // If you specify an attribute name, determine if that attribute has changed.
    hasChanged: function(attr) {
      if (!arguments.length) return !_.isEmpty(this.changed);
      return _.has(this.changed, attr);
    },

    // Return an object containing all the attributes that have changed, or
    // false if there are no changed attributes. Useful for determining what
    // parts of a view need to be updated and/or what attributes need to be
    // persisted to the server. Unset attributes will be set to undefined.
    // You can also pass an attributes object to diff against the model,
    // determining if there *would be* a change.
    changedAttributes: function(diff) {
      if (!diff) return this.hasChanged() ? _.clone(this.changed) : false;
      var val, changed = false, old = this._previousAttributes;
      for (var attr in diff) {
        if (_.isEqual(old[attr], (val = diff[attr]))) continue;
        (changed || (changed = {}))[attr] = val;
      }
      return changed;
    },

    // Get the previous value of an attribute, recorded at the time the last
    // `"change"` event was fired.
    previous: function(attr) {
      if (!arguments.length || !this._previousAttributes) return null;
      return this._previousAttributes[attr];
    },

    // Get all of the attributes of the model at the time of the previous
    // `"change"` event.
    previousAttributes: function() {
      return _.clone(this._previousAttributes);
    },

    // Check if the model is currently in a valid state. It's only possible to
    // get into an *invalid* state if you're using silent changes.
    isValid: function() {
      return !this.validate(this.attributes);
    },

    // Run validation against the next complete set of model attributes,
    // returning `true` if all is well. If a specific `error` callback has
    // been passed, call that instead of firing the general `"error"` event.
    _validate: function(attrs, options) {
      if (options.silent || !this.validate) return true;
      attrs = _.extend({}, this.attributes, attrs);
      var error = this.validate(attrs, options);
      if (!error) return true;
      if (options && options.error) {
        options.error(this, error, options);
      } else {
        this.trigger('error', this, error, options);
      }
      return false;
    }

  });

  // Backbone.Collection
  // -------------------

  // Provides a standard collection class for our sets of models, ordered
  // or unordered. If a `comparator` is specified, the Collection will maintain
  // its models in sort order, as they're added and removed.
  var Collection = Backbone.Collection = function(models, options) {
    options || (options = {});
    if (options.model) this.model = options.model;
    if (options.comparator) this.comparator = options.comparator;
    this._reset();
    this.initialize.apply(this, arguments);
    if (models) this.reset(models, {silent: true, parse: options.parse});
  };

  // Define the Collection's inheritable methods.
  _.extend(Collection.prototype, Events, {

    // The default model for a collection is just a **Backbone.Model**.
    // This should be overridden in most cases.
    model: Model,

    // Initialize is an empty function by default. Override it with your own
    // initialization logic.
    initialize: function(){},

    // The JSON representation of a Collection is an array of the
    // models' attributes.
    toJSON: function(options) {
      return this.map(function(model){ return model.toJSON(options); });
    },

    // Add a model, or list of models to the set. Pass **silent** to avoid
    // firing the `add` event for every new model.
    add: function(models, options) {
      var i, index, length, model, cid, id, cids = {}, ids = {}, dups = [];
      options || (options = {});
      models = _.isArray(models) ? models.slice() : [models];

      // Begin by turning bare objects into model references, and preventing
      // invalid models or duplicate models from being added.
      for (i = 0, length = models.length; i < length; i++) {
        if (!(model = models[i] = this._prepareModel(models[i], options))) {
          throw new Error("Can't add an invalid model to a collection");
        }
        cid = model.cid;
        id = model.id;
        if (cids[cid] || this._byCid[cid] || ((id != null) && (ids[id] || this._byId[id]))) {
          dups.push(i);
          continue;
        }
        cids[cid] = ids[id] = model;
      }

      // Remove duplicates.
      i = dups.length;
      while (i--) {
        models.splice(dups[i], 1);
      }

      // Listen to added models' events, and index models for lookup by
      // `id` and by `cid`.
      for (i = 0, length = models.length; i < length; i++) {
        (model = models[i]).on('all', this._onModelEvent, this);
        this._byCid[model.cid] = model;
        if (model.id != null) this._byId[model.id] = model;
      }

      // Insert models into the collection, re-sorting if needed, and triggering
      // `add` events unless silenced.
      this.length += length;
      index = options.at != null ? options.at : this.models.length;
      splice.apply(this.models, [index, 0].concat(models));
      if (this.comparator) this.sort({silent: true});
      if (options.silent) return this;
      for (i = 0, length = this.models.length; i < length; i++) {
        if (!cids[(model = this.models[i]).cid]) continue;
        options.index = i;
        model.trigger('add', model, this, options);
      }
      return this;
    },

    // Remove a model, or a list of models from the set. Pass silent to avoid
    // firing the `remove` event for every model removed.
    remove: function(models, options) {
      var i, l, index, model;
      options || (options = {});
      models = _.isArray(models) ? models.slice() : [models];
      for (i = 0, l = models.length; i < l; i++) {
        model = this.getByCid(models[i]) || this.get(models[i]);
        if (!model) continue;
        delete this._byId[model.id];
        delete this._byCid[model.cid];
        index = this.indexOf(model);
        this.models.splice(index, 1);
        this.length--;
        if (!options.silent) {
          options.index = index;
          model.trigger('remove', model, this, options);
        }
        this._removeReference(model);
      }
      return this;
    },

    // Add a model to the end of the collection.
    push: function(model, options) {
      model = this._prepareModel(model, options);
      this.add(model, options);
      return model;
    },

    // Remove a model from the end of the collection.
    pop: function(options) {
      var model = this.at(this.length - 1);
      this.remove(model, options);
      return model;
    },

    // Add a model to the beginning of the collection.
    unshift: function(model, options) {
      model = this._prepareModel(model, options);
      this.add(model, _.extend({at: 0}, options));
      return model;
    },

    // Remove a model from the beginning of the collection.
    shift: function(options) {
      var model = this.at(0);
      this.remove(model, options);
      return model;
    },

    // Get a model from the set by id.
    get: function(id) {
      if (id == null) return void 0;
      return this._byId[id.id != null ? id.id : id];
    },

    // Get a model from the set by client id.
    getByCid: function(cid) {
      return cid && this._byCid[cid.cid || cid];
    },

    // Get the model at the given index.
    at: function(index) {
      return this.models[index];
    },

    // Return models with matching attributes. Useful for simple cases of `filter`.
    where: function(attrs) {
      if (_.isEmpty(attrs)) return [];
      return this.filter(function(model) {
        for (var key in attrs) {
          if (attrs[key] !== model.get(key)) return false;
        }
        return true;
      });
    },

    // Force the collection to re-sort itself. You don't need to call this under
    // normal circumstances, as the set will maintain sort order as each item
    // is added.
    sort: function(options) {
      options || (options = {});
      if (!this.comparator) throw new Error('Cannot sort a set without a comparator');
      var boundComparator = _.bind(this.comparator, this);
      if (this.comparator.length == 1) {
        this.models = this.sortBy(boundComparator);
      } else {
        this.models.sort(boundComparator);
      }
      if (!options.silent) this.trigger('reset', this, options);
      return this;
    },

    // Pluck an attribute from each model in the collection.
    pluck: function(attr) {
      return _.map(this.models, function(model){ return model.get(attr); });
    },

    // When you have more items than you want to add or remove individually,
    // you can reset the entire set with a new list of models, without firing
    // any `add` or `remove` events. Fires `reset` when finished.
    reset: function(models, options) {
      models  || (models = []);
      options || (options = {});
      for (var i = 0, l = this.models.length; i < l; i++) {
        this._removeReference(this.models[i]);
      }
      this._reset();
      this.add(models, _.extend({silent: true}, options));
      if (!options.silent) this.trigger('reset', this, options);
      return this;
    },

    // Fetch the default set of models for this collection, resetting the
    // collection when they arrive. If `add: true` is passed, appends the
    // models to the collection instead of resetting.
    fetch: function(options) {
      options = options ? _.clone(options) : {};
      if (options.parse === undefined) options.parse = true;
      var collection = this;
      var success = options.success;
      options.success = function(resp, status, xhr) {
        collection[options.add ? 'add' : 'reset'](collection.parse(resp, xhr), options);
        if (success) success(collection, resp);
      };
      options.error = Backbone.wrapError(options.error, collection, options);
      return (this.sync || Backbone.sync).call(this, 'read', this, options);
    },

    // Create a new instance of a model in this collection. Add the model to the
    // collection immediately, unless `wait: true` is passed, in which case we
    // wait for the server to agree.
    create: function(model, options) {
      var coll = this;
      options = options ? _.clone(options) : {};
      model = this._prepareModel(model, options);
      if (!model) return false;
      if (!options.wait) coll.add(model, options);
      var success = options.success;
      options.success = function(nextModel, resp, xhr) {
        if (options.wait) coll.add(nextModel, options);
        if (success) {
          success(nextModel, resp);
        } else {
          nextModel.trigger('sync', model, resp, options);
        }
      };
      model.save(null, options);
      return model;
    },

    // **parse** converts a response into a list of models to be added to the
    // collection. The default implementation is just to pass it through.
    parse: function(resp, xhr) {
      return resp;
    },

    // Proxy to _'s chain. Can't be proxied the same way the rest of the
    // underscore methods are proxied because it relies on the underscore
    // constructor.
    chain: function () {
      return _(this.models).chain();
    },

    // Reset all internal state. Called when the collection is reset.
    _reset: function(options) {
      this.length = 0;
      this.models = [];
      this._byId  = {};
      this._byCid = {};
    },

    // Prepare a model or hash of attributes to be added to this collection.
    _prepareModel: function(model, options) {
      options || (options = {});
      if (!(model instanceof Model)) {
        var attrs = model;
        options.collection = this;
        model = new this.model(attrs, options);
        if (!model._validate(model.attributes, options)) model = false;
      } else if (!model.collection) {
        model.collection = this;
      }
      return model;
    },

    // Internal method to remove a model's ties to a collection.
    _removeReference: function(model) {
      if (this == model.collection) {
        delete model.collection;
      }
      model.off('all', this._onModelEvent, this);
    },

    // Internal method called every time a model in the set fires an event.
    // Sets need to update their indexes when models change ids. All other
    // events simply proxy through. "add" and "remove" events that originate
    // in other collections are ignored.
    _onModelEvent: function(event, model, collection, options) {
      if ((event == 'add' || event == 'remove') && collection != this) return;
      if (event == 'destroy') {
        this.remove(model, options);
      }
      if (model && event === 'change:' + model.idAttribute) {
        delete this._byId[model.previous(model.idAttribute)];
        this._byId[model.id] = model;
      }
      this.trigger.apply(this, arguments);
    }

  });

  // Underscore methods that we want to implement on the Collection.
  var methods = ['forEach', 'each', 'map', 'reduce', 'reduceRight', 'find',
    'detect', 'filter', 'select', 'reject', 'every', 'all', 'some', 'any',
    'include', 'contains', 'invoke', 'max', 'min', 'sortBy', 'sortedIndex',
    'toArray', 'size', 'first', 'initial', 'rest', 'last', 'without', 'indexOf',
    'shuffle', 'lastIndexOf', 'isEmpty', 'groupBy'];

  // Mix in each Underscore method as a proxy to `Collection#models`.
  _.each(methods, function(method) {
    Collection.prototype[method] = function() {
      return _[method].apply(_, [this.models].concat(_.toArray(arguments)));
    };
  });

  // Backbone.Router
  // -------------------

  // Routers map faux-URLs to actions, and fire events when routes are
  // matched. Creating a new one sets its `routes` hash, if not set statically.
  var Router = Backbone.Router = function(options) {
    options || (options = {});
    if (options.routes) this.routes = options.routes;
    this._bindRoutes();
    this.initialize.apply(this, arguments);
  };

  // Cached regular expressions for matching named param parts and splatted
  // parts of route strings.
  var namedParam    = /:\w+/g;
  var splatParam    = /\*\w+/g;
  var escapeRegExp  = /[-[\]{}()+?.,\\^$|#\s]/g;

  // Set up all inheritable **Backbone.Router** properties and methods.
  _.extend(Router.prototype, Events, {

    // Initialize is an empty function by default. Override it with your own
    // initialization logic.
    initialize: function(){},

    // Manually bind a single named route to a callback. For example:
    //
    //     this.route('search/:query/p:num', 'search', function(query, num) {
    //       ...
    //     });
    //
    route: function(route, name, callback) {
      Backbone.history || (Backbone.history = new History);
      if (!_.isRegExp(route)) route = this._routeToRegExp(route);
      if (!callback) callback = this[name];
      Backbone.history.route(route, _.bind(function(fragment) {
        var args = this._extractParameters(route, fragment);
        callback && callback.apply(this, args);
        this.trigger.apply(this, ['route:' + name].concat(args));
        Backbone.history.trigger('route', this, name, args);
      }, this));
      return this;
    },

    // Simple proxy to `Backbone.history` to save a fragment into the history.
    navigate: function(fragment, options) {
      Backbone.history.navigate(fragment, options);
    },

    // Bind all defined routes to `Backbone.history`. We have to reverse the
    // order of the routes here to support behavior where the most general
    // routes can be defined at the bottom of the route map.
    _bindRoutes: function() {
      if (!this.routes) return;
      var routes = [];
      for (var route in this.routes) {
        routes.unshift([route, this.routes[route]]);
      }
      for (var i = 0, l = routes.length; i < l; i++) {
        this.route(routes[i][0], routes[i][1], this[routes[i][1]]);
      }
    },

    // Convert a route string into a regular expression, suitable for matching
    // against the current location hash.
    _routeToRegExp: function(route) {
      route = route.replace(escapeRegExp, '\\$&')
                   .replace(namedParam, '([^\/]+)')
                   .replace(splatParam, '(.*?)');
      return new RegExp('^' + route + '$');
    },

    // Given a route, and a URL fragment that it matches, return the array of
    // extracted parameters.
    _extractParameters: function(route, fragment) {
      return route.exec(fragment).slice(1);
    }

  });

  // Backbone.History
  // ----------------

  // Handles cross-browser history management, based on URL fragments. If the
  // browser does not support `onhashchange`, falls back to polling.
  var History = Backbone.History = function() {
    this.handlers = [];
    _.bindAll(this, 'checkUrl');
  };

  // Cached regex for cleaning leading hashes and slashes .
  var routeStripper = /^[#\/]/;

  // Cached regex for detecting MSIE.
  var isExplorer = /msie [\w.]+/;

  // Has the history handling already been started?
  History.started = false;

  // Set up all inheritable **Backbone.History** properties and methods.
  _.extend(History.prototype, Events, {

    // The default interval to poll for hash changes, if necessary, is
    // twenty times a second.
    interval: 50,

    // Gets the true hash value. Cannot use location.hash directly due to bug
    // in Firefox where location.hash will always be decoded.
    getHash: function(windowOverride) {
      var loc = windowOverride ? windowOverride.location : window.location;
      var match = loc.href.match(/#(.*)$/);
      return match ? match[1] : '';
    },

    // Get the cross-browser normalized URL fragment, either from the URL,
    // the hash, or the override.
    getFragment: function(fragment, forcePushState) {
      if (fragment == null) {
        if (this._hasPushState || forcePushState) {
          fragment = window.location.pathname;
          var search = window.location.search;
          if (search) fragment += search;
        } else {
          fragment = this.getHash();
        }
      }
      if (!fragment.indexOf(this.options.root)) fragment = fragment.substr(this.options.root.length);
      return fragment.replace(routeStripper, '');
    },

    // Start the hash change handling, returning `true` if the current URL matches
    // an existing route, and `false` otherwise.
    start: function(options) {
      if (History.started) throw new Error("Backbone.history has already been started");
      History.started = true;

      // Figure out the initial configuration. Do we need an iframe?
      // Is pushState desired ... is it available?
      this.options          = _.extend({}, {root: '/'}, this.options, options);
      this._wantsHashChange = this.options.hashChange !== false;
      this._wantsPushState  = !!this.options.pushState;
      this._hasPushState    = !!(this.options.pushState && window.history && window.history.pushState);
      var fragment          = this.getFragment();
      var docMode           = document.documentMode;
      var oldIE             = (isExplorer.exec(navigator.userAgent.toLowerCase()) && (!docMode || docMode <= 7));

      if (oldIE) {
        this.iframe = $('<iframe src="javascript:0" tabindex="-1" />').hide().appendTo('body')[0].contentWindow;
        this.navigate(fragment);
      }

      // Depending on whether we're using pushState or hashes, and whether
      // 'onhashchange' is supported, determine how we check the URL state.
      if (this._hasPushState) {
        $(window).bind('popstate', this.checkUrl);
      } else if (this._wantsHashChange && ('onhashchange' in window) && !oldIE) {
        $(window).bind('hashchange', this.checkUrl);
      } else if (this._wantsHashChange) {
        this._checkUrlInterval = setInterval(this.checkUrl, this.interval);
      }

      // Determine if we need to change the base url, for a pushState link
      // opened by a non-pushState browser.
      this.fragment = fragment;
      var loc = window.location;
      var atRoot  = loc.pathname == this.options.root;

      // If we've started off with a route from a `pushState`-enabled browser,
      // but we're currently in a browser that doesn't support it...
      if (this._wantsHashChange && this._wantsPushState && !this._hasPushState && !atRoot) {
        this.fragment = this.getFragment(null, true);
        window.location.replace(this.options.root + '#' + this.fragment);
        // Return immediately as browser will do redirect to new url
        return true;

      // Or if we've started out with a hash-based route, but we're currently
      // in a browser where it could be `pushState`-based instead...
      } else if (this._wantsPushState && this._hasPushState && atRoot && loc.hash) {
        this.fragment = this.getHash().replace(routeStripper, '');
        window.history.replaceState({}, document.title, loc.protocol + '//' + loc.host + this.options.root + this.fragment);
      }

      if (!this.options.silent) {
        return this.loadUrl();
      }
    },

    // Disable Backbone.history, perhaps temporarily. Not useful in a real app,
    // but possibly useful for unit testing Routers.
    stop: function() {
      $(window).unbind('popstate', this.checkUrl).unbind('hashchange', this.checkUrl);
      clearInterval(this._checkUrlInterval);
      History.started = false;
    },

    // Add a route to be tested when the fragment changes. Routes added later
    // may override previous routes.
    route: function(route, callback) {
      this.handlers.unshift({route: route, callback: callback});
    },

    // Checks the current URL to see if it has changed, and if it has,
    // calls `loadUrl`, normalizing across the hidden iframe.
    checkUrl: function(e) {
      var current = this.getFragment();
      if (current == this.fragment && this.iframe) current = this.getFragment(this.getHash(this.iframe));
      if (current == this.fragment) return false;
      if (this.iframe) this.navigate(current);
      this.loadUrl() || this.loadUrl(this.getHash());
    },

    // Attempt to load the current URL fragment. If a route succeeds with a
    // match, returns `true`. If no defined routes matches the fragment,
    // returns `false`.
    loadUrl: function(fragmentOverride) {
      var fragment = this.fragment = this.getFragment(fragmentOverride);
      var matched = _.any(this.handlers, function(handler) {
        if (handler.route.test(fragment)) {
          handler.callback(fragment);
          return true;
        }
      });
      return matched;
    },

    // Save a fragment into the hash history, or replace the URL state if the
    // 'replace' option is passed. You are responsible for properly URL-encoding
    // the fragment in advance.
    //
    // The options object can contain `trigger: true` if you wish to have the
    // route callback be fired (not usually desirable), or `replace: true`, if
    // you wish to modify the current URL without adding an entry to the history.
    navigate: function(fragment, options) {
      if (!History.started) return false;
      if (!options || options === true) options = {trigger: options};
      var frag = (fragment || '').replace(routeStripper, '');
      if (this.fragment == frag) return;

      // If pushState is available, we use it to set the fragment as a real URL.
      if (this._hasPushState) {
        if (frag.indexOf(this.options.root) != 0) frag = this.options.root + frag;
        this.fragment = frag;
        window.history[options.replace ? 'replaceState' : 'pushState']({}, document.title, frag);

      // If hash changes haven't been explicitly disabled, update the hash
      // fragment to store history.
      } else if (this._wantsHashChange) {
        this.fragment = frag;
        this._updateHash(window.location, frag, options.replace);
        if (this.iframe && (frag != this.getFragment(this.getHash(this.iframe)))) {
          // Opening and closing the iframe tricks IE7 and earlier to push a history entry on hash-tag change.
          // When replace is true, we don't want this.
          if(!options.replace) this.iframe.document.open().close();
          this._updateHash(this.iframe.location, frag, options.replace);
        }

      // If you've told us that you explicitly don't want fallback hashchange-
      // based history, then `navigate` becomes a page refresh.
      } else {
        window.location.assign(this.options.root + fragment);
      }
      if (options.trigger) this.loadUrl(fragment);
    },

    // Update the hash location, either replacing the current entry, or adding
    // a new one to the browser history.
    _updateHash: function(location, fragment, replace) {
      if (replace) {
        location.replace(location.toString().replace(/(javascript:|#).*$/, '') + '#' + fragment);
      } else {
        location.hash = fragment;
      }
    }
  });

  // Backbone.View
  // -------------

  // Creating a Backbone.View creates its initial element outside of the DOM,
  // if an existing element is not provided...
  var View = Backbone.View = function(options) {
    this.cid = _.uniqueId('view');
    this._configure(options || {});
    this._ensureElement();
    this.initialize.apply(this, arguments);
    this.delegateEvents();
  };

  // Cached regex to split keys for `delegate`.
  var delegateEventSplitter = /^(\S+)\s*(.*)$/;

  // List of view options to be merged as properties.
  var viewOptions = ['model', 'collection', 'el', 'id', 'attributes', 'className', 'tagName'];

  // Set up all inheritable **Backbone.View** properties and methods.
  _.extend(View.prototype, Events, {

    // The default `tagName` of a View's element is `"div"`.
    tagName: 'div',

    // jQuery delegate for element lookup, scoped to DOM elements within the
    // current view. This should be prefered to global lookups where possible.
    $: function(selector) {
      return this.$el.find(selector);
    },

    // Initialize is an empty function by default. Override it with your own
    // initialization logic.
    initialize: function(){},

    // **render** is the core function that your view should override, in order
    // to populate its element (`this.el`), with the appropriate HTML. The
    // convention is for **render** to always return `this`.
    render: function() {
      return this;
    },

    // Remove this view from the DOM. Note that the view isn't present in the
    // DOM by default, so calling this method may be a no-op.
    remove: function() {
      this.$el.remove();
      return this;
    },

    // For small amounts of DOM Elements, where a full-blown template isn't
    // needed, use **make** to manufacture elements, one at a time.
    //
    //     var el = this.make('li', {'class': 'row'}, this.model.escape('title'));
    //
    make: function(tagName, attributes, content) {
      var el = document.createElement(tagName);
      if (attributes) $(el).attr(attributes);
      if (content) $(el).html(content);
      return el;
    },

    // Change the view's element (`this.el` property), including event
    // re-delegation.
    setElement: function(element, delegate) {
      if (this.$el) this.undelegateEvents();
      this.$el = (element instanceof $) ? element : $(element);
      this.el = this.$el[0];
      if (delegate !== false) this.delegateEvents();
      return this;
    },

    // Set callbacks, where `this.events` is a hash of
    //
    // *{"event selector": "callback"}*
    //
    //     {
    //       'mousedown .title':  'edit',
    //       'click .button':     'save'
    //       'click .open':       function(e) { ... }
    //     }
    //
    // pairs. Callbacks will be bound to the view, with `this` set properly.
    // Uses event delegation for efficiency.
    // Omitting the selector binds the event to `this.el`.
    // This only works for delegate-able events: not `focus`, `blur`, and
    // not `change`, `submit`, and `reset` in Internet Explorer.
    delegateEvents: function(events) {
      if (!(events || (events = getValue(this, 'events')))) return;
      this.undelegateEvents();
      for (var key in events) {
        var method = events[key];
        if (!_.isFunction(method)) method = this[events[key]];
        if (!method) throw new Error('Method "' + events[key] + '" does not exist');
        var match = key.match(delegateEventSplitter);
        var eventName = match[1], selector = match[2];
        method = _.bind(method, this);
        eventName += '.delegateEvents' + this.cid;
        if (selector === '') {
          this.$el.bind(eventName, method);
        } else {
          this.$el.delegate(selector, eventName, method);
        }
      }
    },

    // Clears all callbacks previously bound to the view with `delegateEvents`.
    // You usually don't need to use this, but may wish to if you have multiple
    // Backbone views attached to the same DOM element.
    undelegateEvents: function() {
      this.$el.unbind('.delegateEvents' + this.cid);
    },

    // Performs the initial configuration of a View with a set of options.
    // Keys with special meaning *(model, collection, id, className)*, are
    // attached directly to the view.
    _configure: function(options) {
      if (this.options) options = _.extend({}, this.options, options);
      for (var i = 0, l = viewOptions.length; i < l; i++) {
        var attr = viewOptions[i];
        if (options[attr]) this[attr] = options[attr];
      }
      this.options = options;
    },

    // Ensure that the View has a DOM element to render into.
    // If `this.el` is a string, pass it through `$()`, take the first
    // matching element, and re-assign it to `el`. Otherwise, create
    // an element from the `id`, `className` and `tagName` properties.
    _ensureElement: function() {
      if (!this.el) {
        var attrs = getValue(this, 'attributes') || {};
        if (this.id) attrs.id = this.id;
        if (this.className) attrs['class'] = this.className;
        this.setElement(this.make(this.tagName, attrs), false);
      } else {
        this.setElement(this.el, false);
      }
    }

  });

  // The self-propagating extend function that Backbone classes use.
  var extend = function (protoProps, classProps) {
    var child = inherits(this, protoProps, classProps);
    child.extend = this.extend;
    return child;
  };

  // Set up inheritance for the model, collection, and view.
  Model.extend = Collection.extend = Router.extend = View.extend = extend;

  // Backbone.sync
  // -------------

  // Map from CRUD to HTTP for our default `Backbone.sync` implementation.
  var methodMap = {
    'create': 'POST',
    'update': 'PUT',
    'delete': 'DELETE',
    'read':   'GET'
  };

  // Override this function to change the manner in which Backbone persists
  // models to the server. You will be passed the type of request, and the
  // model in question. By default, makes a RESTful Ajax request
  // to the model's `url()`. Some possible customizations could be:
  //
  // * Use `setTimeout` to batch rapid-fire updates into a single request.
  // * Send up the models as XML instead of JSON.
  // * Persist models via WebSockets instead of Ajax.
  //
  // Turn on `Backbone.emulateHTTP` in order to send `PUT` and `DELETE` requests
  // as `POST`, with a `_method` parameter containing the true HTTP method,
  // as well as all requests with the body as `application/x-www-form-urlencoded`
  // instead of `application/json` with the model in a param named `model`.
  // Useful when interfacing with server-side languages like **PHP** that make
  // it difficult to read the body of `PUT` requests.
  Backbone.sync = function(method, model, options) {
    var type = methodMap[method];

    // Default options, unless specified.
    options || (options = {});

    // Default JSON-request options.
    var params = {type: type, dataType: 'json'};

    // Ensure that we have a URL.
    if (!options.url) {
      params.url = getValue(model, 'url') || urlError();
    }

    // Ensure that we have the appropriate request data.
    if (!options.data && model && (method == 'create' || method == 'update')) {
      params.contentType = 'application/json';
      params.data = JSON.stringify(model.toJSON());
    }

    // For older servers, emulate JSON by encoding the request into an HTML-form.
    if (Backbone.emulateJSON) {
      params.contentType = 'application/x-www-form-urlencoded';
      params.data = params.data ? {model: params.data} : {};
    }

    // For older servers, emulate HTTP by mimicking the HTTP method with `_method`
    // And an `X-HTTP-Method-Override` header.
    if (Backbone.emulateHTTP) {
      if (type === 'PUT' || type === 'DELETE') {
        if (Backbone.emulateJSON) params.data._method = type;
        params.type = 'POST';
        params.beforeSend = function(xhr) {
          xhr.setRequestHeader('X-HTTP-Method-Override', type);
        };
      }
    }

    // Don't process data on a non-GET request.
    if (params.type !== 'GET' && !Backbone.emulateJSON) {
      params.processData = false;
    }

    // Make the request, allowing the user to override any Ajax options.
    return $.ajax(_.extend(params, options));
  };

  // Wrap an optional error callback with a fallback error event.
  Backbone.wrapError = function(onError, originalModel, options) {
    return function(model, resp) {
      resp = model === originalModel ? resp : model;
      if (onError) {
        onError(originalModel, resp, options);
      } else {
        originalModel.trigger('error', originalModel, resp, options);
      }
    };
  };

  // Helpers
  // -------

  // Shared empty constructor function to aid in prototype-chain creation.
  var ctor = function(){};

  // Helper function to correctly set up the prototype chain, for subclasses.
  // Similar to `goog.inherits`, but uses a hash of prototype properties and
  // class properties to be extended.
  var inherits = function(parent, protoProps, staticProps) {
    var child;

    // The constructor function for the new subclass is either defined by you
    // (the "constructor" property in your `extend` definition), or defaulted
    // by us to simply call the parent's constructor.
    if (protoProps && protoProps.hasOwnProperty('constructor')) {
      child = protoProps.constructor;
    } else {
      child = function(){ parent.apply(this, arguments); };
    }

    // Inherit class (static) properties from parent.
    _.extend(child, parent);

    // Set the prototype chain to inherit from `parent`, without calling
    // `parent`'s constructor function.
    ctor.prototype = parent.prototype;
    child.prototype = new ctor();

    // Add prototype properties (instance properties) to the subclass,
    // if supplied.
    if (protoProps) _.extend(child.prototype, protoProps);

    // Add static properties to the constructor function, if supplied.
    if (staticProps) _.extend(child, staticProps);

    // Correctly set child's `prototype.constructor`.
    child.prototype.constructor = child;

    // Set a convenience property in case the parent's prototype is needed later.
    child.__super__ = parent.prototype;

    return child;
  };

  // Helper function to get a value from a Backbone object as a property
  // or as a function.
  var getValue = function(object, prop) {
    if (!(object && object[prop])) return null;
    return _.isFunction(object[prop]) ? object[prop]() : object[prop];
  };

  // Throw an error when a URL is needed, and none is supplied.
  var urlError = function() {
    throw new Error('A "url" property or function must be specified');
  };

}).call(this);
(function(){
    var root = this;
    var prambanan = root.prambanan = {};
    var helpers = prambanan.helpers = {};
    var builtins = {};
    var slice = Array.prototype.slice;
    /*
     Module import and exports
     */
    _.extend(prambanan, (function(){
        var modules = {};
        function Module(){};
        var dotNotateModule = function(s){
            var splitted = s.split(".");
            var current = modules;
            for(var i = 0; i < splitted.length; i++){
                var key = splitted[i];
                if(_.isUndefined(modules[key])){
                    modules[key] = new Module();
                }
                current = modules[key];
            }
            return current;

        }

        return {
            import: function(ns){
                return dotNotateModule(ns);
            },
            exports: function(ns, values){
                var m = dotNotateModule(ns);
                for(key in values){
                    m[key] = values[key];
                }
            }
        }
    })());

    /*
     Monkey patching mechanism
     */
    _.extend(prambanan, (function(){
        var patches = {};
        return {
            patch: function(name){
                var patch = patches[name];
                if(!patch.applied){
                    patch.patch();
                    patch.applied = true;
                }
            },
            unpatch: function(name){
                var patch = patches[name];
                if(patch.applied){
                    patch.unpatch();
                    patch.applied = false;
                }
            },
            registerPatch: function(name, callback){
                patches[name] = callback;
            },
            registerPrototypePatch: function(name, prototype, patches){
                var original = {};
                var originalExists = {};
                _.each(_.keys(patches), function(key){
                    original[key] = prototype[key]
                    originalExists[key]= _.has(prototype, key);
                });
                this.registerPatch(name, {
                    patch: function(){
                        _.each(_.keys(patches), function(k){
                            prototype[k] = patches[k];
                        });
                    },
                    unpatch: function(){
                        _.each(_.keys(patches), function(k){
                            if(originalExists[k]){
                                prototype[k] = original[k];
                            }
                            else {
                                delete prototype[k];
                            }
                        });
                    }
                });
            }
        }
    })());

    /*
     Compiler helpers
     */
    var subscriptFunctions = {
        l: {
            i: function(list, index){
                return index >= 0
                    ? list[index]
                    : list[list.length + index]
            },
            s: function(list, start, stop, step){
                if(step == null){
                    return list.slice(start, stop);
                }
                else {
                    var result = [];
                    if(start == null)
                        start = 0;
                    if(stop == null)
                        stop = list.length;
                    for(var i = start; i < stop; i+=step){
                        result.push(list[i])
                    }
                    return result;
                }
            }
        },
        d: {
            i: function(list, index){
                list.remove(index);
            },
            s: function(list, start, stop, step){
                if(step != null){
                    throw new Error("delete slice with step not implemented");
                }
                list.remove(start, stop);
            }
        }
    }

    _isSubClass= function(child, parent){
        if(!_.isFunction(parent))
            return false;
        if (child == parent)
            return true;
        if(child.__super__ ){
            if (_isSubClass(child.__super__.constructor, parent)){
                return true;
            }
        }
        if(child.__mixins__){
            for(var i = 0; i < child.__mixins__.length; i++){
                if (_isSubClass(child.__mixins__[i].constructor, parent)){
                    return true;
                }
            }
            return false;
        }
        return false;
    }

    function KwArgs(items){
        this.items = items || {};
    }
    KwArgs.prototype.get = function(name, dft){
        if(_.has(this.items, name))
            return this.items[name];
        return dft;
    }
    KwArgs.prototype.pop = function(name, dft){
        if(_.has(this.items, name)){
            var result = this.items[name];
            delete this.items[name]
            return result;
        }
        return dft;
    }


    _.extend(helpers, {
        subscript: subscriptFunctions,
        pow: Math.pow,
        _:_,
        throw:function(obj, file, lineno){
            obj.file = file;
            obj.lineno = lineno;
            throw obj;
        },
        iter: function(obj){
            return builtins.iter(obj);
        },
        super: function(obj, attr){
            return _.bind((obj.constructor.__super__)[attr], obj)
        },
        class: function(ctor, bases, fn){
            var attrs = fn();
            var instance_attrs = attrs[0];
            var static_attrs = attrs[1];
            var all_attrs = attrs[2];
            for (var prop in all_attrs) {
                instance_attrs[prop] = all_attrs[prop];
                static_attrs[prop] = all_attrs[prop];
            }
            var creator = all_attrs.__metaclass__ || bases[0].prototype.__metaclass__ || builtins.type;
            return creator(ctor, bases, instance_attrs, static_attrs);
        },
        isinstance : function (obj, cls){
            if (obj instanceof cls)
                return true;
            if (!obj.constructor)
                return false;
            return _isSubClass(obj.constructor, cls);
        },
        in: function(item, col){
            if (_.isArray(col)){
                return _.contains(col, item)
            }
            return _.has(col, item)
        },
        make_kwargs: function(items){
            return new KwArgs(items);
        },
        init_args: function(args){
            return slice.call(args,0);
        },
        get_arg : function(index, name, args, dft){
            var arg;
            if(index < args.length){
                arg = args[index];
                if (! (arg instanceof KwArgs))
                    return arg;
                return arg.pop(name, dft);
            }

            arg = args[args.length - 1];
            if (arg instanceof KwArgs)
                return arg.pop(name, dft);
            return dft;
        },
        get_varargs: function(index, args){
            var result = [];
            var start = index;
            var end = args[args.length - 1] instanceof KwArgs ? args.length - 1 : args.length;
            return slice.call(args, start, end);
        },
        get_kwargs:function(args){
            var arg  = args[args.length - 1];
            return arg instanceof KwArgs ? arg : new KwArgs();

        }
    });


    /*
     builtins module
     */
    _.extend(builtins, {
        bool: function(i) {return !!i;},
        int: Number,
        float: Number,
        str: function(o){
            if (!_.isUndefined(o) && o.__str__){
                return o.__str__();
            }
            if(_.isBoolean(o))
                return o ? "True" : "False";
            return String(o);
        },
        basestring: String,
        unicode: String,

        max: Math.max,
        min: Math.min,
        abs: Math.abs,
        round: Math.round,

        all: function(l){
            return _.all(l, function(c){return c === true; })
        },
        any: function(l){
            return _.any(l, function(c){return c === true; })
        },
        len: function(obj){
            return _.isArray(obj) || _.isString(obj) ? obj.length : _.keys(obj).length;
        },
        reverse: function (a) {
            return a.reverse();
        },
        sorted: function(l){
            return _.sortBy(l, function(i){return i;});
        },
        enumerate: function(o){
            return _.map(o, function(i, idx){return [idx, i]})
        },
        set:_.uniq,

        zip:_.zip,
        map: function(f, l){
            return _.map(l, f);
        },
        filter: function(f, l){
            return _.filter(l, f);
        },
        reduce: function(f, l, i){
            return _.reduce(l, function(memo, num){f(num, memo)}, i);
        },
        sum: function(f, l, i){
            return _.reduce(l, function(memo, num){f(num + memo)}, i);
        },

        range: _.range,
        xrange:_.range,

        print: function(s){
            var _s = builtins.str(s)
            if (typeof console != "undefined"){
                console.log(_s);
                return;
            }
            else if (typeof print != "undefined"){
                print(_s)
                return;
            }
        },

        isinstance: function(obj, type){
            return prambanan.helpers.isinstance(obj, type);
        },
        type:  function(ctor, bases, attrs, static_attrs){
            if (arguments.length == 1)
                return ctor.constructor;

            if (ctor){
                attrs.constructor = ctor;
            } else if (attrs.__init__){
                attrs.constructor = attrs.__init__;
            }
            var result = bases[0].extend(attrs, static_attrs)
            var mixins = [];
            if(bases.length > 1){
                for (var i = 1; i < bases.length; i++){
                    var current = bases[i];
                    for(var key in current){
                        if(!(_.has(result, key)))
                            result[key] = current[key];
                    }
                    for(var key in current.prototype){
                        if(!(key in result.__super__))
                            result.prototype[key] = current.prototype[key];
                    }
                    mixins.push(current.prototype);
                }
            }
            result.__mixins__ = mixins;

            return result;
        },
        __import__: function(ns){
            return prambanan.import(ns);
        },
        super: function(cls, self){
        },
        iter: function(o){
            if(_.isArray(o))
                return o;
            if(o instanceof KwArgs){
                return _.keys(o.items);
            }
            if(_.isObject(o))
                return _.keys(o)
            return o;
        },
        None: null
    });


    function t_object(){this.__init__.apply(this, arguments)}
    var object = builtins.object = t_object;
    _.extend(object.prototype, {
        toString: function(){
            if(this.__str__)
                return this.__str__();
            else
                return Object.prototype.toString.call(this);
        },
        __init__: function(){}
    })
    object.extend = Backbone.Model.extend;
    prambanan.exports("__builtin__", builtins);


    /*
     Monkey Paaaaatches
     make some objects to behave like python
     */

    (function(){
        var name = "python.Array";

        prambanan.registerPrototypePatch(name, Array.prototype,  {
            insert: function(index, object){
                this.splice(index, 0, object);
            },
            append: function (object) {
                this[this.length] = object;
            },
            extend: function (list) {
                this.push.apply(this, list);
            },
            remove: function(from, to) {
                var rest = this.slice((to - 1 || from) + 1 || this.length);
                this.length = from < 0 ? this.length + from : from;
                return this.push.apply(this, rest);
            },
            pop: function (index) {
                if (_.isUndefined(index))
                    index = this.length-1;

                if (index == -1 || index >= this.length)
                    return undefined;

                var elt = this[index];
                this.splice(index, 1);
                return elt;
            },
            __str__: function(){
                var result = "[";
                for (var i = 0; i < this.length; i++){
                    if (i != 0)
                        result+=", ";
                    result += builtins.str(this[i]);
                }
                result += "]";
                return result;
            }
        });
        prambanan.patch(name);
    })();

    function sprintf () {
        // http://kevin.vanzonneveld.net
        // +   original by: Ash Searle (http://hexmen.com/blog/)
        // + namespaced by: Michael White (http://getsprink.com)
        // +    tweaked by: Jack
        // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
        // +      input by: Paulo Freitas
        // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
        // +      input by: Brett Zamir (http://brett-zamir.me)
        // +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
        // *     example 1: sprintf("%01.2f", 123.1);
        // *     returns 1: 123.10
        // *     example 2: sprintf("[%10s]", 'monkey');
        // *     returns 2: '[    monkey]'
        // *     example 3: sprintf("[%'#10s]", 'monkey');
        // *     returns 3: '[####monkey]'
        var regex = /%%|%(\d+\$)?([-+\'#0 ]*)(\*\d+\$|\*|\d+)?(\.(\*\d+\$|\*|\d+))?([scboxXuidfegEG])/g;
        var a = arguments,
            i = 0,
            format = a[i++];

        // pad()
        var pad = function (str, len, chr, leftJustify) {
            if (!chr) {
                chr = ' ';
            }
            var padding = (str.length >= len) ? '' : Array(1 + len - str.length >>> 0).join(chr);
            return leftJustify ? str + padding : padding + str;
        };

        // justify()
        var justify = function (value, prefix, leftJustify, minWidth, zeroPad, customPadChar) {
            var diff = minWidth - value.length;
            if (diff > 0) {
                if (leftJustify || !zeroPad) {
                    value = pad(value, minWidth, customPadChar, leftJustify);
                } else {
                    value = value.slice(0, prefix.length) + pad('', diff, '0', true) + value.slice(prefix.length);
                }
            }
            return value;
        };

        // formatBaseX()
        var formatBaseX = function (value, base, prefix, leftJustify, minWidth, precision, zeroPad) {
            // Note: casts negative numbers to positive ones
            var number = value >>> 0;
            prefix = prefix && number && {
                '2': '0b',
                '8': '0',
                '16': '0x'
            }[base] || '';
            value = prefix + pad(number.toString(base), precision || 0, '0', false);
            return justify(value, prefix, leftJustify, minWidth, zeroPad);
        };

        // formatString()
        var formatString = function (value, leftJustify, minWidth, precision, zeroPad, customPadChar) {
            if (precision != null) {
                value = value.slice(0, precision);
            }
            return justify(value, '', leftJustify, minWidth, zeroPad, customPadChar);
        };

        // doFormat()
        var doFormat = function (substring, valueIndex, flags, minWidth, _, precision, type) {
            var number;
            var prefix;
            var method;
            var textTransform;
            var value;

            if (substring == '%%') {
                return '%';
            }

            // parse flags
            var leftJustify = false,
                positivePrefix = '',
                zeroPad = false,
                prefixBaseX = false,
                customPadChar = ' ';
            var flagsl = flags.length;
            for (var j = 0; flags && j < flagsl; j++) {
                switch (flags.charAt(j)) {
                    case ' ':
                        positivePrefix = ' ';
                        break;
                    case '+':
                        positivePrefix = '+';
                        break;
                    case '-':
                        leftJustify = true;
                        break;
                    case "'":
                        customPadChar = flags.charAt(j + 1);
                        break;
                    case '0':
                        zeroPad = true;
                        break;
                    case '#':
                        prefixBaseX = true;
                        break;
                }
            }

            // parameters may be null, undefined, empty-string or real valued
            // we want to ignore null, undefined and empty-string values
            if (!minWidth) {
                minWidth = 0;
            } else if (minWidth == '*') {
                minWidth = +a[i++];
            } else if (minWidth.charAt(0) == '*') {
                minWidth = +a[minWidth.slice(1, -1)];
            } else {
                minWidth = +minWidth;
            }

            // Note: undocumented perl feature:
            if (minWidth < 0) {
                minWidth = -minWidth;
                leftJustify = true;
            }

            if (!isFinite(minWidth)) {
                throw new Error('sprintf: (minimum-)width must be finite');
            }

            if (!precision) {
                precision = 'fFeE'.indexOf(type) > -1 ? 6 : (type == 'd') ? 0 : undefined;
            } else if (precision == '*') {
                precision = +a[i++];
            } else if (precision.charAt(0) == '*') {
                precision = +a[precision.slice(1, -1)];
            } else {
                precision = +precision;
            }

            // grab value using valueIndex if required?
            value = valueIndex ? a[valueIndex.slice(0, -1)] : a[i++];

            switch (type) {
                case 's':
                    return formatString(String(value), leftJustify, minWidth, precision, zeroPad, customPadChar);
                case 'c':
                    return formatString(String.fromCharCode(+value), leftJustify, minWidth, precision, zeroPad);
                case 'b':
                    return formatBaseX(value, 2, prefixBaseX, leftJustify, minWidth, precision, zeroPad);
                case 'o':
                    return formatBaseX(value, 8, prefixBaseX, leftJustify, minWidth, precision, zeroPad);
                case 'x':
                    return formatBaseX(value, 16, prefixBaseX, leftJustify, minWidth, precision, zeroPad);
                case 'X':
                    return formatBaseX(value, 16, prefixBaseX, leftJustify, minWidth, precision, zeroPad).toUpperCase();
                case 'u':
                    return formatBaseX(value, 10, prefixBaseX, leftJustify, minWidth, precision, zeroPad);
                case 'i':
                case 'd':
                    number = (+value) | 0;
                    prefix = number < 0 ? '-' : positivePrefix;
                    value = prefix + pad(String(Math.abs(number)), precision, '0', false);
                    return justify(value, prefix, leftJustify, minWidth, zeroPad);
                case 'e':
                case 'E':
                case 'f':
                case 'F':
                case 'g':
                case 'G':
                    number = +value;
                    prefix = number < 0 ? '-' : positivePrefix;
                    method = ['toExponential', 'toFixed', 'toPrecision']['efg'.indexOf(type.toLowerCase())];
                    textTransform = ['toString', 'toUpperCase']['eEfFgG'.indexOf(type) % 2];
                    value = prefix + Math.abs(number)[method](precision);
                    return justify(value, prefix, leftJustify, minWidth, zeroPad)[textTransform]();
                default:
                    return substring;
            }
        };

        return format.replace(regex, doFormat);
    }

    (function(){
        var name = "python.String";

        prambanan.registerPrototypePatch(name, String.prototype, {
            __mod__: function () {
                var args = Array.prototype.slice.call(arguments, 0);
                args.splice(0, 0, this);
                return sprintf.apply(this, args);
            },
            startswith: function (s) {
                return this.slice(0,s.length) == s;
            },
            endswith: function (s) {
                return this.slice(this.length-s.length) == s;
            },
            join: function(col){
                var result = "";
                for (var i = 0; i < col.length; i++){
                    result+=col[i];
                    if(i != col.length - 1)
                        result+=this;
                }
                return result;
            },
            reverse: function(){
                var s = "";
                var i = this.length;
                while (i>0) {
                    s += this.substring(i-1,i);
                    i--;
                }
                return s;
            }
        });
        prambanan.patch(name);

        prambanan.registerPrototypePatch(name, Number.prototype, {
            __mod__: function (value) {
                return this % value;
            }
        });
        prambanan.patch(name);
    })();

}).call(this)
(function(prambanan) {
    var JS, JSNoOp, __builtin__, __import__, _m_prambanan, select, underscore;
    __builtin__ = prambanan.import('__builtin__');
    __import__ = __builtin__.__import__;
    _m_prambanan = __import__('prambanan.jslib');
    underscore = _m_prambanan.underscore;
    var is_server = false;
    var items = _.items;
    JS = function(fn) {
        return fn;
    };
    JSNoOp = function(target) {
        return target;
    };
    select = function(fn, server, client) {
        return is_server ? server : client;
    };
    prambanan.exports('prambanan', {JS: JS,JSNoOp: JSNoOp,is_server: is_server,items: items,select: select});
})(prambanan);(function(prambanan) {
    var ArithmeticError, AttributeError, BaseException, Exception, IndexError, KeyError, LookupError, NameError, NotImplementedError, RuntimeError, StandardError, SystemError, TypeError, ValueError, ZeroDivisionError, __builtin__, _class, object;
    __builtin__ = prambanan.import('__builtin__');
    ArithmeticError = __builtin__.ArithmeticError;
    Exception = __builtin__.Exception;
    object = __builtin__.object;
    StandardError = __builtin__.StandardError;
    BaseException = __builtin__.BaseException;
    _class = prambanan.helpers.class;

    function t___builtin___BaseException() {
        this.__init__.apply(this, arguments);
    }
    BaseException = _class(t___builtin___BaseException, [object], function() {
        var __init__;
        __init__ = function(self, message) {
            var self;
            self = this;
            if (Error.captureStackTrace) {
                Error.captureStackTrace(self);
            }
            self.message = message;
        };
        return [{__init__: __init__}, {}, {}]
    });

    function t___builtin___Exception() {
        this.__init__.apply(this, arguments);
    }
    Exception = _class(t___builtin___Exception, [BaseException], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___StandardError() {
        this.__init__.apply(this, arguments);
    }
    StandardError = _class(t___builtin___StandardError, [Exception], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___AttributeError() {
        this.__init__.apply(this, arguments);
    }
    AttributeError = _class(t___builtin___AttributeError, [StandardError], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___TypeError() {
        this.__init__.apply(this, arguments);
    }
    TypeError = _class(t___builtin___TypeError, [StandardError], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___ValueError() {
        this.__init__.apply(this, arguments);
    }
    ValueError = _class(t___builtin___ValueError, [StandardError], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___NameError() {
        this.__init__.apply(this, arguments);
    }
    NameError = _class(t___builtin___NameError, [StandardError], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___SystemError() {
        this.__init__.apply(this, arguments);
    }
    SystemError = _class(t___builtin___SystemError, [StandardError], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___LookupError() {
        this.__init__.apply(this, arguments);
    }
    LookupError = _class(t___builtin___LookupError, [StandardError], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___KeyError() {
        this.__init__.apply(this, arguments);
    }
    KeyError = _class(t___builtin___KeyError, [LookupError], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___IndexError() {
        this.__init__.apply(this, arguments);
    }
    IndexError = _class(t___builtin___IndexError, [LookupError], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___ArithmeticError() {
        this.__init__.apply(this, arguments);
    }
    ArithmeticError = _class(t___builtin___ArithmeticError, [StandardError], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___ZeroDivisionError() {
        this.__init__.apply(this, arguments);
    }
    ZeroDivisionError = _class(t___builtin___ZeroDivisionError, [ArithmeticError], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___RuntimeError() {
        this.__init__.apply(this, arguments);
    }
    RuntimeError = _class(t___builtin___RuntimeError, [StandardError], function() { /* pass */
        return [{}, {}, {}]
    });

    function t___builtin___NotImplementedError() {
        this.__init__.apply(this, arguments);
    }
    NotImplementedError = _class(t___builtin___NotImplementedError, [RuntimeError], function() { /* pass */
        return [{}, {}, {}]
    });
    prambanan.exports('__builtin__', {ArithmeticError: ArithmeticError,AttributeError: AttributeError,BaseException: BaseException,Exception: Exception,IndexError: IndexError,KeyError: KeyError,LookupError: LookupError,NameError: NameError,NotImplementedError: NotImplementedError,RuntimeError: RuntimeError,StandardError: StandardError,SystemError: SystemError,TypeError: TypeError,ValueError: ValueError,ZeroDivisionError: ZeroDivisionError});
})(prambanan);(function(prambanan) {
    var JS, NotImplementedError, TypeError, ValueError, __builtin__, __c__days, __c__months, __import__, _class, _dst, _get_arg, _init_args, _m___pyjamas__, _strptime, _subscript, altzone, asctime, ctime, d, float, gmtime, int, isinstance, len, localtime, math, mktime, object, str, strftime, strptime, struct_time, time, timezone, tzname;
    __builtin__ = prambanan.import('__builtin__');
    object = __builtin__.object;
    int = __builtin__.int;
    __import__ = __builtin__.__import__;
    float = __builtin__.float;
    len = __builtin__.len;
    TypeError = __builtin__.TypeError;
    str = __builtin__.str;
    NotImplementedError = __builtin__.NotImplementedError;
    isinstance = __builtin__.isinstance;
    ValueError = __builtin__.ValueError;
    _init_args = prambanan.helpers.init_args;
    _class = prambanan.helpers.class;
    _subscript = prambanan.helpers.subscript;
    _get_arg = prambanan.helpers.get_arg;
    _m___pyjamas__ = __import__('__pyjamas__');
    JS = _m___pyjamas__.JS;
    math = __import__('math');
    timezone = 60 * (new Date(new Date().getFullYear(), 0, 1)).getTimezoneOffset();
    altzone = 60 * (new Date(new Date().getFullYear(), 6, 1)).getTimezoneOffset();
    if (altzone > timezone) {
        d = timezone;
        timezone = altzone;
        altzone = d;
    }
    _dst = timezone - altzone;
    d = (new Date(new Date().getFullYear(), 0, 1));
    d = _subscript.l.i(str(d.toLocaleString()).split(), -1);
    if (_subscript.l.i(d, 0) === "(") {
        d = _subscript.l.s(d, 1, -1, null);
    }
    tzname = [d, null];
    delete;
    __c__days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    __c__months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    time = function() {
        return float(new Date().getTime() / 1000.0);
    };

    function t_time_struct_time() {
        this.__init__.apply(this, arguments);
    }
    struct_time = _class(t_time_struct_time, [object], function() {
        var __getitem__, __getslice__, __init__, __repr__, __str__, n_fields, n_sequence_fields, n_unnamed_fields, tm_hour, tm_isdst, tm_mday, tm_min, tm_mon, tm_sec, tm_wday, tm_yday, tm_year;
        n_fields = 9;
        n_sequence_fields = 9;
        n_unnamed_fields = 0;
        tm_year = null;
        tm_mon = null;
        tm_mday = null;
        tm_hour = null;
        tm_min = null;
        tm_sec = null;
        tm_wday = null;
        tm_yday = null;
        tm_isdst = null;
        __init__ = function(self, ttuple) {
            var _args, self;
            _args = _init_args(arguments);
            ttuple = _get_arg(1, "ttuple", _args, null);
            self = this;
            if (!(ttuple === null)) {
                self.tm_year = ttuple[0];
                self.tm_mon = ttuple[1];
                self.tm_mday = ttuple[2];
                self.tm_hour = ttuple[3];
                self.tm_min = ttuple[4];
                self.tm_sec = ttuple[5];
                self.tm_wday = ttuple[6];
                self.tm_yday = ttuple[7];
                self.tm_isdst = ttuple[8];
            }
        };
        __str__ = function(self) {
            var self, t;
            self = this;
            t = [self.tm_year, self.tm_mon, self.tm_mday, self.tm_hour, self.tm_min, self.tm_sec, self.tm_wday, self.tm_yday, self.tm_isdst];
            return t.__str__();
        };
        __repr__ = function(self) {
            var self;
            self = this;
            return self.__str__();
        };
        __getitem__ = function(self, idx) {
            var self;
            self = this;
            return _subscript.l.i([self.tm_year, self.tm_mon, self.tm_mday, self.tm_hour, self.tm_min, self.tm_sec, self.tm_wday, self.tm_yday, self.tm_isdst], idx);
        };
        __getslice__ = function(self, lower, upper) {
            var self;
            self = this;
            return _subscript.l.s([self.tm_year, self.tm_mon, self.tm_mday, self.tm_hour, self.tm_min, self.tm_sec, self.tm_wday, self.tm_yday, self.tm_isdst], lower, upper, null);
        };
        return [{__init__: __init__,__str__: __str__,__repr__: __repr__,__getitem__: __getitem__,__getslice__: __getslice__}, {}, {}]
    });
    gmtime = function(t) {
        var _args, date, startOfYear, tm, tm_year;
        _args = _init_args(arguments);
        t = _get_arg(0, "t", _args, null);
        if (t === null) {
            t = time();
        }
        date = new Date(t * 1000);
        tm = new struct_time();
        tm_year = tm.tm_year = int(date.getUTCFullYear());
        tm.tm_mon = int(date.getUTCMonth()) + 1;
        tm.tm_mday = int(date.getUTCDate());
        tm.tm_hour = int(date.getUTCHours());
        tm.tm_min = int(date.getUTCMinutes());
        tm.tm_sec = int(date.getUTCSeconds());
        tm.tm_wday = int(date.getUTCDay()) + 6.__mod__(7);
        tm.tm_isdst = 0;
        startOfYear = new Date('Jan 1 ' + tm_year + ' GMT+0000');
        tm.tm_yday = 1 + int(t - startOfYear.getTime() / 1000 / 86400);
        return tm;
    };
    localtime = function(t) {
        var _args, date, dateOffset, dt, startOfDay, startOfYear, startOfYearOffset, tm, tm_mday, tm_mon, tm_year;
        _args = _init_args(arguments);
        t = _get_arg(0, "t", _args, null);
        if (t === null) {
            t = time();
        }
        date = new Date(t * 1000);
        dateOffset = date.getTimezoneOffset();
        tm = new struct_time();
        tm_year = tm.tm_year = int(date.getFullYear());
        tm_mon = tm.tm_mon = int(date.getMonth()) + 1;
        tm_mday = tm.tm_mday = int(date.getDate());
        tm.tm_hour = int(date.getHours());
        tm.tm_min = int(date.getMinutes());
        tm.tm_sec = int(date.getSeconds());
        tm.tm_wday = int(date.getDay()) + 6.__mod__(7);
        tm.tm_isdst = timezone === (60 * date.getTimezoneOffset()) ? 0 : 1;
        startOfYear = new Date(tm_year, 0, 1);
        startOfYearOffset = startOfYear.getTimezoneOffset();
        startOfDay = new Date(tm_year, tm_mon - 1, tm_mday);
        dt = float(startOfDay.getTime() - startOfYear.getTime()) / 1000;
        dt = dt + 60 * (startOfYearOffset - dateOffset);
        tm.tm_yday = 1 + int(dt / 86400.0);
        return tm;
    };
    /**
     * mktime(tuple) -> floating point number
     * Convert a time tuple in local time to seconds since the Epoch.
     */
    mktime = function(t) {
        var date, tm_hour, tm_mday, tm_min, tm_mon, tm_sec, tm_year, ts, utc;
        tm_year = t.tm_year;
        tm_mon = t.tm_mon - 1;
        tm_mday = t.tm_mday;
        tm_hour = t.tm_hour;
        tm_min = t.tm_min;
        tm_sec = t.tm_sec;
        date = new Date(tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec);
        utc = Date.UTC(tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec) / 1000;
        ts = date.getTime() / 1000;
        if (_subscript.l.i(t, 8) === 0) {
            if (ts - utc === timezone) {
                return ts;
            }
            return ts + _dst;
        }
        return ts;
    };
    strftime = function(fmt, t) {
        var _args, date, firstMonday, firstWeek, format, re_pct, remainder, result, startOfYear, tm_hour, tm_mday, tm_min, tm_mon, tm_sec, tm_wday, tm_yday, tm_year, weekNo;
        _args = _init_args(arguments);
        t = _get_arg(1, "t", _args, null);
        if (t === null) {
            t = localtime();
        } else{
        if (!isinstance(t, struct_time) && len(t) !== 9) {
            throw new TypeError("argument must be 9-item sequence, not float");}
        }
        tm_year = t.tm_year;
        tm_mon = t.tm_mon;
        tm_mday = t.tm_mday;
        tm_hour = t.tm_hour;
        tm_min = t.tm_min;
        tm_sec = t.tm_sec;
        tm_wday = t.tm_wday;
        tm_yday = t.tm_yday;
        date = new Date(tm_year, tm_mon - 1, tm_mday, tm_hour, tm_min, tm_sec);
        startOfYear = new Date(tm_year, 0, 1);
        firstMonday = 1 - startOfYear.getDay() + 6.__mod__(7) + 7;
        firstWeek = new Date(tm_year, 0, firstMonday);
        weekNo = date.getTime() - firstWeek.getTime();
        if (weekNo < 0) {
            weekNo = 0;
        } else{weekNo = 1 + int(weekNo / 604800000);}
        format = function(c) {
            if (c === "%") {
                return "%";
            } else{
            if (c === "a") {
                return _subscript.l.s(format("A"), null, 3, null);} else{
            if (c === "A") {
                return _subscript.l.i(__c__days, format("w"));} else{
            if (c === "b") {
                return _subscript.l.s(format("B"), null, 3, null);} else{
            if (c === "B") {
                return _subscript.l.i(__c__months, tm_mon - 1);} else{
            if (c === "c") {
                return date.toLocaleString();} else{
            if (c === "d") {
                return "%02d".__mod__(tm_mday);} else{
            if (c === "H") {
                return "%02d".__mod__(tm_hour);} else{
            if (c === "I") {
                return "%02d".__mod__(tm_hour.__mod__(12));} else{
            if (c === "j") {
                return "%03d".__mod__(tm_yday);} else{
            if (c === "m") {
                return "%02d".__mod__(tm_mon);} else{
            if (c === "M") {
                return "%02d".__mod__(tm_min);} else{
            if (c === "p") {
                if (tm_hour < 12) {
                    return "AM";}
                return "PM";
            } else{
            if (c === "S") {
                return "%02d".__mod__(tm_sec);} else{
            if (c === "U") {
                throw new NotImplementedError("strftime format character '%s'".__mod__(c));} else{
            if (c === "w") {
                return "%d".__mod__(tm_wday + 1.__mod__(7));} else{
            if (c === "W") {
                return "%d".__mod__(weekNo);} else{
            if (c === "x") {
                return "%s".__mod__(date.toLocaleDateString());} else{
            if (c === "X") {
                return "%s".__mod__(date.toLocaleTimeString());} else{
            if (c === "y") {
                return "%02d".__mod__(tm_year.__mod__(100));} else{
            if (c === "Y") {
                return "%04d".__mod__(tm_year);} else{
            if (c === "Z") {
                throw new NotImplementedError("strftime format character '%s'".__mod__(c));}
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            }
            return "%" + c;
        };
        result = "";
        remainder = fmt;
        re_pct = /([^%]*)%(.)(.*)/;
        var a, fmtChar;;
        while (remainder) {{
            a = re_pct.exec(remainder);
            if (!a) {
                result += remainder;
                remainder = false;} else{
            result += a[1];
            fmtChar = a[2];
            remainder = a[3];
            if (typeof fmtChar != 'undefined') {
                result += format(fmtChar);}
            }
            };
        }
        return str(result);
    };
    asctime = function(t) {
        var _args;
        _args = _init_args(arguments);
        t = _get_arg(0, "t", _args, null);
        if (t === null) {
            t = localtime();
        }
        return "%s %s %02d %02d:%02d:%02d %04d".__mod__(_subscript.l.s(_subscript.l.i(__c__days, t.tm_wday - 1.__mod__(7)), null, 3, null), _subscript.l.i(__c__months, t.tm_mon - 1), t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec, t.tm_year);
    };
    ctime = function(t) {
        var _args;
        _args = _init_args(arguments);
        t = _get_arg(0, "t", _args, null);
        return asctime(localtime(t));
    };
    var _DATE_FORMAT_REGXES = {'Y': new RegExp('^-?[0-9]+'),'y': new RegExp('^-?[0-9]{1,2}'),'d': new RegExp('^[0-9]{1,2}'),'m': new RegExp('^[0-9]{1,2}'),'H': new RegExp('^[0-9]{1,2}'),'M': new RegExp('^[0-9]{1,2}')}

    /*
     * _parseData does the actual parsing job needed by `strptime`
     */

    function _parseDate(datestring, format) {
        var parsed = {};
        for (var i1 = 0, i2 = 0; i1 < format.length; i1++, i2++) {
            var c1 = format[i1];
            var c2 = datestring[i2];
            if (c1 == '%') {
                c1 = format[++i1];
                var data = _DATE_FORMAT_REGXES[c1].exec(datestring.substring(i2));
                if (!data.length) {
                    return null;
                }
                data = data[0];
                i2 += data.length - 1;
                var value = parseInt(data, 10);
                if (isNaN(value)) {
                    return null;
                }
                parsed[c1] = value;
                continue;
            }
            if (c1 != c2) {
                return null;
            }
        }
        return parsed;
    }

    /*
     * basic implementation of strptime. The only recognized formats
     * defined in _DATE_FORMAT_REGEXES (i.e. %Y, %d, %m, %H, %M)
     */

    function strptime(datestring, format) {
        var parsed = _parseDate(datestring, format);
        if (!parsed) {
            return null;
        }
        // create initial date (!!! year=0 means 1900 !!!)
        var date = new Date(0, 0, 1, 0, 0);
        date.setFullYear(0); // reset to year 0
        if (typeof parsed.Y != "undefined") {
            date.setFullYear(parsed.Y);
        }
        if (typeof parsed.y != "undefined") {
            date.setFullYear(2000 + parsed.y);
        }
        if (typeof parsed.m != "undefined") {
            if (parsed.m < 1 || parsed.m > 12) {
                return null;
            }
            // !!! month indexes start at 0 in javascript !!!
            date.setMonth(parsed.m - 1);
        }
        if (typeof parsed.d != "undefined") {
            if (parsed.m < 1 || parsed.m > 31) {
                return null;
            }
            date.setDate(parsed.d);
        }
        if (typeof parsed.H != "undefined") {
            if (parsed.H < 0 || parsed.H > 23) {
                return null;
            }
            date.setHours(parsed.H);
        }
        if (typeof parsed.M != "undefined") {
            if (parsed.M < 0 || parsed.M > 59) {
                return null;
            }
            date.setMinutes(parsed.M);
        }
        return date;
    };;
    _strptime = function(datestring, format) {
        var _ex;
        try{
        return float(strptime(datestring.valueOf(), format.valueOf()).getTime() / 1000.0);} catch (_ex) {
            throw new ValueError("Invalid or unsupported values for strptime: '%s', '%s'".__mod__(datestring, format));
        }
    };
    strptime = function(datestring, format) {
        var _ex, tt;
        try{tt = localtime(float(strptime(datestring.valueOf(), format.valueOf()).getTime() / 1000.0));
        tt.tm_isdst = -1;
        return tt;} catch (_ex) {
            throw new ValueError("Invalid or unsupported values for strptime: '%s', '%s'".__mod__(datestring, format));
        }
    };
    prambanan.exports('time', {asctime: asctime,ctime: ctime,gmtime: gmtime,localtime: localtime,mktime: mktime,strftime: strftime,strptime: strptime,struct_time: struct_time,time: time});
})(prambanan);(function(prambanan) {
    var JS, MAXYEAR, MINYEAR, NotImplementedError, TypeError, __Jan_01_0001, __builtin__, __c__days, __c__months, __import__, _class, _get_arg, _init_args, _m___pyjamas__, _m_time, _make_kwargs, _strptime, _subscript, _super, date, datetime, gmtime, int, isinstance, localtime, object, strftime, time, timedelta, tzinfo;
    __builtin__ = prambanan.import('__builtin__');
    TypeError = __builtin__.TypeError;
    int = __builtin__.int;
    __import__ = __builtin__.__import__;
    object = __builtin__.object;
    NotImplementedError = __builtin__.NotImplementedError;
    isinstance = __builtin__.isinstance;
    _subscript = prambanan.helpers.subscript;
    _init_args = prambanan.helpers.init_args;
    _super = prambanan.helpers.super;
    _make_kwargs = prambanan.helpers.make_kwargs;
    _class = prambanan.helpers.class;
    _get_arg = prambanan.helpers.get_arg;
    _m___pyjamas__ = __import__('__pyjamas__');
    JS = _m___pyjamas__.JS;
    _m_time = __import__('time');
    __c__days = _m_time.__c__days;
    __c__months = _m_time.__c__months;
    strftime = _m_time.strftime;
    localtime = _m_time.localtime;
    gmtime = _m_time.gmtime;
    _strptime = _m_time._strptime;
    MINYEAR = 1;
    MAXYEAR = 1000000;
    __Jan_01_0001 = (new Date((new Date('Jan 1 1971')).getTime() - 62167132800000)).getTime();

    function t_datetime_date() {
        this.__init__.apply(this, arguments);
    }
    date = _class(t_datetime_date, [object], function() {
        var __add__, __cmp__, __init__, __str__, __sub__, ctime, fromordinal, fromtimestamp, isocalendar, isoformat, isoweekday, replace, strftime, timetuple, today, toordinal, weekday;
        __init__ = function(self, year, month, day, d) {
            var _args, self;
            _args = _init_args(arguments);
            d = _get_arg(4, "d", _args, null);
            self = this;
            if (d === null) {
                d = new Date(year, month - 1, day, 0, 0, 0, 0);
            }
            self._d = d;
            self.year = d.getFullYear();
            self.month = d.getMonth() + 1.0;
            self.day = d.getDate();
        };
        today = function() {
            return new date(0, 0, 0, new Date());
        };
        today = today;
        fromtimestamp = function(timestamp) {
            var d;
            d = new Date();
            d.setTime(timestamp * 1000.0);
            return new date(0, 0, 0, d);
        };
        fromtimestamp = fromtimestamp;
        fromordinal = function(ordinal) {
            var d, t;
            t = __Jan_01_0001 + ordinal - 1 * 86400000.0;
            d = new Date(t);
            return new date(0, 0, 0, d);
        };
        fromordinal = fromordinal;
        ctime = function(self) {
            var self;
            self = this;
            return "%s %s %2d %02d:%02d:%02d %04d".__mod__(_subscript.l.s(_subscript.l.i(__c__days, self._d.getDay()), null, 3, null), _subscript.l.s(_subscript.l.i(__c__months, self._d.getMonth()), null, 3, null), self._d.getDate(), self._d.getHours(), self._d.getMinutes(), self._d.getSeconds(), self._d.getFullYear());
        };
        isocalendar = function(self) {
            var _d, isoweekday, isoweeknr, isoyear, self;
            self = this;
            isoyear = isoweeknr = isoweekday = null;
            _d = self._d;
            var gregdaynumber = function(year, month, day) {
                    var y = year;
                    var m = month;
                    if (month < 3) {
                        y--;
                        m += 12;
                    }
                    return Math.floor(365.25 * y) - Math.floor(y / 100) + Math.floor(y / 400) + Math.floor(30.6 * (m + 1)) + day - 62;
                };

            var year = _d.getFullYear();
            var month = _d.getMonth();
            var day = _d.getDate();
            var wday = _d.getDay();

            isoweekday = ((wday + 6) % 7) + 1;
            isoyear = year;

            var d0 = gregdaynumber(year, 1, 0);
            var weekday0 = ((d0 + 4) % 7) + 1;

            var d = gregdaynumber(year, month + 1, day);
            isoweeknr = Math.floor((d - d0 + weekday0 + 6) / 7) - Math.floor((weekday0 + 3) / 7);

            if ((month == 11) && ((day - isoweekday) > 27)) {
                isoweeknr = 1;
                isoyear = isoyear + 1;
            }

            if ((month == 0) && ((isoweekday - day) > 3)) {
                d0 = gregdaynumber(year - 1, 1, 0);
                weekday0 = ((d0 + 4) % 7) + 1;
                isoweeknr = Math.floor((d - d0 + weekday0 + 6) / 7) - Math.floor((weekday0 + 3) / 7);
                isoyear--;
            };
            return [isoyear, isoweeknr, isoweekday];
        };
        isoformat = function(self) {
            var self;
            self = this;
            return "%04d-%02d-%02d".__mod__(self.year, self.month, self.day);
        };
        isoweekday = function(self) {
            var self;
            self = this;
            return self._d.getDay() + 6.__mod__(7) + 1;
        };
        replace = function(self, year, month, day) {
            var _args, self;
            _args = _init_args(arguments);
            year = _get_arg(1, "year", _args, null);
            month = _get_arg(2, "month", _args, null);
            day = _get_arg(3, "day", _args, null);
            self = this;
            if (year === null) {
                year = self.year;
            }
            if (month === null) {
                month = self.month;
            }
            if (day === null) {
                day = self.day;
            }
            return new date(year, month, day);
        };
        strftime = function(self, format) {
            var self;
            self = this;
            return strftime(format, self.timetuple());
        };
        timetuple = function(self) {
            var self, tm;
            self = this;
            tm = localtime(int(self._d.getTime() / 1000.0));
            tm.tm_hour = tm.tm_min = tm.tm_sec = 0;
            return tm;
        };
        toordinal = function(self) {
            var self;
            self = this;
            return 1 + int(self._d.getTime() - __Jan_01_0001 / 86400000.0);
        };
        weekday = function(self) {
            var self;
            self = this;
            return self._d.getDay() + 6.__mod__(7);
        };
        __str__ = function(self) {
            var self;
            self = this;
            return self.isoformat();
        };
        __cmp__ = function(self, other) {
            var a, b, self;
            self = this;
            if (isinstance(other, date) || isinstance(other, datetime)) {
                a = self._d.getTime();
                b = other._d.getTime();
                if (a < b) {
                    return -1;
                } else{
                if (a === b) {
                    return 0;}
                }
            } else{
            throw new TypeError("expected date or datetime object");}
            return 1;
        };
        __add__ = function(self, other) {
            var self;
            self = this;
            if (isinstance(other, timedelta)) {
                return new date(self.year, self.month, self.day + other.days);
            } else{
            throw new TypeError("expected timedelta object");}
        };
        __sub__ = function(self, other) {
            var diff, self;
            self = this;
            if (isinstance(other, date) || isinstance(other, datetime)) {
                diff = self._d.getTime() - other._d.getTime();
                return new timedelta(int(diff / 86400000.0), int(diff / 1000.0).__mod__(86400), _make_kwargs({milliseconds: diff.__mod__(86400000)}));
            } else{
            if (isinstance(other, timedelta)) {
                return new date(self.year, self.month, self.day - other.days);} else{
            throw new TypeError("expected date or datetime object");}
            }
        };
        return [{__init__: __init__,ctime: ctime,isocalendar: isocalendar,isoformat: isoformat,isoweekday: isoweekday,replace: replace,strftime: strftime,timetuple: timetuple,toordinal: toordinal,weekday: weekday,__str__: __str__,__cmp__: __cmp__,__add__: __add__,__sub__: __sub__}, {today: today,fromtimestamp: fromtimestamp,fromordinal: fromordinal}, {}]
    });

    function t_datetime_time() {
        this.__init__.apply(this, arguments);
    }
    time = _class(t_datetime_time, [object], function() {
        var __init__, __str__, dst, isoformat, replace, strftime, tzname, utcoffset;
        __init__ = function(self, hour, minute, second, microsecond, tzinfo, d) {
            var _args, self;
            _args = _init_args(arguments);
            minute = _get_arg(2, "minute", _args, 0);
            second = _get_arg(3, "second", _args, 0);
            microsecond = _get_arg(4, "microsecond", _args, 0);
            tzinfo = _get_arg(5, "tzinfo", _args, null);
            d = _get_arg(6, "d", _args, null);
            self = this;
            if (tzinfo !== null) {
                throw new NotImplementedError("tzinfo");
            }
            if (d === null) {
                d = new Date(1970, 1, 1, hour, minute, second, 0.5 + microsecond / 1000.0);
            }
            self._d = d;
            self.hour = d.getHours();
            self.minute = d.getMinutes();
            self.second = d.getSeconds();
            self.microsecond = d.getMilliseconds() * 1000.0;
            self.tzinfo = null;
        };
        dst = function(self) {
            var self;
            self = this;
            throw new NotImplementedError("dst");
        };
        isoformat = function(self) {
            var self, t;
            self = this;
            t = "%02d:%02d:%02d".__mod__(self.hour, self.minute, self.second);
            if (self.microsecond) {
                t += ".%06d".__mod__(self.microsecond);
            }
            return t;
        };
        replace = function(self, hour, minute, second, microsecond, tzinfo) {
            var _args, self;
            _args = _init_args(arguments);
            hour = _get_arg(1, "hour", _args, null);
            minute = _get_arg(2, "minute", _args, null);
            second = _get_arg(3, "second", _args, null);
            microsecond = _get_arg(4, "microsecond", _args, null);
            tzinfo = _get_arg(5, "tzinfo", _args, null);
            self = this;
            if (tzinfo !== null) {
                throw new NotImplementedError("tzinfo");
            }
            if (hour === null) {
                hour = self.hour;
            }
            if (minute === null) {
                minute = self.minute;
            }
            if (second === null) {
                second = self.second;
            }
            if (microsecond === null) {
                microsecond = self.microsecond;
            }
            return new time(hour, minute, second, microsecond);
        };
        strftime = function(self, format) {
            var self;
            self = this;
            return strftime(format, localtime(int(self._d.getTime() / 1000.0)));
        };
        tzname = function(self) {
            var self;
            self = this;
            return null;
        };
        utcoffset = function(self) {
            var self;
            self = this;
            return null;
        };
        __str__ = function(self) {
            var self;
            self = this;
            return self.isoformat();
        };
        return [{__init__: __init__,dst: dst,isoformat: isoformat,replace: replace,strftime: strftime,tzname: tzname,utcoffset: utcoffset,__str__: __str__}, {}, {}]
    });

    function t_datetime_datetime() {
        this.__init__.apply(this, arguments);
    }
    datetime = _class(t_datetime_datetime, [date], function() {
        var __add__, __init__, __str__, __sub__, astimezone, combine, date, fromordinal, fromtimestamp, isoformat, now, replace, strptime, time, timetuple, timetz, utcfromtimestamp, utcnow, utctimetuple;
        __init__ = function(self, year, month, day, hour, minute, second, microsecond, tzinfo, d) {
            var _args, self;
            _args = _init_args(arguments);
            hour = _get_arg(4, "hour", _args, 0);
            minute = _get_arg(5, "minute", _args, 0);
            second = _get_arg(6, "second", _args, 0);
            microsecond = _get_arg(7, "microsecond", _args, 0);
            tzinfo = _get_arg(8, "tzinfo", _args, null);
            d = _get_arg(9, "d", _args, null);
            self = this;
            if (d === null) {
                d = new Date(year, month - 1, day, hour, minute, second, 0.5 + microsecond / 1000.0);
            }
            _super(this, '__init__')(0, 0, 0, d);
            self.hour = d.getHours();
            self.minute = d.getMinutes();
            self.second = d.getSeconds();
            self.microsecond = d.getMilliseconds() * 1000.0;
            self.tzinfo = null;
        };
        combine = function(date, time) {
            return new datetime(date.year, date.month, date.day, time.hour, time.minute, time.second, time.microsecond);
        };
        combine = combine;
        fromtimestamp = function(timestamp, tz) {
            var _args, d;
            _args = _init_args(arguments);
            tz = _get_arg(1, "tz", _args, null);
            if (tz !== null) {
                throw new NotImplementedError("tz");
            }
            d = new Date();
            d.setTime(timestamp * 1000.0);
            return new datetime(0, 0, 0, 0, 0, 0, 0, null, d);
        };
        fromtimestamp = fromtimestamp;
        fromordinal = function(ordinal) {
            var d;
            d = new Date();
            d.setTime(ordinal - 719163.0 * 86400000.0);
            return new datetime(0, 0, 0, 0, 0, 0, 0, null, d);
        };
        fromordinal = fromordinal;
        now = function(tz) {
            var _args;
            _args = _init_args(arguments);
            tz = _get_arg(0, "tz", _args, null);
            if (tz !== null) {
                throw new NotImplementedError("tz");
            }
            return new datetime(0, 0, 0, 0, 0, 0, 0, null, new Date());
        };
        now = now;
        strptime = function(datestring, format) {
            return datetime.fromtimestamp(_strptime(datestring, format));
        };
        strptime = strptime;
        utcfromtimestamp = function(timestamp) {
            var tm;
            tm = gmtime(timestamp);
            return new datetime(tm.tm_year, tm.tm_mon, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec);
        };
        utcfromtimestamp = utcfromtimestamp;
        utcnow = function() {
            var d;
            d = new Date();
            return datetime.utcfromtimestamp(int(d.getTime() / 1000.0));
        };
        utcnow = utcnow;
        timetuple = function(self) {
            var self;
            self = this;
            return localtime(int(self._d.getTime() / 1000.0));
        };
        astimezone = function(self, tz) {
            var self;
            self = this;
            throw new NotImplementedError("astimezone");
        };
        date = function(self) {
            var self;
            self = this;
            return new date(self.year, self.month, self.day);
        };
        time = function(self) {
            var self;
            self = this;
            return new time(self.hour, self.minute, self.second, self.microsecond);
        };
        replace = function(self, year, month, day, hour, minute, second, microsecond, tzinfo) {
            var _args, self;
            _args = _init_args(arguments);
            year = _get_arg(1, "year", _args, null);
            month = _get_arg(2, "month", _args, null);
            day = _get_arg(3, "day", _args, null);
            hour = _get_arg(4, "hour", _args, null);
            minute = _get_arg(5, "minute", _args, null);
            second = _get_arg(6, "second", _args, null);
            microsecond = _get_arg(7, "microsecond", _args, null);
            tzinfo = _get_arg(8, "tzinfo", _args, null);
            self = this;
            if (tzinfo !== null) {
                throw new NotImplementedError("tzinfo");
            }
            if (year === null) {
                year = self.year;
            }
            if (month === null) {
                month = self.month;
            }
            if (day === null) {
                day = self.day;
            }
            if (hour === null) {
                hour = self.hour;
            }
            if (minute === null) {
                minute = self.minute;
            }
            if (second === null) {
                second = self.second;
            }
            if (microsecond === null) {
                microsecond = self.microsecond;
            }
            return new datetime(year, month, day, hour, minute, second, microsecond);
        };
        timetz = function(self) {
            var self;
            self = this;
            throw new NotImplementedError("timetz");
        };
        utctimetuple = function(self) {
            var self;
            self = this;
            return gmtime(self._d.getTime() / 1000.0);
        };
        isoformat = function(self, sep) {
            var _args, self, t;
            _args = _init_args(arguments);
            sep = _get_arg(1, "sep", _args, "T");
            self = this;
            t = "%04d-%02d-%02d%s%02d:%02d:%02d".__mod__(self.year, self.month, self.day, sep, self.hour, self.minute, self.second);
            if (self.microsecond) {
                t += ".%06d".__mod__(self.microsecond);
            }
            return t;
        };
        __add__ = function(self, other) {
            var d, day, hour, microsecond, minute, month, second, self, year;
            self = this;
            if (isinstance(other, timedelta)) {
                year = self.year;
                month = self.month;
                day = self.day + other.days;
                hour = self.hour + other.seconds / 3600.0;
                minute = self.minute + other.seconds / 60.0.__mod__(60);
                second = self.second + other.seconds.__mod__(60);
                microsecond = self.microsecond + other.microseconds;
                d = new Date(year, month, day, hour, minute, second, microsecond);
                return new datetime(0, 0, 0, 0, 0, 0, 0, null, d);
            } else{
            throw new TypeError("expected timedelta object");}
        };
        __sub__ = function(self, other) {
            var d, day, diff, hour, microsecond, minute, month, second, self, year;
            self = this;
            if (isinstance(other, date) || isinstance(other, datetime)) {
                diff = self._d.getTime() - other._d.getTime();
                return new timedelta(int(diff / 86400000.0), int(diff / 1000.0).__mod__(86400), _make_kwargs({milliseconds: diff.__mod__(86400000)}));
            } else{
            if (isinstance(other, timedelta)) {
                year = self.year;
                month = self.month;
                day = self.day - other.days;
                hour = self.hour - other.seconds / 3600.0;
                minute = self.minute - other.seconds / 60.0.__mod__(60);
                second = self.second - other.seconds.__mod__(60);
                microsecond = self.microsecond - other.microseconds;
                d = new Date(year, month, day, hour, minute, second, microsecond);
                return new datetime(0, 0, 0, 0, 0, 0, 0, null, d);} else{
            throw new TypeError("expected date or datetime object");}
            }
        };
        __str__ = function(self) {
            var self;
            self = this;
            return self.isoformat(" ");
        };
        return [{__init__: __init__,timetuple: timetuple,astimezone: astimezone,date: date,time: time,replace: replace,timetz: timetz,utctimetuple: utctimetuple,isoformat: isoformat,__add__: __add__,__sub__: __sub__,__str__: __str__}, {combine: combine,fromtimestamp: fromtimestamp,fromordinal: fromordinal,now: now,strptime: strptime,utcfromtimestamp: utcfromtimestamp,utcnow: utcnow}, {}]
    });

    function t_datetime_timedelta() {
        this.__init__.apply(this, arguments);
    }
    timedelta = _class(t_datetime_timedelta, [object], function() {
        var __init__;
        __init__ = function(self, days, seconds, microseconds, milliseconds, minutes, hours, weeks) {
            var _args, self;
            _args = _init_args(arguments);
            days = _get_arg(1, "days", _args, 0);
            seconds = _get_arg(2, "seconds", _args, 0);
            microseconds = _get_arg(3, "microseconds", _args, 0);
            milliseconds = _get_arg(4, "milliseconds", _args, 0);
            minutes = _get_arg(5, "minutes", _args, 0);
            hours = _get_arg(6, "hours", _args, 0);
            weeks = _get_arg(7, "weeks", _args, 0);
            self = this;
            self.days = weeks * 7.0 + days;
            self.seconds = hours * 3600.0 + minutes * 60.0 + seconds;
            self.microseconds = milliseconds * 1000.0 + microseconds;
        };
        return [{__init__: __init__}, {}, {}]
    });

    function t_datetime_tzinfo() {
        this.__init__.apply(this, arguments);
    }
    tzinfo = _class(t_datetime_tzinfo, [object], function() { /* pass */
        return [{}, {}, {}]
    });
    date.min = new date(1, 1, 1);
    date.max = new date(9999, 12, 31);
    date.resolution = new timedelta(1);
    time.min = new time(0, 0);
    time.max = new time(23, 59, 59, 999999);
    time.resolution = new timedelta(0, 0, 1);
    datetime.min = new datetime(1, 1, 1, 0, 0);
    datetime.max = new datetime(9999, 12, 31, 23, 59, 59, 999999);
    datetime.resolution = new timedelta(0, 0, 1);
    timedelta.min = new timedelta(-999999999);
    timedelta.max = new timedelta(999999999, _make_kwargs({hours: 23,minutes: 59,seconds: 59,microseconds: 999999}));
    timedelta.resolution = new timedelta(0, 0, 1);
    prambanan.exports('datetime', {date: date,datetime: datetime,time: time,timedelta: timedelta,tzinfo: tzinfo});
})(prambanan);(function(prambanan) {
    var TranslationString, TranslationStringFactory,  __keyword_default, _get_arg, _init_args, _make_kwargs;

    _init_args = prambanan.helpers.init_args;
    _make_kwargs = prambanan.helpers.make_kwargs;
    _get_arg = prambanan.helpers.get_arg;

    var i_regex =  /\$\{([\s\S]+?)\}/g;
    /**
     * The constructor for a :term:`translation string`.  A translation
     * string is a Unicode-like object that has some extra metadata.
     * * This constructor accepts one required argument named ``msgid``.
     * ``msgid`` must be the :term:`message identifier` for the
     * translation string.  It must be a ``unicode`` object or a ``str``
     * object encoded in the default system encoding.
     * * Optional keyword arguments to this object's constructor include
     * ``domain``, ``default``, and ``mapping``.
     * * ``domain`` represents the :term:`translation domain`.  By default,
     * the translation domain is ``None``, indicating that this
     * translation string is associated with the default translation
     * domain (usually ``messages``).
     * * ``default`` represents an explicit *default text* for this
     * translation string.  Default text appears when the translation
     * string cannot be translated.  Usually, the ``msgid`` of a
     * translation string serves double duty as as its default text.
     * However, using this option you can provide a different default
     * text for this translation string.  This feature is useful when the
     * default of a translation string is too complicated or too long to
     * be used as a message identifier. If ``default`` is provided, it
     * must be a ``unicode`` object or a ``str`` object encoded in the
     * default system encoding (usually means ASCII).  If ``default`` is
     * ``None`` (its default value), the ``msgid`` value used by this
     * translation string will be assumed to be the value of ``default``.
     * * ``mapping``, if supplied, must be a dictionary-like object which
     * represents the replacement values for any :term:`translation
     * string` *replacement marker* instances found within the ``msgid``
     * (or ``default``) value of this translation string.
     * * After a translation string is constructed, it behaves like most
     * other ``unicode`` objects; its ``msgid`` value will be displayed
     * when it is treated like a ``unicode`` object.  Only when its
     * ``ugettext`` method is called will it be translated.
     * * Its default value is available as the ``default`` attribute of the
     * object, its :term:`translation domain` is available as the
     * ``domain`` attribute, and the ``mapping`` is available as the
     * ``mapping`` attribute.  The object otherwise behaves much like a
     * Unicode string.
     */

    function t_translationstring_TranslationString() {}
    TranslationString = function(msgid, domain, __keyword_default, mapping) {
        var _args, self;
        _args = _init_args(arguments);
        __keyword_default = _get_arg(3, "default", _args, null);
        mapping = _get_arg(4, "mapping", _args, null);
        self = new String(msgid);
        if (msgid.constructor === t_translationstring_TranslationString){
            mapping = mapping || msgid.mapping && _.clone(msgid.mapping);
            msgid = msgid.toString();
        }
        self.mapping = mapping;
        self.__mod__ = __mod__;
        self.template = _.template(msgid, undefined, {interpolate: i_regex});
        self.interpolate = interpolate;
        self.constructor = t_translationstring_TranslationString;
        return self;
    };
    /**
     * Create a new TranslationString instance with an updated mapping.
     * This makes it possible to use the standard python %-style string
     * formatting with translatable strings. Only dictionary
     * arguments are supported.
     */
    function __mod__(options) {
        var mapping, self;
        self = this;
        if (self.mapping) {
            mapping = _.clone(self.mapping);
            _.extend(mapping, options);
        } else{
            mapping = _.clone(options);
        }
        return TranslationString(self, _make_kwargs({mapping: mapping}));
    };
    /**
     * Interpolate the value ``translated`` which is assumed to
     * be a Unicode object containing zero or more *replacement
     * markers* (``${foo}`` or ``${bar}``) using the ``mapping``
     * dictionary attached to this instance.  If the ``mapping``
     * dictionary is empty or ``None``, no interpolation is
     * performed.
     * * If ``translated`` is ``None``, interpolation will be performed
     * against the ``default`` value.
     */
    function interpolate (translated) {
        var self = this;
        try{
            return self.template(self.mapping);
        }
        catch($e){
            return self.toString();
        }
    };
    /**
     * Create a factory which will generate translation strings
     * without requiring that each call to the factory be passed a
     * ``domain`` value.  A single argument is passed to this class'
     * constructor: ``domain``.  This value will be used as the
     * ``domain`` values of :class:`translationstring.TranslationString`
     * objects generated by the ``__call__`` of this class.  The
     * ``msgid``, ``mapping``, and ``default`` values provided to the
     * ``__call__`` method of an instance of this class have the meaning
     * as described by the constructor of the
     * :class:`translationstring.TranslationString`
     */
    TranslationStringFactory = function(domain) {
        var create;
        /**
         * Provided a msgid (Unicode object or :term:`translation
         * string`) and optionally a mapping object, and a *default
         * value*, return a :term:`translation string` object.
         */
        create = function(msgid, mapping, __keyword_default) {
            var _args;
            _args = _init_args(arguments);
            mapping = _get_arg(1, "mapping", _args, null);
            __keyword_default = _get_arg(2, "default", _args, null);
            return TranslationString(msgid, _make_kwargs({domain: domain,default:__keyword_default,mapping: mapping}));
        };
        return create;
    };
    prambanan.exports('translationstring', {TranslationString: TranslationString,TranslationStringFactory: TranslationStringFactory});
})(prambanan);
(function(prambanan) {
    var All, Bool, Boolean, Date, DateTime, Exception, Float, Function, Int, Integer, Invalid, KeyError, Length, Mapping, Number, OneOf, Positional, Range, SchemaNode, SchemaType, Seq, Sequence, Str, String, Time, Tuple, _, __builtin__, __import__, __keyword_function, __keyword_null, _class, _get_arg, _get_kwargs, _get_varargs, _in, _init_args, _iter, _m_colander, _make_kwargs, _marker, _null, _r_max_err, _r_min_err, _subscript, _super, _unflatten_mapping, datetime, deferred, dict, enumerate, int, interpolate, is_nonstr_iter, isinstance, iso8601, iter, itertools, len, list, map, null, object, required, sorted, str, time, timeparse, translationstring, tuple, type, xrange;
    __builtin__ = prambanan.import('__builtin__');
    xrange = __builtin__.xrange;
    map = __builtin__.map;
    Exception = __builtin__.Exception;
    tuple = __builtin__.tuple;
    int = __builtin__.int;
    __import__ = __builtin__.__import__;
    object = __builtin__.object;
    list = __builtin__.list;
    KeyError = __builtin__.KeyError;
    iter = __builtin__.iter;
    dict = __builtin__.dict;
    len = __builtin__.len;
    str = __builtin__.str;
    enumerate = __builtin__.enumerate;
    sorted = __builtin__.sorted;
    isinstance = __builtin__.isinstance;
    type = __builtin__.type;
    _iter = prambanan.helpers.iter;
    _in = prambanan.helpers. in ;
    _get_varargs = prambanan.helpers.get_varargs;
    _subscript = prambanan.helpers.subscript;
    _init_args = prambanan.helpers.init_args;
    _super = prambanan.helpers.super;
    _make_kwargs = prambanan.helpers.make_kwargs;
    _get_kwargs = prambanan.helpers.get_kwargs;
    _class = prambanan.helpers.class;
    _get_arg = prambanan.helpers.get_arg;
    datetime = __import__('datetime');
    time = __import__('time');
    itertools = __import__('itertools');
    translationstring = __import__('translationstring');
    _m_colander = __import__('colander.');
    iso8601 = _m_colander.iso8601;
    _ = translationstring.TranslationStringFactory("colander");
    required = new object();
    _marker = required;

    function t_colander__null() {
        this.__init__.apply(this, arguments);
    }
    _null = _class(t_colander__null, [object], function() {
        var __reduce__, __repr__;
        __repr__ = function(self) {
            var self;
            self = this;
            return "<colander.null>";
        };
        __reduce__ = function(self) {
            var self;
            self = this;
            return "null";
        };
        return [{__repr__: __repr__,__reduce__: __reduce__}, {}, {}]
    });
    __keyword_null = new _null();
    is_nonstr_iter = function(item) {
        return typeof item == Array;
    };
    interpolate = function(msgs) {
        var _i, _len, _list, res, s;
        res = [];
        _list = msgs;
        for (_i = 0, _len = _list.length; _i < _len; _i++) {
            s = _list[_i];
            if (hasattr(s, "interpolate")) {
                res.append(s.interpolate());
            } else{res.append(s);}
        }
        return res;
    };

    function t_colander_Invalid() {
        this.__init__.apply(this, arguments);
    }
    /**
     * An exception raised by data types and validators indicating that
     * the value for a particular node was not valid.
     * * The constructor receives a mandatory ``node`` argument.  This must
     * be an instance of the :class:`colander.SchemaNode` class, or at
     * least something with the same interface.
     * * The constructor also receives an optional ``msg`` keyword
     * argument, defaulting to ``None``.  The ``msg`` argument is a
     * freeform field indicating the error circumstance.
     * * The constructor additionally may receive an optional ``value``
     * keyword, indicating the value related to the error.
     */
    Invalid = _class(t_colander_Invalid, [Exception], function() {
        var __init__, __setitem__, _keyname, add, asdict, messages, paths, pos, positional;
        pos = null;
        positional = false;
        __init__ = function(self, node, msg, value) {
            var _args, self;
            _args = _init_args(arguments);
            msg = _get_arg(2, "msg", _args, null);
            value = _get_arg(3, "value", _args, null);
            self = this;
            _super(this, '__init__')(node, msg);
            self.node = node;
            self.msg = msg;
            self.value = value;
            self.children = [];
        };
        /**
         * Return an iterable of error messages for this exception using the
         * ``msg`` attribute of this error node.  If the ``msg`` attribute is
         * iterable, it is returned.  If it is not iterable, and is
         * non-``None``, a single-element list containing the ``msg`` value is
         * returned.  If the value is ``None``, an empty list is returned.
         */
        messages = function(self) {
            var self;
            self = this;
            if (is_nonstr_iter(self.msg)) {
                return self.msg;
            }
            if (self.msg === null) {
                return [];
            }
            return [self.msg];
        };
        /**
         * Add a child exception; ``exc`` must be an instance of
         * :class:`colander.Invalid` or a subclass.
         * * ``pos`` is a value important for accurate error reporting.  If
         * it is provided, it must be an integer representing the
         * position of ``exc`` relative to all other subexceptions of
         * this exception node.  For example, if the exception being
         * added is about the third child of the exception which is
         * ``self``, ``pos`` might be passed as ``3``.
         * * If ``pos`` is provided, it will be assigned to the ``pos``
         * attribute of the provided ``exc`` object.
         */
        add = function(self, exc, pos) {
            var _args, self;
            _args = _init_args(arguments);
            pos = _get_arg(2, "pos", _args, null);
            self = this;
            if (self.node && isinstance(self.node.typ, Positional)) {
                exc.positional = true;
            }
            if (pos != null) {
                exc.pos = pos;
            }
            self.children.append(exc);
        };
        /**
         * Add a subexception related to a child node with the
         * message ``msg``. ``name`` must be present in the names of the
         * set of child nodes of this exception's node; if this is not
         * so, a :exc:`KeyError` is raised.
         * * For example, if the exception upon which ``__setitem__`` is
         * called has a node attribute, and that node attribute has
         * children that have the names ``name`` and ``title``, you may
         * successfully call ``__setitem__('name', 'Bad name')`` or
         * ``__setitem__('title', 'Bad title')``.  But calling
         * ``__setitem__('wrong', 'whoops')`` will result in a
         * :exc:`KeyError`.
         * * This method is typically only useful if the ``node`` attribute
         * of the exception upon which it is called is a schema node
         * representing a mapping.
         */
        __setitem__ = function(self, name, msg) {
            var _i, _len, _list, child, exc, num, self;
            self = this;
            _list = enumerate(self.node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                child = _list[_i][1];
                if (child.name === name) {
                    exc = new Invalid(child, msg);
                    self.add(exc, num);
                    return;
                }
            }
            throw new KeyError(name);
        };
        /**
         * A generator which returns each path through the exception
         * graph.  Each path is represented as a tuple of exception
         * nodes.  Within each tuple, the leftmost item will represent
         * the root schema node, the rightmost item will represent the
         * leaf schema node.
         */
        paths = function(self) {
            var self, traverse;
            self = this;
            traverse = function(node, stack) {
                var _i, _i1, _len, _len1, _list, _list1, child, path, res;
                res = [];
                stack.append(node);
                if (!node.children) {
                    res.append(tuple(stack));
                }
                _list = node.children;
                for (_i = 0, _len = _list.length; _i < _len; _i++) {
                    child = _list[_i];
                    _list1 = traverse(child, stack);
                    for (_i1 = 0, _len1 = _list1.length; _i1 < _len1; _i1++) {
                        path = _list1[_i1];
                        res.append(path);
                    }
                }
                stack.pop();
            };
            return traverse(self, []);
        };
        _keyname = function(self) {
            var self;
            self = this;
            if (self.positional) {
                return str(self.pos);
            }
            return str(self.node.name);
        };
        /**
         * Return a dictionary containing a basic
         * (non-language-translated) error report for this exception
         */
        asdict = function(self) {
            var _i, _i1, _len, _len1, _list, _list1, errors, exc, keyname, keyparts, msgs, path, paths, self;
            self = this;
            paths = self.paths();
            errors = {};
            _list = paths;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                path = _list[_i];
                keyparts = [];
                msgs = [];
                _list1 = path;
                for (_i1 = 0, _len1 = _list1.length; _i1 < _len1; _i1++) {
                    exc = _list1[_i1];
                    exc.msg && msgs.extend(exc.messages());
                    keyname = exc._keyname();
                    keyname && keyparts.append(keyname);
                }
                _subscript.s.i(errors, ".".join(keyparts), "; ".join(interpolate(msgs)));
            }
            return errors;
        };
        return [{__init__: __init__,messages: messages,add: add,__setitem__: __setitem__,paths: paths,_keyname: _keyname,asdict: asdict}, {}, {}]
    });
    /**
     * Composite validator which succeeds if none of its
     * subvalidators raises an :class:`colander.Invalid` exception
     */
    All = function(validators) {
        var __call__, _args;
        _args = _init_args(arguments);
        validators = _get_varargs(0, _args);
        __call__ = function(node, value) {
            var _ex, _i, _i1, _len, _len1, _list, _list1, e, exc, excs, validator;
            excs = [];
            _list = validators;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                validator = _list[_i];
                try{validator(node, value);} catch (_ex) {
                    if (_ex instanceof Invalid) {
                        e = _ex;
                        excs.append(e);
                    } else{
                    throw _ex}
                }
            }
            if (excs) {
                exc = new Invalid(node, (function() {
                    var _i1, _len1, _list1, _results;
                    _results = [];
                    _list1 = _iter(excs);
                    for (_i1 = 0, _len1 = _list1.length; _i1 < _len1; _i1++) {
                        exc = _list1[_i1];
                        _results.push(exc.msg);
                    }
                    return _results;
                })());
                _list1 = excs;
                for (_i1 = 0, _len1 = _list1.length; _i1 < _len1; _i1++) {
                    e = _list1[_i1];
                    exc.children.extend(e.children);
                }
                throw exc;
            }
        };
        return __call__;
    };
    /**
     * Validator which accepts a function and an optional message;
     * the function is called with the ``value`` during validation.
     * * If the function returns anything falsy (``None``, ``False``, the
     * empty string, ``0``, an object with a ``__nonzero__`` that returns
     * ``False``, etc) when called during validation, an
     * :exc:`colander.Invalid` exception is raised (validation fails);
     * its msg will be the value of the ``message`` argument passed to
     * this class' constructor.
     * * If the function returns a stringlike object (a ``str`` or
     * ``unicode`` object) that is *not* the empty string , a
     * :exc:`colander.Invalid` exception is raised using the stringlike
     * value returned from the function as the exeption message
     * (validation fails).
     * * If the function returns anything *except* a stringlike object
     * object which is truthy (e.g. ``True``, the integer ``1``, an
     * object with a ``__nonzero__`` that returns ``True``, etc), an
     * :exc:`colander.Invalid` exception is *not* raised (validation
     * succeeds).
     * * The default value for the ``message`` when not provided via the
     * constructor is ``Invalid value``.
     */
    Function = function(__keyword_function, message) {
        var __call__, _args;
        _args = _init_args(arguments);
        message = _get_arg(1, "message", _args, _("Invalid value"));
        __call__ = function(node, value) {
            var result;
            result = __keyword_function(value);
            if (!result) {
                throw new Invalid(node, translationstring.TranslationString(message, _make_kwargs({mapping: {val: value}
                })));
            }
            if (isinstance(result, str)) {
                throw new Invalid(node, translationstring.TranslationString(result, _make_kwargs({mapping: {val: value}
                })));
            }
        };
        return __call__;
    };
    _r_min_err = _("${val} is less than minimum value ${min}");
    _r_max_err = _("${val} is greater than maximum value ${max}");
    /**
     * Validator which succeeds if the value it is passed is greater
     * or equal to ``min`` and less than or equal to ``max``.  If ``min``
     * is not specified, or is specified as ``None``, no lower bound
     * exists.  If ``max`` is not specified, or is specified as ``None``,
     * no upper bound exists.
     * * ``min_err`` is used to form the ``msg`` of the
     * :exc:`colander.Invalid` error when reporting a validation failure
     * caused by a value not meeting the minimum.  If ``min_err`` is
     * specified, it must be a string.  The string may contain the
     * replacement targets ``${min}`` and ``${val}``, representing the
     * minimum value and the provided value respectively.  If it is not
     * provided, it defaults to ``'${val} is less than minimum value
     * ${min}'``.
     * * ``max_err`` is used to form the ``msg`` of the
     * :exc:`colander.Invalid` error when reporting a validation failure
     * caused by a value exceeding the maximum.  If ``max_err`` is
     * specified, it must be a string.  The string may contain the
     * replacement targets ``${max}`` and ``${val}``, representing the
     * maximum value and the provided value respectively.  If it is not
     * provided, it defaults to ``'${val} is greater than maximum value
     * ${max}'``.
     */
    Range = function(min, max, min_err, max_err) {
        var __call__, _args;
        _args = _init_args(arguments);
        min = _get_arg(0, "min", _args, null);
        max = _get_arg(1, "max", _args, null);
        min_err = _get_arg(2, "min_err", _args, null);
        max_err = _get_arg(3, "max_err", _args, null);
        if (min_err === null) {
            min_err = _r_min_err;
        }
        if (max_err === null) {
            max_err = _r_max_err;
        }
        __call__ = function(node, value) {
            if (min != null) {
                if (value < min) {
                    throw new Invalid(node, _(min_err, _make_kwargs({mapping: {val: value,min: min}
                    })));
                }
            }
            if (max != null) {
                if (value > max) {
                    throw new Invalid(node, _(max_err, _make_kwargs({mapping: {val: value,max: max}
                    })));
                }
            }
        };
        return __call__;
    };
    /**
     * Validator which succeeds if the value passed to it has a
     * length between a minimum and maximum.  The value is most often a
     * string.
     */
    Length = function(min, max) {
        var __call__, _args;
        _args = _init_args(arguments);
        min = _get_arg(0, "min", _args, null);
        max = _get_arg(1, "max", _args, null);
        __call__ = function(node, value) {
            var max_err, min_err;
            if (min != null) {
                if (len(value) < min) {
                    min_err = _("Shorter than minimum length ${min}", _make_kwargs({mapping: {min: min}
                    }));
                    throw new Invalid(node, min_err);
                }
            }
            if (max != null) {
                if (len(value) > max) {
                    max_err = _("Longer than maximum length ${max}", _make_kwargs({mapping: {max: max}
                    }));
                    throw new Invalid(node, max_err);
                }
            }
        };
        return __call__;
    };
    /**
     * Validator which succeeds if the value passed to it is one of
     * a fixed set of values
     */
    OneOf = function(choices) {
        var __call__;
        __call__ = function(node, value) {
            var c, err;
            if (!_in(value, choices)) {
                c = ", ".join((function() {
                    var _i, _len, _list, _results;
                    _results = [];
                    _list = _iter(choices);
                    for (_i = 0, _len = _list.length; _i < _len; _i++) {
                        x = _list[_i];
                        _results.push("%s".__mod__(x));
                    }
                    return _results;
                })());
                err = _("\"${val}\" is not one of ${choices}", _make_kwargs({mapping: {val: value,choices: c}
                }));
                throw new Invalid(node, err);
            }
        };
        return __call__;
    };

    function t_colander_SchemaType() {
        this.__init__.apply(this, arguments);
    }
    /**
     * Base class for all schema types
     */
    SchemaType = _class(t_colander_SchemaType, [object], function() {
        var flatten, get_value, set_value, unflatten;
        flatten = function(self, node, appstruct, prefix, listitem) {
            var _args, result, self, selfname;
            _args = _init_args(arguments);
            prefix = _get_arg(3, "prefix", _args, "");
            listitem = _get_arg(4, "listitem", _args, false);
            self = this;
            result = {};
            if (listitem) {
                selfname = prefix;
            } else{selfname = "%s%s".__mod__(prefix, node.name);}
            _subscript.s.i(result, selfname, appstruct);
            return result;
        };
        unflatten = function(self, node, paths, fstruct) {
            var name, self;
            self = this;
            name = node.name;;
            return _subscript.l.i(fstruct, name);
        };
        set_value = function(self, node, appstruct, path, value) {
            var self;
            self = this;
            throw new AssertionError("Can't call 'set_value' on a leaf node.");
        };
        get_value = function(self, node, appstruct, path) {
            var self;
            self = this;
            throw new AssertionError("Can't call 'set_value' on a leaf node.");
        };
        return [{flatten: flatten,unflatten: unflatten,set_value: set_value,get_value: get_value}, {}, {}]
    });

    function t_colander_Mapping() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type which represents a mapping of names to nodes.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type imply the named keys and values in the mapping.
     * * The constructor of this type accepts one extra optional keyword
     * argument that other types do not: ``unknown``.  An attribute of
     * the same name can be set on a type instance to control the
     * behavior after construction.
     * * unknown
     * ``unknown`` controls the behavior of this type when an unknown
     * key is encountered in the cstruct passed to the
     * ``deserialize`` method of this instance.  All the potential
     * values of ``unknown`` are strings.  They are:
     * * - ``ignore`` means that keys that are not present in the schema
     * associated with this type will be ignored during
     * deserialization.
     * * - ``raise`` will cause a :exc:`colander.Invalid` exception to
     * be raised when unknown keys are present in the cstruct
     * during deserialization.
     * * - ``preserve`` will preserve the 'raw' unknown keys and values
     * in the appstruct returned by deserialization.
     * * Default: ``ignore``.
     * * Special behavior is exhibited when a subvalue of a mapping is
     * present in the schema but is missing from the mapping passed to
     * either the ``serialize`` or ``deserialize`` method of this class.
     * In this case, the :attr:`colander.null` value will be passed to
     * the ``serialize`` or ``deserialize`` method of the schema node
     * representing the subvalue of the mapping respectively.  During
     * serialization, this will result in the behavior described in
     * :ref:`serializing_null` for the subnode.  During deserialization,
     * this will result in the behavior described in
     * :ref:`deserializing_null` for the subnode.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, a dictionary will be returned, where each of
     * the values in the returned dictionary is the serialized
     * representation of the null value for its type.
     */
    Mapping = _class(t_colander_Mapping, [SchemaType], function() {
        var __init__, _impl, _validate, deserialize, flatten, get_value, serialize, set_value, unflatten;
        __init__ = function(self, unknown) {
            var _args, self;
            _args = _init_args(arguments);
            unknown = _get_arg(1, "unknown", _args, "ignore");
            self = this;
            self.unknown = unknown;
        };
        _validate = function(self, node, value) {
            var _ex, e, self;
            self = this;
            try{
            return dict(value);} catch (_ex) {
                if (_ex instanceof Exception) {
                    e = _ex;
                    throw new Invalid(node, _("\"${val}\" is not a mapping type: ${err}", _make_kwargs({mapping: {val: value,err: e}
                    })));
                } else{
                throw _ex}
            }
        };
        _impl = function(self, node, value, callback) {
            var _ex, _i, _len, _list, e, error, name, num, result, self, subnode, subval;
            self = this;
            value = self._validate(node, value);
            error = null;
            result = {};
            _list = enumerate(node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                subnode = _list[_i][1];
                name = subnode.name;
                subval = value.pop(name, __keyword_null);
                try{_subscript.s.i(result, name, callback(subnode, subval));} catch (_ex) {
                    if (_ex instanceof Invalid) {
                        e = _ex;
                        if (error === null) {
                            error = new Invalid(node);
                        }
                        error.add(e, num);
                    } else{
                    throw _ex}
                }
            }
            if (self.unknown === "raise") {
                if (value) {
                    throw new Invalid(node, _("Unrecognized keys in mapping: \"${val}\"", _make_kwargs({mapping: {val: value}
                    })));
                }
            } else{
            if (self.unknown === "preserve") {
                result.update(value);}
            }
            if (error != null) {
                throw error;
            }
            return result;
        };
        serialize = function(self, node, appstruct) {
            var callback, self;
            self = this;
            if (appstruct === __keyword_null) {
                appstruct = {};
            }
            callback = function(subnode, subappstruct) {
                return subnode.serialize(subappstruct);
            };
            return self._impl(node, appstruct, callback);
        };
        deserialize = function(self, node, cstruct) {
            var callback, self;
            self = this;
            if (cstruct === __keyword_null) {
                return __keyword_null;
            }
            callback = function(subnode, subcstruct) {
                return subnode.deserialize(subcstruct);
            };
            return self._impl(node, cstruct, callback);
        };
        flatten = function(self, node, appstruct, prefix, listitem) {
            var _args, _i, _len, _list, name, result, self, selfprefix, subnode, substruct;
            _args = _init_args(arguments);
            prefix = _get_arg(3, "prefix", _args, "");
            listitem = _get_arg(4, "listitem", _args, false);
            self = this;
            result = {};
            if (listitem) {
                selfprefix = prefix;
            } else{
            if (node.name) {
                selfprefix = "%s%s.".__mod__(prefix, node.name);} else{selfprefix = prefix;}
            }
            _list = node.children;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                subnode = _list[_i];
                name = subnode.name;
                substruct = appstruct.get(name, __keyword_null);
                result.update(subnode.typ.flatten(subnode, substruct, _make_kwargs({prefix: selfprefix})));
            }
            return result;
        };
        unflatten = function(self, node, paths, fstruct) {
            var self;
            self = this;
            return _unflatten_mapping(node, paths, fstruct);
        };
        set_value = function(self, node, appstruct, path, value) {
            var next_appstruct, next_name, next_node, rest, self;
            self = this;
            if (_in(".", path)) {
                (function(_source) {
                    next_name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
                next_node = _subscript.l.i(node, next_name);
                next_appstruct = _subscript.l.i(appstruct, next_name);
                _subscript.s.i(appstruct, next_name, next_node.typ.set_value(next_node, next_appstruct, rest, value));
            } else{_subscript.s.i(appstruct, path, value);}
            return appstruct;
        };
        get_value = function(self, node, appstruct, path) {
            var name, next_node, rest, self;
            self = this;
            if (_in(".", path)) {
                (function(_source) {
                    name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
                next_node = _subscript.l.i(node, name);
                return next_node.typ.get_value(next_node, _subscript.l.i(appstruct, name), rest);
            }
            return _subscript.l.i(appstruct, path);
        };
        return [{__init__: __init__,_validate: _validate,_impl: _impl,serialize: serialize,deserialize: deserialize,flatten: flatten,unflatten: unflatten,set_value: set_value,get_value: get_value}, {}, {}]
    });

    function t_colander_Positional() {
        this.__init__.apply(this, arguments);
    }
    /**
     * Marker abstract base class meaning 'this type has children which
     * should be addressed by position instead of name' (e.g. via seq[0],
     * but never seq['name']).  This is consulted by Invalid.asdict when
     * creating a dictionary representation of an error tree.
     */
    Positional = _class(t_colander_Positional, [object], function() {
        return [{}, {}, {}]
    });

    function t_colander_Tuple() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type which represents a fixed-length sequence of nodes.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type imply the positional elements of the tuple in the order
     * they are added.
     * * This type is willing to serialize and deserialized iterables that,
     * when converted to a tuple, have the same number of elements as the
     * number of the associated node's subnodes.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     */
    Tuple = _class(t_colander_Tuple, [Positional, SchemaType], function() {
        var _impl, _validate, deserialize, flatten, get_value, serialize, set_value, unflatten;
        _validate = function(self, node, value) {
            var nodelen, self, valuelen;
            self = this;
            if (!hasattr(value, "__iter__")) {
                throw new Invalid(node, _("\"${val}\" is not iterable", _make_kwargs({mapping: {val: value}
                })));
            }(function(_source) {
                valuelen = _source[0];
                nodelen = _source[1];
            })([len(value), len(node.children)]);
            if (valuelen !== nodelen) {
                throw new Invalid(node, _("\"${val}\" has an incorrect number of elements (expected ${exp}, was ${was})", _make_kwargs({mapping: {val: value,exp: nodelen,was: valuelen}
                })));
            }
            return list(value);
        };
        _impl = function(self, node, value, callback) {
            var _ex, _i, _len, _list, e, error, num, result, self, subnode, subval;
            self = this;
            value = self._validate(node, value);
            error = null;
            result = [];
            _list = enumerate(node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                subnode = _list[_i][1];
                subval = _subscript.l.i(value, num);
                try{result.append(callback(subnode, subval));} catch (_ex) {
                    if (_ex instanceof Invalid) {
                        e = _ex;
                        if (error === null) {
                            error = new Invalid(node);
                        }
                        error.add(e, num);
                    } else{
                    throw _ex}
                }
            }
            if (error != null) {
                throw error;
            }
            return tuple(result);
        };
        serialize = function(self, node, appstruct) {
            var callback, self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            callback = function(subnode, subappstruct) {
                return subnode.serialize(subappstruct);
            };
            return self._impl(node, appstruct, callback);
        };
        deserialize = function(self, node, cstruct) {
            var callback, self;
            self = this;
            if (cstruct === __keyword_null) {
                return __keyword_null;
            }
            callback = function(subnode, subval) {
                return subnode.deserialize(subval);
            };
            return self._impl(node, cstruct, callback);
        };
        flatten = function(self, node, appstruct, prefix, listitem) {
            var _args, _i, _len, _list, num, result, self, selfprefix, subnode, substruct;
            _args = _init_args(arguments);
            prefix = _get_arg(3, "prefix", _args, "");
            listitem = _get_arg(4, "listitem", _args, false);
            self = this;
            result = {};
            if (listitem) {
                selfprefix = prefix;
            } else{selfprefix = "%s%s.".__mod__(prefix, node.name);}
            _list = enumerate(node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                subnode = _list[_i][1];
                substruct = _subscript.l.i(appstruct, num);
                result.update(subnode.typ.flatten(subnode, substruct, _make_kwargs({prefix: selfprefix})));
            }
            return result;
        };
        unflatten = function(self, node, paths, fstruct) {
            var _i, _len, _list, appstruct, mapstruct, self, subnode;
            self = this;
            mapstruct = _unflatten_mapping(node, paths, fstruct);
            appstruct = [];
            _list = node.children;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                subnode = _list[_i];
                appstruct.append(_subscript.l.i(mapstruct, subnode.name));
            }
            return tuple(appstruct);
        };
        set_value = function(self, node, appstruct, path, value) {
            var _i, _len, _list, index, next_appstruct, next_name, next_node, rest, self;
            self = this;
            appstruct = list(appstruct);
            if (_in(".", path)) {
                (function(_source) {
                    next_name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
            } else{ (function(_source) {
                next_name = _source[0];
                rest = _source[1];})([path, null]);
            }
            _list = enumerate(node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                index = _list[_i][0];
                next_node = _list[_i][1];
                if (next_node.name === next_name) {
                    break;
                }
            }
            if (_i == _len) {
                throw new KeyError(next_name);
            }
            if (rest != null) {
                next_appstruct = _subscript.l.i(appstruct, index);
                _subscript.s.i(appstruct, index, next_node.typ.set_value(next_node, next_appstruct, rest, value));
            } else{_subscript.s.i(appstruct, index, value);}
            return tuple(appstruct);
        };
        get_value = function(self, node, appstruct, path) {
            var _i, _len, _list, index, name, next_node, rest, self;
            self = this;
            if (_in(".", path)) {
                (function(_source) {
                    name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
            } else{ (function(_source) {
                name = _source[0];
                rest = _source[1];})([path, null]);
            }
            _list = enumerate(node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                index = _list[_i][0];
                next_node = _list[_i][1];
                if (next_node.name === name) {
                    break;
                }
            }
            if (_i == _len) {
                throw new KeyError(name);
            }
            if (rest != null) {
                return next_node.typ.get_value(next_node, _subscript.l.i(appstruct, index), rest);
            }
            return _subscript.l.i(appstruct, index);
        };
        return [{_validate: _validate,_impl: _impl,serialize: serialize,deserialize: deserialize,flatten: flatten,unflatten: unflatten,set_value: set_value,get_value: get_value}, {}, {}]
    });

    function t_colander_Sequence() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type which represents a variable-length sequence of nodes,
     * all of which must be of the same type.
     * * The type of the first subnode of the
     * :class:`colander.SchemaNode` that wraps this type is considered the
     * sequence type.
     * * The optional ``accept_scalar`` argument to this type's constructor
     * indicates what should happen if the value found during serialization or
     * deserialization does not have an ``__iter__`` method or is a
     * mapping type.
     * * If ``accept_scalar`` is ``True`` and the value does not have an
     * ``__iter__`` method or is a mapping type, the value will be turned
     * into a single element list.
     * * If ``accept_scalar`` is ``False`` and the value does not have an
     * ``__iter__`` method or is a mapping type, an
     * :exc:`colander.Invalid` error will be raised during serialization
     * and deserialization.
     * * The default value of ``accept_scalar`` is ``False``.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value is returned.
     */
    Sequence = _class(t_colander_Sequence, [Positional, SchemaType], function() {
        var __init__, _impl, _validate, deserialize, flatten, get_value, serialize, set_value, unflatten;
        __init__ = function(self, accept_scalar) {
            var _args, self;
            _args = _init_args(arguments);
            accept_scalar = _get_arg(1, "accept_scalar", _args, false);
            self = this;
            self.accept_scalar = accept_scalar;
        };
        _validate = function(self, node, value, accept_scalar) {
            var self;
            self = this;
            if (hasattr(value, "__iter__") && !hasattr(value, "get")) {
                return list(value);
            }
            if (accept_scalar) {
                return [value];
            } else{
            throw new Invalid(node, _("\"${val}\" is not iterable", _make_kwargs({mapping: {val: value}
            })));
            }
        };
        _impl = function(self, node, value, callback, accept_scalar) {
            var _ex, _i, _len, _list, e, error, num, result, self, subval;
            self = this;
            if (accept_scalar === null) {
                accept_scalar = self.accept_scalar;
            }
            value = self._validate(node, value, accept_scalar);
            error = null;
            result = [];
            _list = enumerate(value);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                subval = _list[_i][1];
                try{result.append(callback(_subscript.l.i(node.children, 0), subval));} catch (_ex) {
                    if (_ex instanceof Invalid) {
                        e = _ex;
                        if (error === null) {
                            error = new Invalid(node);
                        }
                        error.add(e, num);
                    } else{
                    throw _ex}
                }
            }
            if (error != null) {
                throw error;
            }
            return result;
        };
        /**
         * Along with the normal ``node`` and ``appstruct`` arguments,
         * this method accepts an additional optional keyword argument:
         * ``accept_scalar``.  This keyword argument can be used to
         * override the constructor value of the same name.
         * * If ``accept_scalar`` is ``True`` and the ``appstruct`` does
         * not have an ``__iter__`` method or is a mapping type, the
         * value will be turned into a single element list.
         * * If ``accept_scalar`` is ``False`` and the ``appstruct`` does
         * not have an ``__iter__`` method or is a mapping type, an
         * :exc:`colander.Invalid` error will be raised during
         * serialization and deserialization.
         * * The default of ``accept_scalar`` is ``None``, which means
         * respect the default ``accept_scalar`` value attached to this
         * instance via its constructor.
         */
        serialize = function(self, node, appstruct, accept_scalar) {
            var _args, callback, self;
            _args = _init_args(arguments);
            accept_scalar = _get_arg(3, "accept_scalar", _args, null);
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            callback = function(subnode, subappstruct) {
                return subnode.serialize(subappstruct);
            };
            return self._impl(node, appstruct, callback, accept_scalar);
        };
        /**
         * Along with the normal ``node`` and ``cstruct`` arguments, this
         * method accepts an additional optional keyword argument:
         * ``accept_scalar``.  This keyword argument can be used to
         * override the constructor value of the same name.
         * * If ``accept_scalar`` is ``True`` and the ``cstruct`` does not
         * have an ``__iter__`` method or is a mapping type, the value
         * will be turned into a single element list.
         * * If ``accept_scalar`` is ``False`` and the ``cstruct`` does not have an
         * ``__iter__`` method or is a mapping type, an
         * :exc:`colander.Invalid` error will be raised during serialization
         * and deserialization.
         * * The default of ``accept_scalar`` is ``None``, which means
         * respect the default ``accept_scalar`` value attached to this
         * instance via its constructor.
         */
        deserialize = function(self, node, cstruct, accept_scalar) {
            var _args, callback, self;
            _args = _init_args(arguments);
            accept_scalar = _get_arg(3, "accept_scalar", _args, null);
            self = this;
            if (cstruct === __keyword_null) {
                return __keyword_null;
            }
            callback = function(subnode, subcstruct) {
                return subnode.deserialize(subcstruct);
            };
            return self._impl(node, cstruct, callback, accept_scalar);
        };
        flatten = function(self, node, appstruct, prefix, listitem) {
            var _args, _i, _len, _list, childnode, num, result, self, selfprefix, subname, subprefix, subval;
            _args = _init_args(arguments);
            prefix = _get_arg(3, "prefix", _args, "");
            listitem = _get_arg(4, "listitem", _args, false);
            self = this;
            result = {};
            if (listitem) {
                selfprefix = prefix;
            } else{selfprefix = "%s%s.".__mod__(prefix, node.name);}
            childnode = node.children[0];
            _list = enumerate(appstruct);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                subval = _list[_i][1];
                subname = "%s%s".__mod__(selfprefix, num);
                subprefix = subname + ".";
                result.update(childnode.typ.flatten(childnode, subval, _make_kwargs({prefix: subprefix,listitem: true})));
            }
            return result;
        };
        unflatten = function(self, node, paths, fstruct) {
            var child_name, get_child, mapstruct, only_child, rewrite_subpath, self;
            self = this;
            only_child = node.children[0];
            child_name = only_child.name;
            get_child = function(name) {
                return only_child;
            };
            rewrite_subpath = function(subpath) {
                var suffix;
                if (_in(".", subpath)) {
                    suffix = subpath.split(".", 1)[1];
                    return "%s.%s".__mod__(child_name, suffix);
                }
                return child_name;
            };
            mapstruct = _unflatten_mapping(node, paths, fstruct, get_child, rewrite_subpath);
            return (function() {
                var _i, _len, _list, _results;
                _results = [];
                _list = _iter(xrange(len(mapstruct)));
                for (_i = 0, _len = _list.length; _i < _len; _i++) {
                    index = _list[_i];
                    _results.push(_subscript.l.i(mapstruct, str(index)));
                }
                return _results;
            })();
        };
        set_value = function(self, node, appstruct, path, value) {
            var index, next_appstruct, next_name, next_node, rest, self;
            self = this;
            if (_in(".", path)) {
                (function(_source) {
                    next_name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
                index = int(next_name);
                next_node = node.children[0];
                next_appstruct = _subscript.l.i(appstruct, index);
                _subscript.s.i(appstruct, index, next_node.typ.set_value(next_node, next_appstruct, rest, value));
            } else{index = int(path);
            _subscript.s.i(appstruct, index, value);}
            return appstruct;
        };
        get_value = function(self, node, appstruct, path) {
            var index, name, next_node, rest, self;
            self = this;
            if (_in(".", path)) {
                (function(_source) {
                    name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
                index = int(name);
                next_node = node.children[0];
                return next_node.typ.get_value(next_node, _subscript.l.i(appstruct, index), rest);
            }
            return _subscript.l.i(appstruct, int(path));
        };
        return [{__init__: __init__,_validate: _validate,_impl: _impl,serialize: serialize,deserialize: deserialize,flatten: flatten,unflatten: unflatten,set_value: set_value,get_value: get_value}, {}, {}]
    });
    Seq = Sequence;

    function t_colander_String() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a Unicode string.
     * * This type constructor accepts one argument:
     * * ``encoding``
     * Represents the encoding which should be applied to value
     * serialization and deserialization, for example ``utf-8``.  If
     * ``encoding`` is passed as ``None``, the ``serialize`` method of
     * this type will not do any special encoding of the appstruct it is
     * provided, nor will the ``deserialize`` method of this type do
     * any special decoding of the cstruct it is provided; inputs and
     * outputs will be assumed to be Unicode.  ``encoding`` defaults
     * to ``None``.
     * * If ``encoding`` is ``None``:
     * * - A Unicode input value to ``serialize`` is returned untouched.
     * * - A non-Unicode input value to ``serialize`` is run through the
     * ``unicode()`` function without an ``encoding`` parameter
     * (``unicode(value)``) and the result is returned.
     * * - A Unicode input value to ``deserialize`` is returned untouched.
     * * - A non-Unicode input value to ``deserialize`` is run through the
     * ``unicode()`` function without an ``encoding`` parameter
     * (``unicode(value)``) and the result is returned.
     * * If ``encoding`` is not ``None``:
     * * - A Unicode input value to ``serialize`` is run through the
     * ``unicode`` function with the encoding parameter
     * (``unicode(value, encoding)``) and the result (a ``str``
     * object) is returned.
     * * - A non-Unicode input value to ``serialize`` is converted to a
     * Unicode using the encoding (``unicode(value, encoding)``);
     * subsequently the Unicode object is reeencoded to a ``str``
     * object using the encoding and returned.
     * * - A Unicode input value to ``deserialize`` is returned
     * untouched.
     * * - A non-Unicode input value to ``deserialize`` is converted to
     * a ``str`` object using ``str(value``).  The resulting str
     * value is converted to Unicode using the encoding
     * (``unicode(value, encoding)``) and the result is returned.
     * * A corollary: If a string (as opposed to a unicode object) is
     * provided as a value to either the serialize or deserialize
     * method of this type, and the type also has an non-None
     * ``encoding``, the string must be encoded with the type's
     * encoding.  If this is not true, an :exc:`colander.Invalid`
     * error will result.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    String = _class(t_colander_String, [SchemaType], function() {
        var __init__, deserialize, serialize;
        __init__ = function(self, encoding) {
            var _args, self;
            _args = _init_args(arguments);
            encoding = _get_arg(1, "encoding", _args, null);
            self = this;
            self.encoding = encoding;
        };
        serialize = function(self, node, appstruct) {
            var _ex, e, self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            try{
            return str(appstruct);} catch (_ex) {
                if (_ex instanceof Exception) {
                    e = _ex;
                    throw new Invalid(node, _("${val} cannot be serialized: ${err}", _make_kwargs({mapping: {val: appstruct,err: e}
                    })));
                } else{
                throw _ex}
            }
        };
        deserialize = function(self, node, cstruct) {
            var _ex, e, self;
            self = this;
            if (!cstruct) {
                return __keyword_null;
            }
            try{
            return str(cstruct);} catch (_ex) {
                if (_ex instanceof Exception) {
                    e = _ex;
                    throw new Invalid(node, _("${val} is not a string: ${err}", _make_kwargs({mapping: {val: cstruct,err: e}
                    })));
                } else{
                throw _ex}
            }
        };
        return [{__init__: __init__,serialize: serialize,deserialize: deserialize}, {}, {}]
    });
    Str = String;

    function t_colander_Number() {
        this.__init__.apply(this, arguments);
    }
    /**
     * Abstract base class for float, int, decimal
     */
    Number = _class(t_colander_Number, [SchemaType], function() {
        var deserialize, num, serialize;
        num = null;
        serialize = function(self, node, appstruct) {
            var _ex, self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            try{
            return str(self.num(appstruct));} catch (_ex) {
                if (_ex instanceof Exception) {
                    throw new Invalid(node, _("\"${val}\" is not a number", _make_kwargs({mapping: {val: appstruct}
                    })));
                } else{
                throw _ex}
            }
        };
        deserialize = function(self, node, cstruct) {
            var _ex, self;
            self = this;
            if (cstruct !== 0 && !cstruct) {
                return __keyword_null;
            }
            try{
            return self.num(cstruct);} catch (_ex) {
                if (_ex instanceof Exception) {
                    throw new Invalid(node, _("\"${val}\" is not a number", _make_kwargs({mapping: {val: cstruct}
                    })));
                } else{
                throw _ex}
            }
        };
        return [{serialize: serialize,deserialize: deserialize}, {}, {}]
    });

    function t_colander_Integer() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing an integer.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    Integer = _class(t_colander_Integer, [Number], function() {
        var num;
        num = int;
        return [{}, {}, {}]
    });
    Int = Integer;

    function t_colander_Float() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a float.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    Float = _class(t_colander_Float, [Number], function() {
        var num;
        num = float;
        return [{}, {}, {}]
    });

    function t_colander_Boolean() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a boolean object.
     * * During deserialization, a value in the set (``false``, ``0``) will
     * be considered ``False``.  Anything else is considered
     * ``True``. Case is ignored.
     * * Serialization will produce ``true`` or ``false`` based on the
     * value.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    Boolean = _class(t_colander_Boolean, [SchemaType], function() {
        var deserialize, serialize;
        serialize = function(self, node, appstruct) {
            var self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            return appstruct && "true" || "false";
        };
        deserialize = function(self, node, cstruct) {
            var _ex, result, self;
            self = this;
            if (cstruct === __keyword_null) {
                return __keyword_null;
            }
            try{result = str(cstruct);} catch (_ex) {
                throw new Invalid(node, _("${val} is not a string", _make_kwargs({mapping: {val: cstruct}
                })));
            }
            result = result.lower();
            if (_in(result, ["false", "0"])) {
                return false;
            }
            return true;
        };
        return [{serialize: serialize,deserialize: deserialize}, {}, {}]
    });
    Bool = Boolean;

    function t_colander_DateTime() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a Python ``datetime.datetime`` object.
     * * This type serializes python ``datetime.datetime`` objects to a
     * `ISO8601 <http://en.wikipedia.org/wiki/ISO_8601>`_ string format.
     * The format includes the date, the time, and the timezone of the
     * datetime.
     * * The constructor accepts an argument named ``default_tzinfo`` which
     * should be a Python ``tzinfo`` object; by default it is None,
     * meaning that the default tzinfo will be equivalent to UTC (Zulu
     * time).  The ``default_tzinfo`` tzinfo object is used to convert
     * 'naive' datetimes to a timezone-aware representation during
     * serialization.
     * * You can adjust the error message reported by this class by
     * changing its ``err_template`` attribute in a subclass on an
     * instance of this class.  By default, the ``err_template``
     * attribute is the string ``Invalid date``.  This string is used as
     * the interpolation subject of a dictionary composed of ``val`` and
     * ``err``.  ``val`` and ``err`` are the unvalidatable value and the
     * exception caused trying to convert the value, respectively. These
     * may be used in an overridden err_template as ``${val}`` and
     * ``${err}`` respectively as necessary, e.g. ``_('${val} cannot be
     * parsed as an iso8601 date: ${err}')``.
     * * For convenience, this type is also willing to coerce
     * ``datetime.date`` objects to a DateTime ISO string representation
     * during serialization.  It does so by using midnight of the day as
     * the time, and uses the ``default_tzinfo`` to give the
     * serialization a timezone.
     * * Likewise, for convenience, during deserialization, this type will
     * convert ``YYYY-MM-DD`` ISO8601 values to a datetime object.  It
     * does so by using midnight of the day as the time, and uses the
     * ``default_tzinfo`` to give the serialization a timezone.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    DateTime = _class(t_colander_DateTime, [SchemaType], function() {
        var __init__, deserialize, err_template, serialize;
        err_template = _("Invalid date");
        __init__ = function(self, default_tzinfo) {
            var _args, self;
            _args = _init_args(arguments);
            default_tzinfo = _get_arg(1, "default_tzinfo", _args, _marker);
            self = this;
            if (default_tzinfo === _marker) {
                default_tzinfo = iso8601.Utc();
            }
            self.default_tzinfo = default_tzinfo;
        };
        serialize = function(self, node, appstruct) {
            var self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            if (type(appstruct) === datetime.date) {
                appstruct = datetime.datetime.combine(appstruct, new datetime.time());
            }
            if (!isinstance(appstruct, datetime.datetime)) {
                throw new Invalid(node, _("\"${val}\" is not a datetime object", _make_kwargs({mapping: {val: appstruct}
                })));
            }
            return appstruct.isoformat();
        };
        deserialize = function(self, node, cstruct) {
            var _ex, _ex1, day, e, month, result, self, year;
            self = this;
            if (!cstruct) {
                return __keyword_null;
            }
            try{result = iso8601.parse_date(cstruct);} catch (_ex) {
                if ((_ex instanceof iso8601.ParseError) || (_ex instanceof TypeError)) {
                    e = _ex;
                    try{ (function(_source) {
                        year = _source[0];
                        month = _source[1];
                        day = _source[2];})(map(int, cstruct.split("-", 2)));
                    result = new datetime.datetime(year, month, day);
                    } catch (_ex1) {
                        if (_ex1 instanceof Exception) {
                            e = _ex1;
                            throw new Invalid(node, _(self.err_template, _make_kwargs({mapping: {val: cstruct,err: e}
                            })));
                        } else{
                        throw _ex1}
                    }
                } else{
                throw _ex}
            }
            return result;
        };
        return [{__init__: __init__,serialize: serialize,deserialize: deserialize}, {}, {}]
    });

    function t_colander_Date() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a Python ``datetime.date`` object.
     * * This type serializes python ``datetime.date`` objects to a
     * `ISO8601 <http://en.wikipedia.org/wiki/ISO_8601>`_ string format.
     * The format includes the date only.
     * * The constructor accepts no arguments.
     * * You can adjust the error message reported by this class by
     * changing its ``err_template`` attribute in a subclass on an
     * instance of this class.  By default, the ``err_template``
     * attribute is the string ``Invalid date``.  This string is used as
     * the interpolation subject of a dictionary composed of ``val`` and
     * ``err``.  ``val`` and ``err`` are the unvalidatable value and the
     * exception caused trying to convert the value, respectively. These
     * may be used in an overridden err_template as ``${val}`` and
     * ``${err}`` respectively as necessary, e.g. ``_('${val} cannot be
     * parsed as an iso8601 date: ${err}')``.
     * * For convenience, this type is also willing to coerce
     * ``datetime.datetime`` objects to a date-only ISO string
     * representation during serialization.  It does so by stripping off
     * any time information, converting the ``datetime.datetime`` into a
     * date before serializing.
     * * Likewise, for convenience, this type is also willing to coerce ISO
     * representations that contain time info into a ``datetime.date``
     * object during deserialization.  It does so by throwing away any
     * time information related to the serialized value during
     * deserialization.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    Date = _class(t_colander_Date, [SchemaType], function() {
        var deserialize, err_template, serialize;
        err_template = _("Invalid date");
        serialize = function(self, node, appstruct) {
            var self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            if (isinstance(appstruct, datetime.datetime)) {
                appstruct = appstruct.date();
            }
            if (!isinstance(appstruct, datetime.date)) {
                throw new Invalid(node, _("\"${val}\" is not a date object", _make_kwargs({mapping: {val: appstruct}
                })));
            }
            return appstruct.isoformat();
        };
        deserialize = function(self, node, cstruct) {
            var _ex, _ex1, day, e, month, result, self, year;
            self = this;
            if (!cstruct) {
                return __keyword_null;
            }
            try{result = iso8601.parse_date(cstruct);
            result = result.date();} catch (_ex) {
                if ((_ex instanceof iso8601.ParseError) || (_ex instanceof TypeError)) {
                    try{ (function(_source) {
                        year = _source[0];
                        month = _source[1];
                        day = _source[2];})(map(int, cstruct.split("-", 2)));
                    result = new datetime.date(year, month, day);
                    } catch (_ex1) {
                        if (_ex1 instanceof Exception) {
                            e = _ex1;
                            throw new Invalid(node, _(self.err_template, _make_kwargs({mapping: {val: cstruct,err: e}
                            })));
                        } else{
                        throw _ex1}
                    }
                } else{
                throw _ex}
            }
            return result;
        };
        return [{serialize: serialize,deserialize: deserialize}, {}, {}]
    });

    function t_colander_Time() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a Python ``datetime.time`` object.
     * * .. note:: This type is new as of Colander 0.9.3.
     * * This type serializes python ``datetime.time`` objects to a
     * `ISO8601 <http://en.wikipedia.org/wiki/ISO_8601>`_ string format.
     * The format includes the date only.
     * * The constructor accepts no arguments.
     * * You can adjust the error message reported by this class by
     * changing its ``err_template`` attribute in a subclass on an
     * instance of this class.  By default, the ``err_template``
     * attribute is the string ``Invalid date``.  This string is used as
     * the interpolation subject of a dictionary composed of ``val`` and
     * ``err``.  ``val`` and ``err`` are the unvalidatable value and the
     * exception caused trying to convert the value, respectively. These
     * may be used in an overridden err_template as ``${val}`` and
     * ``${err}`` respectively as necessary, e.g. ``_('${val} cannot be
     * parsed as an iso8601 date: ${err}')``.
     * * For convenience, this type is also willing to coerce
     * ``datetime.datetime`` objects to a time-only ISO string
     * representation during serialization.  It does so by stripping off
     * any date information, converting the ``datetime.datetime`` into a
     * time before serializing.
     * * Likewise, for convenience, this type is also willing to coerce ISO
     * representations that contain time info into a ``datetime.time``
     * object during deserialization.  It does so by throwing away any
     * date information related to the serialized value during
     * deserialization.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    Time = _class(t_colander_Time, [SchemaType], function() {
        var deserialize, err_template, serialize;
        err_template = _("Invalid time");
        serialize = function(self, node, appstruct) {
            var self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            if (isinstance(appstruct, datetime.datetime)) {
                appstruct = appstruct.time();
            }
            if (!isinstance(appstruct, datetime.time)) {
                throw new Invalid(node, _("\"${val}\" is not a time object", _make_kwargs({mapping: {val: appstruct}
                })));
            }
            return _subscript.l.i(appstruct.isoformat().split("."), 0);
        };
        deserialize = function(self, node, cstruct) {
            var _ex, _ex1, _ex2, e, result, self;
            self = this;
            if (!cstruct) {
                return __keyword_null;
            }
            try{result = iso8601.parse_date(cstruct);
            result = result.time();} catch (_ex) {
                if ((_ex instanceof iso8601.ParseError) || (_ex instanceof TypeError)) {
                    try{result = timeparse(cstruct, "%H:%M:%S");} catch (_ex1) {
                        if (_ex1 instanceof ValueError) {
                            try{result = timeparse(cstruct, "%H:%M");} catch (_ex2) {
                                if (_ex2 instanceof Exception) {
                                    e = _ex2;
                                    throw new Invalid(node, _(self.err_template, _make_kwargs({mapping: {val: cstruct,err: e}
                                    })));
                                } else{
                                throw _ex2}
                            }
                        } else{
                        throw _ex1}
                    }
                } else{
                throw _ex}
            }
            return result;
        };
        return [{serialize: serialize,deserialize: deserialize}, {}, {}]
    });
    timeparse = function(t, format) {
        return new datetime.datetime(_subscript.l.s(time.strptime(t, format), 0, 6, null)).time();
    };
    var _schema_counter = 0;

    function t_colander_SchemaNode() {
        this.__init__.apply(this, arguments);
    }
    /**
     * Fundamental building block of schemas.
     * * The constructor accepts these positional arguments:
     * * - ``typ`` (required): The 'type' for this node.  It should be an
     * instance of a class that implements the
     * :class:`colander.interfaces.Type` interface.
     * * - ``children``: a sequence of subnodes.  If the subnodes of this
     * node are not known at construction time, they can later be added
     * via the ``add`` method.
     * * The constructor accepts these keyword arguments:
     * * - ``name``: The name of this node.
     * * - ``default``: The default serialization value for this node.
     * Default: :attr:`colander.null`.
     * * - ``missing``: The default deserialization value for this node.  If it is
     * not provided, the missing value of this node will be the special marker
     * value :attr:`colander.required`, indicating that it is considered
     * 'required'.  When ``missing`` is :attr:`colander.required`, the
     * ``required`` computed attribute will be ``True``.
     * * - ``preparer``: Optional preparer for this node.  It should be
     * an object that implements the
     * :class:`colander.interfaces.Preparer` interface.
     * * - ``validator``: Optional validator for this node.  It should be
     * an object that implements the
     * :class:`colander.interfaces.Validator` interface.
     * * - ``after_bind``: A callback which is called after a clone of this
     * node has 'bound' all of its values successfully. This callback
     * is useful for performing arbitrary actions to the cloned node,
     * or direct children of the cloned node (such as removing or
     * adding children) at bind time.  A 'binding' is the result of an
     * execution of the ``bind`` method of the clone's prototype node,
     * or one of the parents of the clone's prototype nodes.  The
     * deepest nodes in the node tree are bound first, so the
     * ``after_bind`` methods of the deepest nodes are called before
     * the shallowest.  The ``after_bind`` callback should should
     * accept two values: ``node`` and ``kw``.  ``node`` will be a
     * clone of the bound node object, ``kw`` will be the set of
     * keywords passed to the ``bind`` method.
     * * - ``title``: The title of this node.  Defaults to a titleization
     * of the ``name`` (underscores replaced with empty strings and the
     * first letter of every resulting word capitalized).  The title is
     * used by higher-level systems (not by Colander itself).
     * * - ``description``: The description for this node.  Defaults to
     * ``''`` (the empty string).  The description is used by
     * higher-level systems (not by Colander itself).
     * * - ``widget``: The 'widget' for this node.  Defaults to ``None``.
     * The widget attribute is not interpreted by Colander itself, it
     * is only meaningful to higher-level systems such as Deform.
     * * Arbitrary keyword arguments remaining will be attached to the node
     * object unmolested.
     * * _counter = itertools.count()
     * * def __new__(cls, *arg, **kw):
     * inst = object.__new__(cls)
     * inst._order = next(cls._counter)
     * return inst
     */
    SchemaNode = _class(t_colander_SchemaNode, [object], function() {
        var __contains__, __delitem__, __getitem__, __init__, __iter__, __repr__, __setitem__, _bind, add, bind, clone, deserialize, flatten, get_value, required, serialize, set_value, unflatten;
        __init__ = function(self, typ, children, kw) {
            var _args, self;
            _args = _init_args(arguments);
            children = _get_varargs(2, _args);
            kw = _get_kwargs(_args);
            self = this;
            self._order = _schema_counter++;
            self.typ = typ;
            self.preparer = kw.pop("preparer", null);
            self.validator = kw.pop("validator", null);
            self.
        default = kw.pop("default", __keyword_null);
            self.missing = kw.pop("missing", required);
            self.name = kw.pop("name", "");
            self.raw_title = kw.pop("title", _marker);
            if (self.raw_title === _marker) {
                self.title = self.name.replace("_", " ").title();
            } else{self.title = self.raw_title;}
            self.description = kw.pop("description", "");
            self.widget = kw.pop("widget", null);
            self.after_bind = kw.pop("after_bind", null);
            self.__dict__.update(kw);
            self.children = list(children);
        };
        /**
         * A property which returns ``True`` if the ``missing`` value
         * related to this node was not specified.
         * * A return value of ``True`` implies that a ``missing`` value wasn't
         * specified for this node or that the ``missing`` value of this node is
         * :attr:`colander.required`.  A return value of ``False`` implies that
         * a 'real' ``missing`` value was specified for this node.
         */
        required = function(self) {
            var self;
            self = this;
            if (isinstance(self.missing, deferred)) {
                return true;
            }
            return self.missing === required;
        };
        /**
         * Serialize the :term:`appstruct` to a :term:`cstruct` based
         * on the schema represented by this node and return the
         * cstruct.
         * * If ``appstruct`` is :attr:`colander.null`, return the
         * serialized value of this node's ``default`` attribute (by
         * default, the serialization of :attr:`colander.null`).
         * * If an ``appstruct`` argument is not explicitly provided, it
         * defaults to :attr:`colander.null`.
         */
        serialize = function(self, appstruct) {
            var _args, cstruct, self;
            _args = _init_args(arguments);
            appstruct = _get_arg(1, "appstruct", _args, __keyword_null);
            self = this;
            if (appstruct === __keyword_null) {
                appstruct = self.
            default;
            }
            if (isinstance(appstruct, deferred)) {
                appstruct = __keyword_null;
            }
            cstruct = self.typ.serialize(self, appstruct);
            return cstruct;
        };
        /**
         * Create and return a data structure which is a flattened
         * representation of the passed in struct based on the schema represented
         * by this node.  The return data structure is a dictionary; its keys are
         * dotted names.  Each dotted name represents a path to a location in the
         * schema.  The values of of the flattened dictionary are subvalues of
         * the passed in struct.
         */
        flatten = function(self, appstruct) {
            var flat, self;
            self = this;
            flat = self.typ.flatten(self, appstruct);
            return flat;
        };
        /**
         * Create and return a data structure with nested substructures based
         * on the schema represented by this node using the flattened
         * representation passed in. This is the inverse operation to
         * :meth:`colander.SchemaNode.flatten`.
         */
        unflatten = function(self, fstruct) {
            var paths, self;
            self = this;
            paths = sorted(fstruct.keys());
            return self.typ.unflatten(self, paths, fstruct);
        };
        /**
         * Uses the schema to set a value in a nested datastructure from a
         * dotted name path.
         */
        set_value = function(self, appstruct, dotted_name, value) {
            var self;
            self = this;
            self.typ.set_value(self, appstruct, dotted_name, value);
        };
        /**
         * Traverses the nested data structure using the schema and retrieves
         * the value specified by the dotted name path.
         */
        get_value = function(self, appstruct, dotted_name) {
            var self;
            self = this;
            return self.typ.get_value(self, appstruct, dotted_name);
        };
        /**
         * Deserialize the :term:`cstruct` into an :term:`appstruct` based
         * on the schema, run this :term:`appstruct` through the
         * preparer, if one is present, then validate the
         * prepared appstruct.  The ``cstruct`` value is deserialized into an
         * ``appstruct`` unconditionally.
         * * If ``appstruct`` returned by type deserialization and
         * preparation is the value :attr:`colander.null`, do something
         * special before attempting validation:
         * * - If the ``missing`` attribute of this node has been set explicitly,
         * return its value.  No validation of this value is performed; it is
         * simply returned.
         * * - If the ``missing`` attribute of this node has not been set
         * explicitly, raise a :exc:`colander.Invalid` exception error.
         * * If the appstruct is not ``colander.null`` and cannot be validated , a
         * :exc:`colander.Invalid` exception will be raised.
         * * If a ``cstruct`` argument is not explicitly provided, it
         * defaults to :attr:`colander.null`.
         */
        deserialize = function(self, cstruct) {
            var _args, appstruct, self;
            _args = _init_args(arguments);
            cstruct = _get_arg(1, "cstruct", _args, __keyword_null);
            self = this;
            appstruct = self.typ.deserialize(self, cstruct);
            if (self.preparer != null) {
                appstruct = self.preparer(appstruct);
            }
            if (appstruct === __keyword_null) {
                appstruct = self.missing;
                if (appstruct === required) {
                    throw new Invalid(self, _("Required"));
                }
                if (isinstance(appstruct, deferred)) {
                    throw new Invalid(self, _("Required"));
                }
                return appstruct;
            }
            if (self.validator != null) {
                if (!isinstance(self.validator, deferred)) {
                    self.validator(self, appstruct);
                }
            }
            return appstruct;
        };
        /**
         * Add a subnode to this node.
         */
        add = function(self, node) {
            var self;
            self = this;
            self.children.append(node);
        };
        /**
         * Clone the schema node and return the clone.  All subnodes
         * are also cloned recursively.  Attributes present in node
         * dictionaries are preserved.
         */
        clone = function(self) {
            var cloned, self;
            self = this;
            cloned = new self.__class__(self.typ);
            cloned.__dict__.update(self.__dict__);
            cloned.children = (function() {
                var _i, _len, _list, _results;
                _results = [];
                _list = _iter(self.children);
                for (_i = 0, _len = _list.length; _i < _len; _i++) {
                    node = _list[_i];
                    _results.push(node.clone());
                }
                return _results;
            })();
            return cloned;
        };
        /**
         * Resolve any deferred values attached to this schema node
         * and its children (recursively), using the keywords passed as
         * ``kw`` as input to each deferred value.  This function
         * *clones* the schema it is called upon and returns the cloned
         * value.  The original schema node (the source of the clone)
         * is not modified.
         */
        bind = function(self, kw) {
            var _args, cloned, self;
            _args = _init_args(arguments);
            kw = _get_kwargs(_args);
            self = this;
            cloned = self.clone();
            cloned._bind(kw);
            return cloned;
        };
        _bind = function(self, kw) {
            var _i, _i1, _len, _len1, _list, _list1, child, k, self, v;
            self = this;
            _list = self.children;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                child = _list[_i];
                child._bind(kw);
            }
            _list1 = self.__dict__.items();
            for (_i1 = 0, _len1 = _list1.length; _i1 < _len1; _i1++) {
                k = _list1[_i1][0];
                v = _list1[_i1][1];
                if (isinstance(v, deferred)) {
                    v = v(self, kw);
                    setattr(self, k, v);
                }
            }
            if (getattr(self, "after_bind", null)) {
                self.after_bind(self, kw);
            }
        };
        /**
         * Remove a subnode by name
         */
        __delitem__ = function(self, name) {
            var _i, _len, _list, idx, node, self;
            self = this;
            _list = enumerate(_subscript.l.s(self.children, null, null, null));
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                idx = _list[_i][0];
                node = _list[_i][1];
                if (node.name === name) {
                    return self.children.pop(idx);
                }
            }
            throw new KeyError(name);
        };
        /**
         * Get a subnode by name.
         */
        __getitem__ = function(self, name) {
            var _i, _len, _list, node, self;
            self = this;
            _list = self.children;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                node = _list[_i];
                if (node.name === name) {
                    return node;
                }
            }
            throw new KeyError(name);
        };
        /**
         * Replace a subnode by name
         */
        __setitem__ = function(self, name, newnode) {
            var _i, _len, _list, idx, node, self;
            self = this;
            _list = enumerate(_subscript.l.s(self.children, null, null, null));
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                idx = _list[_i][0];
                node = _list[_i][1];
                if (node.name === name) {
                    _subscript.s.i(self.children, idx, newnode);
                    newnode.name = name;
                    return node;
                }
            }
            throw new KeyError(name);
        };
        /**
         * Iterate over the children nodes of this schema node
         */
        __iter__ = function(self) {
            var self;
            self = this;
            return iter(self.children);
        };
        __contains__ = function(self, name) {
            var _ex, self;
            self = this;
            try{_subscript.l.i(self, name);} catch (_ex) {
                if (_ex instanceof KeyError) {
                    return false;
                } else{
                throw _ex}
            }
            return true;
        };
        __repr__ = function(self) {
            var self;
            self = this;
            return "<%s.%s object at %d (named %s)>".__mod__(self.__module__, self.__class__.__name__, id(self), self.name);
        };
        return [{__init__: __init__,required: required,serialize: serialize,flatten: flatten,unflatten: unflatten,set_value: set_value,get_value: get_value,deserialize: deserialize,add: add,clone: clone,bind: bind,_bind: _bind,__delitem__: __delitem__,__getitem__: __getitem__,__setitem__: __setitem__,__iter__: __iter__,__contains__: __contains__,__repr__: __repr__}, {}, {}]
    });

    function t_colander_deferred() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A decorator which can be used to define deferred schema values
     * (missing values, widgets, validators, etc.)
     */
    deferred = _class(t_colander_deferred, [object], function() {
        var __call__, __init__;
        __init__ = function(self, wrapped) {
            var self;
            self = this;
            self.wrapped = wrapped;
        };
        __call__ = function(self, node, kw) {
            var self;
            self = this;
            return self.wrapped(node, kw);
        };
        return [{__init__: __init__,__call__: __call__}, {}, {}]
    });
    _unflatten_mapping = function(node, paths, fstruct, get_child, rewrite_subpath) {
        var _args, _i, _len, _list, appstruct, curname, name, node_name, path, prefix, prefix_len, subfstruct, subnode, subpath, subpaths;
        _args = _init_args(arguments);
        get_child = _get_arg(3, "get_child", _args, null);
        rewrite_subpath = _get_arg(4, "rewrite_subpath", _args, null);
        if (get_child === null) {
            get_child = node.__getitem__;
        }
        if (rewrite_subpath === null) {
            rewrite_subpath = function(subpath) {
                return subpath;
            };
        }
        node_name = node.name;
        if (node_name) {
            prefix = node_name + ".";
        } else{prefix = "";}
        prefix_len = len(prefix);
        appstruct = {};
        subfstruct = {};
        subpaths = [];
        curname = null;
        _list = paths;
        for (_i = 0, _len = _list.length; _i < _len; _i++) {
            path = _list[_i];
            if (path === node_name) {
                continue;
            };
            subpath = _subscript.l.s(path, prefix_len, null, null);
            if (_in(".", subpath)) {
                name = _subscript.l.s(subpath, null, subpath.index("."), null);
            } else{name = subpath;}
            if (curname === null) {
                curname = name;
            } else{
            if (name !== curname) {
                subnode = get_child(curname);
                _subscript.s.i(appstruct, curname, subnode.typ.unflatten(subnode, subpaths, subfstruct));
                subfstruct = {};
                subpaths = [];
                curname = name;
            }
            }
            subpath = rewrite_subpath(subpath);
            _subscript.s.i(subfstruct, subpath, _subscript.l.i(fstruct, path));
            subpaths.append(subpath);
        }
        if (curname != null) {
            subnode = get_child(curname);
            _subscript.s.i(appstruct, curname, subnode.typ.unflatten(subnode, subpaths, subfstruct));
        }
        return appstruct;
    };
    prambanan.exports('colander', {All: All,Boolean: Boolean,Date: Date,DateTime: DateTime,Float: Float,Function: Function,Integer: Integer,Invalid: Invalid,Length: Length,Mapping: Mapping,Number: Number,OneOf: OneOf,Positional: Positional,Range: Range,SchemaNode: SchemaNode,SchemaType: SchemaType,Sequence: Sequence,String: String,Time: Time,Tuple: Tuple,deferred: deferred,interpolate: interpolate,is_nonstr_iter: is_nonstr_iter,timeparse: timeparse});
})(prambanan);(function(prambanan) {
    var All, Bool, Boolean, Date, DateTime, Exception, Float, Function, Int, Integer, Invalid, KeyError, Length, Mapping, Number, OneOf, Positional, Range, SchemaNode, SchemaType, Seq, Sequence, Str, String, Time, Tuple, _, __builtin__, __import__, __keyword_function, __keyword_null, _class, _get_arg, _get_kwargs, _get_varargs, _in, _init_args, _iter, _m_colander, _make_kwargs, _marker, _null, _r_max_err, _r_min_err, _subscript, _super, _unflatten_mapping, datetime, deferred, dict, enumerate, int, interpolate, is_nonstr_iter, isinstance, iso8601, iter, itertools, len, list, map, null, object, required, sorted, str, time, timeparse, translationstring, tuple, type, xrange;
    __builtin__ = prambanan.import('__builtin__');
    xrange = __builtin__.xrange;
    map = __builtin__.map;
    Exception = __builtin__.Exception;
    tuple = __builtin__.tuple;
    int = __builtin__.int;
    __import__ = __builtin__.__import__;
    object = __builtin__.object;
    list = __builtin__.list;
    KeyError = __builtin__.KeyError;
    iter = __builtin__.iter;
    dict = __builtin__.dict;
    len = __builtin__.len;
    str = __builtin__.str;
    enumerate = __builtin__.enumerate;
    sorted = __builtin__.sorted;
    isinstance = __builtin__.isinstance;
    type = __builtin__.type;
    _iter = prambanan.helpers.iter;
    _in = prambanan.helpers. in ;
    _get_varargs = prambanan.helpers.get_varargs;
    _subscript = prambanan.helpers.subscript;
    _init_args = prambanan.helpers.init_args;
    _super = prambanan.helpers.super;
    _make_kwargs = prambanan.helpers.make_kwargs;
    _get_kwargs = prambanan.helpers.get_kwargs;
    _class = prambanan.helpers.class;
    _get_arg = prambanan.helpers.get_arg;
    datetime = __import__('datetime');
    time = __import__('time');
    itertools = __import__('itertools');
    translationstring = __import__('translationstring');
    _m_colander = __import__('colander.');
    iso8601 = _m_colander.iso8601;
    _ = translationstring.TranslationStringFactory("colander");
    required = new object();
    _marker = required;

    function t_colander__null() {
        this.__init__.apply(this, arguments);
    }
    _null = _class(t_colander__null, [object], function() {
        var __reduce__, __repr__;
        __repr__ = function(self) {
            var self;
            self = this;
            return "<colander.null>";
        };
        __reduce__ = function(self) {
            var self;
            self = this;
            return "null";
        };
        return [{__repr__: __repr__,__reduce__: __reduce__}, {}, {}]
    });
    __keyword_null = new _null();
    is_nonstr_iter = function(item) {
        return typeof item == Array;
    };
    interpolate = function(msgs) {
        var _i, _len, _list, res, s;
        res = [];
        _list = msgs;
        for (_i = 0, _len = _list.length; _i < _len; _i++) {
            s = _list[_i];
            if (hasattr(s, "interpolate")) {
                res.append(s.interpolate());
            } else{res.append(s);}
        }
        return res;
    };

    function t_colander_Invalid() {
        this.__init__.apply(this, arguments);
    }
    /**
     * An exception raised by data types and validators indicating that
     * the value for a particular node was not valid.
     * * The constructor receives a mandatory ``node`` argument.  This must
     * be an instance of the :class:`colander.SchemaNode` class, or at
     * least something with the same interface.
     * * The constructor also receives an optional ``msg`` keyword
     * argument, defaulting to ``None``.  The ``msg`` argument is a
     * freeform field indicating the error circumstance.
     * * The constructor additionally may receive an optional ``value``
     * keyword, indicating the value related to the error.
     */
    Invalid = _class(t_colander_Invalid, [Exception], function() {
        var __init__, __setitem__, _keyname, add, asdict, messages, paths, pos, positional;
        pos = null;
        positional = false;
        __init__ = function(self, node, msg, value) {
            var _args, self;
            _args = _init_args(arguments);
            msg = _get_arg(2, "msg", _args, null);
            value = _get_arg(3, "value", _args, null);
            self = this;
            _super(this, '__init__')(node, msg);
            self.node = node;
            self.msg = msg;
            self.value = value;
            self.children = [];
        };
        /**
         * Return an iterable of error messages for this exception using the
         * ``msg`` attribute of this error node.  If the ``msg`` attribute is
         * iterable, it is returned.  If it is not iterable, and is
         * non-``None``, a single-element list containing the ``msg`` value is
         * returned.  If the value is ``None``, an empty list is returned.
         */
        messages = function(self) {
            var self;
            self = this;
            if (is_nonstr_iter(self.msg)) {
                return self.msg;
            }
            if (self.msg === null) {
                return [];
            }
            return [self.msg];
        };
        /**
         * Add a child exception; ``exc`` must be an instance of
         * :class:`colander.Invalid` or a subclass.
         * * ``pos`` is a value important for accurate error reporting.  If
         * it is provided, it must be an integer representing the
         * position of ``exc`` relative to all other subexceptions of
         * this exception node.  For example, if the exception being
         * added is about the third child of the exception which is
         * ``self``, ``pos`` might be passed as ``3``.
         * * If ``pos`` is provided, it will be assigned to the ``pos``
         * attribute of the provided ``exc`` object.
         */
        add = function(self, exc, pos) {
            var _args, self;
            _args = _init_args(arguments);
            pos = _get_arg(2, "pos", _args, null);
            self = this;
            if (self.node && isinstance(self.node.typ, Positional)) {
                exc.positional = true;
            }
            if (pos != null) {
                exc.pos = pos;
            }
            self.children.append(exc);
        };
        /**
         * Add a subexception related to a child node with the
         * message ``msg``. ``name`` must be present in the names of the
         * set of child nodes of this exception's node; if this is not
         * so, a :exc:`KeyError` is raised.
         * * For example, if the exception upon which ``__setitem__`` is
         * called has a node attribute, and that node attribute has
         * children that have the names ``name`` and ``title``, you may
         * successfully call ``__setitem__('name', 'Bad name')`` or
         * ``__setitem__('title', 'Bad title')``.  But calling
         * ``__setitem__('wrong', 'whoops')`` will result in a
         * :exc:`KeyError`.
         * * This method is typically only useful if the ``node`` attribute
         * of the exception upon which it is called is a schema node
         * representing a mapping.
         */
        __setitem__ = function(self, name, msg) {
            var _i, _len, _list, child, exc, num, self;
            self = this;
            _list = enumerate(self.node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                child = _list[_i][1];
                if (child.name === name) {
                    exc = new Invalid(child, msg);
                    self.add(exc, num);
                    return;
                }
            }
            throw new KeyError(name);
        };
        /**
         * A generator which returns each path through the exception
         * graph.  Each path is represented as a tuple of exception
         * nodes.  Within each tuple, the leftmost item will represent
         * the root schema node, the rightmost item will represent the
         * leaf schema node.
         */
        paths = function(self) {
            var self, traverse;
            self = this;
            traverse = function(node, stack) {
                var _i, _i1, _len, _len1, _list, _list1, child, path, res;
                res = [];
                stack.append(node);
                if (!node.children) {
                    res.append(tuple(stack));
                }
                _list = node.children;
                for (_i = 0, _len = _list.length; _i < _len; _i++) {
                    child = _list[_i];
                    _list1 = traverse(child, stack);
                    for (_i1 = 0, _len1 = _list1.length; _i1 < _len1; _i1++) {
                        path = _list1[_i1];
                        res.append(path);
                    }
                }
                stack.pop();
            };
            return traverse(self, []);
        };
        _keyname = function(self) {
            var self;
            self = this;
            if (self.positional) {
                return str(self.pos);
            }
            return str(self.node.name);
        };
        /**
         * Return a dictionary containing a basic
         * (non-language-translated) error report for this exception
         */
        asdict = function(self) {
            var _i, _i1, _len, _len1, _list, _list1, errors, exc, keyname, keyparts, msgs, path, paths, self;
            self = this;
            paths = self.paths();
            errors = {};
            _list = paths;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                path = _list[_i];
                keyparts = [];
                msgs = [];
                _list1 = path;
                for (_i1 = 0, _len1 = _list1.length; _i1 < _len1; _i1++) {
                    exc = _list1[_i1];
                    exc.msg && msgs.extend(exc.messages());
                    keyname = exc._keyname();
                    keyname && keyparts.append(keyname);
                }
                _subscript.s.i(errors, ".".join(keyparts), "; ".join(interpolate(msgs)));
            }
            return errors;
        };
        return [{__init__: __init__,messages: messages,add: add,__setitem__: __setitem__,paths: paths,_keyname: _keyname,asdict: asdict}, {}, {}]
    });
    /**
     * Composite validator which succeeds if none of its
     * subvalidators raises an :class:`colander.Invalid` exception
     */
    All = function(validators) {
        var __call__, _args;
        _args = _init_args(arguments);
        validators = _get_varargs(0, _args);
        __call__ = function(node, value) {
            var _ex, _i, _i1, _len, _len1, _list, _list1, e, exc, excs, validator;
            excs = [];
            _list = validators;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                validator = _list[_i];
                try{validator(node, value);} catch (_ex) {
                    if (_ex instanceof Invalid) {
                        e = _ex;
                        excs.append(e);
                    } else{
                    throw _ex}
                }
            }
            if (excs) {
                exc = new Invalid(node, (function() {
                    var _i1, _len1, _list1, _results;
                    _results = [];
                    _list1 = _iter(excs);
                    for (_i1 = 0, _len1 = _list1.length; _i1 < _len1; _i1++) {
                        exc = _list1[_i1];
                        _results.push(exc.msg);
                    }
                    return _results;
                })());
                _list1 = excs;
                for (_i1 = 0, _len1 = _list1.length; _i1 < _len1; _i1++) {
                    e = _list1[_i1];
                    exc.children.extend(e.children);
                }
                throw exc;
            }
        };
        return __call__;
    };
    /**
     * Validator which accepts a function and an optional message;
     * the function is called with the ``value`` during validation.
     * * If the function returns anything falsy (``None``, ``False``, the
     * empty string, ``0``, an object with a ``__nonzero__`` that returns
     * ``False``, etc) when called during validation, an
     * :exc:`colander.Invalid` exception is raised (validation fails);
     * its msg will be the value of the ``message`` argument passed to
     * this class' constructor.
     * * If the function returns a stringlike object (a ``str`` or
     * ``unicode`` object) that is *not* the empty string , a
     * :exc:`colander.Invalid` exception is raised using the stringlike
     * value returned from the function as the exeption message
     * (validation fails).
     * * If the function returns anything *except* a stringlike object
     * object which is truthy (e.g. ``True``, the integer ``1``, an
     * object with a ``__nonzero__`` that returns ``True``, etc), an
     * :exc:`colander.Invalid` exception is *not* raised (validation
     * succeeds).
     * * The default value for the ``message`` when not provided via the
     * constructor is ``Invalid value``.
     */
    Function = function(__keyword_function, message) {
        var __call__, _args;
        _args = _init_args(arguments);
        message = _get_arg(1, "message", _args, _("Invalid value"));
        __call__ = function(node, value) {
            var result;
            result = __keyword_function(value);
            if (!result) {
                throw new Invalid(node, translationstring.TranslationString(message, _make_kwargs({mapping: {val: value}
                })));
            }
            if (isinstance(result, str)) {
                throw new Invalid(node, translationstring.TranslationString(result, _make_kwargs({mapping: {val: value}
                })));
            }
        };
        return __call__;
    };
    _r_min_err = _("${val} is less than minimum value ${min}");
    _r_max_err = _("${val} is greater than maximum value ${max}");
    /**
     * Validator which succeeds if the value it is passed is greater
     * or equal to ``min`` and less than or equal to ``max``.  If ``min``
     * is not specified, or is specified as ``None``, no lower bound
     * exists.  If ``max`` is not specified, or is specified as ``None``,
     * no upper bound exists.
     * * ``min_err`` is used to form the ``msg`` of the
     * :exc:`colander.Invalid` error when reporting a validation failure
     * caused by a value not meeting the minimum.  If ``min_err`` is
     * specified, it must be a string.  The string may contain the
     * replacement targets ``${min}`` and ``${val}``, representing the
     * minimum value and the provided value respectively.  If it is not
     * provided, it defaults to ``'${val} is less than minimum value
     * ${min}'``.
     * * ``max_err`` is used to form the ``msg`` of the
     * :exc:`colander.Invalid` error when reporting a validation failure
     * caused by a value exceeding the maximum.  If ``max_err`` is
     * specified, it must be a string.  The string may contain the
     * replacement targets ``${max}`` and ``${val}``, representing the
     * maximum value and the provided value respectively.  If it is not
     * provided, it defaults to ``'${val} is greater than maximum value
     * ${max}'``.
     */
    Range = function(min, max, min_err, max_err) {
        var __call__, _args;
        _args = _init_args(arguments);
        min = _get_arg(0, "min", _args, null);
        max = _get_arg(1, "max", _args, null);
        min_err = _get_arg(2, "min_err", _args, null);
        max_err = _get_arg(3, "max_err", _args, null);
        if (min_err === null) {
            min_err = _r_min_err;
        }
        if (max_err === null) {
            max_err = _r_max_err;
        }
        __call__ = function(node, value) {
            if (min != null) {
                if (value < min) {
                    throw new Invalid(node, _(min_err, _make_kwargs({mapping: {val: value,min: min}
                    })));
                }
            }
            if (max != null) {
                if (value > max) {
                    throw new Invalid(node, _(max_err, _make_kwargs({mapping: {val: value,max: max}
                    })));
                }
            }
        };
        return __call__;
    };
    /**
     * Validator which succeeds if the value passed to it has a
     * length between a minimum and maximum.  The value is most often a
     * string.
     */
    Length = function(min, max) {
        var __call__, _args;
        _args = _init_args(arguments);
        min = _get_arg(0, "min", _args, null);
        max = _get_arg(1, "max", _args, null);
        __call__ = function(node, value) {
            var max_err, min_err;
            if (min != null) {
                if (len(value) < min) {
                    min_err = _("Shorter than minimum length ${min}", _make_kwargs({mapping: {min: min}
                    }));
                    throw new Invalid(node, min_err);
                }
            }
            if (max != null) {
                if (len(value) > max) {
                    max_err = _("Longer than maximum length ${max}", _make_kwargs({mapping: {max: max}
                    }));
                    throw new Invalid(node, max_err);
                }
            }
        };
        return __call__;
    };
    /**
     * Validator which succeeds if the value passed to it is one of
     * a fixed set of values
     */
    OneOf = function(choices) {
        var __call__;
        __call__ = function(node, value) {
            var c, err;
            if (!_in(value, choices)) {
                c = ", ".join((function() {
                    var _i, _len, _list, _results;
                    _results = [];
                    _list = _iter(choices);
                    for (_i = 0, _len = _list.length; _i < _len; _i++) {
                        x = _list[_i];
                        _results.push("%s".__mod__(x));
                    }
                    return _results;
                })());
                err = _("\"${val}\" is not one of ${choices}", _make_kwargs({mapping: {val: value,choices: c}
                }));
                throw new Invalid(node, err);
            }
        };
        return __call__;
    };

    function t_colander_SchemaType() {
        this.__init__.apply(this, arguments);
    }
    /**
     * Base class for all schema types
     */
    SchemaType = _class(t_colander_SchemaType, [object], function() {
        var flatten, get_value, set_value, unflatten;
        flatten = function(self, node, appstruct, prefix, listitem) {
            var _args, result, self, selfname;
            _args = _init_args(arguments);
            prefix = _get_arg(3, "prefix", _args, "");
            listitem = _get_arg(4, "listitem", _args, false);
            self = this;
            result = {};
            if (listitem) {
                selfname = prefix;
            } else{selfname = "%s%s".__mod__(prefix, node.name);}
            _subscript.s.i(result, selfname, appstruct);
            return result;
        };
        unflatten = function(self, node, paths, fstruct) {
            var name, self;
            self = this;
            name = node.name;;
            return _subscript.l.i(fstruct, name);
        };
        set_value = function(self, node, appstruct, path, value) {
            var self;
            self = this;
            throw new AssertionError("Can't call 'set_value' on a leaf node.");
        };
        get_value = function(self, node, appstruct, path) {
            var self;
            self = this;
            throw new AssertionError("Can't call 'set_value' on a leaf node.");
        };
        return [{flatten: flatten,unflatten: unflatten,set_value: set_value,get_value: get_value}, {}, {}]
    });

    function t_colander_Mapping() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type which represents a mapping of names to nodes.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type imply the named keys and values in the mapping.
     * * The constructor of this type accepts one extra optional keyword
     * argument that other types do not: ``unknown``.  An attribute of
     * the same name can be set on a type instance to control the
     * behavior after construction.
     * * unknown
     * ``unknown`` controls the behavior of this type when an unknown
     * key is encountered in the cstruct passed to the
     * ``deserialize`` method of this instance.  All the potential
     * values of ``unknown`` are strings.  They are:
     * * - ``ignore`` means that keys that are not present in the schema
     * associated with this type will be ignored during
     * deserialization.
     * * - ``raise`` will cause a :exc:`colander.Invalid` exception to
     * be raised when unknown keys are present in the cstruct
     * during deserialization.
     * * - ``preserve`` will preserve the 'raw' unknown keys and values
     * in the appstruct returned by deserialization.
     * * Default: ``ignore``.
     * * Special behavior is exhibited when a subvalue of a mapping is
     * present in the schema but is missing from the mapping passed to
     * either the ``serialize`` or ``deserialize`` method of this class.
     * In this case, the :attr:`colander.null` value will be passed to
     * the ``serialize`` or ``deserialize`` method of the schema node
     * representing the subvalue of the mapping respectively.  During
     * serialization, this will result in the behavior described in
     * :ref:`serializing_null` for the subnode.  During deserialization,
     * this will result in the behavior described in
     * :ref:`deserializing_null` for the subnode.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, a dictionary will be returned, where each of
     * the values in the returned dictionary is the serialized
     * representation of the null value for its type.
     */
    Mapping = _class(t_colander_Mapping, [SchemaType], function() {
        var __init__, _impl, _validate, deserialize, flatten, get_value, serialize, set_value, unflatten;
        __init__ = function(self, unknown) {
            var _args, self;
            _args = _init_args(arguments);
            unknown = _get_arg(1, "unknown", _args, "ignore");
            self = this;
            self.unknown = unknown;
        };
        _validate = function(self, node, value) {
            var _ex, e, self;
            self = this;
            try{
            return dict(value);} catch (_ex) {
                if (_ex instanceof Exception) {
                    e = _ex;
                    throw new Invalid(node, _("\"${val}\" is not a mapping type: ${err}", _make_kwargs({mapping: {val: value,err: e}
                    })));
                } else{
                throw _ex}
            }
        };
        _impl = function(self, node, value, callback) {
            var _ex, _i, _len, _list, e, error, name, num, result, self, subnode, subval;
            self = this;
            value = self._validate(node, value);
            error = null;
            result = {};
            _list = enumerate(node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                subnode = _list[_i][1];
                name = subnode.name;
                subval = value.pop(name, __keyword_null);
                try{_subscript.s.i(result, name, callback(subnode, subval));} catch (_ex) {
                    if (_ex instanceof Invalid) {
                        e = _ex;
                        if (error === null) {
                            error = new Invalid(node);
                        }
                        error.add(e, num);
                    } else{
                    throw _ex}
                }
            }
            if (self.unknown === "raise") {
                if (value) {
                    throw new Invalid(node, _("Unrecognized keys in mapping: \"${val}\"", _make_kwargs({mapping: {val: value}
                    })));
                }
            } else{
            if (self.unknown === "preserve") {
                result.update(value);}
            }
            if (error != null) {
                throw error;
            }
            return result;
        };
        serialize = function(self, node, appstruct) {
            var callback, self;
            self = this;
            if (appstruct === __keyword_null) {
                appstruct = {};
            }
            callback = function(subnode, subappstruct) {
                return subnode.serialize(subappstruct);
            };
            return self._impl(node, appstruct, callback);
        };
        deserialize = function(self, node, cstruct) {
            var callback, self;
            self = this;
            if (cstruct === __keyword_null) {
                return __keyword_null;
            }
            callback = function(subnode, subcstruct) {
                return subnode.deserialize(subcstruct);
            };
            return self._impl(node, cstruct, callback);
        };
        flatten = function(self, node, appstruct, prefix, listitem) {
            var _args, _i, _len, _list, name, result, self, selfprefix, subnode, substruct;
            _args = _init_args(arguments);
            prefix = _get_arg(3, "prefix", _args, "");
            listitem = _get_arg(4, "listitem", _args, false);
            self = this;
            result = {};
            if (listitem) {
                selfprefix = prefix;
            } else{
            if (node.name) {
                selfprefix = "%s%s.".__mod__(prefix, node.name);} else{selfprefix = prefix;}
            }
            _list = node.children;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                subnode = _list[_i];
                name = subnode.name;
                substruct = appstruct.get(name, __keyword_null);
                result.update(subnode.typ.flatten(subnode, substruct, _make_kwargs({prefix: selfprefix})));
            }
            return result;
        };
        unflatten = function(self, node, paths, fstruct) {
            var self;
            self = this;
            return _unflatten_mapping(node, paths, fstruct);
        };
        set_value = function(self, node, appstruct, path, value) {
            var next_appstruct, next_name, next_node, rest, self;
            self = this;
            if (_in(".", path)) {
                (function(_source) {
                    next_name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
                next_node = _subscript.l.i(node, next_name);
                next_appstruct = _subscript.l.i(appstruct, next_name);
                _subscript.s.i(appstruct, next_name, next_node.typ.set_value(next_node, next_appstruct, rest, value));
            } else{_subscript.s.i(appstruct, path, value);}
            return appstruct;
        };
        get_value = function(self, node, appstruct, path) {
            var name, next_node, rest, self;
            self = this;
            if (_in(".", path)) {
                (function(_source) {
                    name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
                next_node = _subscript.l.i(node, name);
                return next_node.typ.get_value(next_node, _subscript.l.i(appstruct, name), rest);
            }
            return _subscript.l.i(appstruct, path);
        };
        return [{__init__: __init__,_validate: _validate,_impl: _impl,serialize: serialize,deserialize: deserialize,flatten: flatten,unflatten: unflatten,set_value: set_value,get_value: get_value}, {}, {}]
    });

    function t_colander_Positional() {
        this.__init__.apply(this, arguments);
    }
    /**
     * Marker abstract base class meaning 'this type has children which
     * should be addressed by position instead of name' (e.g. via seq[0],
     * but never seq['name']).  This is consulted by Invalid.asdict when
     * creating a dictionary representation of an error tree.
     */
    Positional = _class(t_colander_Positional, [object], function() {
        return [{}, {}, {}]
    });

    function t_colander_Tuple() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type which represents a fixed-length sequence of nodes.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type imply the positional elements of the tuple in the order
     * they are added.
     * * This type is willing to serialize and deserialized iterables that,
     * when converted to a tuple, have the same number of elements as the
     * number of the associated node's subnodes.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     */
    Tuple = _class(t_colander_Tuple, [Positional, SchemaType], function() {
        var _impl, _validate, deserialize, flatten, get_value, serialize, set_value, unflatten;
        _validate = function(self, node, value) {
            var nodelen, self, valuelen;
            self = this;
            if (!hasattr(value, "__iter__")) {
                throw new Invalid(node, _("\"${val}\" is not iterable", _make_kwargs({mapping: {val: value}
                })));
            }(function(_source) {
                valuelen = _source[0];
                nodelen = _source[1];
            })([len(value), len(node.children)]);
            if (valuelen !== nodelen) {
                throw new Invalid(node, _("\"${val}\" has an incorrect number of elements (expected ${exp}, was ${was})", _make_kwargs({mapping: {val: value,exp: nodelen,was: valuelen}
                })));
            }
            return list(value);
        };
        _impl = function(self, node, value, callback) {
            var _ex, _i, _len, _list, e, error, num, result, self, subnode, subval;
            self = this;
            value = self._validate(node, value);
            error = null;
            result = [];
            _list = enumerate(node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                subnode = _list[_i][1];
                subval = _subscript.l.i(value, num);
                try{result.append(callback(subnode, subval));} catch (_ex) {
                    if (_ex instanceof Invalid) {
                        e = _ex;
                        if (error === null) {
                            error = new Invalid(node);
                        }
                        error.add(e, num);
                    } else{
                    throw _ex}
                }
            }
            if (error != null) {
                throw error;
            }
            return tuple(result);
        };
        serialize = function(self, node, appstruct) {
            var callback, self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            callback = function(subnode, subappstruct) {
                return subnode.serialize(subappstruct);
            };
            return self._impl(node, appstruct, callback);
        };
        deserialize = function(self, node, cstruct) {
            var callback, self;
            self = this;
            if (cstruct === __keyword_null) {
                return __keyword_null;
            }
            callback = function(subnode, subval) {
                return subnode.deserialize(subval);
            };
            return self._impl(node, cstruct, callback);
        };
        flatten = function(self, node, appstruct, prefix, listitem) {
            var _args, _i, _len, _list, num, result, self, selfprefix, subnode, substruct;
            _args = _init_args(arguments);
            prefix = _get_arg(3, "prefix", _args, "");
            listitem = _get_arg(4, "listitem", _args, false);
            self = this;
            result = {};
            if (listitem) {
                selfprefix = prefix;
            } else{selfprefix = "%s%s.".__mod__(prefix, node.name);}
            _list = enumerate(node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                subnode = _list[_i][1];
                substruct = _subscript.l.i(appstruct, num);
                result.update(subnode.typ.flatten(subnode, substruct, _make_kwargs({prefix: selfprefix})));
            }
            return result;
        };
        unflatten = function(self, node, paths, fstruct) {
            var _i, _len, _list, appstruct, mapstruct, self, subnode;
            self = this;
            mapstruct = _unflatten_mapping(node, paths, fstruct);
            appstruct = [];
            _list = node.children;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                subnode = _list[_i];
                appstruct.append(_subscript.l.i(mapstruct, subnode.name));
            }
            return tuple(appstruct);
        };
        set_value = function(self, node, appstruct, path, value) {
            var _i, _len, _list, index, next_appstruct, next_name, next_node, rest, self;
            self = this;
            appstruct = list(appstruct);
            if (_in(".", path)) {
                (function(_source) {
                    next_name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
            } else{ (function(_source) {
                next_name = _source[0];
                rest = _source[1];})([path, null]);
            }
            _list = enumerate(node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                index = _list[_i][0];
                next_node = _list[_i][1];
                if (next_node.name === next_name) {
                    break;
                }
            }
            if (_i == _len) {
                throw new KeyError(next_name);
            }
            if (rest != null) {
                next_appstruct = _subscript.l.i(appstruct, index);
                _subscript.s.i(appstruct, index, next_node.typ.set_value(next_node, next_appstruct, rest, value));
            } else{_subscript.s.i(appstruct, index, value);}
            return tuple(appstruct);
        };
        get_value = function(self, node, appstruct, path) {
            var _i, _len, _list, index, name, next_node, rest, self;
            self = this;
            if (_in(".", path)) {
                (function(_source) {
                    name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
            } else{ (function(_source) {
                name = _source[0];
                rest = _source[1];})([path, null]);
            }
            _list = enumerate(node.children);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                index = _list[_i][0];
                next_node = _list[_i][1];
                if (next_node.name === name) {
                    break;
                }
            }
            if (_i == _len) {
                throw new KeyError(name);
            }
            if (rest != null) {
                return next_node.typ.get_value(next_node, _subscript.l.i(appstruct, index), rest);
            }
            return _subscript.l.i(appstruct, index);
        };
        return [{_validate: _validate,_impl: _impl,serialize: serialize,deserialize: deserialize,flatten: flatten,unflatten: unflatten,set_value: set_value,get_value: get_value}, {}, {}]
    });

    function t_colander_Sequence() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type which represents a variable-length sequence of nodes,
     * all of which must be of the same type.
     * * The type of the first subnode of the
     * :class:`colander.SchemaNode` that wraps this type is considered the
     * sequence type.
     * * The optional ``accept_scalar`` argument to this type's constructor
     * indicates what should happen if the value found during serialization or
     * deserialization does not have an ``__iter__`` method or is a
     * mapping type.
     * * If ``accept_scalar`` is ``True`` and the value does not have an
     * ``__iter__`` method or is a mapping type, the value will be turned
     * into a single element list.
     * * If ``accept_scalar`` is ``False`` and the value does not have an
     * ``__iter__`` method or is a mapping type, an
     * :exc:`colander.Invalid` error will be raised during serialization
     * and deserialization.
     * * The default value of ``accept_scalar`` is ``False``.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value is returned.
     */
    Sequence = _class(t_colander_Sequence, [Positional, SchemaType], function() {
        var __init__, _impl, _validate, deserialize, flatten, get_value, serialize, set_value, unflatten;
        __init__ = function(self, accept_scalar) {
            var _args, self;
            _args = _init_args(arguments);
            accept_scalar = _get_arg(1, "accept_scalar", _args, false);
            self = this;
            self.accept_scalar = accept_scalar;
        };
        _validate = function(self, node, value, accept_scalar) {
            var self;
            self = this;
            if (hasattr(value, "__iter__") && !hasattr(value, "get")) {
                return list(value);
            }
            if (accept_scalar) {
                return [value];
            } else{
            throw new Invalid(node, _("\"${val}\" is not iterable", _make_kwargs({mapping: {val: value}
            })));
            }
        };
        _impl = function(self, node, value, callback, accept_scalar) {
            var _ex, _i, _len, _list, e, error, num, result, self, subval;
            self = this;
            if (accept_scalar === null) {
                accept_scalar = self.accept_scalar;
            }
            value = self._validate(node, value, accept_scalar);
            error = null;
            result = [];
            _list = enumerate(value);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                subval = _list[_i][1];
                try{result.append(callback(_subscript.l.i(node.children, 0), subval));} catch (_ex) {
                    if (_ex instanceof Invalid) {
                        e = _ex;
                        if (error === null) {
                            error = new Invalid(node);
                        }
                        error.add(e, num);
                    } else{
                    throw _ex}
                }
            }
            if (error != null) {
                throw error;
            }
            return result;
        };
        /**
         * Along with the normal ``node`` and ``appstruct`` arguments,
         * this method accepts an additional optional keyword argument:
         * ``accept_scalar``.  This keyword argument can be used to
         * override the constructor value of the same name.
         * * If ``accept_scalar`` is ``True`` and the ``appstruct`` does
         * not have an ``__iter__`` method or is a mapping type, the
         * value will be turned into a single element list.
         * * If ``accept_scalar`` is ``False`` and the ``appstruct`` does
         * not have an ``__iter__`` method or is a mapping type, an
         * :exc:`colander.Invalid` error will be raised during
         * serialization and deserialization.
         * * The default of ``accept_scalar`` is ``None``, which means
         * respect the default ``accept_scalar`` value attached to this
         * instance via its constructor.
         */
        serialize = function(self, node, appstruct, accept_scalar) {
            var _args, callback, self;
            _args = _init_args(arguments);
            accept_scalar = _get_arg(3, "accept_scalar", _args, null);
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            callback = function(subnode, subappstruct) {
                return subnode.serialize(subappstruct);
            };
            return self._impl(node, appstruct, callback, accept_scalar);
        };
        /**
         * Along with the normal ``node`` and ``cstruct`` arguments, this
         * method accepts an additional optional keyword argument:
         * ``accept_scalar``.  This keyword argument can be used to
         * override the constructor value of the same name.
         * * If ``accept_scalar`` is ``True`` and the ``cstruct`` does not
         * have an ``__iter__`` method or is a mapping type, the value
         * will be turned into a single element list.
         * * If ``accept_scalar`` is ``False`` and the ``cstruct`` does not have an
         * ``__iter__`` method or is a mapping type, an
         * :exc:`colander.Invalid` error will be raised during serialization
         * and deserialization.
         * * The default of ``accept_scalar`` is ``None``, which means
         * respect the default ``accept_scalar`` value attached to this
         * instance via its constructor.
         */
        deserialize = function(self, node, cstruct, accept_scalar) {
            var _args, callback, self;
            _args = _init_args(arguments);
            accept_scalar = _get_arg(3, "accept_scalar", _args, null);
            self = this;
            if (cstruct === __keyword_null) {
                return __keyword_null;
            }
            callback = function(subnode, subcstruct) {
                return subnode.deserialize(subcstruct);
            };
            return self._impl(node, cstruct, callback, accept_scalar);
        };
        flatten = function(self, node, appstruct, prefix, listitem) {
            var _args, _i, _len, _list, childnode, num, result, self, selfprefix, subname, subprefix, subval;
            _args = _init_args(arguments);
            prefix = _get_arg(3, "prefix", _args, "");
            listitem = _get_arg(4, "listitem", _args, false);
            self = this;
            result = {};
            if (listitem) {
                selfprefix = prefix;
            } else{selfprefix = "%s%s.".__mod__(prefix, node.name);}
            childnode = node.children[0];
            _list = enumerate(appstruct);
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                num = _list[_i][0];
                subval = _list[_i][1];
                subname = "%s%s".__mod__(selfprefix, num);
                subprefix = subname + ".";
                result.update(childnode.typ.flatten(childnode, subval, _make_kwargs({prefix: subprefix,listitem: true})));
            }
            return result;
        };
        unflatten = function(self, node, paths, fstruct) {
            var child_name, get_child, mapstruct, only_child, rewrite_subpath, self;
            self = this;
            only_child = node.children[0];
            child_name = only_child.name;
            get_child = function(name) {
                return only_child;
            };
            rewrite_subpath = function(subpath) {
                var suffix;
                if (_in(".", subpath)) {
                    suffix = subpath.split(".", 1)[1];
                    return "%s.%s".__mod__(child_name, suffix);
                }
                return child_name;
            };
            mapstruct = _unflatten_mapping(node, paths, fstruct, get_child, rewrite_subpath);
            return (function() {
                var _i, _len, _list, _results;
                _results = [];
                _list = _iter(xrange(len(mapstruct)));
                for (_i = 0, _len = _list.length; _i < _len; _i++) {
                    index = _list[_i];
                    _results.push(_subscript.l.i(mapstruct, str(index)));
                }
                return _results;
            })();
        };
        set_value = function(self, node, appstruct, path, value) {
            var index, next_appstruct, next_name, next_node, rest, self;
            self = this;
            if (_in(".", path)) {
                (function(_source) {
                    next_name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
                index = int(next_name);
                next_node = node.children[0];
                next_appstruct = _subscript.l.i(appstruct, index);
                _subscript.s.i(appstruct, index, next_node.typ.set_value(next_node, next_appstruct, rest, value));
            } else{index = int(path);
            _subscript.s.i(appstruct, index, value);}
            return appstruct;
        };
        get_value = function(self, node, appstruct, path) {
            var index, name, next_node, rest, self;
            self = this;
            if (_in(".", path)) {
                (function(_source) {
                    name = _source[0];
                    rest = _source[1];
                })(path.split(".", 1));
                index = int(name);
                next_node = node.children[0];
                return next_node.typ.get_value(next_node, _subscript.l.i(appstruct, index), rest);
            }
            return _subscript.l.i(appstruct, int(path));
        };
        return [{__init__: __init__,_validate: _validate,_impl: _impl,serialize: serialize,deserialize: deserialize,flatten: flatten,unflatten: unflatten,set_value: set_value,get_value: get_value}, {}, {}]
    });
    Seq = Sequence;

    function t_colander_String() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a Unicode string.
     * * This type constructor accepts one argument:
     * * ``encoding``
     * Represents the encoding which should be applied to value
     * serialization and deserialization, for example ``utf-8``.  If
     * ``encoding`` is passed as ``None``, the ``serialize`` method of
     * this type will not do any special encoding of the appstruct it is
     * provided, nor will the ``deserialize`` method of this type do
     * any special decoding of the cstruct it is provided; inputs and
     * outputs will be assumed to be Unicode.  ``encoding`` defaults
     * to ``None``.
     * * If ``encoding`` is ``None``:
     * * - A Unicode input value to ``serialize`` is returned untouched.
     * * - A non-Unicode input value to ``serialize`` is run through the
     * ``unicode()`` function without an ``encoding`` parameter
     * (``unicode(value)``) and the result is returned.
     * * - A Unicode input value to ``deserialize`` is returned untouched.
     * * - A non-Unicode input value to ``deserialize`` is run through the
     * ``unicode()`` function without an ``encoding`` parameter
     * (``unicode(value)``) and the result is returned.
     * * If ``encoding`` is not ``None``:
     * * - A Unicode input value to ``serialize`` is run through the
     * ``unicode`` function with the encoding parameter
     * (``unicode(value, encoding)``) and the result (a ``str``
     * object) is returned.
     * * - A non-Unicode input value to ``serialize`` is converted to a
     * Unicode using the encoding (``unicode(value, encoding)``);
     * subsequently the Unicode object is reeencoded to a ``str``
     * object using the encoding and returned.
     * * - A Unicode input value to ``deserialize`` is returned
     * untouched.
     * * - A non-Unicode input value to ``deserialize`` is converted to
     * a ``str`` object using ``str(value``).  The resulting str
     * value is converted to Unicode using the encoding
     * (``unicode(value, encoding)``) and the result is returned.
     * * A corollary: If a string (as opposed to a unicode object) is
     * provided as a value to either the serialize or deserialize
     * method of this type, and the type also has an non-None
     * ``encoding``, the string must be encoded with the type's
     * encoding.  If this is not true, an :exc:`colander.Invalid`
     * error will result.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    String = _class(t_colander_String, [SchemaType], function() {
        var __init__, deserialize, serialize;
        __init__ = function(self, encoding) {
            var _args, self;
            _args = _init_args(arguments);
            encoding = _get_arg(1, "encoding", _args, null);
            self = this;
            self.encoding = encoding;
        };
        serialize = function(self, node, appstruct) {
            var _ex, e, self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            try{
            return str(appstruct);} catch (_ex) {
                if (_ex instanceof Exception) {
                    e = _ex;
                    throw new Invalid(node, _("${val} cannot be serialized: ${err}", _make_kwargs({mapping: {val: appstruct,err: e}
                    })));
                } else{
                throw _ex}
            }
        };
        deserialize = function(self, node, cstruct) {
            var _ex, e, self;
            self = this;
            if (!cstruct) {
                return __keyword_null;
            }
            try{
            return str(cstruct);} catch (_ex) {
                if (_ex instanceof Exception) {
                    e = _ex;
                    throw new Invalid(node, _("${val} is not a string: ${err}", _make_kwargs({mapping: {val: cstruct,err: e}
                    })));
                } else{
                throw _ex}
            }
        };
        return [{__init__: __init__,serialize: serialize,deserialize: deserialize}, {}, {}]
    });
    Str = String;

    function t_colander_Number() {
        this.__init__.apply(this, arguments);
    }
    /**
     * Abstract base class for float, int, decimal
     */
    Number = _class(t_colander_Number, [SchemaType], function() {
        var deserialize, num, serialize;
        num = null;
        serialize = function(self, node, appstruct) {
            var _ex, self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            try{
            return str(self.num(appstruct));} catch (_ex) {
                if (_ex instanceof Exception) {
                    throw new Invalid(node, _("\"${val}\" is not a number", _make_kwargs({mapping: {val: appstruct}
                    })));
                } else{
                throw _ex}
            }
        };
        deserialize = function(self, node, cstruct) {
            var _ex, self;
            self = this;
            if (cstruct !== 0 && !cstruct) {
                return __keyword_null;
            }
            try{
            return self.num(cstruct);} catch (_ex) {
                if (_ex instanceof Exception) {
                    throw new Invalid(node, _("\"${val}\" is not a number", _make_kwargs({mapping: {val: cstruct}
                    })));
                } else{
                throw _ex}
            }
        };
        return [{serialize: serialize,deserialize: deserialize}, {}, {}]
    });

    function t_colander_Integer() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing an integer.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    Integer = _class(t_colander_Integer, [Number], function() {
        var num;
        num = int;
        return [{}, {}, {}]
    });
    Int = Integer;

    function t_colander_Float() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a float.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    Float = _class(t_colander_Float, [Number], function() {
        var num;
        num = float;
        return [{}, {}, {}]
    });

    function t_colander_Boolean() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a boolean object.
     * * During deserialization, a value in the set (``false``, ``0``) will
     * be considered ``False``.  Anything else is considered
     * ``True``. Case is ignored.
     * * Serialization will produce ``true`` or ``false`` based on the
     * value.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    Boolean = _class(t_colander_Boolean, [SchemaType], function() {
        var deserialize, serialize;
        serialize = function(self, node, appstruct) {
            var self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            return appstruct && "true" || "false";
        };
        deserialize = function(self, node, cstruct) {
            var _ex, result, self;
            self = this;
            if (cstruct === __keyword_null) {
                return __keyword_null;
            }
            try{result = str(cstruct);} catch (_ex) {
                throw new Invalid(node, _("${val} is not a string", _make_kwargs({mapping: {val: cstruct}
                })));
            }
            result = result.lower();
            if (_in(result, ["false", "0"])) {
                return false;
            }
            return true;
        };
        return [{serialize: serialize,deserialize: deserialize}, {}, {}]
    });
    Bool = Boolean;

    function t_colander_DateTime() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a Python ``datetime.datetime`` object.
     * * This type serializes python ``datetime.datetime`` objects to a
     * `ISO8601 <http://en.wikipedia.org/wiki/ISO_8601>`_ string format.
     * The format includes the date, the time, and the timezone of the
     * datetime.
     * * The constructor accepts an argument named ``default_tzinfo`` which
     * should be a Python ``tzinfo`` object; by default it is None,
     * meaning that the default tzinfo will be equivalent to UTC (Zulu
     * time).  The ``default_tzinfo`` tzinfo object is used to convert
     * 'naive' datetimes to a timezone-aware representation during
     * serialization.
     * * You can adjust the error message reported by this class by
     * changing its ``err_template`` attribute in a subclass on an
     * instance of this class.  By default, the ``err_template``
     * attribute is the string ``Invalid date``.  This string is used as
     * the interpolation subject of a dictionary composed of ``val`` and
     * ``err``.  ``val`` and ``err`` are the unvalidatable value and the
     * exception caused trying to convert the value, respectively. These
     * may be used in an overridden err_template as ``${val}`` and
     * ``${err}`` respectively as necessary, e.g. ``_('${val} cannot be
     * parsed as an iso8601 date: ${err}')``.
     * * For convenience, this type is also willing to coerce
     * ``datetime.date`` objects to a DateTime ISO string representation
     * during serialization.  It does so by using midnight of the day as
     * the time, and uses the ``default_tzinfo`` to give the
     * serialization a timezone.
     * * Likewise, for convenience, during deserialization, this type will
     * convert ``YYYY-MM-DD`` ISO8601 values to a datetime object.  It
     * does so by using midnight of the day as the time, and uses the
     * ``default_tzinfo`` to give the serialization a timezone.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    DateTime = _class(t_colander_DateTime, [SchemaType], function() {
        var __init__, deserialize, err_template, serialize;
        err_template = _("Invalid date");
        __init__ = function(self, default_tzinfo) {
            var _args, self;
            _args = _init_args(arguments);
            default_tzinfo = _get_arg(1, "default_tzinfo", _args, _marker);
            self = this;
            if (default_tzinfo === _marker) {
                default_tzinfo = iso8601.Utc();
            }
            self.default_tzinfo = default_tzinfo;
        };
        serialize = function(self, node, appstruct) {
            var self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            if (type(appstruct) === datetime.date) {
                appstruct = datetime.datetime.combine(appstruct, new datetime.time());
            }
            if (!isinstance(appstruct, datetime.datetime)) {
                throw new Invalid(node, _("\"${val}\" is not a datetime object", _make_kwargs({mapping: {val: appstruct}
                })));
            }
            return appstruct.isoformat();
        };
        deserialize = function(self, node, cstruct) {
            var _ex, _ex1, day, e, month, result, self, year;
            self = this;
            if (!cstruct) {
                return __keyword_null;
            }
            try{result = iso8601.parse_date(cstruct);} catch (_ex) {
                if ((_ex instanceof iso8601.ParseError) || (_ex instanceof TypeError)) {
                    e = _ex;
                    try{ (function(_source) {
                        year = _source[0];
                        month = _source[1];
                        day = _source[2];})(map(int, cstruct.split("-", 2)));
                    result = new datetime.datetime(year, month, day);
                    } catch (_ex1) {
                        if (_ex1 instanceof Exception) {
                            e = _ex1;
                            throw new Invalid(node, _(self.err_template, _make_kwargs({mapping: {val: cstruct,err: e}
                            })));
                        } else{
                        throw _ex1}
                    }
                } else{
                throw _ex}
            }
            return result;
        };
        return [{__init__: __init__,serialize: serialize,deserialize: deserialize}, {}, {}]
    });

    function t_colander_Date() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a Python ``datetime.date`` object.
     * * This type serializes python ``datetime.date`` objects to a
     * `ISO8601 <http://en.wikipedia.org/wiki/ISO_8601>`_ string format.
     * The format includes the date only.
     * * The constructor accepts no arguments.
     * * You can adjust the error message reported by this class by
     * changing its ``err_template`` attribute in a subclass on an
     * instance of this class.  By default, the ``err_template``
     * attribute is the string ``Invalid date``.  This string is used as
     * the interpolation subject of a dictionary composed of ``val`` and
     * ``err``.  ``val`` and ``err`` are the unvalidatable value and the
     * exception caused trying to convert the value, respectively. These
     * may be used in an overridden err_template as ``${val}`` and
     * ``${err}`` respectively as necessary, e.g. ``_('${val} cannot be
     * parsed as an iso8601 date: ${err}')``.
     * * For convenience, this type is also willing to coerce
     * ``datetime.datetime`` objects to a date-only ISO string
     * representation during serialization.  It does so by stripping off
     * any time information, converting the ``datetime.datetime`` into a
     * date before serializing.
     * * Likewise, for convenience, this type is also willing to coerce ISO
     * representations that contain time info into a ``datetime.date``
     * object during deserialization.  It does so by throwing away any
     * time information related to the serialized value during
     * deserialization.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    Date = _class(t_colander_Date, [SchemaType], function() {
        var deserialize, err_template, serialize;
        err_template = _("Invalid date");
        serialize = function(self, node, appstruct) {
            var self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            if (isinstance(appstruct, datetime.datetime)) {
                appstruct = appstruct.date();
            }
            if (!isinstance(appstruct, datetime.date)) {
                throw new Invalid(node, _("\"${val}\" is not a date object", _make_kwargs({mapping: {val: appstruct}
                })));
            }
            return appstruct.isoformat();
        };
        deserialize = function(self, node, cstruct) {
            var _ex, _ex1, day, e, month, result, self, year;
            self = this;
            if (!cstruct) {
                return __keyword_null;
            }
            try{result = iso8601.parse_date(cstruct);
            result = result.date();} catch (_ex) {
                if ((_ex instanceof iso8601.ParseError) || (_ex instanceof TypeError)) {
                    try{ (function(_source) {
                        year = _source[0];
                        month = _source[1];
                        day = _source[2];})(map(int, cstruct.split("-", 2)));
                    result = new datetime.date(year, month, day);
                    } catch (_ex1) {
                        if (_ex1 instanceof Exception) {
                            e = _ex1;
                            throw new Invalid(node, _(self.err_template, _make_kwargs({mapping: {val: cstruct,err: e}
                            })));
                        } else{
                        throw _ex1}
                    }
                } else{
                throw _ex}
            }
            return result;
        };
        return [{serialize: serialize,deserialize: deserialize}, {}, {}]
    });

    function t_colander_Time() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A type representing a Python ``datetime.time`` object.
     * * .. note:: This type is new as of Colander 0.9.3.
     * * This type serializes python ``datetime.time`` objects to a
     * `ISO8601 <http://en.wikipedia.org/wiki/ISO_8601>`_ string format.
     * The format includes the date only.
     * * The constructor accepts no arguments.
     * * You can adjust the error message reported by this class by
     * changing its ``err_template`` attribute in a subclass on an
     * instance of this class.  By default, the ``err_template``
     * attribute is the string ``Invalid date``.  This string is used as
     * the interpolation subject of a dictionary composed of ``val`` and
     * ``err``.  ``val`` and ``err`` are the unvalidatable value and the
     * exception caused trying to convert the value, respectively. These
     * may be used in an overridden err_template as ``${val}`` and
     * ``${err}`` respectively as necessary, e.g. ``_('${val} cannot be
     * parsed as an iso8601 date: ${err}')``.
     * * For convenience, this type is also willing to coerce
     * ``datetime.datetime`` objects to a time-only ISO string
     * representation during serialization.  It does so by stripping off
     * any date information, converting the ``datetime.datetime`` into a
     * time before serializing.
     * * Likewise, for convenience, this type is also willing to coerce ISO
     * representations that contain time info into a ``datetime.time``
     * object during deserialization.  It does so by throwing away any
     * date information related to the serialized value during
     * deserialization.
     * * If the :attr:`colander.null` value is passed to the serialize
     * method of this class, the :attr:`colander.null` value will be
     * returned.
     * * The subnodes of the :class:`colander.SchemaNode` that wraps
     * this type are ignored.
     */
    Time = _class(t_colander_Time, [SchemaType], function() {
        var deserialize, err_template, serialize;
        err_template = _("Invalid time");
        serialize = function(self, node, appstruct) {
            var self;
            self = this;
            if (appstruct === __keyword_null) {
                return __keyword_null;
            }
            if (isinstance(appstruct, datetime.datetime)) {
                appstruct = appstruct.time();
            }
            if (!isinstance(appstruct, datetime.time)) {
                throw new Invalid(node, _("\"${val}\" is not a time object", _make_kwargs({mapping: {val: appstruct}
                })));
            }
            return _subscript.l.i(appstruct.isoformat().split("."), 0);
        };
        deserialize = function(self, node, cstruct) {
            var _ex, _ex1, _ex2, e, result, self;
            self = this;
            if (!cstruct) {
                return __keyword_null;
            }
            try{result = iso8601.parse_date(cstruct);
            result = result.time();} catch (_ex) {
                if ((_ex instanceof iso8601.ParseError) || (_ex instanceof TypeError)) {
                    try{result = timeparse(cstruct, "%H:%M:%S");} catch (_ex1) {
                        if (_ex1 instanceof ValueError) {
                            try{result = timeparse(cstruct, "%H:%M");} catch (_ex2) {
                                if (_ex2 instanceof Exception) {
                                    e = _ex2;
                                    throw new Invalid(node, _(self.err_template, _make_kwargs({mapping: {val: cstruct,err: e}
                                    })));
                                } else{
                                throw _ex2}
                            }
                        } else{
                        throw _ex1}
                    }
                } else{
                throw _ex}
            }
            return result;
        };
        return [{serialize: serialize,deserialize: deserialize}, {}, {}]
    });
    timeparse = function(t, format) {
        return new datetime.datetime(_subscript.l.s(time.strptime(t, format), 0, 6, null)).time();
    };
    var _schema_counter = 0;

    function t_colander_SchemaNode() {
        this.__init__.apply(this, arguments);
    }
    /**
     * Fundamental building block of schemas.
     * * The constructor accepts these positional arguments:
     * * - ``typ`` (required): The 'type' for this node.  It should be an
     * instance of a class that implements the
     * :class:`colander.interfaces.Type` interface.
     * * - ``children``: a sequence of subnodes.  If the subnodes of this
     * node are not known at construction time, they can later be added
     * via the ``add`` method.
     * * The constructor accepts these keyword arguments:
     * * - ``name``: The name of this node.
     * * - ``default``: The default serialization value for this node.
     * Default: :attr:`colander.null`.
     * * - ``missing``: The default deserialization value for this node.  If it is
     * not provided, the missing value of this node will be the special marker
     * value :attr:`colander.required`, indicating that it is considered
     * 'required'.  When ``missing`` is :attr:`colander.required`, the
     * ``required`` computed attribute will be ``True``.
     * * - ``preparer``: Optional preparer for this node.  It should be
     * an object that implements the
     * :class:`colander.interfaces.Preparer` interface.
     * * - ``validator``: Optional validator for this node.  It should be
     * an object that implements the
     * :class:`colander.interfaces.Validator` interface.
     * * - ``after_bind``: A callback which is called after a clone of this
     * node has 'bound' all of its values successfully. This callback
     * is useful for performing arbitrary actions to the cloned node,
     * or direct children of the cloned node (such as removing or
     * adding children) at bind time.  A 'binding' is the result of an
     * execution of the ``bind`` method of the clone's prototype node,
     * or one of the parents of the clone's prototype nodes.  The
     * deepest nodes in the node tree are bound first, so the
     * ``after_bind`` methods of the deepest nodes are called before
     * the shallowest.  The ``after_bind`` callback should should
     * accept two values: ``node`` and ``kw``.  ``node`` will be a
     * clone of the bound node object, ``kw`` will be the set of
     * keywords passed to the ``bind`` method.
     * * - ``title``: The title of this node.  Defaults to a titleization
     * of the ``name`` (underscores replaced with empty strings and the
     * first letter of every resulting word capitalized).  The title is
     * used by higher-level systems (not by Colander itself).
     * * - ``description``: The description for this node.  Defaults to
     * ``''`` (the empty string).  The description is used by
     * higher-level systems (not by Colander itself).
     * * - ``widget``: The 'widget' for this node.  Defaults to ``None``.
     * The widget attribute is not interpreted by Colander itself, it
     * is only meaningful to higher-level systems such as Deform.
     * * Arbitrary keyword arguments remaining will be attached to the node
     * object unmolested.
     * * _counter = itertools.count()
     * * def __new__(cls, *arg, **kw):
     * inst = object.__new__(cls)
     * inst._order = next(cls._counter)
     * return inst
     */
    SchemaNode = _class(t_colander_SchemaNode, [object], function() {
        var __contains__, __delitem__, __getitem__, __init__, __iter__, __repr__, __setitem__, _bind, add, bind, clone, deserialize, flatten, get_value, required, serialize, set_value, unflatten;
        __init__ = function(self, typ, children, kw) {
            var _args, self;
            _args = _init_args(arguments);
            children = _get_varargs(2, _args);
            kw = _get_kwargs(_args);
            self = this;
            self._order = _schema_counter++;
            self.typ = typ;
            self.preparer = kw.pop("preparer", null);
            self.validator = kw.pop("validator", null);
            self.
        default = kw.pop("default", __keyword_null);
            self.missing = kw.pop("missing", required);
            self.name = kw.pop("name", "");
            self.raw_title = kw.pop("title", _marker);
            if (self.raw_title === _marker) {
                self.title = self.name.replace("_", " ").title();
            } else{self.title = self.raw_title;}
            self.description = kw.pop("description", "");
            self.widget = kw.pop("widget", null);
            self.after_bind = kw.pop("after_bind", null);
            self.__dict__.update(kw);
            self.children = list(children);
        };
        /**
         * A property which returns ``True`` if the ``missing`` value
         * related to this node was not specified.
         * * A return value of ``True`` implies that a ``missing`` value wasn't
         * specified for this node or that the ``missing`` value of this node is
         * :attr:`colander.required`.  A return value of ``False`` implies that
         * a 'real' ``missing`` value was specified for this node.
         */
        required = function(self) {
            var self;
            self = this;
            if (isinstance(self.missing, deferred)) {
                return true;
            }
            return self.missing === required;
        };
        /**
         * Serialize the :term:`appstruct` to a :term:`cstruct` based
         * on the schema represented by this node and return the
         * cstruct.
         * * If ``appstruct`` is :attr:`colander.null`, return the
         * serialized value of this node's ``default`` attribute (by
         * default, the serialization of :attr:`colander.null`).
         * * If an ``appstruct`` argument is not explicitly provided, it
         * defaults to :attr:`colander.null`.
         */
        serialize = function(self, appstruct) {
            var _args, cstruct, self;
            _args = _init_args(arguments);
            appstruct = _get_arg(1, "appstruct", _args, __keyword_null);
            self = this;
            if (appstruct === __keyword_null) {
                appstruct = self.
            default;
            }
            if (isinstance(appstruct, deferred)) {
                appstruct = __keyword_null;
            }
            cstruct = self.typ.serialize(self, appstruct);
            return cstruct;
        };
        /**
         * Create and return a data structure which is a flattened
         * representation of the passed in struct based on the schema represented
         * by this node.  The return data structure is a dictionary; its keys are
         * dotted names.  Each dotted name represents a path to a location in the
         * schema.  The values of of the flattened dictionary are subvalues of
         * the passed in struct.
         */
        flatten = function(self, appstruct) {
            var flat, self;
            self = this;
            flat = self.typ.flatten(self, appstruct);
            return flat;
        };
        /**
         * Create and return a data structure with nested substructures based
         * on the schema represented by this node using the flattened
         * representation passed in. This is the inverse operation to
         * :meth:`colander.SchemaNode.flatten`.
         */
        unflatten = function(self, fstruct) {
            var paths, self;
            self = this;
            paths = sorted(fstruct.keys());
            return self.typ.unflatten(self, paths, fstruct);
        };
        /**
         * Uses the schema to set a value in a nested datastructure from a
         * dotted name path.
         */
        set_value = function(self, appstruct, dotted_name, value) {
            var self;
            self = this;
            self.typ.set_value(self, appstruct, dotted_name, value);
        };
        /**
         * Traverses the nested data structure using the schema and retrieves
         * the value specified by the dotted name path.
         */
        get_value = function(self, appstruct, dotted_name) {
            var self;
            self = this;
            return self.typ.get_value(self, appstruct, dotted_name);
        };
        /**
         * Deserialize the :term:`cstruct` into an :term:`appstruct` based
         * on the schema, run this :term:`appstruct` through the
         * preparer, if one is present, then validate the
         * prepared appstruct.  The ``cstruct`` value is deserialized into an
         * ``appstruct`` unconditionally.
         * * If ``appstruct`` returned by type deserialization and
         * preparation is the value :attr:`colander.null`, do something
         * special before attempting validation:
         * * - If the ``missing`` attribute of this node has been set explicitly,
         * return its value.  No validation of this value is performed; it is
         * simply returned.
         * * - If the ``missing`` attribute of this node has not been set
         * explicitly, raise a :exc:`colander.Invalid` exception error.
         * * If the appstruct is not ``colander.null`` and cannot be validated , a
         * :exc:`colander.Invalid` exception will be raised.
         * * If a ``cstruct`` argument is not explicitly provided, it
         * defaults to :attr:`colander.null`.
         */
        deserialize = function(self, cstruct) {
            var _args, appstruct, self;
            _args = _init_args(arguments);
            cstruct = _get_arg(1, "cstruct", _args, __keyword_null);
            self = this;
            appstruct = self.typ.deserialize(self, cstruct);
            if (self.preparer != null) {
                appstruct = self.preparer(appstruct);
            }
            if (appstruct === __keyword_null) {
                appstruct = self.missing;
                if (appstruct === required) {
                    throw new Invalid(self, _("Required"));
                }
                if (isinstance(appstruct, deferred)) {
                    throw new Invalid(self, _("Required"));
                }
                return appstruct;
            }
            if (self.validator != null) {
                if (!isinstance(self.validator, deferred)) {
                    self.validator(self, appstruct);
                }
            }
            return appstruct;
        };
        /**
         * Add a subnode to this node.
         */
        add = function(self, node) {
            var self;
            self = this;
            self.children.append(node);
        };
        /**
         * Clone the schema node and return the clone.  All subnodes
         * are also cloned recursively.  Attributes present in node
         * dictionaries are preserved.
         */
        clone = function(self) {
            var cloned, self;
            self = this;
            cloned = new self.__class__(self.typ);
            cloned.__dict__.update(self.__dict__);
            cloned.children = (function() {
                var _i, _len, _list, _results;
                _results = [];
                _list = _iter(self.children);
                for (_i = 0, _len = _list.length; _i < _len; _i++) {
                    node = _list[_i];
                    _results.push(node.clone());
                }
                return _results;
            })();
            return cloned;
        };
        /**
         * Resolve any deferred values attached to this schema node
         * and its children (recursively), using the keywords passed as
         * ``kw`` as input to each deferred value.  This function
         * *clones* the schema it is called upon and returns the cloned
         * value.  The original schema node (the source of the clone)
         * is not modified.
         */
        bind = function(self, kw) {
            var _args, cloned, self;
            _args = _init_args(arguments);
            kw = _get_kwargs(_args);
            self = this;
            cloned = self.clone();
            cloned._bind(kw);
            return cloned;
        };
        _bind = function(self, kw) {
            var _i, _i1, _len, _len1, _list, _list1, child, k, self, v;
            self = this;
            _list = self.children;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                child = _list[_i];
                child._bind(kw);
            }
            _list1 = self.__dict__.items();
            for (_i1 = 0, _len1 = _list1.length; _i1 < _len1; _i1++) {
                k = _list1[_i1][0];
                v = _list1[_i1][1];
                if (isinstance(v, deferred)) {
                    v = v(self, kw);
                    setattr(self, k, v);
                }
            }
            if (getattr(self, "after_bind", null)) {
                self.after_bind(self, kw);
            }
        };
        /**
         * Remove a subnode by name
         */
        __delitem__ = function(self, name) {
            var _i, _len, _list, idx, node, self;
            self = this;
            _list = enumerate(_subscript.l.s(self.children, null, null, null));
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                idx = _list[_i][0];
                node = _list[_i][1];
                if (node.name === name) {
                    return self.children.pop(idx);
                }
            }
            throw new KeyError(name);
        };
        /**
         * Get a subnode by name.
         */
        __getitem__ = function(self, name) {
            var _i, _len, _list, node, self;
            self = this;
            _list = self.children;
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                node = _list[_i];
                if (node.name === name) {
                    return node;
                }
            }
            throw new KeyError(name);
        };
        /**
         * Replace a subnode by name
         */
        __setitem__ = function(self, name, newnode) {
            var _i, _len, _list, idx, node, self;
            self = this;
            _list = enumerate(_subscript.l.s(self.children, null, null, null));
            for (_i = 0, _len = _list.length; _i < _len; _i++) {
                idx = _list[_i][0];
                node = _list[_i][1];
                if (node.name === name) {
                    _subscript.s.i(self.children, idx, newnode);
                    newnode.name = name;
                    return node;
                }
            }
            throw new KeyError(name);
        };
        /**
         * Iterate over the children nodes of this schema node
         */
        __iter__ = function(self) {
            var self;
            self = this;
            return iter(self.children);
        };
        __contains__ = function(self, name) {
            var _ex, self;
            self = this;
            try{_subscript.l.i(self, name);} catch (_ex) {
                if (_ex instanceof KeyError) {
                    return false;
                } else{
                throw _ex}
            }
            return true;
        };
        __repr__ = function(self) {
            var self;
            self = this;
            return "<%s.%s object at %d (named %s)>".__mod__(self.__module__, self.__class__.__name__, id(self), self.name);
        };
        return [{__init__: __init__,required: required,serialize: serialize,flatten: flatten,unflatten: unflatten,set_value: set_value,get_value: get_value,deserialize: deserialize,add: add,clone: clone,bind: bind,_bind: _bind,__delitem__: __delitem__,__getitem__: __getitem__,__setitem__: __setitem__,__iter__: __iter__,__contains__: __contains__,__repr__: __repr__}, {}, {}]
    });

    function t_colander_deferred() {
        this.__init__.apply(this, arguments);
    }
    /**
     * A decorator which can be used to define deferred schema values
     * (missing values, widgets, validators, etc.)
     */
    deferred = _class(t_colander_deferred, [object], function() {
        var __call__, __init__;
        __init__ = function(self, wrapped) {
            var self;
            self = this;
            self.wrapped = wrapped;
        };
        __call__ = function(self, node, kw) {
            var self;
            self = this;
            return self.wrapped(node, kw);
        };
        return [{__init__: __init__,__call__: __call__}, {}, {}]
    });
    _unflatten_mapping = function(node, paths, fstruct, get_child, rewrite_subpath) {
        var _args, _i, _len, _list, appstruct, curname, name, node_name, path, prefix, prefix_len, subfstruct, subnode, subpath, subpaths;
        _args = _init_args(arguments);
        get_child = _get_arg(3, "get_child", _args, null);
        rewrite_subpath = _get_arg(4, "rewrite_subpath", _args, null);
        if (get_child === null) {
            get_child = node.__getitem__;
        }
        if (rewrite_subpath === null) {
            rewrite_subpath = function(subpath) {
                return subpath;
            };
        }
        node_name = node.name;
        if (node_name) {
            prefix = node_name + ".";
        } else{prefix = "";}
        prefix_len = len(prefix);
        appstruct = {};
        subfstruct = {};
        subpaths = [];
        curname = null;
        _list = paths;
        for (_i = 0, _len = _list.length; _i < _len; _i++) {
            path = _list[_i];
            if (path === node_name) {
                continue;
            };
            subpath = _subscript.l.s(path, prefix_len, null, null);
            if (_in(".", subpath)) {
                name = _subscript.l.s(subpath, null, subpath.index("."), null);
            } else{name = subpath;}
            if (curname === null) {
                curname = name;
            } else{
            if (name !== curname) {
                subnode = get_child(curname);
                _subscript.s.i(appstruct, curname, subnode.typ.unflatten(subnode, subpaths, subfstruct));
                subfstruct = {};
                subpaths = [];
                curname = name;
            }
            }
            subpath = rewrite_subpath(subpath);
            _subscript.s.i(subfstruct, subpath, _subscript.l.i(fstruct, path));
            subpaths.append(subpath);
        }
        if (curname != null) {
            subnode = get_child(curname);
            _subscript.s.i(appstruct, curname, subnode.typ.unflatten(subnode, subpaths, subfstruct));
        }
        return appstruct;
    };
    prambanan.exports('colander', {All: All,Boolean: Boolean,Date: Date,DateTime: DateTime,Float: Float,Function: Function,Integer: Integer,Invalid: Invalid,Length: Length,Mapping: Mapping,Number: Number,OneOf: OneOf,Positional: Positional,Range: Range,SchemaNode: SchemaNode,SchemaType: SchemaType,Sequence: Sequence,String: String,Time: Time,Tuple: Tuple,deferred: deferred,interpolate: interpolate,is_nonstr_iter: is_nonstr_iter,timeparse: timeparse});
})(prambanan);