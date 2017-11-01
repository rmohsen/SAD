/**
 * Created by Armin on 11/1/2017.
 */
$(document).ready(function () {
    $("input[type='radio'][name='tab-select']").change(function () {
        console.log(this.value);
        change_tab(this.value);
    });
});

function change_tab(new_tab){
    clear_all_tabs();
    $(".tab-container .tab-contents #tab-content-" + new_tab).css("display", "block");
}
function clear_all_tabs(){
    var x = $(".tab-container .tab-contents .tab-content");
    console.log("length: " + x.length);
    for (var i = 0; i < x.length; i++){
        $(x[i]).css("display", "none");
    }
}