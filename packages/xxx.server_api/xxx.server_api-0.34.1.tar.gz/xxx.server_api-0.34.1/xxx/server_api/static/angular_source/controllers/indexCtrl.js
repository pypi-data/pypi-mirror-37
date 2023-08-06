module.exports = function(myModule) {
    myModule.controller('indexCtrl',[
      '$scope', '$rootScope', '$http', '$cookies', 'CouchdbService',
      function ($scope, $rootScope, $http, $cookies, CouchdbService) {
          // check if user is logged in
          if($cookies.get('contactNumber')){$rootScope.contactNumber = $cookies.get('contactNumber')};
          if($cookies.get('session')){$rootScope.session = $cookies.get('session')};
          if(typeof $rootScope.numbersCount === 'undefined'){
              CouchdbService.getNumbersCount(function (data){
                $rootScope.numbersCount = data['doc_count'];
              });
          }
          $rootScope.logout = function(){
              console.log('contactNumber was deleted');

              delete $rootScope.contactNumber;
              delete $rootScope.session;
              $cookies.remove('session'); // removes session, need to be here
          }

      }
    ]);
}
