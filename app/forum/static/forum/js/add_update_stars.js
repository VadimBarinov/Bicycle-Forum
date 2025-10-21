$(document).ready(function () {
    $('form[name=formAddStar]').submit(function () {
        $.ajax({
            data: $(this).serialize(),
            url: currentUrl,
            type: "POST",
            dataType: "json",
            success: function (response) {
                if (response.is_taken == true) {
                    $('#AddStarModal').modal('hide');
                    $('#myStar').removeClass('text-grey');
                    $('#myStar').text('моя оценка:');
                    $('#myStarValue').text(parseFloat(response.star_value).toFixed(1).replace(".",","));
                    if (response.star_bike == 0) {
                        $('#bikeStarImg').attr('src', black_star);
                        $('#bikeStar').addClass('text-grey');
                        $('#bikeStar').text('нет оценок');
                    }
                    else {
                        $('#bikeStarImg').attr('src', grad_star);
                        $('#bikeStar').removeClass('text-grey');
                        $('#bikeStar').text(parseFloat(response.star_bike).toFixed(1).replace(".",","));
                    }
                }
                else {
                  $(location).attr('href', login_url);
                }
            }
        });
        return false;
    });
})