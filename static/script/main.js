$(document).ready(function () {
  $('.sidenav').sidenav();
  $('.parallax').parallax();
  console.log(data);
  if (data['uuid'] !== null) {
    $('.nav').each(function (idx, item) {
        $(item).html('<li><a href="/test">QA 시험</a></li>' + '<li><a href="/submit">QA 제출</a></li>\n' + '<li><a href="/logout">로그아웃</a></li>\n')
    });
  }

});