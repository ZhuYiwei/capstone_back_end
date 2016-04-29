from django.conf.urls import url
__author__ = 'Yiwei'

urlpatterns = [
    url(r'^$', 'ipm.views.home', name='home'),

    # admin
    url(r'^add/', 'ipm.views.add', name='add'),

    url(r'^add_patent/', 'ipm.views.add_patent', name='add_patent'),
    url(r'^add_insight/', 'ipm.views.add_insight', name='add_insight'),
    url(r'^edit_patent/(?P<patent_id>\d+)$', 'ipm.views.edit_patent', name='edit_patent'),
    url(r'^edit_insight/(?P<insight_id>\d+)$', 'ipm.views.edit_insight', name='edit_insight'),
    url(r'^delete_patent/(?P<patent_id>\d+)$', 'ipm.views.delete_patent', name='delete_patent'),
    url(r'^delete_insight/(?P<insight_id>\d+)$', 'ipm.views.delete_insight', name='delete_insight'),

    url(r'^get_patent_json/', 'ipm.views.get_patent_json'),
    url(r'^developer_home/', 'ipm.views.developer_home', name='developer_home'),
    url(r'^patents/', 'ipm.views.get_patents', name='get_patents'),
    url(r'^insights/', 'ipm.views.get_insights', name='get_insights'),

    # mobile query
    url(r'^get_patent_list/', 'ipm.views.get_patent_list', name='get_patent_list'),
    url(r'^get_patent/(?P<patent_id>\d+)$', 'ipm.views.get_patent', name='get_patent'),
    url(r'^get_patent_model/(?P<patent_id>\d+)$', 'ipm.views.get_patent_model', name='get_patent_model'),

    url(r'^get_insight_list/', 'ipm.views.get_insight_list', name='get_insight_list'),
    url(r'^get_insight/(?P<insight_id>\d+)$', 'ipm.views.get_insight', name='get_insight'),

    url(r'^search_patent/', 'ipm.views.search_patent', name='search_patent'),
    url(r'^search_insight/', 'ipm.views.search_insight', name='search_insight'),

    url(r'^send_email/', 'ipm.views.send_email', name='send_email'),
    url(r'^today/', 'ipm.views.today', name='today'),


]
