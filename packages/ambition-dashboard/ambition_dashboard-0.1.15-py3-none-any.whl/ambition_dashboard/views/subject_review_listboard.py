from edc_subject_dashboard.views import SubjectReviewListboardView as Base

from ..model_wrappers import SubjectVisitModelWrapper


class SubjectReviewListboardView(Base):

    listboard_model = 'ambition_subject.subjectvisit'
    model_wrapper_cls = SubjectVisitModelWrapper
    navbar_name = 'ambition_dashboard'
