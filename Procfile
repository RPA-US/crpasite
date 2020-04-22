% prepara el repositorio para su despliegue. 
release: sh -c 'cd airpapi && python manage.py migrate'
% especifica el comando para lanzar Decide
web: sh -c 'cd airpapi && gunicorn decide.wsgi --log-file -'