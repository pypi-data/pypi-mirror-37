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

    if osPlatform in ['windows', 'windowsConnectionMgr']:
        mainObj = Connect(apiServerIp='192.168.70.3',
                          serverIpPort='11009',
                          serverOs=osPlatform
                          )
    
    # Configure BGP on IxNetwork first.
    
    ipv4Obj1 = '/api/v1/sessions/1/ixnetwork/topology/1/deviceGroup/1/ethernet/1/ipv4/1'

    import bgpClass
    protocolObj = Protocol(mainObj)

    bgpObj = bgpClass.BGP(rest = protocolObj,
                          obj = ipv4Obj1,
                          bgp_active = True,
                          bgp_dut_ip_address = '1.1.1.1',
                          bgp_dut_4_byte_as = 101,
                          bgp_enable_4_byte_as = True,
                          bgp_hold_time_interval = 90,
                          bgp_enable_graceful_restart = False,
                          bgp_v4_route_count = '128',
                          bgp_v4_route_start_network = '100.10.10.1',
                          bgp_v4_route_active = True
                      )

    bgpObj.config()

    print('\n----- MODIFYING ----')
    bgpObj.modify(bgp_dut_ip_address = '1.1.1.2',
                  bgp_v4_route_count = '188',
                  bgp_v4_route_start_network = '200.8.8.1',
                  bgp_v4_route_active = False
           )

except (IxNetRestApiException, Exception, KeyboardInterrupt) as errMsg:
    print('\nTest failed! {0}\n'.format(traceback.print_exc()))
    print(errMsg)
    if osPlatform == 'linux':
        mainObj.linuxServerStopAndDeleteSession()
