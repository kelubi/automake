################
#!/usr/bin/env bash
#Lion Changed by stack.sh
# QQ:11315889
# MAIL:11315889@QQ.COM
# Destination path for installation ``DEST``
DEST=${DEST:-/opt/stack}

# You should use the regular user that you used for stack.sh to run this script.
if [[ $EUID -eq 0 ]]; then
    echo "You are running this script as root. Don't. Use the user created by stack.sh instead."    
    exit 1
fi

# Set the destination directories for openstack projects

NOVA_DIR=$DEST/nova
HORIZON_DIR=$DEST/horizon
GLANCE_DIR=$DEST/glance
KEYSTONE_DIR=$DEST/keystone
NOVACLIENT_DIR=$DEST/python-novaclient
OPENSTACKX_DIR=$DEST/openstackx
NOVNC_DIR=$DEST/noVNC
SWIFT_DIR=$DEST/swift
SWIFT_KEYSTONE_DIR=$DEST/swift-keystone2
QUANTUM_DIR=$DEST/quantum

# Default Quantum Plugin
Q_PLUGIN=${Q_PLUGIN:-openvswitch}

# Specify which services to launch.  These generally correspond to screen tabs
ENABLED_SERVICES=${ENABLED_SERVICES:-g-api,g-reg,key,n-api,n-cpu,n-net,n-sch,n-vnc,horizon,mysql,rabbit,openstackx}
# Nova hypervisor configuration.  We default to libvirt whth  **kvm** but will
# drop back to **qemu** if we are unable to load the kvm module.  Stack.sh can
# also install an **LXC** based system.
VIRT_DRIVER=${VIRT_DRIVER:-libvirt}
LIBVIRT_TYPE=${LIBVIRT_TYPE:-kvm}

# nova supports pluggable schedulers.  ``SimpleScheduler`` should work in most
# cases unless you are working on multi-zone mode.
SCHEDULER=${SCHEDULER:-nova.scheduler.simple.SimpleScheduler}

# Use the first IP unless an explicit is set by ``HOST_IP`` environment variable
if [ ! -n "$HOST_IP" ]; then
    HOST_IP=`LC_ALL=C /sbin/ifconfig  | grep -m 1 'inet addr:'| cut -d: -f2 | awk '{print $1}'`
fi

# Service startup timeout
SERVICE_TIMEOUT=${SERVICE_TIMEOUT:-60}
# our screen helper to launch a service in a hidden named screen
function screen_it {
    echo "screen_it $1"
    NL=`echo -ne '\015'`
    if [[ "$ENABLED_SERVICES" =~ "$1" ]]; then
        screen -S stack -X screen -t $1
        # sleep to allow bash to be ready to be send the command - we are
        # creating a new window in screen and then sends characters, so if
        # bash isn't running by the time we send the command, nothing happens
        sleep 2
        screen -S stack -p $1 -X stuff "$2$NL"
    fi
}

# create a new named screen to run processes in
screen -d -m -S stack -t stack
sleep 2


# launch the glance registry service
if [[ "$ENABLED_SERVICES" =~ "g-reg" ]]; then
    echo "waiting for glance registry start..." 
    screen_it g-reg "cd $GLANCE_DIR; bin/glance-registry --config-file=etc/glance-registry.conf"
fi
# launch the glance api and wait for it to answer before continuing
if [[ "$ENABLED_SERVICES" =~ "g-api" ]]; then
    screen_it g-api "cd $GLANCE_DIR; bin/glance-api --config-file=etc/glance-api.conf"
    GLANCE_HOSTPORT=${GLANCE_HOSTPORT:-$HOST_IP:9292}
    echo "Waiting for g-api ($GLANCE_HOSTPORT) to start..."
    if ! timeout $SERVICE_TIMEOUT sh -c "while ! wget -q -O- http://$GLANCE_HOSTPORT; do sleep 1; done"; then
      echo "g-api did not start"
      exit 1
    fi
fi
# launch the keystone and wait for it to answer before continuing
if [[ "$ENABLED_SERVICES" =~ "key" ]]; then
    screen_it key "cd $KEYSTONE_DIR && $KEYSTONE_DIR/bin/keystone --config-file $KEYSTONE_DIR/etc/keystone.conf -d"
    echo "Waiting for keystone to start..."
    if ! timeout $SERVICE_TIMEOUT sh -c "while ! wget -q -O- http://127.0.0.1:5000; do sleep 1; done"; then
      echo "keystone did not start"
      exit 1
    fi
fi
# launch the nova-api and wait for it to answer before continuing
if [[ "$ENABLED_SERVICES" =~ "n-api" ]]; then
    screen_it n-api "cd $NOVA_DIR && $NOVA_DIR/bin/nova-api"
    echo "Waiting for nova-api to start..."
    if ! timeout $SERVICE_TIMEOUT sh -c "while ! wget -q -O- http://127.0.0.1:8774; do sleep 1; done"; then
      echo "nova-api did not start"
      exit 1
    fi
fi
# Quantum
if [[ "$ENABLED_SERVICES" =~ "q-svc" ]]; then


    QUANTUM_PLUGIN_INI_FILE=$QUANTUM_DIR/quantum/plugins.ini
   screen_it q-svc "cd $QUANTUM_DIR && export PYTHONPATH=.:$PYTHONPATH; python $QUANTUM_DIR/bin/quantum $QUANTUM_DIR/etc/quantum.conf"
fi

# Quantum agent (for compute nodes)
if [[ "$ENABLED_SERVICES" =~ "q-agt" ]]; then
    if [[ "$Q_PLUGIN" = "openvswitch" ]]; then
        # Set up integration bridge
        OVS_BRIDGE=${OVS_BRIDGE:-br-int}
        sudo ovs-vsctl --no-wait -- --if-exists del-br $OVS_BRIDGE
        sudo ovs-vsctl --no-wait add-br $OVS_BRIDGE
        sudo ovs-vsctl --no-wait br-set-external-id $OVS_BRIDGE bridge-id br-int
    fi

    # Start up the quantum <-> openvswitch agent
    screen_it q-agt "sleep 4; sudo python $QUANTUM_DIR/quantum/plugins/openvswitch/agent/ovs_quantum_agent.py $QUANTUM_DIR/quantum/plugins/openvswitch/ovs_quantum_plugin.ini -v"
fi
# Launching nova-compute should be as simple as running ``nova-compute`` but
# have to do a little more than that in our script.  Since we add the group
# ``libvirtd`` to our user in this script, when nova-compute is run it is
# within the context of our original shell (so our groups won't be updated).
# Use 'sg' to execute nova-compute as a member of the libvirtd group.
screen_it n-cpu "cd $NOVA_DIR && sg libvirtd $NOVA_DIR/bin/nova-compute"
screen_it n-vol "cd $NOVA_DIR && $NOVA_DIR/bin/nova-volume"
screen_it n-net "cd $NOVA_DIR && $NOVA_DIR/bin/nova-network"
screen_it n-sch "cd $NOVA_DIR && $NOVA_DIR/bin/nova-scheduler"
screen_it n-sch "cd $NOVA_DIR && $NOVA_DIR/bin/nova-scheduler"
screen_it n-vnc "cd $NOVNC_DIR && ./utils/nova-wsproxy.py --flagfile $NOVA_DIR/bin/nova.conf --web . 6080"
screen_it horizon "cd $HORIZON_DIR && sudo tail -f /var/log/apache2/error.log"

echo "Start stack script run complete. Please waite a moment then check the site http://$HOST_IP"