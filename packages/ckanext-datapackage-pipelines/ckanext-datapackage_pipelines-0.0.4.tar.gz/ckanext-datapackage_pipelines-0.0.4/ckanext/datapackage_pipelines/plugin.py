import os

from flask import Blueprint

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckanext.datapackage_pipelines.interfaces import IDatapackagePipelines
from ckanext.datapackage_pipelines.utils import copytree_exists_ok
from ckanext.datapackage_pipelines import views, auth, constants


class Datapackage_PipelinesPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IAuthFunctions)

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'datapackage_pipelines')
        pipelines_directory = config_.get('ckanext.datapackage_pipelines.directory', constants.DEFAULT_PIPELINES_DIRECTORY)
        for plugin in plugins.PluginImplementations(IDatapackagePipelines):
            pipelines_dir, pipelines_src = plugin.register_pipelines()
            copytree_exists_ok(pipelines_src, os.path.join(pipelines_directory, pipelines_dir))

    def get_blueprint(self):
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = u'templates'
        blueprint.add_url_rule(u'/pipelines', u'datapackage_pipelines_dashboard', views.dashboard)
        blueprint.add_url_rule(u'/pipelines/config/<plugin_name>', u'datapackage_pipelines_config', views.config)
        return blueprint

    def get_helpers(self):
        def get_dashboard_url():
            return toolkit.config.get('ckanext.datapackage_pipelines.dashboard_url', constants.DEFAULT_DASHBOARD_URL)
        return {'get_datapackage_pipelines_dashboard_url': get_dashboard_url,}

    def get_auth_functions(self):
        return {constants.CONFIG_ACTION_NAME: auth.config,}
