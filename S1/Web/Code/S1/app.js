/**
 * Created by Armin on 11/1/2017.
 */
$(document).ready(function () {
    $("input[type='radio'][name='tab-select']").change(function () {
        console.log(this.value);
        change_tab(this.value);
        if (this.value === "1"){
            getList();
        }
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
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken;
$(document).ready(function () {
    csrftoken = $("input[name='csrfmiddlewaretoken']").value;
    alert(csrftoken);
});
function getList(){
    $.ajax({
        url: "getList",
        type: "POST",
        data: {
                "X-CSRFToken": csrftoken
            },
        success: function(result){
            $(".tab-container .tab-contents #tab-content-1").html(result);
        },
        error: function (response) {
            $(".tab-container .tab-contents #tab-content-1").html(response.responseText);
        }
    });
}
function addStudent(){
    $.ajax({
        url: "addStudent",
        type: "POST",
        data:{

        }
    });
}