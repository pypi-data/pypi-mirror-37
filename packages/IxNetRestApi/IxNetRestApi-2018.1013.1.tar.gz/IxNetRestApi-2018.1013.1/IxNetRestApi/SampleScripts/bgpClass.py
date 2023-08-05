import re

class BGP():
    '''
    Creates and configures BGP for a given traffic device
    '''
    def __init__(self, rest, obj, **kwargs):
        """
        :param rest: This is the OpenIxia protocolObj.
        :param  obj: This is the OpenIxia IPv4|IPv6 object handle or BGP object handle.
                     If creating a new BGP config, obj needs to be an IPv4|IPv6 object handle.
                     If modifying a new BGP config, obj needs to be a BGP object handle.
        :param **kwargs: The bgp attributes.

        Hubert's instructions:
           Description:

        - Trevor @ Cisco gave us a BGP class and a long list of predefined BGP attributes shown below after my instructions.
        - These predefined BGP attributes are common names for scripts to use for BGP attributes for both Ixia and Spirent configurations.
        - Scripts will be passing in these attributes in the **kwargs parameter.
                                                                                                                      .
        - The challenge is that this BGP class is doing three different things.
                1> Create or modify BGP
                2> Configure Network Group (Route Ranges)
                3> Configure Network Group / IP Prefix Pools / bgpIPRouteRange

        Solution:

           - The first thing we need to do is create a dict to map all the predefined bgp attributes to IxNetwork BGP attributes.
           - I only mapped out a few to test my solution.
           - You need to map out the rest by using the API browser.

           - The function buildIxNetBgpDict() will create three dicts containing IxNetwork bgp attributes for configuring BGP and route ranges.
                1> self.ixNetBgpMapping
                2> self.ixNetNetworkGroupMapping
                3> self.ixNetRouteRangeMapping

           - At the time when the config() function is called, it will know what to configure by reading the three dicts.
           - I have tested the PoC and everything is working.
           - Get the latest OpenIxia update.
           - You should not need to create any new APIs.  Let me know if you need to.

           - You have to do the rest of the mappings.  I only did a few to test my solution.
           - I am attaching two files:
                - bgpClass.py:  This is the bgp class you will be working on.
                - bgpClassTest.py:  This is a script that I created and used for testing the solution.  Please continue using it the way it is.

           - The prerequisite is to configure a BGP config on IxNetwork.
           - You need to configure and verify every attribute that is applicable to IxNetwork.
           - For the ones that applies to IxNetwork, they want us to set the default value for all the attributes defined in this class.
           - Comment out the ones that don't apply.  Don't delete them.
           - Give Hubert a list of attributes that you cannot map to IxNetork BGP attributes.


        """
        self.rest = rest
        self.obj = obj

        # deviceGroupObj is for protocol.configNetworkGroup()
        match = re.match('(/api.*/deviceGroup/[0-9]+).*', obj)
        self.deviceGroupObj = match.group(1)

        # Hubert notes:
        #    I started some mappings for PoC.  India team needs to complete the rest of the attribute mappings..
        #    The keys are the Cisco defined bgp attributes.  The values are mappings to IxNetwork bgp attributes.

        # These mappings are for configBgp()
        self.ixNetBgpMapping = {'bgp_active': 'enableBgp',
                                'bgp_dut_ip_address': 'dutIp',
                                'bgp_dut_4_byte_as': 'localAs4Bytes',
                                'bgp_enable_4_byte_as': 'enable4ByteAs',
                                'bgp_hold_time_interval': 'holdTimer',
                                'bgp_enable_graceful_restart': 'enableGracefulRestart',
                            }

        # These mappings are for configNetworkGroup()
        self.ixNetNetworkGroupMapping = {'bgp_v4_route_count': 'multiplier',
                                         'bgp_v4_route_start_network': 'networkAddress',
                                         'bgp_v6_route_count': 'multiplier'
                                     }

        # Hubert note: You have to configure IPv6 for BGP and get the attributes for the IxNetwork bgp attributes.
        #              Using this dict for configPrefixPoolsRouteProperty()
        self.ixNetRouteRangeMapping = {'bgp_v4_route_active': 'active'
        }


        # Primary Config
        self.bgp_active = None
        self.bgp_router_state = None
        self.bgp_as_num = None
        self.bgp_enable_4_byte_as = None
        self.bgp_4_byte_as = None
        self.bgp_dut = None
        self.bgp_dut_4_byte_as = None
        self.bgp_dut_ip_address = None
        self.bgp_authentication = None
        self.bgp_password = None
        self.bgp_minimum_label = None
        self.bgp_hold_time_interval = None
        self.bgp_keep_alive_interval = None
        self.bgp_enable_graceful_restart = None
        self.bgp_v4_afi = None
        self.bgp_v6_afi = None
        self.bgp_link_state_afi = None
        self.bgp_unicast_subafi = None
        self.bgp_multicast_subafi = None
        self.bgp_mdt_subafi = None
        self.bgp_evpn_subafi = None
        self.bgp_vpls_subafi = None
        self.bgp_flowspec_subafi = None
        self.bgp_labeled_ip_subafi = None
        self.bgp_sr_te_pol_subafi = None
        self.bgp_ei = None
        self.bgp_session_ip = None
        self.bgp_ipv4_route_count = None
        self.bgp_ipv6_route_count = None
        self.bgp_ttl = None

        # v4 Route Config
        self.bgp_v4_route_active = None
        self.bgp_v4_route_count = 1
        self.bgp_v4_route_routes_per_router = None
        self.bgp_v4_route_networks_per_router = None
        self.bgp_v4_route_start_network = None
        self.bgp_v4_route_prefix_incr = None
        self.bgp_v4_route_origin = None
        self.bgp_v4_route_as_path = None
        self.bgp_v4_route_as_paths_per_block = None
        self.bgp_v4_route_as_paths_inc_per_router = None
        self.bgp_v4_route_segment_type = None
        self.bgp_v4_route_next_hop = None
        self.bgp_v4_route_next_hops_incr_per_router = None
        self.bgp_v4_route_communities_per_block = None
        self.bgp_v4_route_extended_communities_per_block = None

        # v6 Route Config
        self.bgp_v6_route_active = None
        self.bgp_v6_route_count = 1
        self.bgp_v6_route_routes_per_router = None
        self.bgp_v6_route_networks_per_router = None
        self.bgp_v6_route_start_network = None
        self.bgp_v6_route_prefix_incr = None
        self.bgp_v6_route_origin = None
        self.bgp_v6_route_as_path = None
        self.bgp_v6_route_as_paths_per_block = None
        self.bgp_v6_route_as_paths_inc_per_router = None
        self.bgp_v6_route_segment_type = None
        self.bgp_v6_route_next_hop = None
        self.bgp_v6_route_next_hops_incr_per_router = None
        self.bgp_v6_route_communities_per_block = None
        self.bgp_v6_route_extended_communities_per_block = None

        self.buildIxNetBgpDict(mode='create', **kwargs)

    def buildIxNetBgpDict(self, mode='create', **kwargs):
        """
        Build a config param dict for IxNetwork BGP.

        :param mode: <create|modify>:  Used by NetworkGroup.
        """
        # Create by Hubert: Convert the user defined attributes to IxNetwork attributes.
        # This function is used by both __init__() and modify().
        self.bgpDict = {}
        self.networkGroupDict = {}
        self.routeRangeDict = {}

        for key,value in kwargs.items():
            if key in self.ixNetBgpMapping:
                # Set the Cisco defined attrbutes with user's value
                self.__dict__[key] = value
                if key == 'bgp_dut_ip_address':
                    self.bgpDict['dutIp'] = {'start': value , 'direction': 'increment', 'step': '0.0.0.0'}
                    continue

                self.bgpDict[self.ixNetBgpMapping[key]] = value

            if key in self.ixNetRouteRangeMapping:
                self.routeRangeDict[self.ixNetRouteRangeMapping[key]] = value

            if key in self.ixNetNetworkGroupMapping:
                if key in ['bgp_v4_route_start_network', 'bgp_v6_route_start_network']:
                    if int(self.__dict__['bgp_v4_route_count']) > 1 or int(self.__dict__['bgp_v6_route_count']) > 1:
                        step = '0.0.0.1'
                    else:
                        step = '0.0.0.0'

                    self.networkGroupDict['networkAddress'] = {'start': value , 'direction': 'increment', 'step': step}
                    continue

                self.networkGroupDict[self.ixNetNetworkGroupMapping[key]] = value

        if self.networkGroupDict != {}:
            if mode == 'create':
                self.networkGroupDict['create'] = self.deviceGroupObj
            if mode == 'modify':
                self.networkGroupDict['modify'] = self.networkGroupObj

    def config(self):
        '''
        Creates a new BGP object for a given device.
        '''
        if self.bgpDict != {}:
            self.bgpObj = self.rest.configBgp(self.obj, **self.bgpDict)

        if self.networkGroupDict != {}:
            self.networkGroupObj, self.prefixPoolObj = self.rest.configNetworkGroup(**self.networkGroupDict)

        if self.routeRangeDict != {}:
            self.routeRangeObj = self.rest.configPrefixPoolsRouteProperty(self.prefixPoolObj,
                                                                          'bgpIPRouteProperty',
                                                                          **self.routeRangeDict)
        return self.bgpObj

    def modify(self, **kwargs):
        '''
        Hubert notes:
           1> Modifies any existing BGP attribute.
           2> Modify Network Group (Route Range)
           3> Modify PrefixPools 'bgpIpRouteProperty'

           Although this class creates/modifies three areas, all the object handle
           are created already.  This class holds all the objects to use.
           So it depends on what **kwargs the user is passing in.
        '''
        self.buildIxNetBgpDict(mode='modify', **kwargs)

        # For modifying, change self.obj to self.bgpObj because OpenIxia configBgp()
        # uses the bgp object handle to modify.
        # If configBgp() doesn't see bgp in the objecthandle, it treats the config as a new BGP configuration.
        # If configBgp() see's bgp in the object handle, it treats it as modify.
        self.obj = self.bgpObj
        self.config()

