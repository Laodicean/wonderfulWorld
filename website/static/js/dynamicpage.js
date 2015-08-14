// JavaScript Documen
$(function() {

    var newHash      = "",
        $mainContent = $("#content"),
        $pageWrap    = $("#page"),
        baseHeight   = 0,
        $el;
        
    //$pageWrap.height($pageWrap.height());
    //baseHeight = $pageWrap.height() - $mainContent.height();
    
    $("nav").delegate("a", "click", function() {
        window.location.hash = $(this).attr("href");
        return false;
    });
    
    $(window).bind('hashchange', function(){
    
        newHash = window.location.hash.substring(1);
        
        if (newHash) {
            //$("#content").hide().load(newHash+"#content");
            $("#subcontent").fadeOut(200, function() {
                    $mainContent.load("" +newHash + " #subcontent");
                });
            $("nav a p").removeClass("current_item");
            $("nav a p").removeClass("menu_item");
            $("nav a p").addClass("menu_item");
            $("nav a[href='"+newHash+"'] p").removeClass("menu_item");
            $("nav a[href='"+newHash+"'] p").addClass("current_item");
        }
        
    });
    
    $(window).trigger('hashchange');

});