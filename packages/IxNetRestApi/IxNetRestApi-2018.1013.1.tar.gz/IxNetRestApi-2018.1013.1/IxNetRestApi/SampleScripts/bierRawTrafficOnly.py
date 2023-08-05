"""
 PLEASE READ DISCLAIMER

    This is a sample script for demo and reference purpose only.
    It is subject to change for content updates without warning.

 REQUIREMENTS
    - Python 2.7 minimum
    - Python module: requests
    - IxNetwork 8.41+

 DESCRIPTION
    - No protocol emulation.
    - Two Ixia ports connected back-2-back.
    - Configures 1 RAW Traffic Items with packet headers: Ethernet, MPLS, BIER, IPv4 and UDP.
         Raw packet header configurations:

           1: Ethernet II
           2: MPLS
                startLabel=1001
           3: BIER
                Nibble=5
                Ver=0
                BSL=64 Bits  <--
                Entropy=0
                OAM=0
                Rsv=0
                DSCP=0
                Proto=IPv4 Packet  <--
                BFIR-Id=1
                BitString <--
           4: IPv4
           5: UDP
                srcPort and dstPort set to default (Auto)

    - Start Traffic
    - Get stats

 USAGE
    python <script>.py windows
    python <script>.py linux
"""

import sys, os, traceback

from IxNetRestApi.IxNetRestApi import *
from IxNetRestApi.IxNetRestApiPortMgmt import PortMgmt
from IxNetRestApi.IxNetRestApiTraffic import Traffic
from IxNetRestApi.IxNetRestApiProtocol import Protocol
from IxNetRestApi.IxNetRestApiStatistics import Statistics

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
    deleteSessionAfterTest = True ;# For Windows Connection Mgr and Linux API server only

    licenseServerIp = '192.168.70.3'
    licenseModel = 'subscription'

    ixChassisIp = '192.168.70.128'
    # [chassisIp, cardNumber, slotNumber]
    portList = [[ixChassisIp, '1', '1'], [ixChassisIp, '1', '2']]

    if osPlatform == 'linux':
        mainObj = Connect(apiServerIp='192.168.70.108',
                          serverIpPort='443',
                          username='admin',
                          password='admin',
                          deleteSessionAfterTest=deleteSessionAfterTest,
                          verifySslCert=False,
                          serverOs=osPlatform,
                          generateLogFile='ixiaDebug.log'
                      )

    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='192.168.70.3',
                          serverIpPort='11009',
                          serverOs=osPlatform,
                          deleteSessionAfterTest=True,
                          generateLogFile='ixiaDebug.log'
                      )

    #---------- Preference Settings End --------------

    if osPlatform == 'windows':
        mainObj.newBlankConfig()

    mainObj.configLicenseServerDetails([licenseServerIp], licenseModel)

    portObj = PortMgmt(mainObj)
    vportList = portObj.assignPorts(portList, forceTakePortOwnership, rawTraffic=True)
    vport1 = vportList[0]
    vport2 = vportList[1]

    # For all parameter options, go to the API configTrafficItem.
    # mode = create or modify
    # Note: Check API configTrafficItem for options.
    trafficObj = Traffic(mainObj)
    trafficStatus = trafficObj.configTrafficItem(mode='create',
                                                 trafficItem = {
                                                     'name':'Stream_BFR_11',
                                                     'trafficType':'raw',
                                                     'trafficItemType': 'l2L3',
                                                     'biDirectional':False,
                                                     'trackBy': ['trackingenabled0']
                                                 },
                                                 endpoints = [{'name':'Flow-Group-1',
                                                               'sources': [vport1],
                                                               'destinations': [vport2]
                                                           }],
                                                 configElements = [{'transmissionType': 'continuous',
                                                                    'frameRate': 10000,
                                                                    'frameRateType': 'framesPerSecond',
                                                                    'frameSize': 512}])

    # Get the traffic item objects for modifying
    trafficItemObj   = trafficStatus[0]
    configElementObj = trafficStatus[2][0]

    # This will show you all the available protocol header options to create
    #trafficObj.showProtocolTemplates(configElementObj)

    stackObj = trafficObj.getPacketHeaderStackIdObj(configElementObj, stackId=1)
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Destination MAC Address',
                                       data={'valueType': 'increment',
                                             'startValue': '00:0c:29:76:b4:39',
                                             'stepValue': '00:00:00:00:00:01',
                                             'countValue': 1})

    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Source MAC Address',
                                       data={'valueType': 'increment',
                                             'startValue': '00:0c:29:aa:86:00',
                                             'stepValue': '00:00:00:00:00:01',
                                             'countValue': 1})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='MPLS', stackNumber=1, action='append')

    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Label Value',
                                       data={'valueType': 'increment',
                                             'startValue': '1001',
                                             'stepValue': '1',
                                             'countValue': 1,
                                             'auto': False})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='BIER', stackNumber=2, action='append')
    # 1=64Bits  2=128Bits  3=256Bits
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='BSL',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '1',
                                             'auto': False})
       
    # 4=IPv4 Packet
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Proto',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '4',
                                             'auto': False})
    
    
    # bit-string
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Egress Peer Set 0',
                                       data={'valueType': 'singleValue',
                                             'singleValue': '400',
                                             'auto': False})

    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='IPv4', stackNumber=3, action='append')

    # src = 10.1.1.1
    trafficObj.configPacketHeaderField(stackObj,
                                    fieldName='Source Address',
                                       data={'valueType': 'increment',
                                             'startValue': '10.1.1.1',
                                             'stepValue': '0.0.0.1',
                                             'countValue': 1})
    
    # dst = 10.1.1.2
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='Destination Address',
                                       data={'valueType': 'increment',
                                             'startValue': '10.1.1.2',
                                             'stepValue': '0.0.0.1',
                                             'countValue': 1})
    
    stackObj = trafficObj.addTrafficItemPacketStack(configElementObj, protocolStackNameToAdd='UDP', stackNumber=4, action='append')
    # 1: UDP-Source-Port
    # 2: UDP-Dest-Port
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='UDP-Source-Port',
                                       data={'auto': True})
    
    trafficObj.configPacketHeaderField(stackObj,
                                       fieldName='UDP-Dest-Port',
                                       data={'auto': True})
    
    trafficObj.showTrafficItemPacketStack(configElementObj)


    trafficObj.startTraffic(regenerateTraffic=True, applyTraffic=True)

    # Check the traffic state before getting stats.
    #    Use one of the below APIs based on what you expect the traffic state should be before calling stats.
    #    'stopped': If you expect traffic to be stopped such as for fixedFrameCount and fixedDuration.
    #    'started': If you expect traffic to be started such as in continuous mode.
    #trafficObj.checkTrafficState(expectedState=['stopped'], timeout=45)
    trafficObj.checkTrafficState(expectedState=['started'], timeout=45)

    statObj = Statistics(mainObj)
    stats = statObj.getStats(viewName='Traffic Item Statistics')

    if releasePortsWhenDone == True:
        portObj.releasePorts(portList)

    if osPlatform == 'linux':
        mainObj.linuxServerStopAndDeleteSession()

    if osPlatform == 'windowsConnectionMgr':
        mainObj.deleteSession()

except (IxNetRestApiException, Exception, KeyboardInterrupt):
    if enableDebugTracing:
        if not bool(re.search('ConnectionError', traceback.format_exc())):
            print('\n%s' % traceback.format_exc())

    if 'mainObj' in locals() and osPlatform == 'linux':
        if deleteSessionAfterTest:
            mainObj.linuxServerStopAndDeleteSession()

    if 'mainObj' in locals() and osPlatform in ['windows', 'windowsConnectionMgr']:
        if releasePortsWhenDone and forceTakePortOwnership:
            portObj.releasePorts(portList)

        if osPlatform == 'windowsConnectionMgr':
            if deleteSessionAfterTest:
                mainObj.deleteSession()
