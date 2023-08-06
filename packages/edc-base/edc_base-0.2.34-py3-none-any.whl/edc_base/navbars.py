from edc_navbar import Navbar, NavbarItem, site_navbars


consent = Navbar(name='edc_base')

consent.append_item(
    NavbarItem(name='edc_base',
               label='Edc Base',
               fa_icon='fa-cogs',
               url_name='edc_base:home_url'))

site_navbars.register(consent)
