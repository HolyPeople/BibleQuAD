var content;
var answer_content; // 정답 answer_content 백업
var count = 0; // 지우고 되돌리기 index

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
    var arr = new Array();
    for (var i = 0; i < array.length; i++) {
        arr[i] = array[i].length;
    }
    return arr;
}

function delete_dot(str) { // '.' 제거
    var output = "";
    for (var i = 0; i < str.length; i++) {
        if (str.charAt(i) == '.') {
            continue;
        }
        output += str.charAt(i);
    }
    return output;
}

function fill_answer_automatically() {
    var selected = getSelection();
    var arr = makeArray(content.innerHTML);
    var offset_min = convertIndexLeft(Math.min(selected.anchorOffset, selected.focusOffset) + 1, arr);
    var offset_max = convertIndexRight(Math.max(selected.anchorOffset, selected.focusOffset) - 1, arr);
    if (!offset_max) offset_max = 0; // 예외 처리
    var sentence = content.innerHTML.substring(offset_min, offset_max);
    sentence = delete_dot(sentence);
    var answer_input = document.getElementById('answer'); // 정답란
    answer_input.value = sentence;
    answer_content = sentence;
}

function 드래그_기능_추가() {
    content = document.getElementById('context');
    content.onclick = fill_answer_automatically;
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
    input.value = answer_content.substring(0, answer_content.length + count);
}

function recover() {
    var input = document.getElementById('answer');
    input.value = answer_content.substring(0, answer_content.length + count);
    if (count == 0) return;
    count++;
}

onload = function () {

    드래그_기능_추가();
}