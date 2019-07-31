function bs_input_file() {
    $(".input-file").before(
        function () {
            if (!$(this).prev().hasClass('input-ghost')) {
                var element = $("<input type='file' class='input-ghost' style='visibility:hidden; height:0'>");
                element.attr("name", $(this).attr("name"));
                element.change(function () {
                    element.next(element).find('input').val((element.val()).split('\\').pop());
                });
                $(this).find("button.btn-choose").click(function () {
                    element.click();
                });
                $(this).find("button.btn-reset").click(function () {
                    element.val(null);
                    $(this).parents(".input-file").find('input').val('');
                });
                $(this).find('input').css("curs or", "pointer");
                $(this).find('input').mousedown(function () {
                    $(this).parents('.input-file').prev().click();
                    return false;
                });
                return element;
            }
        }
    );
}
//This function's for setting checkboxes status.
function myFunction(item_id) {
    var checkBox = document.getElementsByName(item_id);
    for (var i = 0; i < checkBox.length; i++) {
        if (checkBox[i].value[i] == "1") {
            checkBox[i].checked = true;
        }
        else {
            checkBox[i].checked = false;
        }
    }
}
//This function's for updating database.
function update_db(item_id, check_id) {
    var checkBox = document.getElementsByName(item_id);
    var b = '';
    var c = ''
    for (var i = 0; i < checkBox.length; i++) {
        var value = checkBox[i].value[i];
        b += value;
    }
    if (b.charAt(check_id - 1) == '0') {
        c = b.substring(0, check_id - 1) + '1' + b.substring(check_id);
    }
    else {
        c = b.substring(0, check_id - 1) + '0' + b.substring(check_id);
    }
    location.replace("/update/" + item_id + "/" + c);
}

$(function () {
    bs_input_file();
});
