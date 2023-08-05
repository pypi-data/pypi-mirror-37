#!/usr/bin/env python

import StringIO

from InventoryFilter import InventoryFilter


class LibvirtInventory(InventoryFilter):

    def get_host_ips(self, topo):
        ips = []
        if not ('libvirt_res' in topo):
            return ips
        for val in topo.get('libvirt_res', []):
            ips.append(val.get('ip', 'NA'))
        return ips


    def get_inventory(self, topo, layout):

        if len(topo['libvirt_res']) == 0:
            return ""

        inven_hosts = self.get_host_ips(topo)

        # adding sections to respective host groups
        host_groups = self.get_layout_host_groups(layout)
        self.add_sections(host_groups)

        # set children for each host group
        self.set_children(layout)

        # set vars for each host group
        self.set_vars(layout)

        # add ip addresses to each host
        self.add_ips_to_groups(inven_hosts, layout)
        self.add_common_vars(host_groups, layout)
        output = StringIO.StringIO()
        self.config.write(output)

        return output.getvalue()
