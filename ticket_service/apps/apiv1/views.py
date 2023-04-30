from django.views.generic import TemplateView

# Create your views here.


class SwaggerDocs(TemplateView):
    template_name = "apiv1/swagger.html"
