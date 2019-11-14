
$(document).ready(function(){
    $('select').formSelect();
    $('.sidenav').sidenav();
  });

$('#submit').click(function () {
    var prograss = '<div class="progress "><div class="indeterminate light-blue"></div></div>'
    $('#submit_result').html(prograss)
});

$('#question')