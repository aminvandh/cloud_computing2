import libvirt
import xml.etree.ElementTree as ET
import os
import sys

def create_vm(xml, storage_amount):
    conn = libvirt.open("qemu:///system")
    
    if conn is None:
        print("Failed to open connection to qemu")
        sys.exit(1)

    # Modify the XML string before defining the domain
    xml_tree = ET.fromstring(xml)
    disc_allocation = xml_tree.find(".//disk/allocation")
    disc_allocation.set("size", f"{storage_amount}G")

    dom = conn.defineXML(ET.tostring(xml_tree).decode())

    if dom is None:
        print("Is XML empty?")
        sys.exit(1)

    vm_name = dom.name()
    qcow2_path = os.path.expanduser(f"~/{vm_name}_{storage_amount}GB.qcow2")

    if dom.create() < 0:
        print("Cannot boot guest domain")
        sys.exit(1)

    print(f"Guest {vm_name} has booted, ID: {dom.ID()}")

xml = """
<domain type='qemu'>
  <name>22vi22</name>
  <memory unit="MiB">2148</memory>
  <vcpu placement='static'>2</vcpu>
  <devices>
    <controller type="pci" model="pci-root" />
    <disk type="file" device="disk">
      <source file="/home/hooman/ubuntu.img" />
      <target dev="vda" bus="virtio" />
      <allocation size="10G" />
    </disk>
    <graphics type="vnc" port="5901" />
    <serial type='pty'>
      <target port='0'/>
    </serial>
    <console type='pty'>
      <target type='serial' port='0'/>
    </console>
  </devices>
  <os>
    <type arch='x86_64' machine="pc-i440fx-2.12">hvm</type>
    <kernel>/home/hooman/kernel</kernel>
    <cmdline>console=tty1</cmdline>
  </os>
</domain>
"""

create_vm(xml, 10)
