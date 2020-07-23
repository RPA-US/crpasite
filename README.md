[![pipeline status](https://gitlab.com/a8081/tfg/badges/master/pipeline.svg)](https://gitlab.com/a8081/tfg/-/commits/master)
[![coverage report](https://gitlab.com/a8081/tfg/badges/master/coverage.svg)](https://gitlab.com/a8081/tfg/-/commits/master)
# CRPAsite. Incremental and collaborative generation of a taxonomy applied to cognitive RPA components

To prepare the development environment, execute the following commands:

```
git clone https://gitlab.com/a8081/tfg
python3 -m venv env
source env/Scripts/activate
pip install -r requirement.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Python version = 3.7.8

Bachelor thesis. Software Engineering. University of Seville.