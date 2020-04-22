from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image_id = serializers.UUIDField(read_only=True)
    what_am_i_doing = serializers.RegexField(
        regex=r"^69$",
        help_text="test",
        default="69",
        allow_null=True
    )
    image_styles = serializers.ListSerializer(
        child=serializers.ChoiceField(choices=['wide', 'tall', 'thumb', 'social']),
        help_text="Parameter with Items"
    )
    upload = serializers.ImageField(help_text="image serializer help_text")