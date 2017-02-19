$(document).ready(function() {
var led1;
var led2;
var led3;

// var iotSource = new EventSource("{{ url_for('myData') }}");

iotSource.onmessage = function(e) {
  // must convert all single quoted data with double quote format
  var dqf = e.data.replace(/'/g, '"');
  // now we can parse into JSON
  d = JSON.parse(dqf);
  updateSwitch(d["switch"]);
  updateLeds(1, d["led_red"]);
  updateLeds(2, d["led_grn"]);
  updateLeds(3, d["led_blu"]);
  updateSensors(d);
  console.log(d);
}

// update the Switch based on its SSE state monitor
function updateSwitch(switchValue) {
  if (switchValue === '1') {
    // $('#switch').text(9759);
    $('#switch').toggleClass( 'label-default', false);
    $('#switch').toggleClass( 'label-success', true);
  } else if (switchValue === '0') {
    // $('#switch').text('OFF');
    $('#switch').toggleClass( 'label-default', true);
    $('#switch').toggleClass( 'label-success', false);
  }
}

// update the LEDs based on their SSE state monitor
function updateLeds(ledNum,ledValue) {
  if (ledNum === 1) {
    if (ledValue === '1') {
      $('#red_led_label').toggleClass( 'label-default', false);
      $('#red_led_label').toggleClass( 'label-danger', true);
      led1 = "ON"
    } else if (ledValue === '0') {
      $('#red_led_label').toggleClass( 'label-default', true);
      $('#red_led_label').toggleClass( 'label-danger', false);
      led1 = "OFF"
    }
  }
  else if (ledNum === 2) {
    if (ledValue === '1') {
      $('#grn_led_label').toggleClass( 'label-default', false);
      $('#grn_led_label').toggleClass( 'label-success', true);
      led2 = "ON"
    } else if (ledValue === '0') {
      $('#grn_led_label').toggleClass( 'label-default', true);
      $('#grn_led_label').toggleClass( 'label-success', false);
      led2 = "OFF"
    }
  }
  else if (ledNum === 3) {
    if (ledValue === '1') {
      $('#blu_led_label').toggleClass( 'label-default', false);
      $('#blu_led_label').toggleClass( 'label-primary', true);
      led3 = "ON"
    } else if (ledValue === '0') {
      $('#blu_led_label').toggleClass( 'label-default', true);
      $('#blu_led_label').toggleClass( 'label-primary', false);
      led3 = "OFF"
    }
  }
}

// The button click functions run asynchronously in the browser
$('#red_led_btn').click(function() {
  if (led1 === "OFF") {led1 = "ON";} else {led1 = "OFF";}
  var params = 'led=1&state='+led1;
  console.log('Led Command with params:' + params);
  $.post('/ledcmd', params, function(data, status){
          console.log("Data: " + data + "\nStatus: " + status);
  });
});

// The button click functions run asynchronously in the browser
$('#grn_led_btn').click(function() {
  if (led2 === "OFF") {led2 = "ON";} else {led2 = "OFF";}
  var params = 'led=2&state='+led2;
  console.log('Led Command with params:' + params);
  $.post('/ledcmd', params, function(data, status){
          console.log("Data: " + data + "\nStatus: " + status);
  });
});
// The button click functions run asynchronously in the browser
$('#blu_led_btn').click(function() {
  if (led3 === "OFF") {led3 = "ON";} else {led3 = "OFF";}
  var params = 'led=3&state='+led3;
  console.log('Led Command with params:' + params);
  $.post('/ledcmd', params, function(data, status){
          console.log("Data: " + data + "\nStatus: " + status);
  });
});



MBAR_TO_inHG = 0.029529983071;
var data = [];

// from http://stackoverflow.com/questions/2998784/how-to-output-integers-with-leading-zeros-in-javascript
function zeropad(num, size) {
    var s = "000000000" + num;
    return s.substr(s.length-size);
}

function getDateNow() {
  var d = new Date();
  var date = (d.getFullYear()) + '-' + d.getMonth() + 1 + '-' + d.getDate();
  var time = zeropad(d.getHours(),2) + ':' + zeropad(d.getMinutes(),2) + ':' + zeropad(d.getSeconds(),2);
  return {epoch: time, date: (date + " " + time)};
}

updateSensors = (function (d) {
  var t_c = d['temperature'].reading
  var p_mbar = d['pressure'].reading
  var t_f = (t_c * 9) / 5.0 + 32.0;
  var p_inHg = p_mbar * MBAR_TO_inHG;

  var timedata = getDateNow();
  var t =  t_c.toFixed(1) + ' | ' + t_f.toFixed(1);
  var p =  p_mbar.toFixed(1) + ' | ' + p_inHg.toFixed(2);

  var obj = {};
  obj['date'] = timedata.date;
  obj['time'] = timedata.date;
  obj['temp'] = t;
  obj['press'] = p;
  data.push(obj);

  console.log(timedata);
  if (data.length > 5) {
    data.shift();
    clearTable();
    updateTable(data);
    update_temp_chart(data);
  }
});

function updateTable(data) {
  $('tr.param-row').each(function(i) {
    var tm = '<td>' + data[i]['date'] + '</td>';
    var temp = '<td>' + data[i]['temp'] + '</td>';
    var press = '<td>' + data[i]['press'] + '</td>';
    $(this).append(tm);
    $(this).append(temp);
    $(this).append(press);
  });
}

function clearTable() {
  $('tr.param-row').each(function(i) {
    $(this).empty();
  });
}

var graph = new Morris.Line({
  element: 'mytempchart',
  data: [
    // { time: '00:00:01', value: 0 },
    // { time: '00:00:02', value: 0 },
    // { time: '00:00:03', value: 0 },
    // { time: '00:00:04', value: 0 },
    // { time: '00:00:05', value: 0 }
  ],
  xkey: 'time',
  ykeys: ['value'],
  labels: ['Value']
});

function update_temp_chart(data) {
  var chart_data = [
    { time: data[0]['time'], value: data[0]['temp'] },
    { time: data[1]['time'], value: data[1]['temp'] },
    { time: data[2]['time'], value: data[2]['temp'] },
    { time: data[3]['time'], value: data[3]['temp'] },
    { time: data[4]['time'], value: data[4]['temp'] }
  ];
  graph.setData(chart_data);
}

});
