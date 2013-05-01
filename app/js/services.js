'use strict';

/* Services */

angular.module('tmanServices', ['ngResource']).
		factory('Project', function($resource) {
	return $resource('data/:name.json', {}, {
		query: {method:'GET', params:{name:'metadata'}, isArray:false}
	});
});
