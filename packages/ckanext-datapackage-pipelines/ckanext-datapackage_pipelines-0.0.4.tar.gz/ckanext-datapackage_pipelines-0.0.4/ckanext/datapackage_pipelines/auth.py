from ckan.plugins import toolkit
from ckanext.datapackage_pipelines import constants


def config(context, data_dict):
    if toolkit.check_access(constants.CONFIG_PRIVILEGE, context, data_dict):
        return {'success': True}
    else:
        raise toolkit.NotAuthorized()
