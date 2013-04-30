var app = angular.module('tman', []);

app.factory('Projects', function() {
   return [{
      "name": "testproject",
      "timestamps": [{
         "in": "Apr 24 08:16:23 2013",
         "out": "Apr 24 08:31:35 2013",
         "notes": "last commit"
      }, {
         "in": "Apr 23 01:26:42 2013",
         "out": "Apr 23 02:47:35 2013",
         "notes": "interesting feature"
      }, {
         "in": "Apr 19 12:53:56 2013",
         "out": "Apr 19 14:50:35 2013",
         "notes": "bugfix"
      }, {
         "in": "Apr 15 20:26:11 2013",
         "out": "Apr 15 21:11:35 2013",
         "notes": "initializing"
      }]
   }, {
      "name": "importantwork",
      "timestamps": [{
         "in": "Apr 28 22:56:46 2013",
         "out": "Apr 29 05:58:35 2013",
         "notes": "finalizing"
      }, {
         "in": "Mar 11 20:56:46 2013",
         "out": "Mar 12 12:07:45 2013",
         "notes": "bugfix"
      }, {
         "in": "Nov 18 22:56:46 2013",
         "out": "Nov 19 20:54:21 2012",
         "notes": "reverting to old version"
      }, {
         "in": "Dec 23 22:56:46 2013",
         "out": "Dec 24 17:23:59 2012",
         "notes": "beginning project that is important"
      }]
   }];
});

function ProjectCtrl($scope, Projects) {
   $scope.projects = Projects;
}
