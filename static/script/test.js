var s1, s2, s3, s4;

function append_options_by_array(selector_num, arr) {
    var id = "#s" + selector_num;
    console.log($(id));
    console.log(new Option(arr[0]));
    for (var i = 0; i < arr.length; i++) {
        $(id).append(new Option(arr[i]));
    }
    $('select').formSelect();
    $('#result_container').html('')
}

function find_paragraph(search) {

    var result = null;

    $.ajax({
        type : "GET",
        dataType : "text",
        async : false,
        data : {book : search[1], chapter : search[2], verse: search[3]},
        url : "/submit/paragraph",
        success: function (data) {
            result = JSON.parse(data)
            return result;
        },
        error : function (e) {
            alert('서버 연결 도중 에러발생' + e);
        }
    })
    return result;
}

function getArray(obj) {
    var index = [];
    for (var x in obj) {
        console.log(x);
        index.push(x);
    }
    console.log(index);
    return index;
}

$(document).ready(function(){
    $('select').formSelect();
    $('.sidenav').sidenav();

    $('#search_btn').click(function () {
        var search = [];
        var outline = $('#outLine');
        var bible_num = $('#bible_num');
        var content = $('#context');
        $('.selection').each(function (index, item) {
            search.push($(item).val());
        });
        if (search[3] === '-') {
            return;
        }

        var result = find_paragraph(search);
        console.log(search)

        // 검색된 단락이 없을 때
        if (result == null) {
            outline.text("(없음)");
            bible_num.text("(" + "-" + " " + "-" + ":" + "-" + " ~ " + "-" + ":" + "-" + ")");
            content.text("(없음)");
            return;
        }

        //출력
        outline.text(result["단락_제목"]);
        bible_num.text("(" + result["성경"] + " " + result["시작_장"] + ":" + result["시작_절"] + " ~ " + result["끝_장"] + ":" + result["끝_절"] + ")");
        content.text(result["단락_내용"]);
    });

    $('#submit').click(function () {
        var prograss = '<div class="row card-panel">\n' +
            '<div class="red-text center">정답을 추론하고 있습니다.</div>\n' +
            '<div id="submit_result" class=""><div class="progress "><div class="indeterminate light-blue"></div></div></div>\n' +
            '</div>\n';
        $('#result_container').html(prograss);

        $.ajax({
            type : "GET",
            dataType : "text",
            async : false,
            data : {paragraph : $('#context').text(), question : $('#question').val()},
            url : "/test/answer",
            success: function (data) {
                var result = JSON.parse(data)
                $('#result_container').html('<div class="row card-panel">정답<h1 class="center">'+ result['return_object']['MRCInfo']['answer'] +'</h1></div>>')
            },
            error : function (e) {
            }
        })
    });

    $('#question').keyup(function () {
        var question = $('#question');
        var str = question.val().trim();
        if (str.length === 0 || $('#s4 option:selected').val() === '-') {
            $('#submit').attr('disabled', 'disabled');
        } else {
            $('#submit').removeAttr('disabled');
        }
    });

    append_options_by_array(1, getArray(data_JSON));
    $("#s1").change(function () {
        $("#s2").find('option').not(':first').remove();
        $("#s3").find('option').not(':first').remove();
        $("#s4").find('option').not(':first').remove();
        s1 = $("#s1 option:selected").val(); // 구약 or 신약
        var bible = [];
        for (let i = 0; i < data_JSON[s1].length; i++) {
            bible.push(data_JSON[s1][i]["book"]);
        }
        append_options_by_array(2, bible);
    });

    $("#s2").change(function () {
        $("#s3").find('option').not(':first').remove();
        $("#s4").find('option').not(':first').remove();
        s2 = $("#s2 option:selected").index() - 1; // 창세기 or 출애굽기
        var chapter = [];
        for (let i = 1; i <= data_JSON[s1][s2]["chapter"]; i++) {
            chapter.push(i);
        }
        append_options_by_array(3, chapter);
    });

    $("#s3").change(function () {
        $("#s4").find('option').not(':first').remove();
        s3 = $("#s3 option:selected").index(); // 1장 or 2장
        var verse = [];
        for (let i = 1; i <= data_JSON[s1][s2]["verse_counts"][s3 - 1]; i++) {
            verse.push(i);
        }
        append_options_by_array(4, verse);
    });

});
