import mock

import src.lib.charm.frr
import unit_tests.utils as ut_utils


class TestLibCharmFrr(ut_utils.BaseTestCase):

    def test_get_asn(self):
        self.patch_object(src.lib.charm.frr, 'reactive')
        self.patch_object(src.lib.charm.frr, 'hookenv')
        bgpserver = mock.Mock()
        bgpserver.generate_asn.return_value = 4200000000
        self.reactive.relations.endpoint_from_name.return_value = bgpserver
        self.hookenv.config.return_value = False
        asn = src.lib.charm.frr.get_asn()
        self.assertTrue(self.reactive.relations.endpoint_from_name.called)
        self.assertTrue(self.hookenv.config.called)
        self.assertTrue(bgpserver.generate_asn.called)
        self.assertEqual(asn, 4200000000)

    def test_get_asn_16bit(self):
        self.patch_object(src.lib.charm.frr, 'reactive')
        self.patch_object(src.lib.charm.frr, 'hookenv')
        bgpserver = mock.Mock()
        bgpserver.generate_asn_16.return_value = 64542
        self.reactive.relations.endpoint_from_name.return_value = bgpserver

        def _mock_config_16(key):
            if key == 'use-16bit-asn':
                return True
            if key == 'asn':
                return False

        self.hookenv.config = _mock_config_16
        asn = src.lib.charm.frr.get_asn()
        self.assertTrue(self.reactive.relations.endpoint_from_name.called)
        self.assertTrue(bgpserver.generate_asn_16.called)
        self.assertEqual(asn, 64542)

    def test_get_asn_config(self):
        self.patch_object(src.lib.charm.frr, 'reactive')
        self.patch_object(src.lib.charm.frr, 'hookenv')
        bgpserver = mock.Mock()
        bgpserver.generate_asn.return_value = 4200000000
        self.reactive.relations.endpoint_from_name.return_value = bgpserver

        def _mock_config_asn(key):
            if key == 'asn':
                return 4200000042

        self.hookenv.config = _mock_config_asn
        asn = src.lib.charm.frr.get_asn()
        self.assertTrue(self.reactive.relations.endpoint_from_name.called)
        self.assertTrue(bgpserver.generate_asn.called)
        self.assertEqual(asn, 4200000042)
