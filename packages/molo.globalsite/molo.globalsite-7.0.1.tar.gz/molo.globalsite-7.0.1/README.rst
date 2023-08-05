Molo Global Site
==================

.. image:: https://travis-ci.org/praekeltfoundation/molo.globalsite.svg?branch=develop
    :target: https://travis-ci.org/praekeltfoundation/molo.globalsite
    :alt: Continuous Integration

.. image:: https://coveralls.io/repos/github/praekeltfoundation/molo.globalsite/badge.svg?branch=develop
    :target: https://coveralls.io/github/praekeltfoundation/molo.globalsite?branch=develop
    :alt: Code Coverage

Provides code to help with identifying visitors’ country and redirecting them to the relevant country site or the global site using the Molo code base.

Getting Started
==================

Install molo.globalsite package::

   pip install molo.globalsite


In your app settings add::

   INSTALLED_APPS = (
      'molo.globalsite',
   )

   MIDDLEWARE = (
      'molo.globalsite.middleware.CountrySiteRedirectMiddleware'
   )

   # Global Site URL
   GLOBAL_SITE_URL = environ.get('GLOBAL_SITE_URL', '')

   # A path to geoip database.
   GEOIP_PATH = join(dirname(dirname(abspath(__file__))), 'geoip_db')

You can download the geoip database country database from `MaxMind`_ or copy it from molo/globalsite/geoip_db.

.. _MaxMind: http://dev.maxmind.com/geoip/legacy/geolite/#Downloads

Add Global site URL in your app urls.py::

   urlpatterns += patterns('',
        url(r'^globalsite/', include('molo.globalsite.urls', namespace='molo.globalsite', app_name='molo.globalsite')),
   )

Add the HTML block in your country site base template to allow users to change their country site::

    {% block country %}
        {% if settings.globalsite.GlobalSiteSettings.show_country %}
            {% trans "Country" %}: {{request.site}}
            <a href="{% url 'molo.globalsite:change_country' %}">{% trans "Change your country" %}</a>
        {% endif %}
    {% endblock %}


How users are redirected?
=========================

The middleware redirects the user by checking the session and if the country site is set in session it will redirect the user to the country site. If the country site is not in session and the geolocation is activated, it will use user's IP address to detect their country and redirect the user to the supported country site. However if the detected country is not supported or the geolocation is not activated it will display the list of supported country sites.

GlobalSite Settings
===================
The GlobalSite Settings can be accessed in the CMS under settings -> global site settings.

Activate Global Site:
When activated it will set the current site as the global site.

Activate Auto Redirect:
When activated it will automatically redirect the users to the country of their choice when accessing the global site.

Activate Geolocation:
When activated it will detect user's country and redirect them to the supported country site. If the detected country is not available it will display the available country sites.

Description:
Description will be displayed on the homepage of the global site.

show_country:
When activated, the country name will be displayed and users will be able to change their country site.

Country site and Region
=======================
Under Global site in CMS you are able to create the region/s of your country sites as well as the country site.




