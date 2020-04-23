from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
import scaleapi
from drf_yasg import openapi
from drf_yasg.app_settings import swagger_settings
from drf_yasg.inspectors import (
    CoreAPICompatInspector,
    FieldInspector,
    NotHandled,
    SwaggerAutoSchema,
)
from drf_yasg.utils import no_body, swagger_auto_schema
from consumer import serializers

# from fastapi import APIRouter, FastAPI
# from fastapi.responses import JSONResponse

# Create your views here.

client = scaleapi.ScaleClient("test_449f3f6419964ef5ac641ca7f1d4738f")

# SCALE AI
# Test API Key: test_449f3f6419964ef5ac641ca7f1d4738f
# Test Callback Auth Key: test_auth_e921b8e5b13845a1a64f5264022c7358


@api_view(["GET"])
# @permission_classes((IsAuthenticated,))
class text_classification(viewsets.ModelViewSet):
    async def get(self, request):

        # response = client.create_categorization_task(
        #         callback_url='jozuzkie@sharklasers.com',
        #         instruction='Categorize this movie trailer',
        #         attachment_type='website',
        #         attachment='https://www.youtube.com/embed/6ZfuNTqbHE8',
        #         taxonomies={
        #         'watch': {
        #             'type': 'category',
        #             'description': 'Are you going to watch the full movie?',
        #             'choices': ['yes', 'no']
        #         },
        #         'genre': {
        #             'type': 'category',
        #             'description': 'What genre does it belong to?',
        #             'choices': ['Action', 'Adventure', 'Comedy', 'Crime', 'Drama'],
        #             'allow_multiple': True
        #         }
        #         }
        #     )

        req_instruction = "Categorize this movie trailer"
        req_attachment_type = "website"
        req_attachment = "https://www.youtube.com/embed/6ZfuNTqbHE8"
        req_taxonomies = {
            "watch": {
                "type": "category",
                "description": "Are you going to watch the full movie?",
                "choices": ["yes", "no"],
            },
            "genre": {
                "type": "category",
                "description": "What genre does it belong to?",
                "choices": ["Action", "Adventure", "Comedy", "Crime", "Drama"],
                "allow_multiple": True,
            },
        }

        # callback_url = self.request.callback_url
        # req_instruction = self.request.instruction
        # req_attachment_type = self.request.attachment_type
        # req_attachment = self.request.attachment
        # req_taxonomies = self.request.taxonomies

        response = await client.create_categorization_task(
            callback_url="https://airpaapi.herokuapp.com/",
            instruction=req_instruction,
            attachment_type=req_attachment_type,
            attachment=req_attachment,
            taxonomies=req_taxonomies,
        )

        return response


from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser, MultiPartParser


@swagger_auto_schema(
    method="get", operation_description="image GET description override"
)
@swagger_auto_schema(method="post", request_body=serializers.ImageUploadSerializer)
@swagger_auto_schema(
    method="delete",
    manual_parameters=[
        openapi.Parameter(
            name="delete_form_param",
            in_=openapi.IN_FORM,
            type=openapi.TYPE_INTEGER,
            description="this should not crash (form parameter on DELETE method)",
        )
    ],
)
@action(
    detail=True,
    methods=["get", "post", "delete"],
    parser_classes=(MultiPartParser, FileUploadParser),
)
def image(self, request, slug=None):
    """
    image method docstring
    """
    pass
