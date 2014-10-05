// What element we will populate when a selection is made in the spreadsheet
var SELECT_TARGET = null;

function unset_select_target() {
    $('[data-select-target]').removeClass('select-active');
    SELECT_TARGET = null;
}
function set_select_target(new_target) {
    $('[data-select-target]').removeClass('select-active');
    $('[data-select-target="' + new_target + '"]').addClass('select-active');
    SELECT_TARGET = '#' + new_target;
}

$(document).on('click', function(e) {
    var $target = $(e.target);

    if ($target.attr('data-select-target')) {
        set_select_target($target.attr('data-select-target'));
    }
    else {
        unset_select_target();
    }
});

// make the spreadsheet smaller
// take tabindex off the table


// Backbone stuff
var Column = Backbone.Model.extend({});

var ColumnView = Backbone.View.extend({
    events: {
        'click .remove': 'remove',
        'focus input': 'select_target',
    },
    render: function() {
        this.$el.html(_.template(COLUMN_VIEW_TPL, {model: this.model}));
    },
    select_target: function(e) {
        set_select_target($(e.target).attr('data-select-target'));
    },
});

var ColumnList = Backbone.Collection.extend({
    model: Column,
});




// Initialise the backbone stuff
var columnList = new ColumnList();
var columnListView = new Backbone.CollectionView({
    el: $('table#column-table'),
    collection: columnList,
    modelView: ColumnView,
    selectable: false,
    clickToSelect: false,
});


$('#add-series').on('click', function() {
    columnList.add({});
});

columnListView.render();


// Spreadsheet stuff
function load_spreadsheet(spread) {
    var s_no = 0;
    _.each([SHEET_DATA[0]], function(s) {
        var sheet = spread.getSheet(s_no);
        sheet.isPaintSuspended(true);

        var row = 0;
        _.map(s, function(column_data) {
            var col = 0;

            _.each(column_data, function(cell_data) {
                sheet.setText(row, col, cell_data);
                col++;
            });


            row++;
        });

        sheet.isPaintSuspended(false);

        s_no++;

    });
}

function toCellName(row, col) {
    return String.fromCharCode(col + 65) + (row + 1);
}

$('.add-series').on('submit', function() {
    var column_data = [];
    
    columnList.forEach(function(column) {
        column_data.push({ title: $('#input-title-' + column.cid).data('values'), values: $('#input-series-' + column.cid).data('values') });
    });

    $('.add-series').append($('<input type="hidden" name="columns">').val(JSON.stringify(column_data)));
});

$(document).ready(function(){
    $("#ss").wijspread({sheetCount:1}); // create wijspread control
    var spread = $("#ss").wijspread("spread"); // get instance of wijspread control
    load_spreadsheet(spread);

    //var lg_style = new $.wijmo.wijspread.Style();
    //lg_style.backColor = "lightgreen";
    //var sheet = spread.getActiveSheet(); // get active worksheet of the wijspread control
    //sheet.setStyle(0, 0, lg_style, $.wijmo.wijspread.SheetArea.viewport);
   
    function set_value_for_select_target(range, range_values) {
        if (/^[A-Z][0-9]+$/.test(range)) {
            $(SELECT_TARGET).val(range_values);
        }
        else {
            $(SELECT_TARGET).val(range);
        }
        $(SELECT_TARGET).data('values', range_values);
    }

    function get_values_from_range(range) {
        var values = [];
        for (var c = range.col; c <= range.col + range.colCount - 1; c++) {
            for (var r = range.row; r <= range.row + range.rowCount - 1; r++) {
                values.push(spread.getActiveSheet().getCell(r, c).value());
            }
        }
        return values;
    }

    $('#ss').on('click', function(e) {
        //Acquire cell index from mouse-clicked point of regular cells which are neither fixed rows/columns nor row/column headers.
        var offset = $("#ss").offset();
        var x = e.pageX - offset.left;
        var y = e.pageY - offset.top;
        var activeSheet = spread.getActiveSheet();
        var target = activeSheet.hitTest(x, y);

        if(target &&
            (target.rowViewportIndex === 0 || target.rowViewportIndex === 1) &&
            (target.colViewportIndex === 0 || target.colViewportIndex === 1)){
            if (SELECT_TARGET) {
                var selections = activeSheet.getSelections();
                var ranges = selections.toArray();
                var selectedRanges = [];
                _.each(ranges, function(range) {
                    var cellStart = toCellName(range.row, range.col);
                    var cellEnd   = toCellName(range.row + range.rowCount - 1, range.col + range.colCount - 1);
                    selectedRanges.push({start: cellStart, end: cellEnd, values: get_values_from_range(range)});
                });
                if (selectedRanges.length > 1) {
                    $(SELECT_TARGET).val(selectedRanges.join(','));
                    e.stopPropagation();
                }
                else if (selectedRanges.length == 1) {
                    var r = selectedRanges[0];
                    if (r.start == r.end) {
                        var cell_value = activeSheet.getValue(target.row, target.col);
                        if (cell_value) {
                            set_value_for_select_target(r.start, cell_value);
                            e.stopPropagation();
                        }
                        else {
                            // must have clicked elsewhere
                            SELECT_TARGET = null;
                        }
                    }
                    else {
                        set_value_for_select_target(r.start + ':' + r.end, r.values);
                        e.stopPropagation();
                    }
                }
            }
        }
    });
});
