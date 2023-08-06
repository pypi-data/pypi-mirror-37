module.exports = function(myModule) {
    myModule.controller('mypageCtrl',[
      '$scope', '$rootScope', '$http', '$routeParams', '$cookies', 'CouchdbService',
      function ($scope, $rootScope, $http, $routeParams, $cookies, CouchdbService) {
           // check if user is logged in
           if($cookies.get('contactNumber')){$rootScope.contactNumber = $cookies.get('contactNumber')};
           console.log('mypageCtrl started');
           $scope.data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

           var makePostsStatisticGraphics = function(){
               //     2018-03-05
               var formatDate = function formatDa(date) {
                  var day = date.getDate();
                  var monthIndex = date.getMonth() + 1;
                  var year = date.getFullYear();
                  return  year + "-" + monthIndex + "-" + day;
               }

               var time_const = 86400000;
               var threshold = 2592000000;
               var da =  formatDate(new Date());
               var today = new Date(da);
               for (i=0; i<$scope.number.posts.length; i++){
                    if( today - new Date($scope.number.posts[i].date_post.slice(0, 10)) < threshold ){
                       var index = (today - new Date($scope.number.posts[i].date_post.slice(0, 10)) ) / time_const;
                       var temp = $scope.data[30 - index] + 1;
                       $scope.data[30 - index] = temp;
                    }
               }
           }


           CouchdbService.getNumber($routeParams.id, function (number){
                $scope.number = number;
                //           pagination goes here
                $scope.currentPage = 0;
                $scope.pageSize = 50;
                $scope.numberOfPages=function(){
                   return Math.ceil($scope.number.posts.length/$scope.pageSize);
                }
                makePostsStatisticGraphics();
           });

           //     here canvas chart begins
           var monthNames = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"
           ];
           var monthNamesSimple = ["Ja", "Fe", "Ma", "Ap", "Ma", "J", "J", "A", "Se", "Oc", "No", "De"];

           $scope.labels = [];
           for(i=30; i>-1; i--){
               var today = new Date();
               today.setDate(today.getDate() - i);
               var day = today.getDate();
               $scope.labels.push(monthNamesSimple[today.getMonth()]+' '+day);
           }

           $scope.onClick = function (points, evt) {
             console.log(points, evt);
           };

           $scope.datasetOverride =
            {
              label: "Posts",
              lineTension: 0.3,
              backgroundColor: "rgba(2,117,216,0.2)",
              borderColor: "rgba(2,117,216,1)",
              pointRadius: 5,
              pointBackgroundColor: "rgba(2,117,216,1)",
              pointBorderColor: "rgba(255,255,255,0.8)",
              pointHoverRadius: 5,
              pointHoverBackgroundColor: "rgba(2,117,216,1)",
              pointHitRadius: 20,
              pointBorderWidth: 2,
           };
           $scope.options = {
             scales: {
              xAxes: [{
                  time: {
                    unit: 'date'
                  },
                  gridLines: {
                    display: false
                  },
                  ticks: {
                    maxTicksLimit: 12
                  }
              }],
              yAxes: [{
                ticks: {
                  min: 0,
                  max: 20,
                  maxTicksLimit: 4
                },
                gridLines: {
                  color: "rgba(0, 0, 0, .125)",
                }
              }],
            },
               legend: {
                   display: false
               }
           };

    }]);
}