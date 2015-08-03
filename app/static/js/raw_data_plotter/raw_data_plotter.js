/**
 * Created by rezwan on 19/07/15.
 * http://angular-ui.github.io/bootstrap/
 */

/*
 sensor_id = int. must be sent
 start_date = json date, use in case of single date or month case, must be sent
 end_date = json date, optional, for range cases

 Must send by_month or by_date
 by_month = bool, optional, for plots with months
 by_date = bool, optional, for plots with dates

 Must send one of following
 by_timestamp = bool, optional, for 24hr cases
 show_individual_date_or_month = bool, optional, for single point multiple dates or months
 * */
var app = angular.module('myApp', ['ui.bootstrap', "chart.js"]);
// http://jtblin.github.io/angular-chart.js/#getting_started
//http://angular-ui.github.io/bootstrap/
app.controller('myCtrl', function ($scope, $http, $window) {


    $scope.labels = [''];
    $scope.series = [''];


    $scope.data = [
        []
    ]; //list of list

    //$scope.labels = ['0:00','0:10','0:20'];//X
    //$scope.series = [1.2,1.3,1.4];//Series name
    //$scope.data = [ ]; //Y

    //ui panel for ng-show
    $scope.show_step_1 = true;
    $scope.show_step_2 = false;
    $scope.show_step_3 = false;
    $scope.show_step_4 = false;
    $scope.show_step_5 = false;
    $scope.show_button = false;
    $scope.show_plot = false;
    $scope.alerts = [];
    //for flask
    $scope.by_date = false;
    $scope.by_month = false;
    $scope.enable_start_date = false;
    $scope.enable_end_date = false;
    $scope.start_date = null;
    $scope.end_date = null;
    $scope.by_timestamp = false;
    $scope.show_individual_date_or_month = false;
    $scope.sensor = {};

    //for ng-functions
    $scope.min_date = {};
    $scope.max_date = {};
    $scope.show_start_date_calendar = false;
    $scope.show_end_date_calendar = false;

    $scope.sensor_id_from_step_2 = null;
    $scope.logger_list = [];
    $scope.data_list = [];
    $scope.sensor_list = [];

    $scope.dateOptions_month = {
        'year-format': "yyyy",
        'starting-day': 1,
        'datepicker-mode': "'month'",
        'min-mode': "month",
        'showWeeks': "false",
         'close-on-date-selection': "true"
    };

    $scope.dateOptions_day = {
        'year-format': "yyyy",
        'starting-day': 1,
        'datepicker-mode': "'day'",
        'min-mode': "day",
        'showWeeks': "false",
        'close-on-date-selection': "true"
    };


    $scope.msg = "Debugging";
    $scope.reset_controller_variables = function () {
        $scope.init_logger();
        //ui panel for ng-show
        $scope.show_step_1 = true;
        $scope.show_step_2 = false;
        $scope.show_step_3 = false;
        $scope.show_step_4 = false;
        $scope.show_step_5 = false;
        $scope.show_button = false;
        $scope.show_plot = false;
        $scope.alerts = [];
        //for flask
        $scope.by_date = false;
        $scope.by_month = false;
        $scope.enable_start_date = false;
        $scope.enable_end_date = false;
        $scope.start_date = null;
        $scope.end_date = null;
        $scope.sensor = {};
        $scope.by_timestamp = false;
        $scope.show_individual_date_or_month = false;

        //for ng-functions
        $scope.min_date = {};
        $scope.max_date = {};
        $scope.show_start_date_calendar = false;
        $scope.show_end_date_calendar = false;

        $scope.sensor_id_from_step_2 = null;
        $scope.logger_list = [];
        $scope.data_list = [];
        $scope.sensor_list = [];

        //for chart
        $scope.labels = [];//X
        $scope.series = [];//Series name
        $scope.data = [ ]; //Y
    };

   /* sensor_id = int. must be sent
 start_date = json date, use in case of single date or month case, must be sent
 end_date = json date, optional, for range cases

 Must send by_month or by_date
 by_month = bool, optional, for plots with months
 by_date = bool, optional, for plots with dates

 Must send one of following
 by_timestamp = bool, optional, for 24hr cases
 show_individual_date_or_month = bool, optional, for single point multiple dates or months
    * */
    $scope.send_query = function () //Testing query string params for get and data for post
    {
        $http
            .get('ngQueries', {params:
            {
                sensor_id: $scope.sensor.id,
                start_date: $scope.start_date,
                end_date: $scope.end_date,
                by_month: $scope.by_month,
                by_date: $scope.by_date,
                by_timestamp: $scope.by_timestamp,
                show_individual_date_or_month: $scope.show_individual_date_or_month
            }
            })
            .success(function (data, status, headers, config) {
                if (data.success) {

                    $scope.data_list = data.plot_data;
                    $scope.process_plot_data(data);
                    //$scope.get_sensor_list( $scope.logger_list[0].logger.id)
                    //$scope.msg = 'Loaded dataList' + " " + data.plot_data.length;
                } else {
                    $window.alert('Retrieval failed 22');
                }
            })
            .error(function (data, status, headers, config) {
                $window.alert('Retrieval failed');
            });

    };
    $scope.process_plot_data=function(data)
    {
         $scope.msg = 'Loaded dataList' + " " + data.plot_data.length;
        //var count =0;
        var temp_X = [];
        var temp_Y = [];
        var display = '';
        $scope.labels=[];
        $scope.data = [];
        $scope.series=[];
        for (var i=0;i<data.plot_data.length;i++)
        {
            //display = display + " "+ data.plot_data[i].Y.ch_avg;
            temp_X.push(data.plot_data[i].X);
            temp_Y.push(parseFloat(data.plot_data[i].Y.ch_avg));
        }


        //$scope.msg = display;
        //{
        //   temp_X.push(data.plot_data[i].X);
        //    //console.log(item.X);
        //    temp_Y.push(data.plot_data[i].Y.ch_avg);
        //    count = count+1;
        //    //$scope.data.push(item.Y.ch_avg);
        //}
        $scope.labels.push.apply($scope.labels,temp_X);

        $scope.data = new Array(1);
        $scope.data[0] = new Array(temp_Y.length);
        //$scope.data[0].push(temp_Y);
        $scope.legend = true;
        //$scope.options ={
        //    'scaleShowLabels': 'false',
        //    'tooltipFontSize': '20'
        //
        //};
        for(var j = 0; j<temp_Y.length;j++)
        {
            $scope.data[0][j] = temp_Y[j];
        }

        $scope.series.push(data.y_label);
        //display ='';
        //for (var i = 0; i<labels.length;i++)
        //{
        //     display = display + " label = "+ $scope.labels[i] +" data = "+ $scope.data[i];
        //}
    //     $scope.labels = ['0:00','0:10','0:20'];
    //$scope.series = ['Series A','Series B'];
    //
    //
    //$scope.data = [
    //    [1.2,1.3,1.4],
    //    [1.2,10.3,2.4]
    //];
        $scope.show_plot = true;
    };
    $scope.init_logger = function () {
        $scope.msg = "inside send to loggerlist";
        $http
            .get('getLoggers')
            .success(function (data, status, headers, config) {
                if (data.success) {

                    $scope.logger_list = data.loggerList;
                    //$scope.get_sensor_list( $scope.logger_list[0].logger.id)
                    $scope.msg = 'Loaded loggerList' + " " + $scope.logger_list.length;
                } else {
                    $window.alert('Retrieval failed 22');
                }
            })
            .error(function (data, status, headers, config) {
                $window.alert('Retrieval failed');
            });
    };
    $scope.init_logger();


    $scope.get_sensor_list = function (logger_id) {
        //step 1
        $scope.show_step_2 = false;
        $scope.show_step_3 = false;
        $scope.show_step_4 = false;
        $scope.show_step_5 = false;
        $scope.show_button = false;
        $scope.show_plot = false;
        $scope.msg = "inside send to sensorlist";
        $http
            .get('getSensors/' + logger_id)
            .success(function (data, status, headers, config) {
                if (data.success) {

                    $scope.sensor_list = data.sensorList;

                    $scope.msg = 'Loaded sensorList' + " " + $scope.sensor_list.length;
                    $scope.show_step_2 = true;
                } else {
                    $window.alert('Retrieval failed 22');
                }
            })
            .error(function (data, status, headers, config) {
                $window.alert('Retrieval failed');
            });
    };

    $scope.get_sensor_details = function (sensor_select_value) {
        //step 2
        $scope.show_step_3 = false;
        $scope.show_step_4 = false;
        $scope.show_step_5 = false;
        $scope.show_button = false;
        $scope.show_plot = false;
        $scope.sensor_id_from_step_2 = sensor_select_value;
        $scope.msg = 'Id of the selected sensor ' + $scope.sensor_id_from_step_2;

        $http
            .get('getSensorDetails/' + $scope.sensor_id_from_step_2)
            .success(function (data, status, headers, config) {
                if (data.success) {

                    $scope.sensor = data.sensor;
                    //$scope.get_sensor_list( $scope.logger_list[0].logger.id)
                    $scope.msg = 'Loaded Sensor details' + " " + $scope.sensor.id;
                    $scope.sensor_id_from_step_2 = $scope.sensor.id;
                    $scope.get_maximum_minimum_dates_of_available_data($scope.sensor.id);
                    $scope.show_step_3 = true;
                } else {
                    $window.alert('Retrieval failed 22');
                }
            })
            .error(function (data, status, headers, config) {
                $scope.sensor_id_from_step_2 = null;
                $window.alert('Retrieval failed');
            });

    };
    $scope.option_month_or_date = function (option) {
        //step 3a
        $scope.show_step_4 = false;
        $scope.show_step_5 = false;
        $scope.show_button = false;
        $scope.show_plot = false;
        $scope.enable_start_date = false;
        $scope.enable_end_date = false;
        $scope.end_date = null;
        $scope.start_date = null;
        if (option.valueOf() == 'by_date') {
            $scope.by_date = true;
            $scope.by_month = false;
            //$scope.dateOptions = $scope.dateOptions_day;
            // $scope.show_step_4 = true;
        }
        else if (option.valueOf() == 'by_month') {
            $scope.by_date = false;
            $scope.by_month = true;
            //$scope.dateOptions = $scope.dateOptions_month;
            //$scope.show_step_4 = true;
        }
        else {
            $scope.by_date = false;
            $scope.by_month = false;
        }
    };

    $scope.option_single_or_range = function (option) {
        $scope.show_step_4 = false;
        $scope.show_step_5 = false;
        $scope.show_button = false;
        $scope.show_plot = false;
        $scope.show_start_date_calendar = false;
        $scope.show_end_date_calendar = false;
        $scope.end_date_ui = null;
        $scope.start_date_ui = null;
        //  $scope.enable_start_date = false;
        //$scope.enable_end_date = false;
        //after step 3b
        if (option.valueOf() == 'single') {
            //set up calendar
            $scope.msg = 'got single';
            $scope.show_start_date_calendar = true;
            $scope.show_end_date_calendar = false;
            $scope.end_date = null;
            $scope.start_date = null;
            $scope.show_step_4 = true;
        }
        else if (option.valueOf() == 'range') {
            //set up calendar
            $scope.msg = 'got range';
            $scope.show_start_date_calendar = true;
            $scope.show_end_date_calendar = true;
            $scope.end_date = null;
            $scope.start_date = null;
            $scope.show_step_4 = true;
        }
        else {
            $scope.msg = 'got' + option;
            $scope.show_start_date_calendar = false;
            $scope.show_end_date_calendar = false;
            $scope.end_date = null;
            $scope.start_date = null;
            $scope.show_step_4 = false;
        }
    };

    $scope.get_maximum_minimum_dates_of_available_data = function (sensor_id) {
        $http
            .get('getAvailableDates/' + sensor_id)
            .success(function (data, status, headers, config) {
                if (data.success) {

                    $scope.min_date = new Date(data.min_date);
                    $scope.max_date = new Date(data.max_date);
                    //$scope.get_sensor_list( $scope.logger_list[0].logger.id)
                    $scope.msg = 'got min date' + " " + $scope.min_date + " and max Date " + $scope.max_date;
                    $scope.minDate = $scope.min_date;
                    $scope.maxDate = $scope.max_date;

                    $scope.show_step_3 = true;
                } else {
                    $window.alert('Retrieval failed 22');
                }
            })
            .error(function (data, status, headers, config) {
                $window.alert('Retrieval failed');
            });
    };
    /////////////////////angular ui date picker functions//////////////////////////


    $scope.update_end_date = function (end_date_ui) {
        var temp_date = new Date(end_date_ui);

        //tried suggested action but did not work https://github.com/angular-ui/bootstrap/issues/2628
        temp_date.setMinutes(1440); //this is a hard code...date picker always lags one day

        $scope.end_date = temp_date;
        $scope.show_step_5 = false;
        $scope.show_button = false;
        $scope.show_plot = false;

    };
    $scope.update_start_date = function (start_date_ui) {
        var temp_date = new Date(start_date_ui);

        //tried suggested action but did not work https://github.com/angular-ui/bootstrap/issues/2628
        temp_date.setMinutes(1440); //this is a hard code...date picker always lags one day

        $scope.start_date = temp_date;
        $scope.show_step_5 = false;
        $scope.show_button = false;
        $scope.show_plot = false;

    };

    $scope.closeAlert = function (index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.validate_date = function () {
        //validate date

        $scope.show_step_5 = false;
        $scope.show_button = false;
        $scope.show_plot = false;


        if ($scope.show_end_date_calendar && $scope.start_date && $scope.end_date) {
            if ($scope.end_date >= $scope.start_date) {
                $scope.show_step_5 = true;
            }
            else {

                $scope.alerts.push({type: 'danger', msg: 'From date must be earlier than To date.'});
            }
        }
        else if ($scope.start_date && !$scope.show_end_date_calendar) {
            $scope.end_date = null;
            $scope.show_step_5 = true;
        }
        else {

            $scope.alerts.push({type: 'danger', msg: 'please set dates'});
        }
        //$scope.show_button = true;
        //$scope.show_plot = true;

    };

    $scope.option_plot_type=function(option_value)
    {
        //step 5
        //$scope.show_step_5 = false;
        $scope.show_button = false;
        $scope.show_plot = false;
        $scope.by_timestamp = false;
        $scope.show_individual_date_or_month = false;
        if (option_value.valueOf()=='singlevalue')
        {
            $scope.by_timestamp = false;
            $scope.show_individual_date_or_month = false;
            $scope.show_button = true;
        }
        else if (option_value.valueOf()=='individual')
        {
            $scope.by_timestamp = false;
            $scope.show_individual_date_or_month = true;
            $scope.show_button = true;
        }
        else if (option_value.valueOf()=='timestamp')
        {
            $scope.by_timestamp = true;
            $scope.show_individual_date_or_month = false;
            $scope.show_button = true;
        }
        else
        {
            $scope.msg = 'got' + option_value;
            $scope.show_step_5 = false;
            $scope.show_button = false;
            $scope.show_plot = false;
            $scope.by_timestamp = false;
            $scope.show_individual_date_or_month = false;
        }
    };


    $scope.open_start = function ($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened_start = true;
    };

    $scope.open_end = function ($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened_end = true;
    };


    //$scope.formats = ['dd-MMMM-yyyy','MMMM.yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
    // $scope.format = $scope.formats[0];

    //////////////////////////////////////////////////////////////////////////////
});