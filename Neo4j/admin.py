from django.contrib import admin
from Neo4j.models import *
from .models import *
from django.db import models
# from neo_admin import NeoAdmin
# Register your models here.

admin.site.register(Contact_Us)
admin.site.register(Main_Page_Content)
admin.site.register(About)
admin.site.register(Help)



# admin.site.register(signups, NeoAdmin)