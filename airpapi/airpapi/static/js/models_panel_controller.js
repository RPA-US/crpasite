angular.module('ModelsListApp',[])
    .controller('modelsListController',['$scope', '$http', modelsListController])
    .filter('translateStatus', function () {
       let MODEL_STATUS = {0:'Bloqueado', 1:'Sin entrenar', 2:'Entrenado'};
       return (input) => {
           if(MODEL_STATUS[input] !== undefined){
               return MODEL_STATUS[input];
           }
           else{
               return 'Estado erróneo';
           }
       }
    });

function modelsListController($scope, $http) {
    $scope.errorMessage = "";
    $scope.infoMessage = "";
    $scope.finderText = "";
    $scope.modelsList = "";

    /**
     * Método de inicio del controlador en el que pasar le la información con origen en el contexto de la página
     * @param token
     * @param idProject
     * @param externalIdProject
     * @param implementerURL
     */
    $scope.init = (token, idProject, externalIdProject, implementerURL) => {
        $scope.token = token;
        $scope.implementerURL = implementerURL;
        $scope.idProject = externalIdProject;
        getModelsList();
    };

    let getModelsList = () => {
        $http.defaults.headers.common.Authorization = 'Token ' + $scope.token;
        $http.get($scope.implementerURL + '/get-models-list/' + $scope.idProject).then(function (response) {
            if(response.data.success != null){
                $scope.modelsList = response.data.models_list;
            }
            else {
                console.log(response.data.error);
                $scope.errorMessage = response.data.error;
            }
        },
        (error) => {
            console.log(error.data);
            $scope.errorMessage = " Error en la conexión GET: " + $scope.implementerURL;
        })
    };

    /**
     * Hace la búsqueda de los términos introducidos en el buscador para filtrar los modelos de ML de la vista de
     * listado de modelos
     * @param modelDict Diccionario con la información de los modelos ML
     * @returns {boolean}
     */
    $scope.showElement = (modelDict) => {
        let MODEL_STATUS = {0:'Bloqueado', 1:'Sin entrenar', 2:'Entrenado'};
        // Si no hay nada introducido en el input text se deben mostrar todos los elementos
        if ($scope.cleanString($scope.finderText)) {
            // Se buscará el termino introducido en el nombre del dataset, de la entrevista y el estado
            let termsArray = [modelDict.name, modelDict.survey_name, MODEL_STATUS[modelDict.status]];
            termsArray = termsArray.filter(function(e){return e});
            for (let i in termsArray){
                // Se hace la búsqueda limpiando los términos a buscar y pasando el string a minúscula
                if ($scope.cleanString(termsArray[i]).includes($scope.cleanString($scope.finderText))){
                    return true
                }
            }
            return false
        }
        return true;
    };

    /**
     * Limpia los mensajes de aviso o error
     * @param source Elemento a limpiar
     */
    $scope.clearAlert = (source) => {
        if (source === 'error'){
            $scope.errorMessage = "";
        }
        else if (source === 'info'){
            $scope.infoMessage = "";
        }
    };

    /**
     * Método que limpia el buscador de elementos del panel
     */
    $scope.clearFinder = () => {
        $scope.finderText = "";
    };

    /**
     * Limpia una cadena eliminando tildes y pasando a minúsculas
     * @param inputText
     * @returns {string}
     */
    $scope.cleanString = (inputText) => {
        return inputText.normalize('NFD')
            .replace(/([aeio])\u0301|(u)[\u0301\u0308]/gi,"$1$2").normalize().toLowerCase();
    };
}