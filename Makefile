PWN_HOSTNAME=cleanagotchi
PWN_VERSION=master

all: clean install image

install:
	curl https://releases.hashicorp.com/packer/1.3.5/packer_1.3.5_linux_amd64.zip -o /tmp/packer.zip
	unzip /tmp/packer.zip -d /tmp
	sudo mv /tmp/packer /usr/bin/packer
	git clone https://github.com/solo-io/packer-builder-arm-image /tmp/packer-builder-arm-image
	cd /tmp/packer-builder-arm-image && go get -d ./... && go build
	sudo cp /tmp/packer-builder-arm-image/packer-builder-arm-image /usr/bin

image:
	cd builder && sudo /usr/bin/packer build -var "pwn_hostname=$(PWN_HOSTNAME)" -var "pwn_version=$(PWN_VERSION)" cleanagotchi.json
	sudo mv builder/output-cleanagotchi/image cleanagotchi-raspbian-lite-$(PWN_VERSION).img
	sudo sha256sum cleanagotchi-raspbian-lite-$(PWN_VERSION).img > cleanagotchi-raspbian-lite-$(PWN_VERSION).sha256
	sudo zip cleanagotchi-raspbian-lite-$(PWN_VERSION).zip cleanagotchi-raspbian-lite-$(PWN_VERSION).sha256 cleanagotchi-raspbian-lite-$(PWN_VERSION).img

clean:
	rm -rf /tmp/packer-builder-arm-image
	rm -f cleanagotchi-raspbian-lite-*.zip cleanagotchi-raspbian-lite-*.img cleanagotchi-raspbian-lite-*.sha256
	rm -rf builder/output-cleanagotchi  builder/packer_cache
