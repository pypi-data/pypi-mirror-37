# Copyright 2014 IBM Corp.
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

import copy

import mock
from oslo_config import cfg
import webob

from nova.api.openstack.compute import tenant_networks \
        as networks_v21
from nova import exception
from nova import test
from nova.tests import fixtures as nova_fixtures
from nova.tests.unit.api.openstack import fakes

CONF = cfg.CONF

NETWORKS = [
    {
        "id": 1,
        "cidr": "10.20.105.0/24",
        "label": "new net 1"
    },
    {
        "id": 2,
        "cidr": "10.20.105.0/24",
        "label": "new net 2"
    }
]

DEFAULT_NETWORK = [
    {
        "id": 3,
        "cidr": "None",
        "label": "default"
    }
]

NETWORKS_WITH_DEFAULT_NET = copy.deepcopy(NETWORKS)
NETWORKS_WITH_DEFAULT_NET.extend(DEFAULT_NETWORK)

DEFAULT_TENANT_ID = CONF.api.neutron_default_tenant_id


def fake_network_api_get_all(context):
    if (context.project_id == DEFAULT_TENANT_ID):
        return DEFAULT_NETWORK
    else:
        return NETWORKS


class TenantNetworksTestV21(test.NoDBTestCase):
    ctrlr = networks_v21.TenantNetworkController
    validation_error = exception.ValidationError
    use_neutron = False

    def setUp(self):
        super(TenantNetworksTestV21, self).setUp()
        # os-tenant-networks only supports Neutron when listing networks or
        # showing details about a network, create and delete operations
        # result in a 503 and 500 response, respectively.
        self.flags(enable_network_quota=True,
                   use_neutron=self.use_neutron)
        self.useFixture(nova_fixtures.RegisterNetworkQuota())
        self.controller = self.ctrlr()
        self.req = fakes.HTTPRequest.blank('')
        self.original_value = CONF.api.use_neutron_default_nets

    def tearDown(self):
        super(TenantNetworksTestV21, self).tearDown()
        CONF.set_override("use_neutron_default_nets", self.original_value,
                          group='api')

    def _fake_network_api_create(self, context, **kwargs):
        self.assertEqual(context.project_id, kwargs['project_id'])
        return NETWORKS

    @mock.patch('nova.network.api.API.disassociate')
    @mock.patch('nova.network.api.API.delete')
    def _test_network_delete_exception(self, delete_ex, disassociate_ex, expex,
                                       delete_mock, disassociate_mock):
        ctxt = self.req.environ['nova.context']

        if delete_mock:
            delete_mock.side_effect = delete_ex
        if disassociate_ex:
            disassociate_mock.side_effect = disassociate_ex

        if self.use_neutron:
            expex = webob.exc.HTTPInternalServerError
        self.assertRaises(expex, self.controller.delete, self.req, 1)

        if not self.use_neutron:
            disassociate_mock.assert_called_once_with(ctxt, 1)
            if not disassociate_ex:
                delete_mock.assert_called_once_with(ctxt, 1)

    def test_network_delete_exception_network_not_found(self):
        ex = exception.NetworkNotFound(network_id=1)
        expex = webob.exc.HTTPNotFound
        self._test_network_delete_exception(None, ex, expex)

    def test_network_delete_exception_policy_failed(self):
        ex = exception.PolicyNotAuthorized(action='dummy')
        expex = webob.exc.HTTPForbidden
        self._test_network_delete_exception(ex, None, expex)

    def test_network_delete_exception_network_in_use(self):
        ex = exception.NetworkInUse(network_id=1)
        expex = webob.exc.HTTPConflict
        self._test_network_delete_exception(ex, None, expex)

    @mock.patch('nova.network.api.API.delete')
    @mock.patch('nova.network.api.API.disassociate')
    def test_network_delete(self, disassociate_mock, delete_mock):
        ctxt = self.req.environ['nova.context']

        delete_method = self.controller.delete
        res = delete_method(self.req, 1)
        # NOTE: on v2.1, http status code is set as wsgi_code of API
        # method instead of status_int in a response object.
        if isinstance(self.controller, networks_v21.TenantNetworkController):
            status_int = delete_method.wsgi_code
        else:
            status_int = res.status_int
        self.assertEqual(202, status_int)

        disassociate_mock.assert_called_once_with(ctxt, 1)
        delete_mock.assert_called_once_with(ctxt, 1)

    def test_network_show(self):
        with mock.patch.object(self.controller.network_api, 'get',
                               return_value=NETWORKS[0]):
            res = self.controller.show(self.req, 1)
        self.assertEqual(NETWORKS[0], res['network'])

    def test_network_show_not_found(self):
        ctxt = self.req.environ['nova.context']
        with mock.patch.object(self.controller.network_api, 'get',
                               side_effect=exception.NetworkNotFound(
                                   network_id=1)) as get_mock:
            self.assertRaises(webob.exc.HTTPNotFound,
                              self.controller.show, self.req, 1)
        get_mock.assert_called_once_with(ctxt, 1)

    def _test_network_index(self, default_net=True):
        CONF.set_override("use_neutron_default_nets", default_net, group='api')

        expected = NETWORKS
        if default_net:
            expected = NETWORKS_WITH_DEFAULT_NET

        with mock.patch.object(self.controller.network_api, 'get_all',
                               side_effect=fake_network_api_get_all):
            res = self.controller.index(self.req)
        self.assertEqual(expected, res['networks'])

    def test_network_index_with_default_net(self):
        self._test_network_index()

    def test_network_index_without_default_net(self):
        self._test_network_index(default_net=False)

    @mock.patch('nova.objects.Quotas.check_deltas')
    @mock.patch('nova.network.api.API.create')
    def test_network_create(self, create_mock, check_mock):
        create_mock.side_effect = self._fake_network_api_create

        body = copy.deepcopy(NETWORKS[0])
        del body['id']
        body = {'network': body}
        res = self.controller.create(self.req, body=body)

        self.assertEqual(NETWORKS[0], res['network'])

    @mock.patch('nova.objects.Quotas.check_deltas')
    @mock.patch('nova.network.api.API.delete')
    @mock.patch('nova.network.api.API.create')
    def test_network_create_quota_error_during_recheck(self, create_mock,
                                                       delete_mock,
                                                       check_mock):
        create_mock.side_effect = self._fake_network_api_create
        ctxt = self.req.environ['nova.context']

        # Simulate a race where the first check passes and the recheck fails.
        check_mock.side_effect = [None, exception.OverQuota(overs='networks')]

        body = copy.deepcopy(NETWORKS[0])
        del body['id']
        body = {'network': body}
        self.assertRaises(webob.exc.HTTPForbidden,
                          self.controller.create, self.req, body=body)

        self.assertEqual(2, check_mock.call_count)
        call1 = mock.call(ctxt, {'networks': 1}, ctxt.project_id)
        call2 = mock.call(ctxt, {'networks': 0}, ctxt.project_id)
        check_mock.assert_has_calls([call1, call2])

        # Verify we removed the network that was added after the first quota
        # check passed.
        delete_mock.assert_called_once_with(ctxt, NETWORKS[0]['id'])

    @mock.patch('nova.objects.Quotas.check_deltas')
    @mock.patch('nova.network.api.API.create')
    def test_network_create_no_quota_recheck(self, create_mock, check_mock):
        create_mock.side_effect = self._fake_network_api_create
        ctxt = self.req.environ['nova.context']
        # Disable recheck_quota.
        self.flags(recheck_quota=False, group='quota')

        body = copy.deepcopy(NETWORKS[0])
        del body['id']
        body = {'network': body}
        self.controller.create(self.req, body=body)

        # check_deltas should have been called only once.
        check_mock.assert_called_once_with(ctxt, {'networks': 1},
                                           ctxt.project_id)

    @mock.patch('nova.objects.Quotas.check_deltas')
    def test_network_create_quota_error(self, check_mock):
        ctxt = self.req.environ['nova.context']

        check_mock.side_effect = exception.OverQuota(overs='networks')
        body = {'network': {"cidr": "10.20.105.0/24",
                            "label": "new net 1"}}
        self.assertRaises(webob.exc.HTTPForbidden,
                          self.controller.create, self.req, body=body)
        check_mock.assert_called_once_with(ctxt, {'networks': 1},
                                           ctxt.project_id)

    @mock.patch('nova.objects.Quotas.check_deltas')
    @mock.patch('nova.network.api.API.create')
    def _test_network_create_exception(self, ex, expex, create_mock,
                                       check_mock):
        ctxt = self.req.environ['nova.context']

        create_mock.side_effect = ex
        body = {'network': {"cidr": "10.20.105.0/24",
                            "label": "new net 1"}}
        if self.use_neutron:
            expex = webob.exc.HTTPServiceUnavailable
        self.assertRaises(expex, self.controller.create, self.req, body=body)
        check_mock.assert_called_once_with(ctxt, {'networks': 1},
                                           ctxt.project_id)

    def test_network_create_exception_policy_failed(self):
        ex = exception.PolicyNotAuthorized(action='dummy')
        expex = webob.exc.HTTPForbidden
        self._test_network_create_exception(ex, expex)

    def test_network_create_exception_conflictcidr(self):
        ex = exception.CidrConflict(cidr='dummy', other='dummy')
        expex = webob.exc.HTTPConflict
        self._test_network_create_exception(ex, expex)

    def test_network_create_exception_service_unavailable(self):
        ex = Exception
        expex = webob.exc.HTTPServiceUnavailable
        self._test_network_create_exception(ex, expex)

    def test_network_create_empty_body(self):
        self.assertRaises(exception.ValidationError,
                          self.controller.create, self.req, body={})

    def test_network_create_without_cidr(self):
        body = {'network': {"label": "new net 1"}}
        self.assertRaises(self.validation_error,
                          self.controller.create, self.req, body=body)

    def test_network_create_bad_format_cidr(self):
        body = {'network': {"cidr": "123",
                            "label": "new net 1"}}
        self.assertRaises(self.validation_error,
                          self.controller.create, self.req, body=body)

    def test_network_create_empty_network(self):
        body = {'network': {}}
        self.assertRaises(self.validation_error,
                          self.controller.create, self.req, body=body)

    def test_network_create_without_label(self):
        body = {'network': {"cidr": "10.20.105.0/24"}}
        self.assertRaises(self.validation_error,
                          self.controller.create, self.req, body=body)


class TenantNeutronNetworksTestV21(TenantNetworksTestV21):
    use_neutron = True

    def test_network_create(self):
        self.assertRaises(
            webob.exc.HTTPServiceUnavailable,
            super(TenantNeutronNetworksTestV21, self).test_network_create)

    def test_network_create_quota_error_during_recheck(self):
        self.assertRaises(
            webob.exc.HTTPServiceUnavailable,
            super(TenantNeutronNetworksTestV21, self)
                .test_network_create_quota_error_during_recheck)

    def test_network_create_no_quota_recheck(self):
        self.assertRaises(
            webob.exc.HTTPServiceUnavailable,
            super(TenantNeutronNetworksTestV21, self)
                .test_network_create_no_quota_recheck)

    def test_network_delete(self):
        self.assertRaises(
            webob.exc.HTTPInternalServerError,
            super(TenantNeutronNetworksTestV21, self).test_network_delete)


class TenantNetworksEnforcementV21(test.NoDBTestCase):

    def setUp(self):
        super(TenantNetworksEnforcementV21, self).setUp()
        self.controller = networks_v21.TenantNetworkController()
        self.req = fakes.HTTPRequest.blank('')

    def test_create_policy_failed(self):
        rule_name = 'os_compute_api:os-tenant-networks'
        self.policy.set_rules({rule_name: "project:non_fake"})
        exc = self.assertRaises(
            exception.PolicyNotAuthorized,
            self.controller.create,
            self.req, body={'network': {'label': 'test',
                                        'cidr': '10.0.0.0/32'}})
        self.assertEqual(
            "Policy doesn't allow %s to be performed." % rule_name,
            exc.format_message())

    def test_index_policy_failed(self):
        rule_name = 'os_compute_api:os-tenant-networks'
        self.policy.set_rules({rule_name: "project:non_fake"})
        exc = self.assertRaises(
            exception.PolicyNotAuthorized,
            self.controller.index,
            self.req)
        self.assertEqual(
            "Policy doesn't allow %s to be performed." % rule_name,
            exc.format_message())

    def test_delete_policy_failed(self):
        rule_name = 'os_compute_api:os-tenant-networks'
        self.policy.set_rules({rule_name: "project:non_fake"})
        exc = self.assertRaises(
            exception.PolicyNotAuthorized,
            self.controller.delete,
            self.req, fakes.FAKE_UUID)
        self.assertEqual(
            "Policy doesn't allow %s to be performed." % rule_name,
            exc.format_message())

    def test_show_policy_failed(self):
        rule_name = 'os_compute_api:os-tenant-networks'
        self.policy.set_rules({rule_name: "project:non_fake"})
        exc = self.assertRaises(
            exception.PolicyNotAuthorized,
            self.controller.show,
            self.req, fakes.FAKE_UUID)
        self.assertEqual(
            "Policy doesn't allow %s to be performed." % rule_name,
            exc.format_message())


class TenantNetworksDeprecationTest(test.NoDBTestCase):

    def setUp(self):
        super(TenantNetworksDeprecationTest, self).setUp()
        self.controller = networks_v21.TenantNetworkController()
        self.req = fakes.HTTPRequest.blank('', version='2.36')

    def test_all_apis_return_not_found(self):
        self.assertRaises(exception.VersionNotFoundForAPIMethod,
            self.controller.index, self.req)
        self.assertRaises(exception.VersionNotFoundForAPIMethod,
            self.controller.show, self.req, fakes.FAKE_UUID)
        self.assertRaises(exception.VersionNotFoundForAPIMethod,
            self.controller.delete, self.req, fakes.FAKE_UUID)
        self.assertRaises(exception.VersionNotFoundForAPIMethod,
            self.controller.create, self.req, {})
