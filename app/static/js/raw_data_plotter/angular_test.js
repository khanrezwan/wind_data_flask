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
var app = angular.module('myApp', ['ui.bootstrap',"chart.js"]);
// http://jtblin.github.io/angular-chart.js/#getting_started
//http://angular-ui.github.io/bootstrap/
app.controller('myCtrl',function($scope, $http, $window) {


    $scope.labels = ['2006', '2007', '2008', '2009', '2010', '2011', '2012'];
    $scope.series = ['Series A', 'Series B'];

    $scope.data = [
        [65, 59, 80, 81, 56, 55, 40],
        [28, 48, 40, 19, 86, 27, 90]
    ];


    $scope.firstName= "John";
    $scope.lastName= "Doe";
    //$scope.dt = '';
    $scope.logger_list = [];
    $scope.data_list =[];
    $scope.sensor_list = [];
    $scope.count = 0;
    $scope.msg = "Debugging";
    $scope.send_query = function() //Testing query string params for get and data for post
    {
        $http
            .get('test_strings',{params:{sensor_id:$scope.sensor_select_value, date: null}})
            .success(function(data, status, headers, config) {
                if (data.success) {

                    $scope.data_list = data.dataList;
                    //$scope.get_sensor_list( $scope.logger_list[0].logger.id)
                    $scope.msg = 'Loaded dataList' +" "+ $scope.data_list.length;
                } else {
                    $window.alert('Retrieval failed 22');
                }
            })
            .error(function(data, status, headers, config) {
                $window.alert('Retrieval failed');
            });

    };

    $scope.init_logger = function(){
        $scope.msg = "inside send to loggerlist";
        $http
            .get('getLoggers')
            .success(function(data, status, headers, config) {
                if (data.success) {

                    $scope.logger_list = data.loggerList;
                    //$scope.get_sensor_list( $scope.logger_list[0].logger.id)
                    $scope.msg = 'Loaded loggerList' +" "+ $scope.logger_list.length;
                } else {
                    $window.alert('Retrieval failed 22');
                }
            })
            .error(function(data, status, headers, config) {
                $window.alert('Retrieval failed');
            });
    };
    $scope.init_logger();
    $scope.some_func = function()
    {
        console.log(angular.element(document.getElementById('datetimepicker10')));
    };
    //$scope.some_func();
    $scope.send_to_flask = function(n) {
        $scope.msg = "inside send to flask";
        $http
            .get('test_ret/' + n)
            .success(function(data, status, headers, config) {
                if (data.success) {
                    $scope.msg= data.todoList;
                } else {
                    $window.alert('Retrieval failed 22');
                }
            })
            .error(function(data, status, headers, config) {
                $window.alert('Retrieval failed');
            });
    };

    $scope.get_sensor_list = function(logger_id){
        $scope.msg = "inside send to sensorlist";
        $http
            .get('getSensors/'+logger_id)
            .success(function(data, status, headers, config) {
                if (data.success) {

                    $scope.sensor_list = data.sensorList;

                    $scope.msg = 'Loaded sensorList' +" "+ $scope.sensor_list.length;
                } else {
                    $window.alert('Retrieval failed 22');
                }
            })
            .error(function(data, status, headers, config) {
                $window.alert('Retrieval failed');
            });
    };

    $scope.test_counter = function(n)
    {
        $scope.count = $scope.count+1;
        $scope.msg = ' Count '+ n;
    };
    /////////////////////angular ui date picker example//////////////////////////
    $scope.today = function() {
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

    $scope.toggleMin = function() {
        $scope.minDate = $scope.minDate ? null : new Date();
    };
    //$scope.toggleMin();

    $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened = true;
    };

    $scope.dateOptions = {
        'year-format': "yyyy",
        'starting-day': 1,
        'datepicker-mode':"'month'",
        'min-mode':"month",
        'showWeeks': "false",
        'show-button-bar':"false",
        'close-on-date-selection' : "false",
        'current-text' : 'This Month'


    };

    $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate', 'MMMM.yyyy'];
    // $scope.format = $scope.formats[0];



    //////////////////////////////////////////////////////////////////////////////
});