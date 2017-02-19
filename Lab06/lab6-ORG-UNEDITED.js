$(document).ready(function() {

  // the key event receiver function
  iotSource.onmessage = function(e) {
    // must convert all single quoted data with double quote format
    var double_quote_formatted_data = e.data.replace(/'/g, '"');
    // now we can parse into JSON
    parsed_json_data = JSON.parse(double_quote_formatted_data);
    // console.log(parsed_json_data);

    // update Env Table Data
    // update Env Chart Data
    // update Imu Table Data
    // update Imu Chart Data
    // update Joystick Data
    // update Dislay Data
  }

  // global arrays needed to buffer data points across events
  var env_table_data = [];
  var env_temp_data  = [];
  var imu_table_data = [];
  var imu_chart_data = [];

  // ============================ DATE FUNCTIONS ==============================
  // from http://stackoverflow.com/questions/2998784/how-to-output-integers-with-leading-zeros-in-javascript
  function zeropad(num, size) {
      var s = "000000000" + num;
      return s.substr(s.length-size);
  }

  function getDateNow() {
    var d = new Date();
    var date = (d.getFullYear()) + '-' + d.getMonth() + 1 + '-' + d.getDate();
    var time = zeropad(d.getHours(),2) + ':' + zeropad(d.getMinutes(),2) + ':' + zeropad(d.getSeconds(),2);
    return {time: time, date: (date + " " + time)};
  }
  // ============================ DATE FUNCTIONS ==============================

  // ============================== ENV TABLE =================================
  updateEnvironmentalTableData = (function (d) {
    // ... update the Env table data ...
  });

  function updateEnvironmentalTable(data) {
    $('tr.env-param-row').each(function(i) {
      // ... update Environmental table data ...
    });
  }
  // ============================== ENV TABLE =================================

  // ============================ INERTIAL TABLE ==============================
  updateInertialTableData = (function (d) {
    // ... update the Imu table data ...
  });

  function updateInertialTable(data) {
    $('tr.imu-param-row').each(function(i) {
      // ... code to update the inertial table ...
    });
  }
  // ============================ INERTIAL TABLE ==============================

  function clearEnvTables() {
    $('tr.env-param-row').each(function(i) {
      $(this).empty();
      // console.log("Env",i);
    });
  }

  function clearImuTables() {
    $('tr.imu-param-row').each(function(i) {
      $(this).empty();
      // console.log("Imu",i);
    });
  }

  // ============================== ACCEL CHART ================================
  // initialize the accel chart structure
  var accel_chart = new Morris.Line({
    element: 'accel-chart',
    data: [
    ],
    xkey: 'time',
    ykeys: ['x','y','z'],
    labels: ['Accel-X','Accel-Y','Accel-Z']
  });

  // build the chart data from the JavaScript sensor object data
  updateInertialChartData = (function (data) {

    // ... code for building chart data ...

  });

  // build the chart data array for MorrisJS structure
  function update_accel_chart(data) {
    var chart_data = [];

    // ... code to populate chart_data array ...

    accel_chart.setData(chart_data);
  };
  // ============================== ACCEL CHART ================================
});
