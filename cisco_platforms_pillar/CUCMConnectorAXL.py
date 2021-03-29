# -*- coding: utf-8 -*-
"""
Cisco CUCM connector class
This class creates a connection object via AXL\SOAP to the specified CUCM server using the specified AXL-enabled credentials

@author: Alfonso Sandoval Rosas
"""
import urllib3, logging
from ZeepDebugPlugin import *
from zeep import Client, xsd
from zeep.cache import SqliteCache
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

class CUCMConnectorAXL:

    def __init__(self,CUCM_IP,AXL_Username,AXL_Password,CUCM_Version = '11.5',debug = False,logger = False):
        """
        Constructor initiates session establishment process when the instance is created

        Parameters
        ----------
        AXL_Username : string
            AXL-enabled CUCM username
        AXL_Password : string
            AXL-enabled CUCM password
        CUCM_IP : string
            Target CUCM IP address    
        CUCM_Version : string. Default: 11.5    
            Target CUCM version
        debug : boolean. Default: False
            Toggle debug plugin for seeing incoming/outgoing SOAP requests in console
        logger : logging instance. Default: False
            Custom logger for ERROR-type messages handling
        """
        self._AXL_Username = AXL_Username
        self._AXL_Password = AXL_Password
        self._CUCM_IP = CUCM_IP
        self._CUCM_Version = CUCM_Version
        self._debug = debug
        self._logger = logger
        self._CLIENT = ''
        self._connect_cucm()
        self._test_connection()

    def _connect_cucm(self):
        """Session establishment with target CUCM node. Returns zeep object"""

        try:
            WSDL = f'schema/{self._CUCM_Version}/AXLAPI.wsdl'
            if('9.' in self._CUCM_Version):
                urllib3.disable_warnings()
                urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
                WSDL = 'schema/9.1/AXLAPI.wsdl'
                try:
                    urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
                except AttributeError:
                    pass
            else:
                urllib3.disable_warnings(InsecureRequestWarning)
                
            BINDING_NAME = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
            ADDRESS = "https://{ip}:8443/axl/".format(ip=self._CUCM_IP)
            session = Session()
            session.verify = False
            session.auth = HTTPBasicAuth(self._AXL_Username, self._AXL_Password)
            transport = Transport(cache=SqliteCache(), session=session, timeout=10)
            if self._debug:
                client = Client(wsdl=WSDL, transport=transport, plugins=[ZeepDebugPlugin()])
            else:
                client = Client(wsdl=WSDL, transport=transport)
            self._CLIENT = client.create_service(BINDING_NAME, ADDRESS)
        except FileExistsError:
            self._CLIENT = False
            if self._logger:
                self._logger.error(f'Please verify the existance of the WSDL files corresponding to the CUCM version in the /schema folder' )
            else:
                logging.error( f'Please verify the existance of the WSDL files corresponding to the CUCM version in the /schema folder' )
            pass

    def _test_connection(self):
        """Test query for connection validation"""
        if self._debug:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug( f'Test connection query to: ({self._CUCM_IP}) ...')
        try:
            self._CLIENT.listCallManagerGroup(
                searchCriteria = {'name':'%'},
                returnedTags = {'name':''}
            )
        except Exception as err:
            self._CLIENT = False
            if 'Max retries exceeded' in str(err):
                if self._logger:
                    self._logger.error(f'Server ({self._CUCM_IP}) is unreachable' )
                else:
                    logging.error( f'Server ({self._CUCM_IP}) is unreachable' )
            elif 'Unknown fault occured' in str(err):
                if self._logger:
                    self._logger.error( f'Conection error to ({self._CUCM_IP}): Possible credentials mismatch' )
                else:
                    logging.error( f'Conection error to ({self._CUCM_IP}): Possible credentials mismatch' )
            else:
                if self._logger:
                    self._logger.error(f'Conection error to ({self._CUCM_IP}): {err}')
                else:
                    logging.error( f'Conection error to ({self._CUCM_IP}): {err}')
            pass

    def isValid(self):
       """Returns current self._CLIENT value. The value will be False if the test when creating the instance was not successful"""
       
       return self._CLIENT

    @staticmethod
    def connector(CUCM_IP,AXL_Username,AXL_Password,CUCM_Version = '11.5',debug = False):
        """Returns a standalone connector. No class methods. For testing purposes"""

        WSDL = f'schema/{CUCM_Version}/AXLAPI.wsdl'
        if('9.' in CUCM_Version):
            urllib3.disable_warnings()
            urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
            WSDL = 'schema/9.1/AXLAPI.wsdl'
            try:
                urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
            except AttributeError:
                pass
        else:
            urllib3.disable_warnings(InsecureRequestWarning)
			
        BINDING_NAME = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
        ADDRESS = "https://{ip}:8443/axl/".format(ip=CUCM_IP)
        session = Session()
        session.verify = False
        session.auth = HTTPBasicAuth(AXL_Username, AXL_Password)
        transport = Transport(cache=SqliteCache(), session=session, timeout=10)
        if debug:
            client = Client(wsdl=WSDL, transport=transport, plugins=[ZeepDebugPlugin()])
        else:
            client = Client(wsdl=WSDL, transport=transport)
        return client.create_service(BINDING_NAME, ADDRESS)