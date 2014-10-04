/** @jsx React.DOM */
var SheetPart = React.createClass({
    render: function () {
        console.log("RAWR2");
        return <p>HI!</p>;
    }
});
console.log("RAWR");
React.renderComponent(SheetPart,document.getElementById('sheet'));