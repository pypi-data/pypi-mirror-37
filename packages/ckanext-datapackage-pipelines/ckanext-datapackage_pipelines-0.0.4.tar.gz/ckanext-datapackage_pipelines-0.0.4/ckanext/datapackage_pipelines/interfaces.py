# encoding: utf-8

import ckan.plugins.interfaces as interfaces


class IDatapackagePipelines(interfaces.Interface):

    def register_pipelines(self):
        # return 'ckanext-upload_via_email', os.path.join(os.path.dirname(__file__), '..', '..', 'pipelines')
        pass

    def get_pipelines_config(self):
        # Returns dict of key value configurations for the extension
        # This will be exposed to the pipelines server via an authenticated REST API
        pass
