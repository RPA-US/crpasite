import logging
import requests
from urllib.parse import urljoin
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.mail import EmailMessage
from django.template import loader
from django.template.context_processors import csrf
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from datetime import datetime
from rest_framework import status, permissions
from rest_framework.views import APIView
from .serializers import ProjectStatusSerializer
from .settings import EMAIL_HOST_USER, MICROSERVICE_RPA_URL, MICROSERVICE_ML_URL, MASTER_TOKEN_ADMIN, MICROSERVICE_CORE_URL
from .forms import ProjectForm, AIRPAPIRegistrationForm, UserForm
from .models import WebProjects


def index(request):
    """
    Vista principal
    :param request:
    :return:
    """
    return render(request, 'index.html',
                  context={'title': _("Proyectos"), 'subtitle': _('Listado de Proyectos')})


@login_required
def profile(request):
    """Renders the user profile page."""
    assert isinstance(request, HttpRequest)

    return render(request, 'profile.html', context={
        'title': _('Perfil de usuario'),
        'year': datetime.now().year,
        'subtitle': _('Gestione su cuenta de AIRPAPI')})

def examples_view(request):
    """
    Vista principal
    :param request:
    :return:
    """
    return render(request, 'utilities_examples.html',
                  context={'title': "Ejemplos de casos de Uso", 'subtitle': 'Ejemplos de uso de las utilidades desarrolladas por DaliaSoft'})


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'contact.html',
        {
            'title': _('Contacto'),
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'about.html',
        {
            'title': 'DaliaSoft',
            'year': datetime.now().year,
        }
    )

def custom_login(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'login.html',
        {
            'title': _('Login'),
            'subtitle':'Introduzca Credenciales',
            'year': datetime.now().year,
        }
    )



def register_user(request):
    if request.method == 'POST':
        form = AIRPAPIRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            form.write_features()

            destinatarios = [EMAIL_HOST_USER]
            subject = loader.render_to_string('register/mail_to_system_subject.html',
                                              {'user': form.cleaned_data['username']})
            message = loader.render_to_string('register/mail_to_system.html',
                                              {'user': form.cleaned_data['username'],
                                               'surname': form.cleaned_data['first_name'],
                                               'name': form.cleaned_data['last_name'],
                                               'mail': form.cleaned_data['email']
                                               })
            msg = EmailMessage(subject, message, bcc=destinatarios)
            msg.send()
            return redirect('home')
        else:
            return render(request, 'register/register.html', {'form': form, 'title': _('Registro de usuario'),
                                                              "subtitle":_('Rellene el siguiente formulario para '
                                                                           'solicitar su registro en AIRPAPI. En '
                                                                           'breve el Sistema dará respuesta a su '
                                                                           'solitud.')})

    elif request.method == 'GET':
        if not request.user.is_authenticated:
            form = AIRPAPIRegistrationForm()
            token = {}
            token.update(csrf(request))
            token['form'] = form
            return render(request, 'register/register.html', {'form': form, 'title': _('Registro de usuario'),"subtitle":_('Rellene el siguiente formulario para '
                                                                           'su registro en AIRPAPI')})
        else:
            return redirect('home')


@login_required
def profile(request):
    """Renders the user profile page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'GET':
        form = UserForm(instance=request.user)

        return render(request, 'profile.html', context={
            'form': form,
            'title': _('Perfil de usuario'),
            'year': datetime.now().year,
            'subtitle': _('Gestione su cuenta de AIRPAPI')})
    elif request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            logging.exception('Error al guardar el formulario: {}'.format(form.errors))
        return redirect('home')


@login_required
def manage_project_view(request, id_project):
    """
    Muestra la vista de creación y edición de proyectos en un formulario. Sólo muestra los campos que pueden modificarse
    :param request:
    :param id_project: Clave primaria del proyecto para modificar un proyecto creado. Valor 0 para llamadas de nuevo proyecto.
    :return:
    """
    if request.method == 'GET':
        if int(id_project) is 0:
            # Si el parámetro es 0 corresponde a la creación de un nuevo proyecto
            form = ProjectForm(initial={'web_cd_user': request.user})
            project_name = _('Nuevo proyecto')
        else:
            try:
                project = WebProjects.objects.get(pk=int(id_project))
                form = ProjectForm(instance=project)
                project_name =  _('Proyecto %(project)s')%{'project': project.web_tx_name}
            except WebProjects.DoesNotExist:
                raise Http404(_('No existe el proyecto buscado'))

        return render(request, 'manage_project.html', context={'form': form, 'title': _('Gestion de proyectos'),
                                                               'subtitle': project_name, 'id_project': int(id_project)})
    elif request.method == 'POST':
        if int(id_project) is 0:
            form = ProjectForm(request.POST)
        else:
            try:
                project = WebProjects.objects.get(pk=int(id_project))
                form = ProjectForm(request.POST, instance=project)
            except WebProjects.DoesNotExist:
                raise Http404(_('No existe el proyecto buscado'))

        if form.is_valid():
            form.save()
        else:
            logging.debug('Error al guardar el formulario: {}'.format(form.errors))
        return redirect('home')


@login_required
def projects_view(request):
    """
    Muestra los proyectos asociados a un usuario, indicando el módulo más actualizado que ha se usado.
    """
    try:
        user_projects = WebProjects.objects.filter(web_cd_user=request.user, web_lg_deleted=False).order_by('-web_fh_updated','-web_fh_created')
        return render(request, 'projects_panel.html', context={'title': _('Panel de proyectos'), 'projects': user_projects})
    except Exception as ex:
        logging.debug('Error al obtener los proyectos. Error {}'.format(str(ex)))
        raise Http404(_('Error al obtener los proyectos'))



@login_required
def recommend_list_view(request, id_project,id_survey):
    """
    Genera la vista con el listado de las recomendaciones para el proyecto seleccionado.
    """
    try:
        project = WebProjects.objects.get(pk=int(id_project))
        url_recommendation = MICROSERVICE_FUZZY_URL.rstrip('/')
        url_survey = MICROSERVICE_SURVEY_URL.rstrip('/')
        token_admin = MASTER_TOKEN_ADMIN

        return render(request, 'recomm_panel.html', context={'title':'{} {}'.format(_('Proyecto'),project.web_tx_name),
                                                             'subtitle':  _('Recomendaciones'),
                                                             'token': token_admin, 'url_survey': url_survey,
                                                             'url_recommendation': url_recommendation,
                                                             'active_module': 'recomm',
                                                             'id_survey': id_survey,
                                                             'project': project})
    except Exception as ex:
        logging.debug('Error al obtener los proyectos. Error {}'.format(str(ex)))
        raise Http404(_('Error al obtener los proyectos'))

@login_required
def datasets_list_view(request, id_project):
    """
    Genera la vista con el listado de las recomendaciones para el proyecto seleccionado.
    """
    try:
        project = WebProjects.objects.get(pk=int(id_project))
        url_dataset = MICROSERVICE_MODELLER_URL.rstrip('/')
        url_survey = MICROSERVICE_SURVEY_URL.rstrip('/')
        token_admin = MASTER_TOKEN_ADMIN

        return render(request, 'modeller_panel.html', context={'title':'{} {}'.format(_('Proyecto'),project.web_tx_name),
                                                             'subtitle': _('Datasets'),
                                                             'token': token_admin, 'url_survey': url_survey,
                                                             'url_dataset': url_dataset,
                                                             'active_module': 'model',
                                                             'project': project})
    except Exception as ex:
        logging.debug('Error al obtener los proyectos. Error {}'.format(str(ex)))
        raise Http404(_('Error al obtener los proyectos'))


@login_required
def load_dataset_view(request, source, identifiers ,id_project):
    try:
        project = WebProjects.objects.get(pk=int(id_project))
        url_modeller = MICROSERVICE_MODELLER_URL.rstrip('/')
        url_survey = MICROSERVICE_SURVEY_URL.rstrip('/')
        token_admin = MASTER_TOKEN_ADMIN

        return render(request, 'modeller.html', context={'title':'{} {}'.format(_('Proyecto'),project.web_tx_name),
                                                         'subtitle': _('Datasets'), 'source':source,
                                                         'token': token_admin, 'active_module': 'model',
                                                         'project': project, 'url_survey': url_survey,
                                                         'url_modeller': url_modeller, 'identifiers':identifiers})
    except Exception as ex:
        logging.exception('Error al cargar la vista de cargar dataset. Error {}'.format(str(ex)))
        raise Http404(_('Error al cargar la vista de carga de dataset'))


@login_required
def surveys_list_view(request, id_project, id_survey):
    """
    Genera la vista con el listado de las entrevistas para el proyecto seleccionado. Carga las entrevistas con una
    llamada al módulo Survey
    """
    try:
        project = WebProjects.objects.get(pk=int(id_project))
        url_survey = MICROSERVICE_SURVEY_URL.rstrip('/')
        url_fuzzy = MICROSERVICE_FUZZY_URL.rstrip('/')
        token_admin = MASTER_TOKEN_ADMIN
        return render(request, 'surveys_panel.html', context={'subtitle': _('Entrevistas'), 'token': token_admin,
                                                              'url_survey': url_survey, 'url_fuzzy': url_fuzzy,
                                                              'active_module': 'charact', 'project':project,
                                                              'id_survey': id_survey,
                                                              'title': '{} {}'.format(_('Proyecto'), project.web_tx_name)})
    except Exception as ex:
        logging.debug('Error al obtener los proyectos. Error {}'.format(str(ex)))
        raise Http404(_('Error al obtener los proyectos. Inténtelo de nuevo, si sigue '
                        'persistiendo el error póngase en contacto con el administrador de la página'))


@login_required
def models_list_view(request, id_project):
    """
    Genera la vista con el listado de modelos del implementador para el proyecto seleccionado.
    """
    try:
        project = WebProjects.objects.get(pk=int(id_project))
        url_implementer = MICROSERVICE_IMPLEMENTER_URL.rstrip('/')
        token_admin = MASTER_TOKEN_ADMIN
        return render(request, 'models_panel.html', context={'subtitle': _('Modelos'), 'token': token_admin,
                                                          'active_module': 'implem', 'project': project,
                                                             'url_implementer': url_implementer,
                                                          'title': '{} {}'.format(_('Proyecto'), project.web_tx_name)})
    except Exception as ex:
        logging.debug('Error al obtener el listado de modelos. Error {}'.format(str(ex)))
        raise Http404(_('Error al obtener el listado de modelos. Inténtelo de nuevo, si sigue '
                        'persistiendo el error póngase en contacto con el administrador de la página'))


@login_required
def delete_project_view(request, id_project):
    """
    Elimina de base de datos el proyecto seleccionado.
    """
    try:
        # Llama al método de eliminar los elementos asociados al proyecto
        external_id_project = WebProjects.objects.get(pk=id_project).web_tx_identifier
        survey_url = urljoin(MICROSERVICE_SURVEY_URL, 'delete-project-surveys/{}'.format(external_id_project))
        response = requests.delete(survey_url, headers={'Authorization': 'Token {}'.format(MASTER_TOKEN_ADMIN)})
        if response.status_code == status.HTTP_200_OK:
            # Si se han eliminado los elementos, se procede a la eliminación del proyecto
            project = WebProjects.objects.get(pk=int(id_project))
            project.web_lg_deleted = True
            project.save()
        else:
            raise Http404(_('Error al eliminar los elementos asociados al proyecto. Inténtelo de nuevo, si sigue '
                            'persistiendo el error póngase en contacto con el administrador de la página'))
    except WebProjects.DoesNotExist:
        logging.exception(_('No existe el proyecto a eliminar'))
        raise Http404(_('No se ha encontrado el proyecto a eliminar. Inténtelo de nuevo, si sigue '
                        'persistiendo el error póngase en contacto con el administrador de la página'))
    return redirect('home')


class ProjectStatus(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    @staticmethod
    def get_object(id_project):
        try:
            return WebProjects.objects.get(web_tx_identifier=id_project, web_lg_deleted=False)
        except WebProjects.DoesNotExist:
            raise

    def put(self, request, id_project):
        """
        Actualiza el estado del proyecto con el identificador pedido.
        Parámetros:
            - id_recomm: Identificador de proyecto.
            - recomm_status: Nuevo estado en el que se encuentra el proyecto.

        Devolución:
            - JSON con el identificador de proyecto y el nuevo estado del mismo. Error en caso de encontrar algún fallo en la petición.
        """
        try:
            project = self.get_object(id_project)
            serializer = ProjectStatusSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'success': 'Actualización de estado correcta', 'data': serializer.data},
                                    status=status.HTTP_200_OK)
            return JsonResponse({'error': 'Error al actualizar. Error {}'.format(serializer.errors)},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return JsonResponse({'error': 'No existe ningun proyecto con el identificador requerido'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

    def get(self, request, id_project):
        """
        Devuelve el estado en el que se encuentra el proyecto con el identificador pedido
        Parámetros:
            - id_recomm: Identificador de proyecto.

        Devolución:
            - JSON con el identificador de proyecto y el estado del mismo. Error en caso de encontrar algún fallo en la petición.
        """
        try:
            status_project = self.get_object(id_project)
            serializer = ProjectStatusSerializer(status_project)
            return JsonResponse({'success':'Lectura de estado correcta', 'data':serializer.data}, status=status.HTTP_200_OK)
        except WebProjects.DoesNotExist:
            return JsonResponse({'error': 'No existe ningun proyecto con el identificador requerido'},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            logging.exception(str(ex))
            return JsonResponse({'error': 'Error al recuperar el estado del proyecto'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
