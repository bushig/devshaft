$('#likes').click(function(){


    $.ajax({
        type: 'POST',
        url: '/api/assets/',
        data: '',
        success: function(data) {
            $(this).toggleClass('btn-default');
            $(this).toggleClass('btn-success active');
            $(this).find('i').toggleClass('fa-rotate-270');
            $('#likes_count').html(function(i, val) { return +val+1 });
            console.log(data);
        },
        error: function(){
            alert('error');
        }
    })
});