module.exports = function(myModule) {
    myModule.controller('indexCtrl',[
      '$scope', '$rootScope', '$http', '$cookies', 'CouchdbService', 'WebappService',
      function ($scope, $rootScope, $http, $cookies, CouchdbService, WebappService) {
          // check if user is logged in
          if($cookies.get('contactNumber')){$rootScope.contactNumber = $cookies.get('contactNumber')};
          if(typeof $rootScope.numbersCount === 'undefined'){
              CouchdbService.getNumbersCount(function (data){
                $rootScope.numbersCount = data['doc_count'];
              });
          }
          $rootScope.logout = function(){
              console.log('contactNumber was deleted');

              delete $rootScope.contactNumber;
              $cookies.remove('session'); // removes session, need to be here
          }

          $rootScope.new_post = function(){
              WebappService.new_post($rootScope.contactNumber, function (data){
                console.log(data);
              });
          }


      }
    ]);
}
