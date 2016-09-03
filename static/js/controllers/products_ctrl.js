angular.module('glassApp')
    .controller('products_ctrl', function ($scope, $http) {
        $scope.cur_lang = sessionStorage['cur_lang'];
        $scope.data = JSON.parse(sessionStorage['data']);
        $scope.repeat = false;
        $scope.infos = infos;
        $scope.curPage = 'products';
        var type = sessionStorage.getItem('type_');
        var kind = sessionStorage.getItem('kind_');
        var index = parseInt(sessionStorage.getItem('index_'));
        getType($scope, $scope.data.products);

        if (type && kind) {
            $scope.show_type = type;
            $scope.show_kind = kind;
            $scope.show_index = index;
            $scope.num = $scope.data.products[type].details[kind].length;
            $scope.details = $scope.data.products[type].details[kind];
            $scope.images = getImages($scope.data.products[type].details[kind]);
        } else {
            $scope.show_index = 0;
            $scope.show_kind = $scope.type1.kinds[0];
            var key = Object.keyAt($scope.type1.details, 0);
            $scope.num = $scope.type1.details[key].length;
            $scope.details = $scope.data.products[$scope.show_type].details
                [$scope.show_kind];
            $scope.images = getImages($scope.type1.details[$scope.show_kind]);
        }

        setTimeout(function () {
            for (var i = 0; i < $scope.num; i++)
                if (i != $scope.show_index) {
                    $('.detail')[i].style.display = 'none';
                } else {
                    $('.detail')[i].style.display = 'block';
                }
        }, 200);

        $scope.getDescription = function (type, kind) {
            $scope.show_type = type;
            $scope.show_kind = kind;
            $scope.show_index = 0;
            $scope.num = $scope.data.products[type].details[kind].length;
            $scope.details = $scope.data.products[type].details[kind];
            $scope.images = getImages($scope.data.products[type].details[kind]);
            setTimeout(function () {
                for (var i = 0; i < $scope.num - 1; i++)
                    $('.detail')[i].style.display = 'none';
                $('.detail')[0].style.display = 'block';
            }, 100);
        };

        $scope.right = function () {
            $scope.show_index++;
            if ($scope.show_index >= $scope.num) $scope.show_index = 0;
        };

        $scope.left = function () {
            $scope.show_index--;
            if ($scope.show_index < 0) $scope.show_index = $scope.num - 1;
        };

        $scope.setDownloadUrl = function () {
            var id = $scope.data.products[$scope.show_type].details[$scope.show_kind][$scope.show_index].id;
            $scope.downloadUrl = '/download/' + $scope.show_type + '/' + $scope.show_kind
                + '/' + $scope.show_kind + '_' + id;
        };

        $scope.setType = function (type) {
            if ($scope.show_type == type) {
                if ($scope.repeat) $scope.repeat = false;
                else $scope.repeat = true;
            } else {
                $scope.repeat = false;
            }
            $scope.show_type = type;
            $scope.show_kind = $scope.data.products[type].kinds[0].key;
            $scope.details = $scope.data.products[type].details[$scope.show_kind];
            $scope.show_index = 0;
            $scope.num = $scope.data.products[type].details[$scope.show_kind].length;
            $scope.images = getImages($scope.data.products[type].details[$scope.show_kind]);
            setTimeout(function () {
                for (var i = 0; i < $scope.num - 1; i++)
                    $('.detail')[i].style.display = 'none';
                $('.detail')[0].style.display = 'block';
            }, 100);
        };

        $scope.alertCollects = function () {
            $('.alert_collect').fadeIn('slow');
        };

        $scope.removeCollects = function () {
            $('.alert_collect').fadeOut('slow');
        };

        $scope.submitCollect = function () {
            var number = $('.alert_collect input').val();
            var message = $('.alert_collect textarea').val();
            if (number != '') {
                var detail = $scope.data.products[$scope.show_type].details
                    [$scope.show_kind][$scope.show_index];
                var url = '/collect/add';
                var req = {
                    method: 'POST',
                    url: url,
                    data: {
                        detail: detail,
                        number: number,
                        message: message
                    }
                };
                $http(req).then(function (response) {
                    
                });
                $('.alert_collect').fadeOut('slow');
            } else {
                $scope.info = infos.alert.err[$scope.cur_lang];
            }
        };
    });

Object.keyAt = function (obj, index) {
    var i = 0;
    for (var key in obj) {
        if ((index || 0) === i++) return key;
    }
};

function getImages(details) {
    var images = [];
    for (var i = 0; i < details.length; i++)
        images.push(details[i].image)
    return images;
}


function getType($scope, data) {
    var index = 1;
    for (var obj in $scope.data.products) {
        $scope['type' + index] = data[obj];
        index++;
    }
}

var infos = {
    "download": {
        "zh": "下载高清图",
        "en": "Hd Images",
        "es": "Hd fotos"
    },
    "collect": {
        "zh": "收藏该产品",
        "en": "Collect",
        "es": "La colección"
    },
    "detail": {
        "zh": "产品细节图",
        "en": "Detail Images",
        "es": "Los detalles de la figura de productos"
    },
    "alert": {
        "h1": {
            "zh": "收藏商品",
            "en": "Collect product",
            "es": "La colección de productos"
        },
        "h2": {
            "zh": "请输入商品收藏的数量及备注信息,我们将尽快联系您",
            "en": "Please enter the number of goods collection and note information, we will contact you as soon as possible",
            "es": "Por favor ingrese su colección de cantidad y productos de información lo antes posible, vamos a comentar con usted"
        },
        "number": {
            "zh": "数量",
            "en": "Number",
            "es": "El número"
        },
        "other": {
            "zh": "备注",
            "en": "Note",
            "es": "comentar"
        },
        "submit": {
            "zh": "确认收藏",
            "en": "Confirm the collection",
            "es": "Confirma la colección"
        },
        "err": {
            "zh": "请输入商品数量",
            "en": "Please enter the product number",
            "es": "Por favor ingrese número de productos"
        }
    }
};
