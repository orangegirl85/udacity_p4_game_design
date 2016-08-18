'use strict';

/**
 * The root ticTacToeApp module.
 *
 * @type {ticTacToeApp|*|{}}
 */
var ticTacToeApp = ticTacToeApp || {};

/**
 * @ngdoc module
 * @name ticTacToeControllers
 *
 * @description
 * Angular module for controllers.
 *
 */
ticTacToeApp.controllers = angular.module('ticTacToeControllers', ['ui.bootstrap']);



/**
 * @ngdoc controller
 * @name RootCtrl
 *
 * @description
 * The root controller having a scope of the body element and methods used in the application wide
 * such as user authentications.
 *
 */
ticTacToeApp.controllers.controller('RootCtrl', function ($scope) {
    $scope.title = 'Tic Tac Toe';
});

