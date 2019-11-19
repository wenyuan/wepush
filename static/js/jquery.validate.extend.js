// 自定义jquert-validate验证方法
// name:自定义方法的名称，method：函数体, message:错误消息
$(function () {
    // 用户名验证
    $.validator.addMethod("regUsername", function (value, element, param) {
        return new RegExp(/^[a-zA-Z_][a-zA-Z0-9_]{4,16}$/).test(value);
    }, "用户名只能为字母数字和下划线,且不能以数字开头");
    // 密码验证
    $.validator.addMethod("regPassword", function (value, element, param) {
        return new RegExp(/^(?![^A-Za-z]+$)(?![^0-9]+$)[\x21-\x7e]{6,16}$/).test(value);
    }, "密码长度在6~16位，必须同时包含字母和数字，可以有特殊符号");
    // 字符串是否为空格验证
    $.validator.addMethod("notBlankStr", function (value, element, param) {
        return value.trim().length !== 0;
    }, "不能全为空格");
    // 字符串是否为JSON格式
    $.validator.addMethod("isJsonStr", function (value, element, param) {
        if (typeof value !== 'string') {
            return false
        }
        try {
            var obj = JSON.parse(value);
            return obj && typeof obj === "object" && isNaN(obj.length)
        }
        catch (e) {
            return false;
        }
    }, "参数格式错误，必须是JSON格式的字符串");
});
