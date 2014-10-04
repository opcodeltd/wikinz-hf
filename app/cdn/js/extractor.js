// What element we will populate when a selection is made in the spreadsheet
var SELECT_TARGET = null;

$(document).on('click', function(e) {
    var $target = $(e.target);
    $('[data-select-target]').removeClass('select-active');

    if ($target.attr('data-select-target')) {
        var select_target = $target.attr('data-select-target');
        $('[data-select-target="' + select_target + '"]').addClass('select-active');
        SELECT_TARGET = '#' + select_target;
    }
    else {
        SELECT_TARGET = null;
    }
});


// Backbone stuff
var Column = Backbone.Model.extend({});

var ColumnView = Backbone.View.extend({
    events: {
        'click .remove': 'remove',
    },
    render: function() {
        this.$el.html(_.template(COLUMN_VIEW_TPL, {model: this.model}));
    },
});

var ColumnList = Backbone.Collection.extend({
    model: Column,
    initialize: function() {
    },
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


columnList.add(new Column({series: 'A2:A10', title: 'A1'}));

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

$(document).ready(function(){
    $("#ss").wijspread({sheetCount:1}); // create wijspread control
    var spread = $("#ss").wijspread("spread"); // get instance of wijspread control
    load_spreadsheet(spread);

    //var lg_style = new $.wijmo.wijspread.Style();
    //lg_style.backColor = "lightgreen";
    //var sheet = spread.getActiveSheet(); // get active worksheet of the wijspread control
    //sheet.setStyle(0, 0, lg_style, $.wijmo.wijspread.SheetArea.viewport);

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
                var ranges = activeSheet.getSelections().toArray();
                var selectedRanges = [];
                _.each(ranges, function(range) {
                    var cellStart = toCellName(range.row, range.col);
                    var cellEnd   = toCellName(range.row + range.rowCount - 1, range.col + range.colCount - 1);
                    selectedRanges.push({start: cellStart, end: cellEnd});
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
                            $(SELECT_TARGET).val(cell_value);
                            e.stopPropagation();
                        }
                        else {
                            // must have clicked elsewhere
                            SELECT_TARGET = null;
                        }
                    }
                    else {
                        $(SELECT_TARGET).val(r.start + ':' + r.end);
                        e.stopPropagation();
                    }
                }
            }
        }
    });
});
