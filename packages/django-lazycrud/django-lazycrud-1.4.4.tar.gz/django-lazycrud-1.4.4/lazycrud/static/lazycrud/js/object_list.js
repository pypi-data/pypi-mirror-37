$(function() {
    $.extend(true, $.fn.dataTable.defaults, {
        oLanguage: {
            sUrl: $('body').data('staticurl') + 'lazycrud/js/dataTables/lang-ita.js'
        }
    });

    $.fn.dataTable.moment('DD/MM/YYYY');
    $.fn.dataTable.moment('DD/MM/YYYY HH:mm');

    $('body').off('mousedown contextmenu', '.clickable_row');
    $('body').on('mousedown', '.clickable_row', function(e) {
        var url = $(this).data('url');
        if ($(this).data('target') == '_blank' || e.button == 2) {
            // data-target="_blank" o click con tasto destro: nuova finestra
            window.open(url);
        } else {
            // qualunque altro tasto: stessa finestra
            window.location.href = url;
        }
    });

    $('.table-datatables').each(function() {
        var dt_options = {};
        if ($(this).data('datatables-options') !== undefined) {
            dt_options = $(this).data('datatables-options');
        }
        $(this).dataTable(dt_options);
    });
});
