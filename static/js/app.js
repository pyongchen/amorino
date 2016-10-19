angular.module('glassApp', ['ngAnimate'])
    .config(function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');
    });