from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,               {'fields': ['topic_description']}),
            ('Date information', {'fields': ['publication_date'], 'classes': ['collapse']}),
                ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
