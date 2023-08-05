from ambition_auth.group_names import TMG
from ambition_dashboard.model_wrappers import AppointmentModelWrapper
from ambition_rando.view_mixins import RandomizationListViewMixin
from django.utils.safestring import mark_safe
from edc_appointment.constants import IN_PROGRESS_APPT
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_permissions.constants.group_names import AUDITOR
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from ....model_wrappers import SubjectVisitModelWrapper
from ....model_wrappers import SubjectConsentModelWrapper
from ....model_wrappers import SubjectLocatorModelWrapper


class DashboardView(
        EdcBaseViewMixin, SubjectDashboardViewMixin,
        RandomizationListViewMixin,
        NavbarViewMixin, BaseDashboardView):

    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model = 'ambition_subject.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    navbar_name = 'ambition_dashboard'
    navbar_selected_item = 'consented_subject'
    subject_locator_model = 'edc_locator.subjectlocator'
    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper
    visit_model_wrapper_cls = SubjectVisitModelWrapper

    def message_if_appointment_in_progress(self):
        group_names = [obj.name for obj in self.request.user.groups.all()]
        if (self.appointment.appt_status != IN_PROGRESS_APPT
                and TMG not in group_names
                and AUDITOR not in group_names):
            self.message_user(mark_safe(
                f'Wait!. Another user has switch the current appointment! '
                f'<BR>Appointment {self.appointment} is no longer "in progress".'))
