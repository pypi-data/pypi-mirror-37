$(function() {
    var datetimepicker_icons = {
        time: "fa fa-clock-o",
        date: "fa fa-calendar",
        previous: "fa fa-chevron-left",
        next: "fa fa-chevron-right",
        up: "fa fa-chevron-circle-up",
        down: "fa fa-chevron-circle-down",
        close: "fa fa-times",
    };

    $('.dateinput').datetimepicker({
        format: 'DD/MM/YYYY',
        icons: datetimepicker_icons,
    });

    $('.timeinput').datetimepicker({
        format: 'HH:mm',
        icons: datetimepicker_icons,
        stepping: 15,
    });

    $('.datetimeinput').datetimepicker({
        locale: 'it',
        icons: datetimepicker_icons,
        stepping: 15,
        showClose: true,
    });
});
