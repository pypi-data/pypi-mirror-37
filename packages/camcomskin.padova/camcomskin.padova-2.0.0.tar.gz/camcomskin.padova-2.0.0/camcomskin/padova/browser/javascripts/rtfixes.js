/********************************************/
/* RedTurtle fixes for Bootstrap validation */
/********************************************/

$(document).ready( function() {
  // alternative to "-webkit-min-device-pixel-ratio: 0"
  // Safari, Chrome, Opera >= 14, Android 4.0.4
  var isWebkit = (!!window.chrome) || (/constructor/i.test(window.HTMLElement));
  if(isWebkit) {
    var content = 'input[type="date"].form-control,'+
      'input[type="time"].form-control,'+
      'input[type="datetime-local"].form-control,'+
      'input[type="month"].form-control {'+
        'line-height: 34px;'+
      '}'+
      'input[type="date"].input-sm,'+
      'input[type="time"].input-sm,'+
      'input[type="datetime-local"].input-sm,'+
      'input[type="month"].input-sm,'+
      '.input-group-sm input[type="date"],'+
      '.input-group-sm input[type="time"],'+
      '.input-group-sm input[type="datetime-local"],'+
      '.input-group-sm input[type="month"] {'+
        'line-height: 30px;'+
      '}'+
      'input[type="date"].input-lg,'+
      'input[type="time"].input-lg,'+
      'input[type="datetime-local"].input-lg,'+
      'input[type="month"].input-lg,'+
      '.input-group-lg input[type="date"],'+
      '.input-group-lg input[type="time"],'+
      '.input-group-lg input[type="datetime-local"],'+
      '.input-group-lg input[type="month"] {'+
        'line-height: 46px;'+
      '}';
    $('head').append('<style>'+content+'</style>');
  }

  // alternative to \9 hack for IE9
  var isIE9 = document.all && document.addEventListener && !window.atob;
  if(isIE9) {
    var content = 'input[type="radio"],'+
      'input[type="checkbox"] {'+
        'margin-top: 1px;'+
      '}'+
      '.radio input[type="radio"],'+
      '.radio-inline input[type="radio"],'+
      '.checkbox input[type="checkbox"],'+
      '.checkbox-inline input[type="checkbox"] {'+
        'margin-top: 4px;'+
      '}';
    $('head').append('<style>'+content+'</style>');
  }
});
