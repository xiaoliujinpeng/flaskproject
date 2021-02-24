$(function () {
    function render_time() {
        return moment($(this).data('timestamp')).format('lll')
    }
    $('[data-toggle="tooltip"]').tooltip(
        {title: render_time}
    );
});


/* 显示切换icon面板*/
$(function(){
    var icon_button=$("#select_icon_btn");
    icon_button.click(function(){
        $("#icon_show").toggle();
        return false;
    })
})


/*当点击icon图标时发生*/
$(function(){
    var as=$("a[name^='icon']");
    console.log(as);
    as.click(function(){
        var icon_name_input=$("#icon_name");
        icon_name_input.attr('value',this.name);
        return false;
    })
})