ubuntu_version=20.04
base_image=ubuntu-${ubuntu_version}-server-cloudimg-amd64.img
ubuntu_url=https://cloud-images.ubuntu.com/releases/${ubuntu_version}/release/${base_image}
intermediary_disk=ubuntu-builder-vm-disk.qcow2
user_data=user-data.yaml
user_data_img=user-data.img
build_machine_name=ubuntu-build-vm
cache_dir=cache
image_base_disk_size="20G"
mem_in_gigs=4
mem_mbytes=$(shell echo $$((${mem_in_gigs} * 1024)))
cpus=4
virt_network=default


init: clean
	mkdir -p ${cache_dir}
	systemctl start libvirtd
	if [ ! -f "${cache_dir}/${base_image}" ]; then wget ${ubuntu_url} -P ${cache_dir}; fi

init-build-machine: clean
	cloud-localds "${cache_dir}/${user_data_img}" ${user_data}
	qemu-img create -b ${base_image} -F qcow2 -f qcow2 ${cache_dir}/${intermediary_disk} ${image_base_disk_size}

	virt-install --name ${build_machine_name} \
  		--virt-type kvm \
		--memory ${mem_mbytes} \
		--vcpus ${cpus} \
  		--boot hd,menu=on \
  		--disk path=${cache_dir}/${intermediary_disk},device=disk \
  		--disk path=${cache_dir}/${user_data_img},format=raw \
  		--graphics none \
  		--os-variant ubuntu${ubuntu_version} \
  		--network ${virt_network} \
  		--noautoconsole

build: init-build-machine
build_machine_ip=$(shell virsh domifaddr ubuntu-build-vm | sed 1,2d | awk '{print $4}' | awk '{gsub("/24", ""); print}')





clean:
	virsh destroy ${build_machine_name} || true
	virsh undefine ${build_machine_name} || true
	rm -f ${cache_dir}/${intermediary_disk} || true
	rm -f ${cache_dir}/${user_data_img} || true

install:
	@echo "Installing required packages"
	apt-get update -y
	apt-get install -y \
    	qemu\
    	qemu-kvm\
    	libvirt-daemon\
    	libvirt-clients\
    	bridge-utils\
    	virt-manager\
    	cloud-image-utils\
   		libguestfs-tools\
    	build-essential
	systemctl enable libvirtd