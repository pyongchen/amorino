angular.module('glassApp')
    .controller('collects_ctrl', function ($scope, $http) {
        $scope.cur_lang = sessionStorage['cur_lang'];
        $scope.infos = infos;
        $http.get('/get_data/collect').then(function (response) {
            $scope.collects = response.data.user;
        });
        $scope.setUpdateInfo = function (id, number, message) {
            $scope.id = id;
            $scope.number = number;
            $scope.message = message;
        };

        $scope.setDeleteInfo = function (id) {
            $scope.id = id;
        };

        $scope.submitUpdate = function () {
            var url = 'collect/update';
            var req = {
                method: 'POST',
                url: url,
                data: {
                    number: $scope.number,
                    message: $scope.message,
                    id: $scope.id
                }
            };
            $http(req).then(function (response) {
                $scope.collects = response.data.user;
            })
        };

        $scope.submitDelete = function () {
            var url = 'collect/delete';
            var req = {
                method: 'POST',
                url: url,
                data: {
                    id: $scope.id
                }
            };
            $http(req).then(function (response) {
                $scope.collects = response.data.user;
            })
        };

        $scope.btnClick = function (index, id) {
            if ($scope.collects[index].status == 'edit') {
                $scope.collects[index].status = 'confirm';
                $('.detail-text-box input').css('background-color', '#8c8c8c');
                $('#note').css('position', 'absolute');
                $('.mobile-collect-com textarea').css('margin-left', '10px');
            } else {
                var number = $('.number-box').val();
                var message = $('.message-box').val();
                var url = 'collect/update';
                var req = {
                    method: 'POST',
                    url: url,
                    data: {
                        number: number,
                        message: message,
                        id: id
                    }
                };
                $http(req).then(function (response) {
                    $scope.collects = response.data.user;
                });
                $scope.collects[index].status = 'edit';
                $('.detail-text-box input').css('background-color', '');
            }
        };

    });

var infos = {
    "head": {
        "zh": "的收藏夹",
        "en": "'s favorites",
        "es": "colección de clip"
    },
    "confirm": {
        "zh": "确认",
        "en": "Confirm",
        "es": ""
    },
    "edit": {
        "zh": "编辑",
        "en": "Edit",
        "es": "editor"
    },
    "delete": {
        "zh": "删除",
        "en": "Delete",
        "es": "Deleción"
    },
    "number": {
        "zh": "数量",
        "en": "Number",
        "es": "El número"
    },
    "message": {
        "zh": "备注",
        "en": "Note",
        "es": "comentar"
    },
    "alert": {
        "makeSure": {
            "zh": "确定要删除此收藏?",
            "en": "Sure you want to delete this collection?",
            "es": "Seguro que va a borrar la colección?"
        },
        "yes": {
            "zh": "确定",
            "en": "Yes",
            "es": "sí"
        },
        "no": {
            "zh": "取消",
            "en": "No",
            "es": "No"
        }
    }
};