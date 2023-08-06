module.exports = function(myModule) {
    myModule.service('CouchdbService',['$http', '$rootScope', '$cookies', 'NumbersConfig',
     function($http, $rootScope, $cookies, NumbersConfig) {

        function getNumbersBlock(currentPage, pageSize, callback){
    //        ?limit=5&skip=5
            var query_url = NumbersConfig.remote_db +'/_design/numbers/_view/list_numbers?limit=' + pageSize.toString()+'&descending=true';
            if(currentPage != 0){
                var skip = currentPage * pageSize;
                query_url = query_url + '&skip=' + skip.toString();

                var expDateCurPage = new Date();
                expDateCurPage.setDate(expDateCurPage.getDate() + 1);
                $cookies.put('currentPage', currentPage, {'expires': expDateCurPage});
            }

            var promise = $http.get(query_url).then(function (response) {
                numbers = response.data.rows;
                callback(numbers)
            });
        }

        function getNumber(id, callback) {
            var query_url = NumbersConfig.remote_db +'/' + id;


            var promise = $http.get(query_url).then(function (response) {
                cp = response.data;
                callback(cp);
            });
        }

        function getNumbersCount(callback){
          var promise = $http.get(NumbersConfig.remote_db + '/').then(function(response){
          cp = response.data;
          callback(cp);
          });
        }

        return {
            getNumber:getNumber,
            getNumbersBlock:getNumbersBlock,
            getNumbersCount:getNumbersCount
        }
    }]);
}
