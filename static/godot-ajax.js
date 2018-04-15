// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// assets likes
$('#likes_asset').click(function() {
    var entryid = $(this).data()['entryid'];
    $.ajax({
        type: 'POST',
        url: '/api/assets/'+entryid+'/likes/',
        data: {csrfmiddlewaretoken: csrftoken},
        statusCode: {
            201: function () {
                $('#likes').toggleClass('btn-default');
                $('#likes').toggleClass('btn-success active');
                $('#likes').find('i').toggleClass('fa-rotate-270');
                $('#liked').html('Liked ');
                $('#likes_count').html(function (i, val) {
                    return +val + 1
                });
            },
            204: function () {
                $('#likes').toggleClass('btn-default');
                $('#likes').toggleClass('btn-success active');
                $('#likes').find('i').toggleClass('fa-rotate-270');
                $('#liked').html('Like ');
                $('#likes_count').html(function (i, val) {
                    return +val - 1
                });
            }
        }
    })
});

// framework likes
$('#likes_framework').click(function() {
    var frameworkid = $(this).data()['frameworkid'];
    $.ajax({
        type: 'POST',
        url: '/api/frameworks/'+frameworkid+'/likes/',
        data: {csrfmiddlewaretoken: csrftoken},
        statusCode: {
            201: function () {
                $('#likes').toggleClass('btn-default');
                $('#likes').toggleClass('btn-success active');
                $('#likes').find('i').toggleClass('fa-rotate-270');
                $('#liked').html('Liked ');
                $('#likes_count').html(function (i, val) {
                    return +val + 1
                });
            },
            204: function () {
                $('#likes').toggleClass('btn-default');
                $('#likes').toggleClass('btn-success active');
                $('#likes').find('i').toggleClass('fa-rotate-270');
                $('#liked').html('Like ');
                $('#likes_count').html(function (i, val) {
                    return +val - 1
                });
            }
        }
    })
});

$('#deleteEntry').click(function() {
    var entryid = $(this).data()['entryid'];
    console.log(entryid, csrftoken);
    $(this).toggle(1000);
    $.ajax({
        type: 'DELETE',
        url: '/api/assets/'+entryid+'/',
        data: {csrfmiddlewaretoken: csrftoken},

        success: function (response) {
        console.log(response);
      },

        error: function (xhr, ajaxOptions, thrownError) {
            console.log(thrownError);
        }
    })
});