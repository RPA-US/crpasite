# TFG. A Framework for Sharing RPA Components Through Plataforms​

Ingeniería Informática. Ingeniería del Software. Trabajo Fin de Grado

Para preparar el entorno de desarrollo ejecute:
Version de python=python3.5

git clone https://gitlab.com/a8081/tfg
python3 -m venv env
source env/Scripts/activate
pip install -r requirement.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver