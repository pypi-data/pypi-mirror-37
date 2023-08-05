from flask import render_template, jsonify
from ckan.plugins import toolkit
from ckanext.datapackage_pipelines import constants
from ckan import plugins
from ckanext.datapackage_pipelines.interfaces import IDatapackagePipelines
from os import path


def dashboard():
    return render_template(u'datapackage_pipelines/dashboard.html')


def config(plugin_name):
    assert toolkit.h.check_access(constants.CONFIG_ACTION_NAME)
    for plugin in plugins.PluginImplementations(IDatapackagePipelines):
        if plugin.name == plugin_name:
            return jsonify(dict(plugin.get_pipelines_config(),
                                data_path=path.join(toolkit.config.get('ckan.storage_path'), 'pipelines', plugin_name)))
    raise Exception()
