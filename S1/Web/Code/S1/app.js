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
    //alert(csrftoken);
});
function getList(){
    $.ajax({
        url: "show",
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
        url: "add",
        type: "POST",
        data:{
            first_name: $("#add-student").find("input[name='first_name']").prop("value").trim(),
            last_name: $("#add-student").find("input[name='last_name']").prop("value").trim(),
            national_id: $("#add-student").find("input[name='identity_code']").prop("value").trim(),
            birth_date: $("#add-student").find("input[name='birth_date']").prop("value").trim()
        }, success: function (result) {
                alert("Added Successfully!");
        }, error: function (result) {
            $("#response").html(result.responseText);
            if ($("#response #info p").html().trim() == "user tekrari")
                alert("دانشجوی مورد نظر در سامانه موجود می باشد.");
        }
    });
}
function removeStudent(){
    $.ajax({
        url: "remove",
        type: "POST",
        data:{
            national_id: $("#add-student").find("input[name='identity_code']").prop("value").trim()
        }, success: function (result) {
                alert("Remove Successfully!");
        }, error: function (result) {
            $("#response").html(result.responseText);
            if ($("#response #info p").html().trim() == "no user")
                alert("دانشجوی مورد نظر در سامانه موجود نمی باشد.");

        }
    });
}
function editStudent(){
    $.ajax({
        url: "edit",
        type: "POST",
        data:{
            first_name: $("#edit-student").find("input[name='first_name']").prop("value").trim(),
            last_name: $("#edit-student").find("input[name='last_name']").prop("value").trim(),
            national_id: $("#edit-student").find("input[name='identity_code']").prop("value").trim(),
            birth_date: $("#edit-student").find("input[name='birth_date']").prop("value").trim()
        }, success: function (result) {
                alert("Edited Successfully!");
        }, error: function (result) {
            $("#response").html(result.responseText);
            if ($("#response #info p").html().trim() == "no user")
                alert("دانشجوی مورد نظر در سامانه موجود نمی باشد.");
        }
    });
}

function emptyCheck(element, container){
    if (element.value.trim() == ""){
        $(container).find("." + $(element).attr("name") + "_v").prop("value", "E");
    } else {
        $(container).find("." + $(element).attr("name") + "_v").prop("value", "V");
    }
}

$(document).on("click", "#add-student .sbmt", function () {
    if ($("#add-student .first_name_v").prop("value") == "V" &&
        $("#add-student .last_name_v").prop("value") == "V" &&
        $("#add-student .identity_code_v").prop("value") == "V" &&
        $("#add-student .birth_date_v").prop("value") == "V")
        addStudent();
    else {
        if ($("#add-student .first_name_v").prop("value") == "E"){
            $("#add-student input[name='first_name']").css("background-color", "#ffa7a5");
        }
        if ($("#add-student .last_name_v").prop("value") == "E"){
            $("#add-student input[name='last_name']").css("background-color", "#ffa7a5");
        }
        if ($("#add-student .identity_code_v").prop("value") == "E"){
            $("#add-student input[name='identity_code']").css("background-color", "#ffa7a5");
        }
        if ($("#add-student .birth_date_v").prop("value") == "E"){
            $("#add-student input[name='birth_date']").css("background-color", "#ffa7a5");
        }
        alert("برخی فیلد ها پر نشده اند.")
    }
});
$(document).on("focusout", "#add-student input[name='first_name']", function () {
    emptyCheck(this, $("#add-student"))
});
$(document).on("focusout", "#add-student input[name='last_name']", function () {
    emptyCheck(this, $("#add-student"))
});
$(document).on("focusout", "#add-student input[name='identity_code']", function () {
    emptyCheck(this, $("#add-student"))
});
$(document).on("focusout", "#add-student input[name='birth_date']", function () {
    emptyCheck(this, $("#add-student"))
});
$(document).on("focus", "input[name='first_name']", function () {
    $(this).css("background-color", "white");
});
$(document).on("focus", "input[name='last_name']", function () {
    $(this).css("background-color", "white");
});
$(document).on("focus", "input[name='identity_code']", function () {
    $(this).css("background-color", "white");
});
$(document).on("focus", "input[name='birth_date']", function () {
    $(this).css("background-color", "white");
});



$(document).on("click", "#remove-student .sbmt", function () {
    if ($("#remove-student .identity_code_v").prop("value") == "V")
        removeStudent();
    else {
        if ($("#remove-student .identity_code_v").prop("value") == "E"){
            $("#remove-student input[name='identity_code']").css("background-color", "#ffa7a5");
        }
        alert("برخی فیلد ها پر نشده اند.")
    }
});

$(document).on("focusout", "#remove-student input[name='identity_code']", function () {
    emptyCheck(this, $("#remove-student"))
});




$(document).on("click", "#edit-student .sbmt", function () {
    if ($("#edit-student .first_name_v").prop("value") == "V" &&
        $("#edit-student .last_name_v").prop("value") == "V" &&
        $("#edit-student .identity_code_v").prop("value") == "V" &&
        $("#edit-student .birth_date_v").prop("value") == "V")
        editStudent();
    else {
        if ($("#edit-student .first_name_v").prop("value") == "E"){
            $("#edit-student input[name='first_name']").css("background-color", "#ffa7a5");
        }
        if ($("#edit-student .last_name_v").prop("value") == "E"){
            $("#edit-student input[name='last_name']").css("background-color", "#ffa7a5");
        }
        if ($("#edit-student .identity_code_v").prop("value") == "E"){
            $("#edit-student input[name='identity_code']").css("background-color", "#ffa7a5");
        }
        if ($("#edit-student .birth_date_v").prop("value") == "E"){
            $("#edit-student input[name='birth_date']").css("background-color", "#ffa7a5");
        }
        alert("برخی فیلد ها پر نشده اند.")
    }

});
$(document).on("focusout", "#edit-student input[name='first_name']", function () {
    emptyCheck(this, $("#edit-student"))
});
$(document).on("focusout", "#edit-student input[name='last_name']", function () {
    emptyCheck(this, $("#edit-student"))
});
$(document).on("focusout", "#edit-student input[name='identity_code']", function () {
    emptyCheck(this, $("#edit-student"))
});
$(document).on("focusout", "#edit-student input[name='birth_date']", function () {
    emptyCheck(this, $("#edit-student"))
});
