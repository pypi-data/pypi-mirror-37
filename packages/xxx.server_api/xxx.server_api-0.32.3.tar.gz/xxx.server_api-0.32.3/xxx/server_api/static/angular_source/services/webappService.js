module.exports = function(myModule) {
    myModule.service('WebappService', [
    '$http', '$rootScope', '$location', '$cookies', 'NumbersConfig',
     function($http, $rootScope, $location, $cookies, NumbersConfig) {

        var target_url = NumbersConfig.remote_webapp + '/webapp_';

        function registerNewUser(contactNumber, hashed_password, nickName, callback) {
            var payload = {'contact_number': contactNumber,
                           'hashed_password': hashed_password,
                            'nick_name': nickName};
            var promise = $http.post(target_url+'register', payload).then(function (response) {
                cp = response.data;
                if(response.status === 200){
                    alert('Registration was successful, now you may login.');
                    $location.path('/login');

                }else{
                    alert('Error during registration.');
                    callback(cp);
                }
            });
        }

        function login(contactNumber, hashed_password, callback) {
            var payload = {'contact_number': contactNumber,
                           'hashed_password': hashed_password};
            var promise = $http.post(target_url+'login', payload).then(function (response) {
                cp = response.data;

                if(cp['data']['status'] === 200){
                    var expDatePageSize = new Date();
                    expDatePageSize.setDate(expDatePageSize.getDate() + 7);
                    $cookies.put('contactNumber', contactNumber, {'expires': expDatePageSize});
//                    $cookies.put('savePassword', true);
//                    if(savePassword){
//                        $cookies.put('hashed_password', hashed_password, {'expires': expDatePageSize});
//                        $rootScope.hashed_password = hashed_password;
//                    }
                    $rootScope.contactNumber = contactNumber;
//                    $rootScope.savePassword = savePassword;
                    $location.path('/index');
                }else{
                    alert('Error during login. User doesnt exist or password in not correct.');
                    callback(cp);
                }
            });
        }
        function new_post(contactNumber, callback) {
                    var payload = {'contact_number': contactNumber,
                                   'session': $cookies.get('session')};
                    console.log('session is');
                    console.log($cookies.get('session'));
                    var promise = $http.post(target_url+'new_post', payload).then(function (response) {
                        cp = response.data;
                        console.log('cp');
                        console.log(cp);
                        if(cp['data']['status'] === 200){
                           console.log('response is 200');
                        }else{
                            alert('Error during login. User doesnt exist or password in not correct.');
                            callback(cp);
                        }
                    });
                }

        return {
            registerNewUser:registerNewUser,
            login:login,
            new_post:new_post
        }
    }]);
}
