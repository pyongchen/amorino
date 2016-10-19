angular.module('admin', ['angularUtils.directives.dirPagination'])
    .config(['$interpolateProvider', function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');
    }])
    .controller('admin_ctrl', function ($scope, $http) {
        $scope.add_kind = '';

        $http.get('/get_data/admin').then(function (response) {
            $scope.data = response.data;
            $scope.users = $scope.data.users;
        });

        $http.get('/get_data/home').then(function (response) {
            $scope.home = response.data;
        });

        $http.get('/get_data/frame').then(function (response) {
            $scope.frame = response.data;
        });

        $scope.addUser = function () {
            var url = '/admin/user/add';
            var username = $('#add_username').val();
            var password = $('#password').val();
            var req = {
                method: 'POST',
                url: url,
                data: {
                    username: username,
                    password: password
                }
            };
            $http(req).then(function (response) {
                $scope.users = response.data.users;
                $scope.info = response.data.info;
            })
        };

        $scope.deleteUser = function () {
            var url = '/admin/user/delete';
            var username = $('#del_username').val();
            var req = {
                method: 'POST',
                url: url,
                data: {
                    username: username
                }
            };
            $http(req).then(function (response) {
                $scope.users = response.data.users;
                $scope.info = response.data.info;
            })
        };

        $scope.changeData = function (type, p1, p2, p3, kind,
                                      name, material, color, size, price, image, otherImages) {
            if (type == 'update') {
                var len = image.split('/').length;
                var imgName = image.split('/')[len - 1];
                $scope.postUrl = '/admin/products/update/'
                    + p1 + '/' + p2 + '/' + p3 + '/' + imgName;
                $scope.show_type = kind;
                $scope.show_kind = name;
                $scope.show_material = material;
                $scope.show_color = color;
                $scope.show_size = size;
                $scope.show_price = price;
                $scope.show_image = image;
                $scope.otherImages = otherImages;

            } else if (type == 'delete') {
                var arr = kind.split('/');
                var img = arr[arr.length - 1];
                $scope.postUrl = '/admin/products/delete/' + p1 + '/' + p2 + '/' + p3 + '/' + img;
            } else {
                $scope.postUrl = '/admin/products/add/'
                    + p1 + '/' + p2 + '/null' + '/null';
            }
        };

        $scope.submitChange = function () {
            var url = $scope.postUrl;
            var req = {
                method: 'POST',
                url: url,
                data: {
                    type: $scope.deleteType,
                    key: $scope.deleteKind.key,
                    upload: $scope.file
                }
            };
            $http(req).then(function (response) {
                $scope.data = response.data;
            })
        };

        $scope.setDeleteKind = function (type, kind) {
            $scope.deleteType = type;
            $scope.deleteKind = kind;
        };

        $scope.setAddType = function (type) {
            $scope.add_type_ = type;
        };

        $scope.isDeleteKind = function (info) {
            var url = '/admin/products_kind_delete/';
            var req = {
                method: 'POST',
                url: url,
                data: {
                    type: $scope.deleteType,
                    key: $scope.deleteKind.key
                }
            };
            if (info == 'yes') {
                $http(req).then(function (response) {
                    $scope.data = response.data;
                    $scope.info = "类型:" + $scope.deleteKind.zh + "已下架"
                });
            } else {
                $scope.info = '';
            }
        };

        $scope.addKind = function () {
            var kind = $scope.add_kind;
            var url = '/admin/products_kind_add';
            var req = {
                method: 'POST',
                url: url,
                data: {
                    type: $scope.add_type_,
                    kind: kind
                }
            };
            $http(req).then(function (response) {
                $scope.data = response.data;
                $scope.info = "新款式:" + kind + "已上传"
            });
        };

        $scope.listTop = function (type, kind, index) {
            var url = '/admin/listTop';
            var req = {
                method: 'POST',
                url: url,
                data: {
                    type: type,
                    kind: kind,
                    index: index
                }
            };
            $http(req).then(function (response) {
                $scope.data = response.data;
            });
        };

        $scope.addType = function () {
            var url = '/admin/products_type_add';
            var req = {
                method: 'POST',
                url: url,
                data: {
                    type: $scope.add_type
                }
            };
            $http(req).then(function (response) {
                $scope.data = response.data;
                $scope.info = "新类型:" + $scope.add_type + "已上传"
            });
        };

        $scope.deleteType = function (typeName) {
            $scope.delete_type = typeName;
            console.log(typeName);
        };

        $scope.isDeleteType = function (info) {
            if (info == 'yes') {
                var url = '/admin/products_type_delete/';
                var req = {
                    method: 'POST',
                    url: url,
                    data: {
                        type: $scope.delete_type.key
                    }
                };
                $http(req).then(function (response) {
                    $scope.data = response.data;
                    $scope.info = "类型:" + $scope.delete_type.zh + "已下架";
                });
            } else {
                $scope.info = '';
            }
        };

        $scope.changeFrame = function () {
            var url = '/admin/frame';
            var file = document.getElementById('frame_data');
            var formData = new FormData(file);
            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function () {
                    $http.get('/get_data/frame').then(function (response) {
                        $scope.frame = response.data;
                    });
                }
            });
        };

        $scope.homeFirstChange = function () {
            var url = '/admin/home/first';
            var file = document.getElementById('firstForm');
            var formData = new FormData(file);
            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function () {
                    $http.get('/get_data/home').then(function (response) {
                        $scope.home = response.data;
                    });
                }
            });
        };

        $scope.homePartChange = function (part) {
            var url = '/admin/home/' + part;
            var file = document.getElementById(part + 'Form');
            var formData = new FormData(file);
            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function () {
                    $http.get('/get_data/home').then(function (response) {
                        $scope.home = response.data;
                    });
                }
            });
        };
    });