angular.module('glassApp')
    .controller('homeCtrl', function ($scope, $http, dataProvider) {
        $scope.home = {};
        $scope.curPage = 'home';
        var lang = sessionStorage.getItem('cur_lang');
        if (lang) {
            $scope.cur_lang = lang;
        } else {
            sessionStorage.setItem('cur_lang', 'zh');
            $scope.cur_lang = 'zh'
        }
        getBaseInfo($scope, $http);
        $http.get('/get_data/frame').then(function (response) {
            $scope.frame = response.data;
        });
        $http.get('/login').then(function (response) {
            if (response.data != 'None') $scope.username = response.data;
        });

        dataProvider.init_home().then(function () {
            $scope.first = dataProvider.get('first');
            $scope.second = dataProvider.get('second');
            $scope.third = dataProvider.get('third');
        });

        dataProvider.init_data().then(function () {
            $scope.data = dataProvider.get('data');
            $scope.all = getAllDetails($scope.data);
        });

        $scope.goToDetail = function (type, kind, index) {
            if ($(".username").text()) {
                sessionStorage.setItem('type_', type);
                sessionStorage.setItem('kind_', kind);
                sessionStorage.setItem('index_', index);
                $scope.detail_url = '/products_detail';
            } else {
                $('#login').css('z-index', 99999);
                $('#login').fadeIn('slow');
                $scope.detail_url = '/login_page'
            }
        };
        
        $scope.show_login = function () {
            $('#login').fadeIn('slow');
        };

        $scope.login = function () {
            var username = $('#username').val();
            var password = $('#password').val();
            var url = '/login';
            var req = {
                method: 'POST',
                url: url,
                data: {
                    username: username,
                    password: password
                }
            };
            $http(req).then(function (response) {
                var data = JSON.parse(response.data);
                if (data.success == '') {
                    $scope.username = null;
                    $scope.info = data.fail[$scope.cur_lang];
                } else {
                    $scope.username = data.success;
                    $scope.info = '';
                    $('#login').fadeOut();
                }
            });
        };

        $scope.collects = function () {
            $http.get('/login').then(function (response) {
                if(response.data == 'None') {
                    alert($scope.baseInfo.alert.logout[$scope.cur_lang])
                }
                $scope.username = response.data;
            });
        };

        $scope.logout = function () {
            sessionStorage.removeItem('username');
            $scope.username = null;
            $scope.password = '';
        };
            
        $scope.getKind = function (type, kind) {
            sessionStorage.setItem('type', type);
            sessionStorage.setItem('kind', kind);
        };
        
        $('.langs').each(function (index) {
            var lang = ['zh', 'en', 'es'];
            $(this).click(function () {
                sessionStorage['cur_lang'] = lang[index];
                setTimeout(function () {
                    location.reload();
                }, 1000);
            })
        });
        $(".back-to-top").click(function() {
			$('body').animate({scrollTop : 0}, 'slow');
		});
        $('.close').click(function () {
            $('#login').fadeOut();
        });
    });

function getBaseInfo($scope, $http) {
    $http.get('/get_data/base_info').then(function (response) {
        $scope.baseInfo = response.data;
    })
}


function getAllDetails(data) {
    var pros = data.products;
    var all = [];
    for (var key1 in pros) {
        var details = pros[key1].details;
        for (var key2 in details) {
            var kinds = details[key2];
            var index = 0;
            for (var key3 in kinds) {
                var detail = kinds[key3];
                detail.type = key1;
                detail.kind = key2;
                detail.index = index;
                all.push(detail);
                index++;
            }
        }
    }
    return all;
}