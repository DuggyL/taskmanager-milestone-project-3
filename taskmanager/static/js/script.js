$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('.collapsible').collapsible();
    $(".tooltipped").tooltip();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: "dd mmmm yyyy",
        yearRange: 1,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });

    var elem = document.querySelector('.collapsible.expandable');
    var instance = M.Collapsible.init(elem, {
    accordion: false
    });