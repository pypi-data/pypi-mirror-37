from django.urls import re_path
from grade_conversion_calculator.views import demo


urlpatterns = [
    re_path(r'^calculator-demo/?$', demo, name='calculator_demo'),
]
