$('#likes').click(function() {
    $.ajax({
        type: 'POST',
        url: '/api/assets/11/likes/',
        data: {csrfmiddlewaretoken: "DfNmvh3lMYKgrQ0nGS3yuIB4k5bfvzJ8"},
        statusCode: {
            201: function () {
                $('#likes').toggleClass('btn-default');
                $('#likes').toggleClass('btn-success active');
                $('#likes').find('i').toggleClass('fa-rotate-270');
                $('#likes_count').html(function (i, val) {
                    return +val + 1
                });
            },
            204: function () {
                $('#likes').toggleClass('btn-default');
                $('#likes').toggleClass('btn-success active');
                $('#likes').find('i').toggleClass('fa-rotate-270');
                $('#likes_count').html(function (i, val) {
                    return +val - 1
                });
            }
        }
    })
});