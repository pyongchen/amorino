angular.module('glassApp')
    .factory('dataProvider', function dataProvider($http) {
        return {
            'init_home': function () {
                return $http.get('/get_data/home').then(function (response) {
                    var first = response.data.first;
                    var second = response.data.second;
                    var third = response.data.third;
                    sessionStorage['first'] = JSON.stringify(first);
                    sessionStorage['second'] = JSON.stringify(second);
                    sessionStorage['third'] = JSON.stringify(third);
                });
            },
            'init_data': function () {
                return $http.get('/get_data/user').then(function (response) {
                    sessionStorage['data'] = JSON.stringify(response.data);
                })
            },
            'get': function (key) {
                return JSON.parse(sessionStorage[key])
            }
        };
    });