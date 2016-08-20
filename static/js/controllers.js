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
ticTacToeApp.controllers = angular.module('ticTacToeControllers', ['ui.bootstrap', 'LocalStorageModule']);


/**
 * @ngdoc controller
 * @name ModalUserCtrl
 *
 * @description
 * Controller for showing Create User Modal.
 *
 */
ticTacToeApp.controllers.controller('ModalUserCtrl', function($scope, $modal, $log){

    $scope.createUser = function() {
        var modalInstance = $modal.open({
          templateUrl: '/partials/create-user.html',
          controller: 'CreateUserInstanceCtrl'
        });

        modalInstance.result.then(function () {
            $log.info('Saved: ');
        }, function () {
          $log.info('Modal dismissed at: ' + new Date());
        });
    };
});

/**
 * @ngdoc controller
 * @name CreateUserInstanceCtrl
 *
 * @description
 * Controller for creating a User.
 *
 */
ticTacToeApp.controllers.controller('CreateUserInstanceCtrl', function($scope, $modalInstance, $log){
    $scope.user = $scope.user || {};

    $scope.submit = function (form) {
            if(form.$invalid) {
                return;
            }
            /**
             * Invokes the tic_tac_toe.create_user method.
             */
            gapi.client.tic_tac_toe.create_user($scope.user).
                execute(function (resp) {
                    $scope.$apply(function () {
                        if (resp.error) {
                            // The request has failed.
                            var errorMessage = resp.error.message || '';
                            $scope.messages = 'Failed to create a user : ' + errorMessage;
                            $scope.alertStatus = 'warning';
                            $log.error($scope.messages );
                        } else {
                            // The request has succeeded.
                            $scope.messages = resp.result.message;
                            $scope.alertStatus = 'success';
                            $scope.user = {};
                            $log.info($scope.messages + ' : ' + JSON.stringify(resp.result));
                        }
                    });
                });
        };

   $scope.close = function() {
     $modalInstance.close();
   }

});


/**
 * @ngdoc controller
 * @name ModalNewGameCtrl
 *
 * @description
 * Controller for showing New Game Modal.
 *
 */
ticTacToeApp.controllers.controller('ModalNewGameCtrl', function($scope, $modal, $log){

    $scope.newGame = function() {
        var modalInstance = $modal.open({
          templateUrl: '/partials/new-game.html',
          controller: 'NewGameInstanceCtrl'
        });

        modalInstance.result.then(function () {
            $log.info('Saved: ');
        }, function () {
          $log.info('Modal dismissed at: ' + new Date());
        });
    };
});

/**
 * @ngdoc controller
 * @name NewGameInstanceCtrl
 *
 * @description
 * Controller for creating a New Game.
 *
 */
ticTacToeApp.controllers.controller('NewGameInstanceCtrl', function($scope, $modalInstance, $log, localStorageService){
    $scope.new_game = $scope.new_game || {};

    $scope.submit = function (form) {
            if(form.$invalid) {
                return;
            }
            /**
             * Invokes the tic_tac_toe.new_game method.
             */
            gapi.client.tic_tac_toe.new_game($scope.new_game).
                execute(function (resp) {
                    $scope.$apply(function () {
                        if (resp.error) {
                            // The request has failed.
                            var errorMessage = resp.error.message || '';
                            $scope.messages = 'Failed to create new game : ' + errorMessage;
                            $scope.alertStatus = 'warning';
                            $log.error($scope.messages );
                        } else {
                            // The request has succeeded.
                            $scope.messages = 'New game has been created! Players : ' + resp.result.user_name1 + ' ' + resp.result.user_name2;
                            $scope.alertStatus = 'success';
                            localStorageService.set('game_url_key', resp.result.urlsafe_key);
                            $scope.new_game = {};
                            $log.info($scope.messages + ' : ' + JSON.stringify(resp.result));
                        }
                    });
                });
        };

   $scope.close = function() {
     $modalInstance.close();
   }

});

/**
 * @ngdoc controller
 * @name RootCtrl
 *
 * @description
 * The root controller having a scope of the body element and methods used in the application wide.
 *
 */
ticTacToeApp.controllers.controller('RootCtrl', function ($scope, $log, localStorageService) {
    $scope.table = $scope.table || {};

    $scope.current_player = $scope.current_player || 'PLAYER_X';
    $scope.board = $scope.board || ['', '', '', '', '', '', '', '', ''];

    $scope.$watch(function(){
      return localStorageService.get('game_url_key');
    }, function(value){
      $scope.currentGameKey = value;
    });

    $scope.getGame = function(urlsafe_key) {
        gapi.client.tic_tac_toe.get_game({urlsafe_game_key: urlsafe_key}).
            execute(function (resp) {
                $scope.$apply(function () {
                    if (resp.error) {
                        // The request has failed.
                        var errorMessage = resp.error.message || '';
                        $scope.messages = 'Failed to get game : ' + errorMessage;
                        $scope.alertStatus = 'warning';
                        $log.error($scope.messages );
                    } else {
                        // The request has succeeded.
                        $scope.messages = 'Get game succeded : ' + resp.result.message;
                        $scope.alertStatus = 'success';
                        $scope.table = {
                            urlsafe_game_key: resp.result.urlsafe_key,
                            current_player: resp.result.current_player
                        };
                        $log.info($scope.messages + ' : ' + JSON.stringify(resp.result));

                    }
                });
            });

    }
});

