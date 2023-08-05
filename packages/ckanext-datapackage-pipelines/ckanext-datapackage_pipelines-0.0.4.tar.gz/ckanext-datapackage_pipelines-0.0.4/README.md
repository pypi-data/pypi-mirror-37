# ckanext-datapackage_pipelines

[![CKAN pipelines server Docker image: orihoch/datapackage-pipelines-ckan](https://img.shields.io/badge/CKAN%20pipelines%20server%20Docker%20image-orihoch/datapackage--pipelines--ckanext-darkgreen.svg)](https://hub.docker.com/r/orihoch/datapackage-pipelines-ckanext/)

Integrate [datapackage-pipelines](https://github.com/frictionlessdata/datapackage-pipelines) with CKAN

Minimal supported CKAN version: 2.8.1

## Installation

### Install the plugin

* Create a directory to hold the pipelines, ckan pipeline extensions write to that directory
  * `sudo mkdir -p /var/ckan/pipelines`
  * `sudo chown -R $USER:$GROUP /var/ckan`
  * This directory should be shared between the pipelines server and CKAN
* Activate your CKAN virtual environment
* Install the ckanext-datapackage_pipelines package into your virtual environment:
  * `pip install ckanext-datapackage_pipelines`
* Add `datapackage_pipelines` to the `ckan.plugins` setting in your CKAN
* Restart CKAN.

### Start the datapackage-pipelines server

The following command starts a local pipelines server for development on the host network

CKAN_API_KEY should be a CKAN user's api key which has sysadmin privileges

If you are running the CKAN Redis server on the same host, you should modify the port to prevent collision
with the pipelines server Redis which runs on port 6379.

The pipelines server runs on port 5050.

```
docker run -v /var/ckan/pipelines:/pipelines:rw \
           -e CKAN_API_KEY=*** \
           -e CKAN_URL=http://localhost:5000 \
           --net=host \
           orihoch/datapackage-pipelines-ckanext server
```

## Usage

Pipelines dashboard is available publically at http://your-ckan-url/pipelines

CKAN plugins can use the pipelines server by implementing the `IDatapackagePipelines` interface which contains the following  methods:

* `register_pipelines` - returns the pipelines name (usually the name of the plugin) and directory to get the plugin's
pipelines from. When CKAN is restarted the pipelines are copied by default to /var/ckan/pipelines - this directory should be
shared between CKAN and the pipelines server. If the plugin pipelines directories contains a `requirements.txt` it will be
installed on restart of the pipelines server.
* `get_pipelines_config` - returns a dict of key-value pairs containing the plugin's configuration or other data which should be available to the pipeline processors.

Pipeline processors can get this configuration using  `datapackage_pipelines_ckanext.helpers.get_plugin_configuration(plugin_name)`.

The following pipelines processors are available:

* `ckanext.dump_to_path` - same as standard library `dump.to_path` but dumps to the CKAN data directory.
  * parameters:
  * `plugin`: **required** name of the plugin
  * `out-path`: relative path within the plugin's data directory

* `ckanext.load_resource` - same as standard library `load_resource` but loads from CKAN data directory.
  * parameters:
  * `path`: **required** relative path to the datapackage in the plugin's data directory
  * `plugin`: **required** the plugin's name

To support pipeline dependencies, rename your `pipeline-spec.yaml` to `ckanext.source-spec.yaml`

Following is an example pipeline spec where the `download_data` pipeline will run on a schedule
and after each scheduled run the `load_data_to_ckan` pipeline will run:

```
download_data:
  schedule:
    crontab: "1 2 * * *"
  pipeline:
  - ...

load_data_to_ckan:
  dependencies:
  - ckanext-pipeline: your_plugin_name download_data
```

## CKAN Plugin Configuration

Following are the supported configurations and default values

```
ckanext.datapackage_pipelines.directory = /var/ckan/pipelines
ckanext.datapackage_pipelines.dashboard_url = http://localhost:5050
```
