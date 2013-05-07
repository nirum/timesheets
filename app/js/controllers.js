'use strict';

/* Controllers */

function ProjectListCtrl($scope, Project) {
   $scope.metadata = Project.query();
}

function ProjectDetailCtrl($scope, $routeParams, Project) {
   $scope.name = $routeParams.projectname;
   $scope.timestamps = Project.get({
      name: 'projects/' + $routeParams.projectname
   })
}

function TmanCtrl($scope, $timeout, angularFireCollection) {
   var url = 'https://tman.firebaseio.com/projects';
   $scope.projects = angularFireCollection(url);
   $scope.projectname = "";
   $scope.addTime = function() {
      var now = new Date().getTime();
      $scope.projects.add({
         project: $scope.projectname,
         timestamp: now
      });
      $scope.projectname = "";
   }
}

function UserCtrl($scope, $timeout, angularFire) {
   var ref = new Firebase('https://tman.firebaseio.com');
   var authClient = new FirebaseAuthClient(ref, function(err, user) {
			 if (err) {
					 console.log('err!');
					 console.log(err);
					 console.log(JSON.stringify(err));
			 }
			 else {
					 if (user) {
							 console.log('logged in!');
					 }
					 else {
							 console.log('logged out!');
					 }
			 }
			//if (!err && user) {
			//angularFire(ref, $scope, "test");
			//}
   });
   //$scope.email = "";
   //$scope.password = "";
   //$scope.rememberme = true;
   //$scope.login = function() {
      //auth.login('password', {
         //email: $scope.email,
         //password: $scope.password,
         //rememberMe: $scope.rememberme
      //});
   //}
}

function ChatCtrl($scope, $timeout, angularFireCollection) {
   $scope.header = "Chat";
   var url = 'https://tman.firebaseio.com/chat';
   $scope.messages = angularFireCollection(url);
   $scope.username = 'Guest' + Math.floor(Math.random() * 101);
   $scope.addMessage = function() {
      $scope.messages.add({
         from: $scope.username,
         content: $scope.message
      });
      $scope.message = "";
   }
}
