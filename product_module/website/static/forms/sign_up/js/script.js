$(document).ready(function(){

    // firstname validation
    let fname_error = 1;
    $('#fname').keyup(function(){
        fname_validation();
    });
    function fname_validation(){
        let fn = $('#fname').val();
        if (fn == "") {
            // $('#fname-error').show();
            $('#fname-error').text("*Fill FirstName...!");
            // $('#fname-error').focus();
            fname_error = 0;
            // return 0;
        } else if ((fn.length < 2) || (fn.length > 10)) {
            // $('#fname-error').show();
            $('#fname-error').text("*First name length must be between 2 to 10...!");
            // $('#fname-error').focus();
            fname_error = 0;
            // return 0;
        } else {
            $('#fname-error').text("");
            // $('fname-error').hide();
            fname_error = 1;
        }
    }


    // lastname validation
    let lname_error = 1;
    $('#lname').keyup(function () {
        lname_validation();
    });
    function lname_validation() {
        let ln = $('#lname').val();
        if (ln.length == '') {
            // $('#lname-error').show();
            $('#lname-error').text("*Fill LastName...!");
            // $('#lname-error').focus();
            lname_error = 0;
            // return 0;
        } else if ((ln.length < 2) || (ln.length > 10)) {
            // $('#lname-error').show();
            $('#lname-error').text("*Last name length must be between 2 to 10...!");
            // $('#lname-error').focus();
            lname_error = 0;
            // return 0;
        } else {
            // $('lname-error').hide();
            $('#lname-error').text("");
            lname_error = 1;
        }
    }


    // username validation
    let uname_error = 1;
    $('#uname').keyup(function () {
        uname_validation();
    });
    function uname_validation() {
        let un = $('#uname').val();
        if (un.length == '') {
            // $('#uname-error').show();
            $('#uname-error').text("*Fill UserName...!");
            // $('#uname-error').focus();
            uname_error = 0;
            // return 0;
        } else if ((un.length < 2) || (un.length > 10)) {
            // $('#uname-error').show();
            $('#uname-error').text("*User name length must be between 2 to 10...!");
            // $('#uname-error').focus();
            uname_error = 0;
            // return 0;
        } else {
            // $('uname-error').hide();
            $('#uname-error').text("");
            uname_error = 1;
        }
    }


    // email validation
    let email_error = 1;
    $('#email').keyup(function () {
        email_validation();
    });
    function email_validation() {
        let email = $('#email').val();
        let i = email.search(/^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/);
        if (email.length == '') {
            // $('#email-error').show();
            $('#email-error').text("*Fill UserName...!");
            // $('#email-error').focus();
            email_error = 0;
            // return 0;
        }
        else if (i < 0) {
            // $('#email-error').show();
            $('#email-error').text("*Enter correct Email ID...!");
            // $('#email-error').focus();
            email_error = 0;
            // return 0;
        }
        else {
            // $('email-error').hide();
            $('#email-error').text("");
            email_error = 1;
        }
    }


    // password validation
    let pswd_error = 1;
    $('#pswd').keyup(function () {
        pswd_validation();
    });
    function pswd_validation() {
        let pswd = $('#pswd').val();
        if (pswd.length == '') {
            // $('#pswd-error').show();
            $('#pswd-error').text("*Fill this...!");
            // $('#pswd-error').focus();
            pswd_error = 0;
            // return 0;
        }
        else if ((pswd.length < 4) || (pswd.length > 25)) {
            // $('#pswd-error').show();
            $('#pswd-error').text("*Password range must be between 4 to 25...!");
            // $('#pswd-error').focus();
            pswd_error = 0;
            // return 0;
        }
        else {
            // $('#pswd-error').hide();
            $('#pswd-error').text("");
            pswd_error = 1;
        }
    }

    // confirm password validation
    let cpswd_error = 1;
    $('#cpswd').keyup(function () {
        cpswd_validation();
    });
    function cpswd_validation() {
        let pswd = $('#pswd').val();
        let cpswd = $('#cpswd').val();
        if (cpswd.length == '') {
            // $('#cpswd-error').show();
            $('#cpswd-error').text("*Fill this...!");
            // $('#cpswd-error').focus();
            cpswd_error = 0;
        }
        else if (cpswd != pswd) {
            // $('#cpswd-error').show();
            $('#cpswd-error').text("*Password not matching...!");
            // $('#cpswd-error').focus();
            cpswd_error = 0;
        }
        else {
            // $('#cpswd-error').hide();
            $('#cpswd-error').text("");
            cpswd_error = 1;
        }
    }

    // Submit
    $('#submit').click(function () {
        fname_validation();
        lname_validation();
        uname_validation();
        email_validation();
        pswd_validation();
        cpswd_validation();

        if ((fname_error == 1) && (lname_error == 1) && (uname_error == 1) && (email_error == 1) && (pswd_error == 1) && (cpswd_error == 1)){
            return true;
        }else {
            alert("Enter correct details...!")
            return false;
        }
    });
});