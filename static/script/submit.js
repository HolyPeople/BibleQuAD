var answer_back_up; // 정답 내용 백업
var count = 0; // 지우고 되돌리기 index
var s1, s2, s3, s4; // 셀렉터 값

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

function erase() {
    var input = document.getElementById('answer');
    var answer = input.value;
    var array = makeArray(answer);
    if (array[array.length - 1] == 1) { // 한 글자 남았을 때
        alert('더 이상 지울 수 없습니다.');
        return;
    }
    count--;
    input.value = answer_back_up.substring(0, answer_back_up.length + count);
}

function recover() {
    var input = document.getElementById('answer');
    input.value = answer_back_up.substring(0, answer_back_up.length + count);
    if (count === 0) return;
    count++;
}

function find_paragraph(search) {
    // for (let i = 0; i < pg.length; i++) {
    //     if (pg[i]["신/구약"] != search[0] || pg[i]["성경"] != search[1]) continue;
    //     if (pg[i]["시작_장"] > search[2] || pg[i]["끝_장"] < search[2]) continue;
    //     if (pg[i]["시작_장"] == search[2]) {
    //         if (pg[i]["시작_절"] <= search[3] || pg[i]["끝_절"] >= search[3]) return pg[i];
    //     }
    //     else { // 시작_장보다 크지만 끝_장보다 작거나 같은 장인 경우
    //         if (pg[i]["끝_장"] > search[2]) return pg[i];
    //         else { // 끝_장과 같은 장인 경우
    //             if (pg[i]["끝_절"] >= search[3]) return pg[i];
    //         }
    //     }
    // }
    return null;
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
}

$(document).ready(function () {
    // 드래그 시 자동으로 답변란 채워짐
    $('#context').click(function () {
        count = 0;
        var selected = getSelection();
        var arr = makeArray(this.innerHTML);
        var offset_min = convertIndexLeft(Math.min(selected.anchorOffset, selected.focusOffset) + 1, arr);
        var offset_max = convertIndexRight(Math.max(selected.anchorOffset, selected.focusOffset) - 1, arr);
        if (!offset_max) offset_max = 0; // 예외 처리
        var sentence = this.innerHTML.substring(offset_min, offset_max);
        sentence = delete_dot(sentence);
        var answer_input = document.getElementById('answer'); // 정답란
        answer_input.value = sentence;
        answer_back_up = sentence;
    });

    // 단락 검색
    $('#img_search').click(function () {
        var search = [];
        var outline = $('#outLine');
        var bible_num = $('#bible_num');
        var content = $('#context');
        $('.selector').each(function (index, item) {
            search.push($(item).val());
        });
        var result = find_paragraph(search);

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
});