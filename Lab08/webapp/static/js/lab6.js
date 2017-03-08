$(document).ready(function() {

  // the key event receiver function
  iotSource.onmessage = function(e) {
    // must convert all single quoted data with double quote format
    var double_quote_formatted_data = e.data.replace(/'/g, '"');
    // now we can parse into JSON
    parsed_json_data = JSON.parse(double_quote_formatted_data);
    // console.log(parsed_json_data);

    updateEnvironmentalTableData(parsed_json_data);
    updateInertialTableData(parsed_json_data);
    updateInertialChartData(parsed_json_data);
    updateEnvChartData(parsed_json_data);
    // update Imu Chart Data
    // update Joystick Data
    // update Dislay Data
  }

  // global arrays needed to buffer data points across events
  var env_table_data = [];
  var env_chart_data  = [];
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
      var t = '<td>' + data[i]['environmental']['temperature'].value.toFixed(2) + '</td>';
      var p = '<td>' + data[i]['environmental']['pressure'].value.toFixed(2) + '</td>';
      var h = '<td>' + data[i]['environmental']['humidity'].value.toFixed(2) + '</td>';
      $(this).append(tm);
      $(this).append(t);
      $(this).append(p);
      $(this).append(h);
    });
  }
  // ============================== ENV TABLE =================================

  // ============================ INERTIAL TABLE ==============================
  updateInertialTableData = (function (d) {
    var imu = d;
    var timedata = getDateNow();
    imu['date'] = timedata.date;
    imu['time'] = timedata.time;

    imu_table_data.push(imu);
    if (imu_table_data.length > 4) {
      imu_table_data.shift();
      clearImuTables();
      updateInertialTable(imu_table_data);
    }
  });

  function updateInertialTable(data) {
    $('tr.imu-param-row').each(function(i) {
      var datetime = '<td>' + data[i]['date'] + '</td>';
      var accelx   = '<td>' + data[i]['inertial']['accelerometer']['x'].toFixed(2) + '</td>';
      var accely   = '<td>' + data[i]['inertial']['accelerometer']['y'].toFixed(2) + '</td>';
      var accelz   = '<td>' + data[i]['inertial']['accelerometer']['z'].toFixed(2) + '</td>';
      var pitch    = '<td>' + data[i]['inertial']['orientation']['pitch'].toFixed(1) + '</td>';
      var roll     = '<td>' + data[i]['inertial']['orientation']['roll'].toFixed(1) + '</td>';
      var yaw      = '<td>' + data[i]['inertial']['orientation']['yaw'].toFixed(1) + '</td>';
      var compass  = '<td>' + data[i]['inertial']['orientation']['compass'].toFixed(0) + '</td>';
      $(this).append(datetime);
      $(this).append(accelx);
      $(this).append(accely);
      $(this).append(accelz);
      $(this).append(pitch);
      $(this).append(roll);
      $(this).append(yaw);
      $(this).append(compass);
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

  // ============================== ENV CHART ================================
  // initialize the accel chart structure
  var env_chart = new Morris.Line({
    element: 'env-chart',
    data: [
    ],
    xkey: 'time',
    ykeys: ['h'],
    labels: ['%RH']
  });

  // build the chart data from the JavaScript sensor object data
  updateEnvChartData = (function (data) {
    var env = data
    var timedata = getDateNow()
    env['date'] = timedata.date;
    env['time'] = timedata.time;

    env_chart_data.push(env);
    if (env_chart_data.length > 16) {
      env_chart_data.shift()
    }
    update_env_chart(env_chart_data);
  });

  // build the environmental chart data array for MorrisJS structure
  function update_env_chart(data) {
    var chart_data = [];
    data.forEach(function(d){
      env_record = {
        time: d['date'],
        h: d['environmental']['humidity'].value.toFixed(2)
      };
      // console.log(i,accel_record);
      // i += 1;
      chart_data.push(env_record);
    });
    env_chart.setData(chart_data);
  };
  // ============================== ENV CHART ================================

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
    var imu = data
    var timedata = getDateNow()
    imu['date'] = timedata.date;
    imu['time'] = timedata.time;

    imu_chart_data.push(imu);
    if (imu_chart_data.length > 16) {
      imu_chart_data.shift()
    }
    update_accel_chart(imu_chart_data);
  });

  // build the chart data array for MorrisJS structure
  function update_accel_chart(data) {
    var chart_data = [];
    // var i = 0;
    data.forEach(function(d){
      accel_record = {
        time: d['date'],
        x: d['inertial']['accelerometer']['x'].toFixed(2),
        y: d['inertial']['accelerometer']['y'].toFixed(2),
        z: d['inertial']['accelerometer']['z'].toFixed(2)
      };
      chart_data.push(accel_record);
    });
    accel_chart.setData(chart_data);
  };
  // ============================== ACCEL CHART ================================
});
