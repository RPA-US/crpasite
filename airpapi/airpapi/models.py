import uuid
from urllib.parse import urljoin
from colorful.fields import RGBColorField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

# python manage.py makemigrations airpapi --settings=airpapi.settings

class WebMicroservices(models.Model):
    """
    Contiene información relacionada con los microservicios que componen el proyecto, así como los tokens guardados en
    el resto de microservicios. También contiene los enlaces a las URL de admin de los servicios.
    """
    web_id_microservice=models.AutoField(primary_key=True)
    web_tx_name=models.CharField(max_length=64,unique=True,verbose_name=_('Nombre'))
    web_tx_user=models.CharField(max_length=40,verbose_name=_('Token Usuario'))
    web_tx_admin = models.CharField(max_length=40, verbose_name=_('Token Administrador'))
    web_tx_urlbase=models.URLField(max_length=255, verbose_name=_('URL Base'))

    class Meta:
        managed = True
        db_table = 'web_microservices'
        verbose_name = _('Modulo AIRPAPI')
        verbose_name_plural = _('Modulos AIRPAPI')

    def __str__(self):
        return self.web_tx_name

    def get_admin_url(self):
        return urljoin(self.web_tx_urlbase, 'admin')


class WebProjects(models.Model):
    """
    Almacena la información relacionada con los proyectos que pueden ser creados y gestionados por los usuarios.
    """
    status_choices = ((0,_('Inicializado')),(1,_('Caracterizador')),(2,_('Recomendador')),(3,_('Modelador'))
                      ,(4,_('Implementador')))

    web_id_project = models.AutoField(primary_key=True)
    web_tx_name = models.CharField(max_length=32, verbose_name=_('Nombre'))
    web_tx_description = models.TextField(verbose_name=_('Descripción del proyecto'), null=True, blank=True)
    web_tx_identifier = models.CharField(max_length=40, verbose_name=_('Identificador de proyecto'), unique=True)
    web_cl_colour = RGBColorField(default='#3399CC', verbose_name=_('Color asociado'))
    web_tx_status = models.IntegerField(verbose_name=_('Estado del proyecto'), choices=status_choices, default=0)
    web_fh_created = models.DateTimeField(verbose_name=_('Fecha de creación'))
    web_fh_updated = models.DateTimeField(null=True, verbose_name=_('Fecha de actualización'), blank=True)
    web_lg_deleted = models.BooleanField(default=False, verbose_name=_('Borrado lógico'))
    web_cd_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, db_column='web_cd_user')

    class Meta:
        managed = True
        db_table = 'web_projects'
        verbose_name = _('Proyecto')
        verbose_name_plural = _('Proyectos')
        unique_together = (('web_tx_name','web_cd_user'),)

    def __str__(self):
        return self.web_tx_name

    def save(self, *args, **kwargs):
        # Con el if-else se comprueba si es una nueva entrada o la modificación de una ya creada
        if self._state.adding is True:
            # Si se está creando una nueva tabla rellena el campo fh_created
            self.web_fh_created = timezone.now()
            # Generación del identificador de proyecto
            self.web_tx_identifier = str(uuid.uuid4())
        else:
            # Para modificaciones, actualiza el campo fh_updated
            self.web_fh_updated = timezone.now()

        # Comprueba si no está asociado a ningún usuario para marcar el proyecto como eliminado lógicamente
        if self.web_cd_user is None:
            self.web_lg_deleted = True

        super(WebProjects, self).save(*args, **kwargs)