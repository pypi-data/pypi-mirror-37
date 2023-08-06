from genie.abstract import Lookup # noqa
from genie.libs import ops, conf # noqa
from genie.utils.diff import Diff # noqa

def compare_stuff(obj1, obj2):
    diff = Diff(obj1, obj2)
    diff.findDiff()
    print(diff)


def get_interface_counters(dev):
    """
    returns parsed and normalized interface counters
    """
    if not dev.is_connected():
        dev.connect()
    abstract = Lookup.from_device(dev)
    # Find the Interface Parsers for this device
    # 1) Directory must exists in genie.libs.ops.<feature>
    # 2) Then abstraction will kick in to find the right one
    # 3) The directory syntax is <feature>.<feature.<Feature>
    #    Where the class is capitalized but the directory/files arent.
    intf = abstract.ops.interface.interface.Interface(dev)
    intf.learn()
    return intf.info


def get_routing_table(dev):
    """
    returns a parsed and normalized routing table
    """
    if not dev.is_connected():
        dev.connect()
    abstract = Lookup.from_device(dev)
    # The directory syntax is <feature>.<feature.<Feature>
    routing = abstract.ops.routing.routing.Routing(dev)
    routing.learn()
    return routing.info


def configure_loopback(dev, number, ip, mask, apply=True):
    """
    creates (it also removes the config immediately)
    """
    from genie.conf.base import Interface
    if not dev.is_connected():
        dev.connect()
    # this is a bug....shouldn't have to do this...
    if dev.os == 'iosxe':
        interface = Interface(device=dev, name='Loopback{}'.format(number))
    elif dev.os == 'nxos':
        interface = Interface(device=dev, name='loopback{}'.format(number))

    # Add some configuration
    interface.ipv4 = ip
    interface.ipv4.netmask = mask

    print("\n")
    print("******************************************************")
    print("Configuring interface {} on {}  ".format(dev.name, interface.name))
    print("******************************************************")

    interface.build_config(apply=True)
    print("\n")
    print("******************************************************")
    print("Removing interface {} on {}  ".format(dev.name, interface.name))
    print("******************************************************")

    interface.build_unconfig(apply=True)
    return interface


# reported
# def create_ethernet(dev):
#     from genie.conf.base import Interface
#     if not dev.is_connected():
#         dev.connect()
#     interface = Interface(device=dev, name='Ethernet1/55')
#     # Add some configuration
#     interface.ipv4 = '200.1.1.2'
#     interface.ipv4.netmask = '255.255.255.0'
#     interface.shutdown = False
#     # Verify configuration generated
#     interface.build_config(apply=False)
#     return interface


def bgp_ops(dev):
    if not dev.is_connected():
        dev.connect()
    abstract = Lookup.from_device(dev)
    bgp = abstract.ops.bgp.bgp.Bgp(dev)
    bgp.learn()
    return bgp.info
