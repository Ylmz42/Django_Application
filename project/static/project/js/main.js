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
function checkBoxChecked(item_id) {

    var checkBox = document.getElementById(item_id);

    if (checkBox.value == "1") {
        checkBox.checked = true;
    }
    else {
        checkBox.checked = false;
    }
}

function isChecklistChecked(app_id) {

    var checkBox = document.getElementsByClassName(app_id);

    for (var i = 0; i < checkBox.length; i++) {

        if (checkBox[i].value[i] == "1") {
            checkBox[i].disabled = false;

            if (checkBox[i].name[i] == "1") {
                checkBox[i].checked = true;
            }
            else {
                checkBox[i].checked = false;
            }
        }
        else {
            checkBox[i].disabled = true;
        }
    }
}

$(function () {
    bs_input_file();
});