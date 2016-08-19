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
          controller: 'CreateUserInstanceCtrl',
          scope: $scope
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

