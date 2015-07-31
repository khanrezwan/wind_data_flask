/**
 * Created by rezwan on 19/07/15.
 * http://angular-ui.github.io/bootstrap/
 */

/* ToDo ng-app will send query to ngQueries with following params
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


    $scope.labels = ['2006', '2007', '2008', '2009', '2010', '2011', '2012'];
    $scope.series = ['Series A', 'Series B'];


    $scope.data = [
        [65, 59, 80, 81, 56, 55, 40],
        [28, 48, 40, 19, 86, 27, 90]
    ];

    //ui panel for ng-show
    $scope.show_step_1 = true;
    $scope.show_step_2 = false;
    $scope.show_step_3 = false;
    $scope.show_step_4 = false;
    $scope.show_step_5 = false;
    $scope.show_button = false;
    $scope.show_plot = false;
    //for flask
    $scope.by_date = false;
    $scope.by_month = false;
    $scope.start_date = null;
    $scope.end_date = null;
    $scope.sensor = {};

    //for ng-functions
    $scope.min_date ={};
    $scope.max_date ={};
    $scope.sensor_id_from_step_2 = null;
    $scope.logger_list = [];
    $scope.data_list = [];
    $scope.sensor_list = [];

    $scope.msg = "Debugging";
    $scope.send_query = function () //Testing query string params for get and data for post
    {
        $http
            .get('getPlotDataDate24Hr', {
                params: {
                    sensor_id: $scope.sensor_select_value,
                    date: $scope.sensor_select_value
                }
            })
            .success(function (data, status, headers, config) {
                if (data.success) {

                    $scope.data_list = data.dataList;
                    //$scope.get_sensor_list( $scope.logger_list[0].logger.id)
                    $scope.msg = 'Loaded dataList' + " " + $scope.data_list.length;
                } else {
                    $window.alert('Retrieval failed 22');
                }
            })
            .error(function (data, status, headers, config) {
                $window.alert('Retrieval failed');
            });

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
    //$scope.some_func = function () {
    //    console.log(angular.element(document.getElementById('datetimepicker10')));
    //};
    ////$scope.some_func();
    //$scope.send_to_flask = function (n) {
    //    $scope.msg = "inside send to flask";
    //    $http
    //        .get('test_ret/' + n)
    //        .success(function (data, status, headers, config) {
    //            if (data.success) {
    //                $scope.msg = data.todoList;
    //            } else {
    //                $window.alert('Retrieval failed 22');
    //            }
    //        })
    //        .error(function (data, status, headers, config) {
    //            $window.alert('Retrieval failed');
    //        });
    //};

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
    $scope.option_month_or_date = function(option){
        //step 3a
        $scope.show_step_4 = false;
        $scope.show_step_5 = false;
        $scope.show_button = false;
        $scope.show_plot = false;
        if (option.valueOf() == 'by_date')
        {
            $scope.by_date = true;
            $scope.by_month = false;
            // $scope.show_step_4 = true;
        }
        else if (option.valueOf() == 'by_month')
        {
             $scope.by_date = false;
            $scope.by_month = true;
            //$scope.show_step_4 = true;
        }
        else
        {
             $scope.by_date = false;
            $scope.by_month = false;
        }
    };

    $scope.option_single_or_range = function(option)
    {
        $scope.show_step_4 = false;
        $scope.show_step_5 = false;
        $scope.show_button = false;
        $scope.show_plot = false;
        //after step 3b
    };

    $scope.get_maximum_minimum_dates_of_available_data = function(sensor_id)
    {
        $http
            .get('getAvailableDates/' + sensor_id)
            .success(function (data, status, headers, config) {
                if (data.success) {

                    $scope.min_date = new Date(data.min_date);
                    $scope.max_date = new Date(data.max_date);
                    //$scope.get_sensor_list( $scope.logger_list[0].logger.id)
                    $scope.msg = 'got min date' + " " + $scope.min_date + " and max Date " + $scope.max_date;
                    $scope.show_step_3 = true;
                } else {
                    $window.alert('Retrieval failed 22');
                }
            })
            .error(function (data, status, headers, config) {
                $window.alert('Retrieval failed');
            });
    };
    /////////////////////angular ui date picker example//////////////////////////
    $scope.today = function () {
        $scope.dt = new Date();
    };
    $scope.today();
    $scope.date = new Date();
    $scope.clear = function () {
        $scope.dt = null;
    };

    // Disable weekend selection
    //$scope.disabled = function(date, mode) {
    //  return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
    //};

    $scope.toggleMin = function () {
        $scope.minDate = $scope.minDate ? null : new Date();
    };
    //$scope.toggleMin();

    $scope.open = function ($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened = true;
    };

    $scope.dateOptions = {
        'year-format': "yyyy",
        'starting-day': 1,
        'datepicker-mode': "'month'",
        'min-mode': "month",
        'showWeeks': "false",
        'show-button-bar': "false",
        'close-on-date-selection': "false",
        'current-text': 'This Month'


    };

    $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate', 'MMMM.yyyy'];
    // $scope.format = $scope.formats[0];


    //////////////////////////////////////////////////////////////////////////////
});