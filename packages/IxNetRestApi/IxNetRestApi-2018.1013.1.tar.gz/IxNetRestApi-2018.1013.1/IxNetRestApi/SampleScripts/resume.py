"""
Description
    The sample shows how to connect to an existing configuration.

    For  Windows Connection Mgr
         Starting with version 8.50, Windows supports https.
         To connect to an existing session, you must include the following three parameters:
             serverIpPort=<the ssl port>
             sessionId=<the session ID>
             httpsSecured=True
"""

import os, sys, traceback, time

from IxNetRestApi.IxNetRestApi import *
from IxNetRestApi.IxNetRestApiProtocol import Protocol
from IxNetRestApi.IxNetRestApiTraffic import Traffic
from IxNetRestApi.IxNetRestApiFileMgmt import FileMgmt
from IxNetRestApi.IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApi.IxNetRestApiStatistics import Statistics
from IxNetRestApi.IxNetRestApiPacketCapture import PacketCapture

# Default the API server to either windows or linux.
osPlatform = 'windows'

if len(sys.argv) > 1:
    if sys.argv[1] not in ['windows', 'windowsConnectionMgr', 'linux']:
        sys.exit("\nError: %s is not a known option. Choices are 'windows' or 'linux'." % sys.argv[1])
    osPlatform = sys.argv[1]

try:
    #---------- Preference Settings --------------

    forceTakePortOwnership = True
    releasePortsWhenDone = False
    enableDebugTracing = True
    deleteSessionAfterTest = False ;# For Windows Connection Mgr and Linux API server only

    # If the licenses are activated in the Linux based XGS chassis or if the licenses are configured 
    # in the Windows IxNetwork GUI API server in preferences, then you won't need to config license.
    configLicense = True
    licenseServerIp = '192.168.70.3'
    licenseModel = 'subscription'
    licenseTier = 'tier3'

    ixChassisIp = '192.168.70.128'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'],
                [ixChassisIp, '1', '2']]

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.9',
                          serverIpPort='443',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=osPlatform,
                          apiKey='173c9e239c714c8ea73d549c0e62cc82',
                          sessionId=5
                          )

    if osPlatform in ['windows']:
        mainObj = Connect(apiServerIp='192.168.70.3',
                          serverIpPort='11009',
                          serverOs=osPlatform,
                          deleteSessionAfterTest=deleteSessionAfterTest
                          )
    
    if osPlatform in ['windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='192.168.70.3',
                          serverIpPort='11009',
                          serverOs=osPlatform,
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          sessionId=8020,
                          httpsSecured=False
                          )
    
    trafficObj = Traffic(mainObj)
    statObj = Statistics(mainObj)
    protocolObj = Protocol(mainObj)
    portObj = PortMgmt(mainObj)
    
    
except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    print('\nTest failed! {0}\n'.format(traceback.print_exc()))
    print(errMsg)
    if osPlatform == 'linux':
        mainObj.linuxServerStopAndDeleteSession()
