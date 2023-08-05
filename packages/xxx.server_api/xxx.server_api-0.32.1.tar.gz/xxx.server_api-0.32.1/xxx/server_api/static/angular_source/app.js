var jquery = require('jquery');
var jqueryeasing = require('jquery.easing');
var fancybox = require('@fancyapps/fancybox');
var bootstrap = require('bootstrap');
var chartjs = require('chart.js');
var angular = require('angular');
var ngCookies = require('angular-cookies');
var ngRoute = require('angular-route');
var ngChart = require('angular-chart.js');
var CryptoJS = require('crypto-js');
var firebase = require('firebase');


var appRequires = [ngRoute, ngCookies, ngChart];

var app = angular.module('myModule', appRequires)
                 .config(['$routeProvider', '$locationProvider', '$httpProvider',
                 function ($routeProvider, $locationProvider, $httpProvider){
                   $routeProvider
                     .when("/index", {
                       templateUrl: "static/angular_source/templates/index.html",
                       controller: "indexCtrl"
                     })
                     .when("/tables", {
                       templateUrl: "static/angular_source/templates/tables.html",
                       controller: "tablesCtrl"
                     })
                     .when("/detail/:id", {
                       templateUrl: "static/angular_source/templates/detail.html",
                       controller: "detailCtrl"
                     })
                     .when("/login", {
                       templateUrl: "static/angular_source/templates/login.html",
                       controller: "authCtrl"
                     })
                     .when("/register", {
                       templateUrl: "static/angular_source/templates/register.html",
                       controller: "authCtrl"
                     })
                     .when("/mypage/:id", {
                       templateUrl: "static/angular_source/templates/mypage.html",
                       controller: "mypageCtrl"
                     })
                     .otherwise({
                     redirectTo: "/index"
                     })
                   $locationProvider.html5Mode(true);
                   $httpProvider.defaults.withCredentials = true;
                 }]);

//db_url from base.html
app.constant('NumbersConfig', {
                   remote_db: db_url,
                   remote_webapp: webapp_url
                 })

//  connect controollers services filters
require('./services/couchdbService')(app);
require('./services/webappService')(app);
require('./filters/filters')(app);
require('./controllers/tablesCtrl')(app);
require('./controllers/indexCtrl')(app);
require('./controllers/detailCtrl')(app);
require('./controllers/mypageCtrl')(app);
require('./controllers/authCtrl')(app, CryptoJS, firebase);
//custom js
require('../js/sb-admin');
