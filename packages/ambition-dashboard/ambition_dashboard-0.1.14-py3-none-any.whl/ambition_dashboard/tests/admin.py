from django.contrib.admin import AdminSite as DjangoAdminSite

from .models import SubjectConsent, SubjectLocator
from .models import SubjectRequisition, SubjectVisit, SubjectScreening


class AdminSite(DjangoAdminSite):
    site_title = 'Ambition Subject'
    site_header = 'Ambition Subject'
    index_title = 'Ambition Subject'
    site_url = '/administration/'


ambition_test_admin = AdminSite(name='ambition_test_admin')

ambition_test_admin.register(SubjectScreening)
ambition_test_admin.register(SubjectConsent)
ambition_test_admin.register(SubjectLocator)
ambition_test_admin.register(SubjectVisit)
ambition_test_admin.register(SubjectRequisition)
