# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2017, 2018 CERN.
#
# REANA is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# REANA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# REANA; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.
"""REANA cluster client configuration."""

import pkg_resources

from .backends.kubernetes import KubernetesBackend

cluster_spec_default_file_path = pkg_resources.resource_filename(
    'reana_cluster', 'configurations/reana-cluster.yaml')
"""REANA cluster specification file default location."""

generated_cluster_conf_default_path = './cluster_config/'
"""Default location to output configuration files for REANA cluster backend."""

cluster_spec_schema_file_path = pkg_resources.resource_filename(
    'reana_cluster', 'schemas/reana-cluster.json')
"""REANA cluster specification schema location."""

supported_backends = {
    'kubernetes': KubernetesBackend,
}
"""Dictionary to extend REANA cluster with new cluster backend."""

reana_env_exportable_info_components = ['reana-server']
"""Components which information will be produced by ``reana-client env``."""

reana_cluster_ready_necessary_components = ['cwl-default-worker',
                                            'job-controller',
                                            'message-broker',
                                            'server',
                                            'workflow-controller',
                                            'workflow-monitor',
                                            'yadage-default-worker',
                                            'zeromq-msg-proxy']
"""Components which must be running for the cluster status to be ready."""
