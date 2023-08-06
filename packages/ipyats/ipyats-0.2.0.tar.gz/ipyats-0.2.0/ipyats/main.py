import argparse
import os
from IPython import embed

from genie.conf import Genie
from ats.topology import loader
from genie.abstract import Lookup # noqa
from genie.libs import ops, conf # noqa
from genie.utils.diff import Diff # noqa

import ipyats.tasks as tasks # noqa
from ipyats.utils import show_source  # noqa

import ipyats.public_testbeds


def main():

    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument('--testbed', dest='testbed', type=loader.load)
    args, unknown = parser.parse_known_args()

    if not args.testbed:
        print("""
    **************************************************************
    You didn't specify a testbed, we'll load up a Devnet sandbox.

    Next time try with your own testbed file by running

    ipyats --testbed <your file>
    **************************************************************
        """)
        path = os.path.abspath(os.path.join(ipyats.__file__, os.pardir))
        testbed = path + '/public_testbeds/devnet_sandbox.yaml'
        testbed = loader.load(testbed)
        testbed = Genie.init(testbed)

    else:

        # pyats testbed != genie testbed
        testbed = Genie.init(args.testbed)

    print("""
    Welcome to ipyATS!

    your testbed is now available as the `testbed` object

    You can start by exploring some of the common operations available for the
    testbed by typing

    dir(testbed)

    To get you started, we've also included some common tasks, give them
    a try and then checkout the code in the `tasks` folder

    dir(tasks)

    You can checkout the source code for any of these funtions by passing
    them to show_source

    e.g show_source(tasks.get_routing_table)
    """)

    # if it's sandbox, these will come in handy
    if testbed.name == "devnet_always_on_sandbox":
        csr = testbed.devices['csr1000v'] # noqa
        nx = testbed.devices['sbx-n9kv-ao'] # noqa
        print("""
    Detected Always-On Sandbox, creating some handy objects

    Created objects `csr` and `nx`")

    csr = testbed.devices['csr1000v']
    nx = testbed.devices['sbx-n9kv-ao']
    """)

    # bail to iPython
    embed()


if __name__ == '__main__':
    main()
