var answer_back_up = []; // 정답 내용 백업
var count = []; // 지우고 되돌리기 index
var s1, s2, s3, s4; // 셀렉터 값
var multiple_answer_box = []; // 중복 답변란
var mab_num = 0; // 중복 답변란 개수
var focused_box = 0; // 포커스된 답변란의 index
var answer_starts = [];
var result = null;
var no_answer = false;

function convertIndexLeft(index, array) { // index번째 문자가 포함된 단어의 왼쪽 index 추출
    var sum = 0;
    for (var i = 0; i < array.length; i++) {
        if (index >= sum && index <= sum + array[i]) {
            return sum;
        }
        sum += array[i] + 1;
    }
}

function convertIndexRight(index, array) { // index번째 문자가 포함된 단어의 오른쪽 index 추출
    var sum = 0;
    for (var i = 0; i < array.length; i++) {
        if (index >= sum && index <= sum + array[i]) {
            return sum + array[i];
        }
        sum += array[i] + 1;
    }
}

function makeArray(str) { // index번째 단어의 문자 개수를 나타내는 배열 리턴
    var array = str.split(' ');
    var arr = [];
    for (var i = 0; i < array.length; i++) {
        arr[i] = array[i].length;
    }
    return arr;
}

function delete_dot(str) { // '.' 제거
    var output = "";
    for (var i = 0; i < str.length; i++) {
        if (str.charAt(i) === '.') {
            continue;
        }
        output += str.charAt(i);
    }
    return output;
}

function erase(event) {
    var tar = event.target;
    var parent = $('#QA_container');
    var child_index = Array.prototype.indexOf.call(parent.children(), tar) - 1; // 답변란 index
    if (child_index == -2)
        child_index = Array.prototype.indexOf.call(parent.children(), tar.parentElement) - 1;
    var input_to_erase = parent.children().eq(child_index);
    var answer = input_to_erase.val();
    var array = makeArray(answer);
    if (array[array.length - 1] == 1) { // 한 글자 남았을 때
        alert('더 이상 지울 수 없습니다.');
        return;
    }
    var i = Math.floor(child_index / 4);
    if(answer_back_up[i] == null) {
        return;
    }
    count[i]--;
    input_to_erase.get(0).value = answer_back_up[i].substring(0, answer_back_up[i].length + count[i]);
}

function recover(event) {
    var tar = event.target;
    var parent = $('#QA_container');
    var child_index = Array.prototype.indexOf.call(parent.children(), tar) - 2; // 답변란 index
    if (child_index == -3)
        child_index = Array.prototype.indexOf.call(parent.children(), tar.parentElement) - 2;
    var input_to_recover = parent.children().eq(child_index);
    var i = Math.floor(child_index / 4);
    if(answer_back_up[i] == null) {
        return;
    }
    input_to_recover.get(0).value = answer_back_up[i].substring(0, answer_back_up[i].length + count[i]);
    if (count[i] == 0) return;
    count[i]++;
}

function ans_box_listener(event) {
    var parent = $('#QA_container'); // 삭제 버튼의 parent
    var box_index = Array.prototype.indexOf.call(parent.children(), event.target);
    focused_box = box_index;
}

function del_btn_listener(event) {
    var tar_btn = event.target; // 중복 답변란 + 삭제 버튼
    var parent = $('#QA_container'); // 삭제 버튼의 parent
    var btn_index = Array.prototype.indexOf.call(parent.children(), tar_btn); // 누른 버튼의 index
    if (btn_index == -1) {
        btn_index = Array.prototype.indexOf.call(parent.children(), tar_btn.parentElement);
    }
    parent.children().eq(btn_index - 3).remove();
    parent.children().eq(btn_index - 3).remove();
    parent.children().eq(btn_index - 3).remove();
    parent.children().eq(btn_index - 3).remove();
    var index = (btn_index - 3) / 4;
    remove_shift(multiple_answer_box, index, mab_num);
    remove_shift(answer_back_up, index, mab_num);
    remove_shift(count, index, mab_num);
    remove_shift(answer_starts, index, mab_num);
    mab_num--; // 중복 답변란 개수 --
}

function checkbox_listener(event) {
    if ($('#checkbox_input').is(':checked')) { // checked
        no_answer = true;
        while (true) { // 중복 답변 다 삭제하기
            if ($("#QA_container").children().length == 4) break;
            var delete_btn = $("#QA_container").children().eq(7);
            delete_btn.trigger("click");
        }
        $("#answer").val("(없음)");
    }
    else { // unchecked
        no_answer = false;
        $("#answer").val("");
    }
}

function add() {
    if (no_answer == true) return;
    if (mab_num == 9) return; // 중복 답변은 10개로 제한
    // 중복 답변란 추가
    multiple_answer_box[mab_num] = $('<input class="col s9 " onclick="ans_box_listener(event)" type="text" name="answer'+mab_num+'" id="answer'+mab_num+'" readonly="true" placeholder="정답을 드래그 하여 선택해 주세요">').appendTo('#QA_container');
    // 지우기 버튼 추가
    $('<button onclick="erase(event)" class="col s1 btn_ans1 waves-effect waves-red btn-small white"><i class="black-text material-icons">keyboard_backspace</i></button>').appendTo('#QA_container');
    // 복원 버튼 추가
    $('<button onclick="recover(event)" class="col s1 btn_ans2 waves-effect waves-yellow btn-small white"><i class="black-text material-icons">restore</i></button>').appendTo('#QA_container');
    // 삭제 버튼 추가
    $('<button onclick="del_btn_listener(event)" class="col s1 btn_ans3 waves-effect waves-red btn-small white"><i class="black-text material-icons">delete_forever</i></button>').appendTo('#QA_container');

    mab_num++; // 중복 답변란 개수 ++
}

function find_paragraph(search) {

    var result = null;

    $.ajax({
        type: "GET",
        dataType: "text",
        async: false,
        data: { book: search[1], chapter: search[2], verse: search[3] },
        url: "/submit/paragraph",
        success: function (data) {
            result = JSON.parse(data);
            return result;
        },
        error: function (e) {
            alert('서버 연결 도중 에러발생' + e);
        }
    })
    return result;
}

function getArray(obj) {
    var index = [];
    for (var x in obj) {
        index.push(x);
    }
    return index;
}

function append_options_by_array(selector_num, arr) {
    var id = "#s" + selector_num;
    for (let i = 0; i < arr.length; i++) {
        $(id).append(new Option(arr[i]));
    }
    $('select').formSelect();
}

function remove_shift(array, index, size) { // 배열에서 remove and shift
    let i;
    for (i = index; i < size; i++) {
        array[i] = array[i + 1];
    }
    array[i] = null;
}

$(document).ready(function () {
    $('.btn_ans1').click(erase);
    $('.btn_ans2').click(recover);
    $('.btn_ans3').click(add);

    $('select').formSelect();
    $('.sidenav').sidenav();
    $('.modal').modal();

    // 드래그 시 자동으로 답변란 채워짐
    $('#context').click(function () {
        if (no_answer == true) return;
        var i = Math.floor(focused_box / 4);
        count[i] = 0;
        var selected = getSelection();
        var arr = makeArray(this.innerHTML);
        var offset_min = convertIndexLeft(Math.min(selected.anchorOffset, selected.focusOffset) + 1, arr);
        var offset_max = convertIndexRight(Math.max(selected.anchorOffset, selected.focusOffset) - 1, arr);
        if (!offset_max) offset_max = 0; // 예외 처리
        var sentence = this.innerHTML.substring(offset_min, offset_max);
        var range = selected.getRangeAt(0);
        range.setStart(selected.anchorNode, offset_min);
        range.setEnd(selected.focusNode, offset_max);
        sentence = delete_dot(sentence);
        $('#QA_container').children().eq(focused_box).val(sentence); // 답변 채우기
        answer_back_up[i] = sentence;
        answer_starts[i] = offset_min;
    });

    // 단락 검색
    $('#img_search').click(function () {
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
        result = find_paragraph(search);

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

    // 셀렉터 설정
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

    $('#question').keyup(function () {
       var str =  $('#question').val().trim();
       if (str.length == 0) {
           $('#submit').attr('disabled', 'disabled');
       } else {
           $('#submit').removeAttr('disabled');
       }
    });

    $('#submit').click(function () {
        if(result == null) {
            alert("본문도 선택안하고 정답을 어떻게 알죠?")
            return;
        }
        var question = $('#question').val();
        var qa = {is_impossible : false,
            question : question,
            answers : [],
            paragraph_id : result['id']}
        if (!no_answer) {
            if ($('#answer').val().trim().length == 0) {
                alert("정답을 선택해 주세요!");
                return;
            }
            var answers = [{text: $('#answer').val(), answer_start: answer_starts[0]}];
            for (var i = 0; i < mab_num; i++) {
                if (multiple_answer_box[i].val().trim().length != 0)
                    answers.push({text: multiple_answer_box[i].val(), answer_start: answer_starts[i + 1]});
            }
            qa['answers'] = answers;
        } else {
            qa['is_impossible'] = true
        }

        $.ajax({
            url: '/submit/qa',
            type: 'POST',
            dataType: 'text/json',
            data: {json:JSON.stringify(qa)},
            complete: function () {
                while (true) { // 중복 답변 다 삭제하기
                if ($("#QA_container").children().length == 4) break;
                var delete_btn = $("#QA_container").children().eq(7);
                delete_btn.trigger("click");
                }
                $("#answer").val("");
                $("#question").val("");
            }
        })
    });
});