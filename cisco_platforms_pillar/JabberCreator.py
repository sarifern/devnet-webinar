from CUCMConnectorAXL import *
import logging

class JabberCreator(CUCMConnectorAXL):
    def add_jabber_device(self, device_name, lines, site, team, username):
        """
            Creates a Jabber device with the specified settings
            This example takes as default many of the common settings, although it can be adjusted according to your needs
        """
        phone={
                    'name': device_name,
                    'devicePoolName': f'{site}-DP',
                    'ownerUserName': username,
                    'description': f'({team}) Remote Agent - Site {site}',
                    'product': 'Cisco Unified Client Services Framework',
                    'class': 'Phone',
                    'protocol': 'SIP',
                    'protocolSide': 'User',
                    'locationName': 'Hub_None',
                    'sipProfileName': 'Standard SIP Profile',
                    'commonPhoneConfigName': 'Standard Common Phone Profile',
                    'phoneTemplateName': 'Standard Client Services Framework',
                    'useTrustedRelayPoint': 'Default',
                    'builtInBridgeStatus': 'Default',
                    'packetCaptureMode': 'None',
                    'certificateOperation': 'No Pending Operation',
                    'deviceMobilityMode': 'Off',
                    'lines': {
                        'line': lines
                    }
                }

        try:
            return self._CLIENT.addPhone(phone)
        except Exception as e:
            if self._logger:
                self._logger.error(str(e))
            return f'ERROR: {str(e)}'