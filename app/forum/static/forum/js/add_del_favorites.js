$(document).ready(function () {
    $('form[name=formFavorite]').submit(function () {
        $.ajax({
            data: $(this).serialize(),
            url: currentUrl,
            type: "POST",
            dataType: "json",
            success: function (response) {
                if (response.is_taken == true) {
                  if (response.is_added == true){
                    $('#clickOnHeartFavorite' + response.bike_selected).attr('src', grad_heart);
                    $('#clickOnBtnFavorite'+ response.bike_selected).removeClass('btn-primary').addClass('btn-outline-primary');
                    $('#clickOnBtnFavorite'+ response.bike_selected).text('В избранном');
                  }
                  else {
                    $('#clickOnHeartFavorite'+ response.bike_selected).attr('src', black_heart);
                    $('#clickOnBtnFavorite'+ response.bike_selected).removeClass('btn-outline-primary').addClass('btn-primary');
                    $('#clickOnBtnFavorite'+ response.bike_selected).text('В избранное');
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