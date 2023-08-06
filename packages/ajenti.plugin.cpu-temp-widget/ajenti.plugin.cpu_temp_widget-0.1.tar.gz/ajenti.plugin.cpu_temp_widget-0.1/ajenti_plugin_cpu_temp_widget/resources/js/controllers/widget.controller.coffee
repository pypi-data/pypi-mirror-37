angular.module('ajenti.cpu_temp_widget').controller 'CpuTempWidgetController', ($scope) ->
    # $scope.widget is our widget descriptor here
    $scope.$on 'widget-update', ($event, id, data) ->
        if id != $scope.widget.id
            return
        $scope.core = data

angular.module('ajenti.cpu_temp_widget').controller 'CpuTempWidgetConfigController', ($scope, $http) ->
    $http.get("/api/cpu/cores").success (data) ->
        $scope.cores = data
    .error (err) ->
        $scope.cores = null



