# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_policy import policy

from nova.policies import base


BASE_POLICY_NAME = 'os_compute_api:os-security-groups'


security_groups_policies = [
    policy.DocumentedRuleDefault(
        BASE_POLICY_NAME,
        base.RULE_ADMIN_OR_OWNER,
        """List, show, add, or remove security groups.

APIs which are directly related to security groups resource are deprecated:
Lists, shows information for, creates, updates and deletes
security groups. Creates and deletes security group rules. All these
APIs are deprecated.

APIs which are related to server resource are not deprecated:
Lists Security Groups for a server. Add Security Group to a server
and remove security group from a server. Expand security_groups in
server representation""",
    [
        {
            'method': 'GET',
            'path': '/os-security-groups'
        },
        {
            'method': 'GET',
            'path': '/os-security-groups/{security_group_id}'
        },
        {
            'method': 'POST',
            'path': '/os-security-groups'
        },
        {
            'method': 'PUT',
            'path': '/os-security-groups/{security_group_id}'
        },
        {
            'method': 'DELETE',
            'path': '/os-security-groups/{security_group_id}'
        },
        {
            'method': 'GET',
            'path': '/servers/{server_id}/os-security-groups'
        },
        {
            'method': 'POST',
            'path': '/servers/{server_id}/action (addSecurityGroup)'
        },
        {
            'method': 'POST',
            'path': '/servers/{server_id}/action (removeSecurityGroup)'
        },
        {
            'method': 'POST',
            'path': '/servers'
        },
        {
            'method': 'GET',
            'path': '/servers/{server_id}'
        },
        {
            'method': 'GET',
            'path': '/servers/detail'
        }
    ],
    deprecated_for_removal=True,
    deprecated_reason=(
        'Nova API extension concept has been removed in Pike. Those '
        'extensions have their own policies enforcement. As there is '
        'no extensions now, "os_compute_api:os-security-groups" policy '
        'for POST, GET /servers which was added for extensions is not '
        'needed any more. NOTE: This policy is deprecated only for '
        'POST /servers, GET /servers/{server_id} & GET /servers/detail. '
        'This policy for other API operations is still valid and not '
        'deprecated'
    ),
    deprecated_since='17.0.0'),
]


def list_rules():
    return security_groups_policies
