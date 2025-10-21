$(document).ready(function () {
    $('form[name=formDeleteStar]').submit(function () {
        $.ajax({
            data: $(this).serialize(),
            url: currentUrl,
            type: "POST",
            dataType: "json",
            success: function (response) {
                if (response.is_taken == true) {
                    window.location.reload();
                }
            }
        });
        return false;
    });
})