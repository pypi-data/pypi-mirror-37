from mock import patch, MagicMock

from cloudshell.firewall.fortinet.helpers.exceptions import FortiNetException
from cloudshell.firewall.fortinet.runners.autoload_runner import FortiNetAutoloadRunner
from cloudshell.firewall.fortinet.snmp.snmp_handler import FortiNetSnmpHandler
from tests.firewall.fortinet.base_test import BaseFortiNetTestCase, CliEmulator, Command, \
    CONFIG_SNMP_V2_PROMPT, ENABLE_PROMPT, CONFIG_SNMP_SYSINFO_PROMPT, EDIT_COMMUNITY_PROMPT, \
    CONFIG_SNMP_HOSTS_PROMPT, EDIT_SNMP_HOSTS_PROMPT, CONFIG_SNMP_V3_PROMPT, EDIT_SNMP_USER_PROMPT


@patch('cloudshell.devices.snmp_handler.QualiSnmp', MagicMock())
@patch('cloudshell.firewall.fortinet.flows.autoload_flow.SNMPAutoload', MagicMock())
@patch('cloudshell.cli.session.ssh_session.paramiko', MagicMock())
@patch('cloudshell.cli.session.ssh_session.SSHSession._clear_buffer', MagicMock(return_value=''))
class TestEnableDisableSnmp(BaseFortiNetTestCase):

    def _setUp(self, attrs=None):
        attrs = attrs or {}
        snmp_attrs = {
            'SNMP Version': 'v2c',
            'SNMP Read Community': 'public',
            'SNMP V3 User': 'quali_user',
            'SNMP V3 Password': 'password',
            'SNMP V3 Private Key': 'private_key',
            'SNMP V3 Authentication Protocol': 'No Authentication Protocol',
            'SNMP V3 Privacy Protocol': 'No Privacy Protocol',
            'Enable SNMP': 'True',
            'Disable SNMP': 'False',
        }
        snmp_attrs.update(attrs)
        super(TestEnableDisableSnmp, self)._setUp(snmp_attrs)
        self.snmp_handler = FortiNetSnmpHandler(
            self.resource_config, self.logger, self.api, self.cli_handler)
        self.runner = FortiNetAutoloadRunner(self.resource_config, self.logger, self.snmp_handler)

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v2(self, send_mock, recv_mock):
        self._setUp()

        emu = CliEmulator([
            Command(
                'show system snmp community',
                'config system snmp community\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
            Command('config system snmp sysinfo', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('set status enable', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command('config system snmp community', CONFIG_SNMP_V2_PROMPT),
            Command('edit 100', EDIT_COMMUNITY_PROMPT),
            Command('set name public', EDIT_COMMUNITY_PROMPT),
            Command('set status enable', EDIT_COMMUNITY_PROMPT),
            Command('set query-v2c-status enable', EDIT_COMMUNITY_PROMPT),
            Command('config hosts', CONFIG_SNMP_HOSTS_PROMPT),
            Command('edit 1', EDIT_SNMP_HOSTS_PROMPT),
            Command('end', EDIT_COMMUNITY_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command(
                'show system snmp community',
                'config system snmp community\n'
                '    edit 100\n'
                '        set name "public"\n'
                '        config hosts\n'
                '            edit 1\n'
                '            next\n'
                '        end\n'
                '    next\n'
                'end'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v2_already_enabled(self, send_mock, recv_mock):
        self._setUp()

        emu = CliEmulator([
            Command(
                'show system snmp community',
                'config system snmp community\n'
                '    edit 100\n'
                '        set name "public"\n'
                '        config hosts\n'
                '            edit 1\n'
                '            next\n'
                '        end\n'
                '    next\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v2_community_index_is_used(self, send_mock, recv_mock):
        edit_community_prompt = EDIT_COMMUNITY_PROMPT.replace('100', '101')
        self._setUp()

        emu = CliEmulator([
            Command(
                'show system snmp community',
                '    edit 100\n'
                '        set name "other_community"\n'
                '        config hosts\n'
                '            edit 1\n'
                '            next\n'
                '        end\n'
                '    next\n'
                'config system snmp community\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
            Command('config system snmp sysinfo', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('set status enable', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command('config system snmp community', CONFIG_SNMP_V2_PROMPT),
            Command('edit 101', edit_community_prompt),
            Command('set name public', edit_community_prompt),
            Command('set status enable', edit_community_prompt),
            Command('set query-v2c-status enable', edit_community_prompt),
            Command('config hosts', CONFIG_SNMP_HOSTS_PROMPT),
            Command('edit 1', EDIT_SNMP_HOSTS_PROMPT),
            Command('end', edit_community_prompt),
            Command('end', ENABLE_PROMPT),
            Command(
                'show system snmp community',
                'config system snmp community\n'
                '    edit 100\n'
                '        set name "other_community"\n'
                '        config hosts\n'
                '            edit 1\n'
                '            next\n'
                '        end\n'
                '    next\n'
                '    edit 101\n'
                '        set name "public"\n'
                '        config hosts\n'
                '            edit 1\n'
                '            next\n'
                '        end\n'
                '    next\n'
                'end'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v2_not_enabled(self, send_mock, recv_mock):
        self._setUp()

        emu = CliEmulator([
            Command(
                'show system snmp community',
                'config system snmp community\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
            Command('config system snmp sysinfo', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('set status enable', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command('config system snmp community', CONFIG_SNMP_V2_PROMPT),
            Command('edit 100', EDIT_COMMUNITY_PROMPT),
            Command('set name public', EDIT_COMMUNITY_PROMPT),
            Command('set status enable', EDIT_COMMUNITY_PROMPT),
            Command('set query-v2c-status enable', EDIT_COMMUNITY_PROMPT),
            Command('config hosts', CONFIG_SNMP_HOSTS_PROMPT),
            Command('edit 1', EDIT_SNMP_HOSTS_PROMPT),
            Command('end', EDIT_COMMUNITY_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command(
                'show system snmp community',
                'config system snmp community\n'
                'end'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.assertRaisesRegexp(
            FortiNetException,
            'Failed to create SNMP community "public"',
            self.runner.discover,
        )

        emu.check_calls()

    def test_enable_snmp_v2_write_community(self):
        self._setUp({'SNMP Write Community': 'private'})

        self.assertRaisesRegexp(
            FortiNetException,
            '^FortiNet devices doesn\'t support write communities$',
            self.runner.discover,
        )

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_disable_snmp_v2(self, send_mock, recv_mock):
        self._setUp({
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
        })

        emu = CliEmulator([
            Command(
                'show system snmp community',
                'config system snmp community\n'
                '    edit 100\n'
                '        set name "public"\n'
                '        config hosts\n'
                '            edit 1\n'
                '            next\n'
                '        end\n'
                '    next\n'
                'end'
                '{}'.format(ENABLE_PROMPT)),
            Command('config system snmp community', CONFIG_SNMP_V2_PROMPT),
            Command('delete 100', CONFIG_SNMP_V2_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command(
                'show system snmp community',
                'config system snmp community\n'
                'end'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_disable_snmp_v2_already_disabled(self, send_mock, recv_mock):
        self._setUp({
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
        })

        emu = CliEmulator([
            Command(
                'show system snmp community',
                'config system snmp community\n'
                'end'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_disable_snmp_v2_is_not_disabled(self, send_mock, recv_mock):
        self._setUp({
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
        })

        emu = CliEmulator([
            Command(
                'show system snmp community',
                'config system snmp community\n'
                '    edit 100\n'
                '        set name "public"\n'
                '        config hosts\n'
                '            edit 1\n'
                '            next\n'
                '        end\n'
                '    next\n'
                'end'
                '{}'.format(ENABLE_PROMPT)),
            Command('config system snmp community', CONFIG_SNMP_V2_PROMPT),
            Command('delete 100', CONFIG_SNMP_V2_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command(
                'show system snmp community',
                'config system snmp community\n'
                '    edit 100\n'
                '        set name "public"\n'
                '        config hosts\n'
                '            edit 1\n'
                '            next\n'
                '        end\n'
                '    next\n'
                'end'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.assertRaisesRegexp(
            FortiNetException,
            'Failed to remove SNMP community "public"',
            self.runner.discover,
        )

        emu.check_calls()

    def test_disable_snmp_v2_write_community(self):
        self._setUp({
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
            'SNMP Write Community': 'private',
        })

        self.assertRaisesRegexp(
            FortiNetException,
            '^FortiNet devices doesn\'t support write communities$',
            self.runner.discover,
        )

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v3(self, send_mock, recv_mock):
        self._setUp({'SNMP Version': 'v3'})

        emu = CliEmulator([
            Command(
                'show system snmp user',
                'config system snmp user\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
            Command('config system snmp sysinfo', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('set status enable', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command('config system snmp user', CONFIG_SNMP_V3_PROMPT),
            Command('edit quali_user', EDIT_SNMP_USER_PROMPT),
            Command('set status enable', EDIT_SNMP_USER_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command(
                'show system snmp user',
                'config system snmp user\n'
                '    edit "quali_user"\n'
                '    next\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_snmp_v3_user_already_created(self, send_mock, recv_mock):
        self._setUp({'SNMP Version': 'v3'})

        emu = CliEmulator([
            Command(
                'show system snmp user',
                'config system snmp user\n'
                '    edit "quali_user"\n'
                '    next\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_snmp_v3_user_didnt_created(self, send_mock, recv_mock):
        self._setUp({'SNMP Version': 'v3'})

        emu = CliEmulator([
            Command(
                'show system snmp user',
                'config system snmp user\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
            Command('config system snmp sysinfo', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('set status enable', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command('config system snmp user', CONFIG_SNMP_V3_PROMPT),
            Command('edit quali_user', EDIT_SNMP_USER_PROMPT),
            Command('set status enable', EDIT_SNMP_USER_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command(
                'show system snmp user',
                'config system snmp user\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.assertRaisesRegexp(
            FortiNetException,
            r'^Failed to create SNMP User "quali_user"$',
            self.runner.discover,
        )

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v3_with_auth(self, send_mock, recv_mock):
        self._setUp({
            'SNMP Version': 'v3',
            'SNMP V3 Authentication Protocol': 'MD5',
        })

        emu = CliEmulator([
            Command(
                'show system snmp user',
                'config system snmp user\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
            Command('config system snmp sysinfo', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('set status enable', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command('config system snmp user', CONFIG_SNMP_V3_PROMPT),
            Command('edit quali_user', EDIT_SNMP_USER_PROMPT),
            Command('set status enable', EDIT_SNMP_USER_PROMPT),
            Command('set security-level auth-no-priv', EDIT_SNMP_USER_PROMPT),
            Command('set auth-proto md5', EDIT_SNMP_USER_PROMPT),
            Command('set auth-pwd password', EDIT_SNMP_USER_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command(
                'show system snmp user',
                'config system snmp user\n'
                '    edit "quali_user"\n'
                '        set security-level auth-no-priv\n'
                '        set auth-proto md5\n'
                '        set auth-pwd ENC 3iJai3...\n'
                '    next\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_enable_snmp_v3_with_auth_and_priv(self, send_mock, recv_mock):
        self._setUp({
            'SNMP Version': 'v3',
            'SNMP V3 Authentication Protocol': 'SHA',
            'SNMP V3 Privacy Protocol': 'AES-128',
        })

        emu = CliEmulator([
            Command(
                'show system snmp user',
                'config system snmp user\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
            Command('config system snmp sysinfo', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('set status enable', CONFIG_SNMP_SYSINFO_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command('config system snmp user', CONFIG_SNMP_V3_PROMPT),
            Command('edit quali_user', EDIT_SNMP_USER_PROMPT),
            Command('set status enable', EDIT_SNMP_USER_PROMPT),
            Command('set security-level auth-priv', EDIT_SNMP_USER_PROMPT),
            Command('set auth-proto sha', EDIT_SNMP_USER_PROMPT),
            Command('set auth-pwd password', EDIT_SNMP_USER_PROMPT),
            Command('set priv-proto aes', EDIT_SNMP_USER_PROMPT),
            Command('set priv-pwd private_key', EDIT_SNMP_USER_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command(
                'show system snmp user',
                'config system snmp user\n'
                '    edit "quali_user"\n'
                '        set security-level auth-priv\n'
                '        set auth-proto sha\n'
                '        set auth-pwd ENC 142A8NXCPlqD...\n'
                '        set priv-pwd ENC KTmph2yQ...\n'
                '    next\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    def test_enable_snmp_v3_with_not_supported_priv_protocol(self):
        self._setUp({
            'SNMP Version': 'v3',
            'SNMP V3 Authentication Protocol': 'SHA',
            'SNMP V3 Privacy Protocol': 'AES-192',
        })

        self.assertRaisesRegexp(
            FortiNetException,
            'Doen\'t supported private key protocol AES-192',
            self.runner.discover,
        )

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_disable_snmp_v3(self, send_mock, recv_mock):
        self._setUp({
            'SNMP Version': 'v3',
            'SNMP V3 Authentication Protocol': 'SHA',
            'SNMP V3 Privacy Protocol': 'AES-128',
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
        })

        emu = CliEmulator([
            Command(
                'show system snmp user',
                'config system snmp user\n'
                '    edit "quali_user"\n'
                '        set security-level auth-priv\n'
                '        set auth-proto sha\n'
                '        set auth-pwd ENC 142A8NXCPlqD...\n'
                '        set priv-pwd ENC KTmph2yQ...\n'
                '    next\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
            Command('config system snmp user', CONFIG_SNMP_V3_PROMPT),
            Command('delete quali_user', CONFIG_SNMP_V3_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command(
                'show system snmp user',
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    def test_disable_snmp_v3_with_not_supported_priv_protocol(self):
        self._setUp({
            'SNMP Version': 'v3',
            'SNMP V3 Authentication Protocol': 'SHA',
            'SNMP V3 Privacy Protocol': 'AES-192',
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
        })

        self.assertRaisesRegexp(
            FortiNetException,
            'Doen\'t supported private key protocol AES-192',
            self.runner.discover,
        )

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_remove_snmp_v3_user_already_deleted(self, send_mock, recv_mock):
        self._setUp({
            'SNMP Version': 'v3',
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
        })

        emu = CliEmulator([
            Command(
                'show system snmp user',
                'config system snmp user\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.runner.discover()

        emu.check_calls()

    @patch('cloudshell.cli.session.ssh_session.SSHSession._receive_all')
    @patch('cloudshell.cli.session.ssh_session.SSHSession.send_line')
    def test_snmp_v3_user_didnt_deleted(self, send_mock, recv_mock):
        self._setUp({
            'SNMP Version': 'v3',
            'Enable SNMP': 'False',
            'Disable SNMP': 'True',
        })

        emu = CliEmulator([
            Command(
                'show system snmp user',
                'config system snmp user\n'
                '    edit "quali_user"\n'
                '    next\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
            Command('config system snmp user', CONFIG_SNMP_V3_PROMPT),
            Command('delete quali_user', CONFIG_SNMP_V3_PROMPT),
            Command('end', ENABLE_PROMPT),
            Command(
                'show system snmp user',
                'config system snmp user\n'
                '    edit "quali_user"\n'
                '    next\n'
                'end\n'
                '{}'.format(ENABLE_PROMPT)),
        ])
        send_mock.side_effect = emu.send_line
        recv_mock.side_effect = emu.receive_all

        self.assertRaisesRegexp(
            FortiNetException,
            r'^Failed to disable SNMP User "quali_user"$',
            self.runner.discover,
        )

        emu.check_calls()


class TestSnmpAutoload(BaseFortiNetTestCase):
    def _setUp(self, attrs=None):
        attrs = attrs or {}
        snmp_attrs = {
            'SNMP Version': 'v2c',
            'SNMP Read Community': 'public',
            'Enable SNMP': 'False',
            'Disable SNMP': 'False',
        }
        snmp_attrs.update(attrs)
        super(TestSnmpAutoload, self)._setUp(snmp_attrs)
        self.snmp_handler = FortiNetSnmpHandler(
            self.resource_config, self.logger, self.api, self.cli_handler)
        self.runner = FortiNetAutoloadRunner(self.resource_config, self.logger, self.snmp_handler)

    def setUp(self):
        self._setUp()

    @patch('cloudshell.devices.snmp_handler.QualiSnmp')
    def test_autoload(self, snmp_mock):
        property_map = {
            ('SNMPv2-MIB', 'sysObjectID', 0): 'SNMPv2-SMI::enterprises.12356.101.1.60',
            ('SNMPv2-MIB', 'sysContact', '0'): 'admin',
            ('SNMPv2-MIB', 'sysName', '0'): 'FortiGate-VM64-KVM',
            ('SNMPv2-MIB', 'sysLocation', '0'): 'somewhere',
            ('FORTINET-FORTIGATE-MIB', 'fgSysVersion', 0): 'v6.0.2,build0163,180725 (GA)',
            ('SNMPv2-MIB', 'sysObjectID', '0'): 'FORTINET-FORTIGATE-MIB::fgtVM64KVm',
            ('ENTITY-MIB', 'entPhysicalModelName', 1): 'FGT_VM64KVM',
            ('ENTITY-MIB', 'entPhysicalSerialNum', 1): 'FGVMEVBICE74EA11',
            ('IF-MIB', 'ifName', 2): 'port1',
            ('IF-MIB', 'ifAlias', 2): '',
            ('IF-MIB', 'ifHighSpeed', 2): '10000',
            ('EtherLike-MIB', 'dot3StatsDuplexStatus', 2): '',
            ('MAU-MIB', 'ifMauAutoNegAdminStatus', 2): 'No Such Object currently exists at this OID',
            ('IF-MIB', 'ifName', 3): 'port2',
            ('IF-MIB', 'ifAlias', 3): '',
            ('IF-MIB', 'ifHighSpeed', 3): '10000',
            ('EtherLike-MIB', 'dot3StatsDuplexStatus', 3): "'fullDuplex'",
            ('MAU-MIB', 'ifMauAutoNegAdminStatus', 3): 'No Such Object currently exists at this OID',
            ('IF-MIB', 'ifName', 4): 'port3',
            ('IF-MIB', 'ifAlias', 4): '',
            ('IF-MIB', 'ifHighSpeed', 4): '10000',
            ('EtherLike-MIB', 'dot3StatsDuplexStatus', 4): '',
            ('MAU-MIB', 'ifMauAutoNegAdminStatus', 4): 'No Such Object currently exists at this OID',
            ('IF-MIB', 'ifName', 6): 'aggr',
            ('IF-MIB', 'ifAlias', 6): '',
        }
        table_map = {
            ('ENTITY-MIB', 'entPhysicalClass'): {
                1: {'entPhysicalClass': "'chassis'", 'suffix': '1'}},
            ('IF-MIB', 'ifTable'): {
                1: {'ifType': "'tunnel'", 'suffix': '1', 'ifOutDiscards': '2',
                    'ifAdminStatus': "'up'", 'ifMtu': '1500', 'ifInDiscards': '0',
                    'ifInErrors': '0', 'ifDescr': '', 'ifOperStatus': "'up'", 'ifOutUcastPkts': '0',
                    'ifInOctets': '0', 'ifLastChange': '0', 'ifPhysAddress': '',
                    'ifInUcastPkts': '0', 'ifSpecific': 'SNMPv2-SMI::zeroDotZero.0',
                    'ifOutErrors': '0', 'ifIndex': '1', 'ifOutQLen': '0', 'ifSpeed': '0',
                    'ifOutNUcastPkts': '0', 'ifOutOctets': '0', 'ifInUnknownProtos': '0',
                    'ifInNUcastPkts': '0'},
                2: {'ifType': "'ethernetCsmacd'", 'suffix': '2', 'ifOutDiscards': '0',
                    'ifAdminStatus': "'up'", 'ifMtu': '1500', 'ifInDiscards': '0',
                    'ifInErrors': '0', 'ifDescr': '', 'ifOperStatus': "'up'",
                    'ifOutUcastPkts': '50888', 'ifInOctets': '12467448', 'ifLastChange': '0',
                    'ifPhysAddress': '52:54:00:e5:48:f5', 'ifInUcastPkts': '187601',
                    'ifSpecific': 'SNMPv2-SMI::zeroDotZero.0', 'ifOutErrors': '0', 'ifIndex': '2',
                    'ifOutQLen': '0', 'ifSpeed': '4294967295', 'ifOutNUcastPkts': '0',
                    'ifOutOctets': '6495430', 'ifInUnknownProtos': '0', 'ifInNUcastPkts': '0'},
                3: {'ifType': "'ethernetCsmacd'", 'suffix': '3', 'ifOutDiscards': '0',
                    'ifAdminStatus': "'up'", 'ifMtu': '1500', 'ifInDiscards': '0',
                    'ifInErrors': '0', 'ifDescr': '', 'ifOperStatus': "'up'",
                    'ifOutUcastPkts': '9145', 'ifInOctets': '9514847', 'ifLastChange': '0',
                    'ifPhysAddress': '52:54:00:5c:65:1a', 'ifInUcastPkts': '150387',
                    'ifSpecific': 'SNMPv2-SMI::zeroDotZero.0', 'ifOutErrors': '0', 'ifIndex': '3',
                    'ifOutQLen': '0', 'ifSpeed': '4294967295', 'ifOutNUcastPkts': '0',
                    'ifOutOctets': '1133912', 'ifInUnknownProtos': '0', 'ifInNUcastPkts': '0'},
                4: {'ifType': "'ethernetCsmacd'", 'suffix': '4', 'ifOutDiscards': '0',
                    'ifAdminStatus': "'up'", 'ifMtu': '1500', 'ifInDiscards': '0',
                    'ifInErrors': '0', 'ifDescr': '', 'ifOperStatus': "'up'",
                    'ifOutUcastPkts': '9145', 'ifInOctets': '9514831', 'ifLastChange': '0',
                    'ifPhysAddress': '52:54:00:66:1f:8d', 'ifInUcastPkts': '150387',
                    'ifSpecific': 'SNMPv2-SMI::zeroDotZero.0','ifOutErrors': '0', 'ifIndex': '4',
                    'ifOutQLen': '0', 'ifSpeed': '4294967295', 'ifOutNUcastPkts': '0',
                    'ifOutOctets': '1133912', 'ifInUnknownProtos': '0', 'ifInNUcastPkts': '0'},
                6: {'ifType': "'ieee8023adLag'", 'suffix': '6', 'ifOutDiscards': '0',
                    'ifAdminStatus': "'up'", 'ifMtu': '1500', 'ifInDiscards': '0',
                    'ifInErrors': '0', 'ifDescr': '', 'ifOperStatus': "'down'",
                    'ifOutUcastPkts': '18290', 'ifInOctets': '19029678', 'ifLastChange': '0',
                    'ifPhysAddress': '52:54:00:5c:65:1a', 'ifInUcastPkts': '300774',
                    'ifSpecific': 'SNMPv2-SMI::zeroDotZero.0','ifOutErrors': '0', 'ifIndex': '6',
                    'ifOutQLen': '0', 'ifSpeed': '0', 'ifOutNUcastPkts': '0',
                    'ifOutOctets': '2267824', 'ifInUnknownProtos': '0', 'ifInNUcastPkts': '0'}},
            ('ENTITY-MIB', 'entPhysicalContainsTable'): {
                '1.4': {'entPhysicalChildIndex': '4', 'suffix': '1.4'},
                '1.2': {'entPhysicalChildIndex': '2', 'suffix': '1.2'},
                '1.3': {'entPhysicalChildIndex': '3', 'suffix': '1.3'}},
            ('IP-MIB', 'ipAddrTable'): {
                '192.168.122.240': {'ipAdEntAddr': '192.168.122.240', 'ipAdEntIfIndex': '2',
                                    'suffix': '192.168.122.240', 'ipAdEntNetMask': '255.255.255.0',
                                    'ipAdEntBcastAddr': '1', 'ipAdEntReasmMaxSize': '65535'},
                '192.168.121.239': {'ipAdEntAddr': '192.168.121.239', 'ipAdEntIfIndex': '6',
                                    'suffix': '192.168.121.239', 'ipAdEntNetMask': '255.255.255.0',
                                    'ipAdEntBcastAddr': '1', 'ipAdEntReasmMaxSize': '65535'}},
            ('IPV6-MIB', 'ipv6AddrEntry'): {
                '2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d': {'ipAdEntIfIndex': '2'},
                '2001:0db8:11a3:09d7:1f34:8a2e:07a0:766d': {},
            },
            ('IEEE8023-LAG-MIB', 'dot3adAggPortAttachedAggID'): {},
            ('LLDP-MIB', 'lldpRemSysName'): {},
            ('LLDP-MIB', 'lldpLocPortDesc'): {},
        }

        snmp_mock().get_property.side_effect = lambda *args: property_map[args]
        snmp_mock().get_table.side_effect = lambda *args: table_map[args]

        details = self.runner.discover()

        contact_name = sys_name = location = model = os_version = None
        for attr in details.attributes:
            if attr.relative_address == '':
                if attr.attribute_name == 'Contact Name':
                    contact_name = attr.attribute_value
                elif attr.attribute_name == 'System Name':
                    sys_name = attr.attribute_value
                elif attr.attribute_name == 'Location':
                    location = attr.attribute_value
                elif attr.attribute_name == 'Model':
                    model = attr.attribute_value
                elif attr.attribute_name == 'OS Version':
                    os_version = attr.attribute_value

        self.assertEqual('admin', contact_name)
        self.assertEqual('FortiGate-VM64-KVM', sys_name)
        self.assertEqual('somewhere', location)
        self.assertEqual('fgtVM64KVm', model)
        self.assertEqual('v6.0.2,build0163,180725 (GA)', os_version)

        ports = []
        power_ports = []
        port_channels = []
        chassis = None

        for resource in details.resources:
            if resource.model == 'GenericPort':
                ports.append(resource)
            elif resource.model == 'GenericChassis':
                chassis = resource
            elif resource.model == 'GenericPowerPort':
                power_ports.append(resource)
            elif resource.model == 'GenericPortChannel':
                port_channels.append(resource)

        ports.sort(key=lambda p: p.name)
        power_ports.sort(key=lambda pw: pw.name)
        port_channels.sort(key=lambda pc: pc.name)

        self.assertEqual('Chassis 1', chassis.name)

        expected_port_names = ['port1', 'port2', 'port3']
        self.assertListEqual([port.name for port in ports], sorted(expected_port_names))

        expected_power_port_names = []
        self.assertListEqual([pw.name for pw in power_ports], sorted(expected_power_port_names))

        expected_port_channel_names = ['aggr']
        self.assertListEqual([pc.name for pc in port_channels], sorted(expected_port_channel_names))

    @patch('cloudshell.devices.snmp_handler.QualiSnmp')
    def test_not_supported_os(self, snmp_mock):
        property_map = {
            ('SNMPv2-MIB', 'sysObjectID', 0): 'some another value',
        }
        snmp_mock().get_property.side_effect = lambda *args: property_map[args]

        self.assertRaisesRegexp(
            FortiNetException,
            '^Unsupported device OS$',
            self.runner.discover,
        )

    @patch('cloudshell.devices.snmp_handler.QualiSnmp')
    def test_adjacent(self, snmp_mock):
        property_map = {
            ('SNMPv2-MIB', 'sysObjectID', 0): 'SNMPv2-SMI::enterprises.12356.101.1.60',
            ('SNMPv2-MIB', 'sysContact', '0'): 'admin',
            ('SNMPv2-MIB', 'sysName', '0'): 'FortiGate-VM64-KVM',
            ('SNMPv2-MIB', 'sysLocation', '0'): 'somewhere',
            ('FORTINET-FORTIGATE-MIB', 'fgSysVersion', 0): 'v6.0.2,build0163,180725 (GA)',
            ('SNMPv2-MIB', 'sysObjectID', '0'): 'FORTINET-FORTIGATE-MIB::fgtVM64KVm',
            ('ENTITY-MIB', 'entPhysicalModelName', 1): 'FGT_VM64KVM',
            ('ENTITY-MIB', 'entPhysicalSerialNum', 1): 'FGVMEVBICE74EA11',
            ('IF-MIB', 'ifName', 2): 'port1',
            ('IF-MIB', 'ifAlias', 2): '',
            ('IF-MIB', 'ifHighSpeed', 2): '10000',
            ('EtherLike-MIB', 'dot3StatsDuplexStatus', 2): '',
            ('MAU-MIB', 'ifMauAutoNegAdminStatus', 2): 'No Such Object currently exists at this OID',

            ('LLDP-MIB', 'lldpRemPortDesc', '12.50.1.12'): 'Ethernet 12',
        }
        table_map = {
            ('ENTITY-MIB', 'entPhysicalClass'): {
                1: {'entPhysicalClass': "'chassis'", 'suffix': '1'}},
            ('ENTITY-MIB', 'entPhysicalContainsTable'): {
                '1.2': {'entPhysicalChildIndex': '2', 'suffix': '1.2'}},
            ('IF-MIB', 'ifTable'): {
                1: {'ifType': "'tunnel'", 'suffix': '1', 'ifOutDiscards': '2',
                    'ifAdminStatus': "'up'", 'ifMtu': '1500', 'ifInDiscards': '0',
                    'ifInErrors': '0', 'ifDescr': '', 'ifOperStatus': "'up'", 'ifOutUcastPkts': '0',
                    'ifInOctets': '0', 'ifLastChange': '0', 'ifPhysAddress': '',
                    'ifInUcastPkts': '0', 'ifSpecific': 'SNMPv2-SMI::zeroDotZero.0',
                    'ifOutErrors': '0', 'ifIndex': '1', 'ifOutQLen': '0', 'ifSpeed': '0',
                    'ifOutNUcastPkts': '0', 'ifOutOctets': '0', 'ifInUnknownProtos': '0',
                    'ifInNUcastPkts': '0'},
                2: {'ifType': "'ethernetCsmacd'", 'suffix': '2', 'ifOutDiscards': '0',
                    'ifAdminStatus': "'up'", 'ifMtu': '1500', 'ifInDiscards': '0',
                    'ifInErrors': '0', 'ifDescr': '', 'ifOperStatus': "'up'",
                    'ifOutUcastPkts': '50888', 'ifInOctets': '12467448', 'ifLastChange': '0',
                    'ifPhysAddress': '52:54:00:e5:48:f5', 'ifInUcastPkts': '187601',
                    'ifSpecific': 'SNMPv2-SMI::zeroDotZero.0', 'ifOutErrors': '0', 'ifIndex': '2',
                    'ifOutQLen': '0', 'ifSpeed': '4294967295', 'ifOutNUcastPkts': '0',
                    'ifOutOctets': '6495430', 'ifInUnknownProtos': '0', 'ifInNUcastPkts': '0'}},
            ('IEEE8023-LAG-MIB', 'dot3adAggPortAttachedAggID'): {},
            ('IP-MIB', 'ipAddrTable'): {},
            ('IPV6-MIB', 'ipv6AddrEntry'): {},
            ('LLDP-MIB', 'lldpRemSysName'): {
                '12.50.1.12': {'lldpRemSysName': 'Other_device'}},
            ('LLDP-MIB', 'lldpLocPortDesc'): {
                '50.1': {'lldpLocPortDesc': 'port1'}},
        }

        snmp_mock().get_property.side_effect = lambda *args: property_map[args]
        snmp_mock().get_table.side_effect = lambda *args: table_map[args]

        self.runner.discover()

    @patch('cloudshell.devices.snmp_handler.QualiSnmp')
    def test_not_expected_port(self, snmp_mock):
        property_map = {
            ('SNMPv2-MIB', 'sysObjectID', 0): 'SNMPv2-SMI::enterprises.12356.101.1.60',
            ('SNMPv2-MIB', 'sysContact', '0'): 'admin',
            ('SNMPv2-MIB', 'sysName', '0'): 'FortiGate-VM64-KVM',
            ('SNMPv2-MIB', 'sysLocation', '0'): 'somewhere',
            ('FORTINET-FORTIGATE-MIB', 'fgSysVersion', 0): 'v6.0.2,build0163,180725 (GA)',
            ('SNMPv2-MIB', 'sysObjectID', '0'): 'FORTINET-FORTIGATE-MIB::fgtVM64KVm',
            ('ENTITY-MIB', 'entPhysicalModelName', 1): 'FGT_VM64KVM',
            ('ENTITY-MIB', 'entPhysicalSerialNum', 1): 'FGVMEVBICE74EA11',
            ('IF-MIB', 'ifName', 2): 'port1',
            ('IF-MIB', 'ifAlias', 2): '',
            ('IF-MIB', 'ifHighSpeed', 2): '10000',
            ('EtherLike-MIB', 'dot3StatsDuplexStatus', 2): '',
            (
            'MAU-MIB', 'ifMauAutoNegAdminStatus', 2): 'No Such Object currently exists at this OID',
            ('IF-MIB', 'ifName', 3): 'port2',
            ('IF-MIB', 'ifAlias', 3): '',
            ('IF-MIB', 'ifHighSpeed', 3): '10000',
            ('EtherLike-MIB', 'dot3StatsDuplexStatus', 3): '',
            (
            'MAU-MIB', 'ifMauAutoNegAdminStatus', 3): 'No Such Object currently exists at this OID',
            ('IF-MIB', 'ifName', 4): 'port3',
            ('IF-MIB', 'ifAlias', 4): '',
            ('IF-MIB', 'ifHighSpeed', 4): '10000',
            ('EtherLike-MIB', 'dot3StatsDuplexStatus', 4): '',
            (
            'MAU-MIB', 'ifMauAutoNegAdminStatus', 4): 'No Such Object currently exists at this OID',
            ('IF-MIB', 'ifName', 6): 'aggr',
            ('IF-MIB', 'ifAlias', 6): '',
        }
        table_map = {
            ('ENTITY-MIB', 'entPhysicalClass'): {
                1: {'entPhysicalClass': "'chassis'", 'suffix': '1'}},
            ('IF-MIB', 'ifTable'): {
                1: {'ifType': "'tunnel'", 'suffix': '1', 'ifOutDiscards': '2',
                    'ifAdminStatus': "'up'", 'ifMtu': '1500', 'ifInDiscards': '0',
                    'ifInErrors': '0', 'ifDescr': '', 'ifOperStatus': "'up'", 'ifOutUcastPkts': '0',
                    'ifInOctets': '0', 'ifLastChange': '0', 'ifPhysAddress': '',
                    'ifInUcastPkts': '0', 'ifSpecific': 'SNMPv2-SMI::zeroDotZero.0',
                    'ifOutErrors': '0', 'ifIndex': '1', 'ifOutQLen': '0', 'ifSpeed': '0',
                    'ifOutNUcastPkts': '0', 'ifOutOctets': '0', 'ifInUnknownProtos': '0',
                    'ifInNUcastPkts': '0'},
                2: {'ifType': "'ethernetCsmacd'", 'suffix': '2', 'ifOutDiscards': '0',
                    'ifAdminStatus': "'up'", 'ifMtu': '1500', 'ifInDiscards': '0',
                    'ifInErrors': '0', 'ifDescr': '', 'ifOperStatus': "'up'",
                    'ifOutUcastPkts': '50888', 'ifInOctets': '12467448', 'ifLastChange': '0',
                    'ifPhysAddress': '52:54:00:e5:48:f5', 'ifInUcastPkts': '187601',
                    'ifSpecific': 'SNMPv2-SMI::zeroDotZero.0', 'ifOutErrors': '0', 'ifIndex': '2',
                    'ifOutQLen': '0', 'ifSpeed': '4294967295', 'ifOutNUcastPkts': '0',
                    'ifOutOctets': '6495430', 'ifInUnknownProtos': '0', 'ifInNUcastPkts': '0'}},
            ('ENTITY-MIB', 'entPhysicalContainsTable'): {},  # empty table
            ('IP-MIB', 'ipAddrTable'): {
                '192.168.122.240': {'ipAdEntAddr': '192.168.122.240', 'ipAdEntIfIndex': '2',
                                    'suffix': '192.168.122.240', 'ipAdEntNetMask': '255.255.255.0',
                                    'ipAdEntBcastAddr': '1', 'ipAdEntReasmMaxSize': '65535'}},
            ('IPV6-MIB', 'ipv6AddrEntry'): {},
            ('IEEE8023-LAG-MIB', 'dot3adAggPortAttachedAggID'): {},
            ('LLDP-MIB', 'lldpRemSysName'): {},
            ('LLDP-MIB', 'lldpLocPortDesc'): {},
        }

        snmp_mock().get_property.side_effect = lambda *args: property_map[args]
        snmp_mock().get_table.side_effect = lambda *args: table_map[args]

        self.assertRaisesRegexp(
            FortiNetException,
            'Cannot add a port to a chassis',
            self.runner.discover,
        )
