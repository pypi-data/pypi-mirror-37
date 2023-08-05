from django.conf import settings
from edc_subject_dashboard import SubjectVisitModelWrapper as BaseSubjectVisitModelWrapper
from django.urls.base import reverse


class SubjectVisitModelWrapper(BaseSubjectVisitModelWrapper):

    model = 'ambition_subject.subjectvisit'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')

    @property
    def dashboard_direct_href(self):
        return reverse('ambition_dashboard:subject_dashboard_url',
                       kwargs=dict(
                           subject_identifier=self.object.subject_identifier,
                           appointment=str(self.object.appointment.pk)))
