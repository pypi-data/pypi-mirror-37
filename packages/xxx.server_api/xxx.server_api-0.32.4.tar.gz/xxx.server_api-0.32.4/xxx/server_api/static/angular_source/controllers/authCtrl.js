module.exports = function(myModule, CryptoJS, firebase) {
    myModule.controller('authCtrl',[
      '$scope', '$http', '$routeParams', '$cookies', 'WebappService',
      function ($scope, $http, $routeParams, $cookies, WebappService) {
        var setUpVariables = function(){
            $scope.nickName = null;
            $scope.confirmPassword = null;
            $scope.errorMessage = null;
            $scope.registerButtonHide = false;
            $scope.confirmCodeUser = null;

            if($cookies.get('contactNumber')){
               $scope.contactNumber = $cookies.get('contactNumber');
            } else {
               $scope.contactNumber = null;
            }
            if($cookies.get('hashed_password')){
               $scope.hashed_password = $cookies.get('hashed_password');
            } else {
               $scope.hashed_password = null;
            }
            $scope.password = null;
//            if($cookies.get('savePassword')){
//               $scope.savePassword = $cookies.get('savePassword');
//               console.log('setup savePassword');
//               console.log($scope.savePassword);
//            } else {
//               $scope.savePassword = false;
//            }
        };
        setUpVariables();

        $scope.register = function(){
          $scope.errorMessage = null;
          if(!$scope.nickName){
              $scope.errorMessage = "Nickname is required ";
          }
          if($scope.password){
              if($scope.password != $scope.confirmPassword){
                $scope.errorMessage = "Passwords don't match";
              }
          } else {
              $scope.errorMessage = "Password is required ";
          }

          if($scope.contactNumber){
              if($scope.contactNumber.length != 13){
                $scope.errorMessage = "Number length is wrong (length of +380961231212 is 13) ";
              }
          } else {
              $scope.errorMessage = "Number is required ";
          }

          if(!$scope.errorMessage){
            $scope.registerButtonHide = true;
            firebase_function($scope.contactNumber);
          }
        };
        $scope.registerNewUser = function(){
          $scope.errorMessage = null;

          $scope.confirmationResult.confirm($scope.confirmCodeUser).then(function (result) {
              console.log('Confirmation success');
          }).catch(function (error) {
              $scope.errorMessage = 'Confirmation code is not correct ';
          });

          if(!$scope.errorMessage){
//          should send to api backend
            $scope.hashed_password = String(CryptoJS.SHA256($scope.password));
            WebappService.registerNewUser($scope.contactNumber, $scope.hashed_password, $scope.nickName,
             function (responseMessage){
                $scope.responseMessage = responseMessage;
            });
          }
        };
        var firebase_function = function(phoneNumber){
            var config = {
                apiKey: "AIzaSyAB2od_dh3CDeqjSgYF-ScgMs0E1Re892g",
                authDomain: "yummygirls.ga",
                databaseURL: "https://yummygirls-ce013.firebaseio.com",
                projectId: "yummygirls-ce013",
                storageBucket: "yummygirls-ce013.appspot.com",
                messagingSenderId: "788287545352"
             };
            firebase.initializeApp(config);
            firebase.auth().languageCode = 'it';
            firebase.auth().useDeviceLanguage();

            this.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container', {
              'size': 'normal',
              'callback': function(response) {
                console.log('recaptcha solved');
              },
              'expired-callback': function() {
                console.log('recaptcha expired');
              }
            });

            var appVerifier = this.recaptchaVerifier;
            firebase.auth().signInWithPhoneNumber(phoneNumber, appVerifier)
                .then(function (confirmationResult) {
                  $scope.confirmationResult= confirmationResult;
                }).catch(function (error) {
                  console.log(error);
                });

        };

        $scope.login = function(){
            $scope.errorMessage = null;
            if($scope.contactNumber){
                if($scope.contactNumber.length != 13){
                  $scope.errorMessage = "Number length is wrong (length of +380961231212 is 13) ";
                }
              } else {
                $scope.errorMessage = "Number is required ";
              }

            if(!$scope.password){ $scope.errorMessage = "Password is required ";};
            if(!$scope.errorMessage){
                $scope.hashed_password = String(CryptoJS.SHA256($scope.password));
                WebappService.login($scope.contactNumber, $scope.hashed_password,
                 function (responseMessage){
                    console.log(responseMessage);
                    $scope.responseMessage = responseMessage;
                });
            }
        };

      }
 ]);
}

