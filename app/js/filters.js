'use strict';

/* Filters */

angular.module('tmanFilters', []).
filter('timeAgo', function() {
  return function(input) {
			// input is an iso8601 string
			return moment(input).fromNow();
  };
}).
filter('timeDiff', function() {
  return function(input) {
			// input is a JSON object
			return moment(input["out"]).from(moment(input["in"])).replace(/^in/,'');
  };
});
