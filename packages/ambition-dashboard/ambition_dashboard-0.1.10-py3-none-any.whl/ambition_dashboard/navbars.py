from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'ambition_dashboard' else False

navbar = Navbar(name='ambition_dashboard')

navbar.append_item(
    NavbarItem(
        name='screened_subject',
        title='Screening',
        label='screening',
        fa_icon='fas fa-user-plus',
        permission_codename='nav_screening_section',
        url_name=settings.DASHBOARD_URL_NAMES['screening_listboard_url'],
        no_url_namespace=no_url_namespace))

navbar.append_item(
    NavbarItem(
        name='consented_subject',
        title='Subjects',
        label='subjects',
        fa_icon='far fa-user-circle',
        permission_codename='nav_subject_section',
        url_name=settings.DASHBOARD_URL_NAMES['subject_listboard_url'],
        no_url_namespace=no_url_namespace))

navbar.append_item(
    NavbarItem(
        name='tmg_home',
        label='TMG Reports',
        fa_icon='fas fa-chalkboard-teacher',
        permission_codename='nav_tmg_section',
        url_name='ambition_dashboard:tmg_home_url',
        no_url_namespace=no_url_namespace))

navbar.append_item(
    NavbarItem(
        name='tmg_ae',
        label='AE Reports',
        # fa_icon='fas fa-chalkboard-teacher',
        permission_codename='nav_tmg_section',
        url_name=settings.DASHBOARD_URL_NAMES['tmg_ae_listboard_url'],
        no_url_namespace=no_url_namespace))

navbar.append_item(
    NavbarItem(
        name='tmg_death',
        label='Death Reports',
        # fa_icon='fas fa-chalkboard-teacher',
        permission_codename='nav_tmg_section',
        url_name=settings.DASHBOARD_URL_NAMES['tmg_death_listboard_url'],
        no_url_namespace=no_url_namespace))

navbar.append_item(
    NavbarItem(
        name='tmg_summary',
        label='Summary',
        # fa_icon='fas fa-chalkboard-teacher',
        permission_codename='nav_tmg_section',
        url_name=settings.DASHBOARD_URL_NAMES['tmg_summary_listboard_url'],
        no_url_namespace=no_url_namespace))

site_navbars.register(navbar)
