$(document).ready(function() {

  // global arrays needed to buffer data points across events
  var env_table_data = [];

  // the key event receiver function
  iotSource.onmessage = function(e) {
    // must convert all single quoted data with double quote format
    // console.log(e.data);
    var double_quote_formatted_data = e.data.replace(/'/g, '"');
    // now we can parse into JSON
    // console.log(double_quote_formatted_data);
    parsed_json_data = JSON.parse(double_quote_formatted_data);
    console.log(parsed_json_data);
    updateEnvironmentalTableData(parsed_json_data);
    updateStepperMotor(parsed_json_data);
  }

  // ============================ STEPPER MOTOR ===============================
  // Buttons
  $('#motor_start').click(function() {
    console.log('Start Motor Up!');
    $.get('/motor/1');
  });
  $('#motor_stop').click(function() {
    console.log('Stop Motor');
    $.get('/motor/0');
  });
  $('#motor_zero').click(function() {
    console.log('Zero Motor Position');
    $.get('/motor_zero');
  });
  $('#motor_multistep').click(function() {
    var params = 'steps='+$('#motor_steps').val()+"&direction="+$('#motor_direction').val();
    console.log('Multistep with params:' + params);
    $.post('/motor_multistep', params, function(data, status){
                console.log("Data: " + data + "\nStatus: " + status);
            });
  });

  // Text Fields
  $('#motor_speed').change(function() {
    console.log('Changed motor speed to ' + $('#motor_speed').val());
    $.get('/motor_speed/'+$('#motor_speed').val());
  });
  $('#motor_position').change(function() {
    console.log('Changed motor position to ' + $('#motor_position').val());
    $.get('/motor_position/'+$('#motor_position').val());
  });

  $('#motor_steps').change(function() {
    console.log('Changed motor steps to ' + $('#motor_steps').val());
    $.get('/motor_steps/'+$('#motor_steps').val());
  });

  $('#motor_direction').change(function() {
    console.log('Changed motor steps to ' + $('#motor_direction').val());
    $.get('/motor_direction/'+$('#motor_direction').val());
  });

  // ============================ STEPPER MOTOR ===============================
  function updateStepperMotor(data) {
    $('#motor_position').text(data['motor']['position']);
    if (data['motor']['state'] === '1') {
      $('#motor_state').toggleClass('label-default', false);
      $('#motor_state').toggleClass('label-success', true);
    } else if (data['motor']['state'] === '0') {
      $('#motor_state').toggleClass('label-default', true);
      $('#motor_state').toggleClass('label-success', false);
    }
  }
  // ============================ STEPPER MOTOR ===============================

  // ============================ DATE FUNCTIONS ==============================
  // previous lab
  function zeropad(num, size) {
      var s = "000000000" + num;
      return s.substr(s.length-size);
  }

  function getDateNow() {
    var d = new Date();
    var date = (d.getFullYear()) + '-' + d.getMonth() + 1 + '-' + d.getDate();
    var time = zeropad(d.getHours(),2) + ':' + zeropad(d.getMinutes(),2) +
    ':' + zeropad(d.getSeconds(),2) + '.' + zeropad(d.getMilliseconds(),3);
    return {time: time, date: (date + " " + time)};
  }
  // ============================ DATE FUNCTIONS ==============================

  // ============================== ENV TABLE =================================
  updateEnvironmentalTableData = (function (d) {
    var env = d;
    var timedata = getDateNow();
    env['date'] = timedata.date;
    env['time'] = timedata.time;

    env_table_data.push(env);
    if (env_table_data.length > 4) {
      env_table_data.shift();
      clearEnvTables();
      updateEnvironmentalTable(env_table_data);
    }
  });

  function updateEnvironmentalTable(data) {
    $('tr.env-param-row').each(function(i) {
      var tm = '<td>' + data[i].date + '</td>';
      var t = '<td>' + data[i]['environmental']['temperature'].reading.toFixed(2) + '</td>';
      var p = '<td>' + data[i]['environmental']['pressure'].reading.toFixed(2) + '</td>';
      $(this).append(tm);
      $(this).append(t);
      $(this).append(p);
    });
  }
  function clearEnvTables() {
    $('tr.env-param-row').each(function(i) {
      $(this).empty();
    });
  }
  // ============================== ENV TABLE =================================

  // Renders the jQuery-ui elements
  $("#tabs").tabs();

  // ===================================================================
  // RED LED SLIDER
  $( "#slider1" ).slider({
    orientation: "vertical",
    range: "min",
    min: 0,
    max: 100,
    value: 50,
    animate: true,
    slide: function( event, ui ) {
      $( "#pwm1" ).val( ui.value );
      console.log("red led duty cycle(%):",ui.value);
    }
  });
  $( "#pwm1" ).val( $( "#slider1" ).slider( "value" ) );
  // ... add code to control PWM driver for hardware ...
  // ===================================================================
  // GREEN LED SLIDER
  $( "#slider2" ).slider({
    orientation: "vertical",
    range: "min",
    min: 0,
    max: 100,
    value: 50,
    animate: true,
    slide: function( event, ui ) {
      $( "#pwm2" ).val( ui.value );
      console.log("grn led duty cycle(%):",ui.value);
    }
  });
  $( "#pwm2" ).val( $( "#slider2" ).slider( "value" ) );
  // ... add code to control PWM driver for hardware ...
  // ===================================================================



});
