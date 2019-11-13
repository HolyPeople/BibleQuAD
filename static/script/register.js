
$(document).ready(function() {
    var passwd = $('#password');
    var pw = $('#passwd');
    var chkPW = $('#chkpw');
    var name = $('#name');
    var account = $('#account');
    var nameQuery = false;
    var accountQuery = false;
    var button = $('#submit');


    passwd.keyup(function() {
        pw.html(checkStrength(passwd.val()));
        checkPassword();
    });

    chkPW.keyup(function () {
        checkPassword();
    });

    function checkPassword() {
        if (passwd.val() === chkPW.val()) {
            chkPW.removeClass();
            chkPW.addClass('valid');
            checkValid();
        }
        else {
            chkPW.removeClass();
            chkPW.addClass('invalid');
        }
    }

    name.keyup(function () {
        var a = name.val().replace(/ /gi, '');
        name.val(a);
        request(name, nameQuery);
        checkValid();
    });

    account.keyup(function () {
        var a = account.val().replace(/ /gi, '');
        account.val(a);
        var regExp = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
        if (account.val().match(regExp) !== null) {
            $("#helper").attr('data-error','사용 불가능한 이메일 입니다.');
            request(account, accountQuery);
        } else {
            account.removeClass();
            account.addClass('invalid');
            $("#helper").attr('data-error','이메일 형식이여야 합니다.');
        }
    });

    function request(obj, objQuery) {
        if (obj.val().length === 0) {
            obj.removeClass(); obj.addClass('validate');
            return;
        }
        if (objQuery) return;
        objQuery = true;
        $.ajax({
            url : "/auth-query",
            type : "POST",
            data : {key : "name", value : obj.val()},
            dataType : "text",
            success: function (data) {
                objQuery = false;
                data = JSON.parse(data);
                if (data['result']) {obj.removeClass(); obj.addClass('invalid');} else {obj.removeClass(); obj.addClass('valid');}
            },
            error : function (e) {
                objQuery = false;
            }
        });
    }

    function checkStrength(password) {
        var strength = 0;
        if (password.length < 8) {
            passwd.removeClass();
            passwd.addClass('invalid');
            pw.removeClass();
            pw.addClass('short');
            return '너무 짧습니다.';
        }
        passwd.removeClass();
        passwd.addClass('valid');
        if (password.length > 9) strength += 1;
        if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1;
        if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) strength += 1;
        if (password.match(/([!%&@#$^*?_~])/)) strength += 1;
        if (password.match(/(.*[!%&@#$^*?_~].*[!%&@#$^*?_~])/)) strength += 1;
// Calculated strength value, we can return messages
// If value is less than 2
        if (strength < 2) {
            pw.removeClass();
            pw.addClass('weak');
            return '약함';
        } else if (strength === 2) {
            pw.removeClass();
            pw.addClass('good');
            return '좋음';
        } else {
            pw.removeClass();
            pw.addClass('strong');
            return '강함';
        }
    }

    function checkValid() {
        if (name.attr('class') === 'valid' && account.attr('class') === 'valid' && passwd.attr('class') === 'valid' && chkPW.attr('class') === 'valid') {
            button.removeAttr('disabled');
        } else {
            button.attr('disabled', 'disabled');
        }
    }

});