$(document).ready(function(){

    var postview=$("#test-markdown-view");
    var navList=$(".nav_list");
    var hs=postview.children("h1,h2,h3,h4,h5");

    for(var i=0;i<hs.length;i++){

        var atag=$("<a href='#'></a>");
        if(hs.get(i).tagName.toLowerCase().indexOf("h1") != -1){
            atag.css({"padding-left":"5px","font-weight":"800"});

        }
        if(hs.get(i).tagName.toLowerCase().indexOf("h2") != -1){
            atag.css("padding-left","20px");
        }
        if(hs.get(i).tagName.toLowerCase().indexOf("h3") != -1){
            atag.css("padding-left","35px");
        }
        if(hs.get(i).tagName.toLowerCase().indexOf("h4") != -1){
            atag.css("padding-left","50px");
        }
        if(hs.get(i).tagName.toLowerCase().indexOf("h5") != -1){
            atag.css("padding-left","65px");
        }
        atag.text(hs.eq(i).text());
        atag.attr("href",`#${hs.eq(i).attr('id')}`);
        atag.addClass("d-block");
        var li=$("<li></li>");
        li.addClass("list-group-item")
        li.addClass("navbar-nav")
        li.css({"padding":"0"})
        li.append(atag);

        navList.append(li);
    }
})
