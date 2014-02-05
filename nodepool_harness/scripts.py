import logging
import argparse
import os

# ssh-keygen -f nodepool -N ""
# ssh-add nodepool

PROVIDER="rax-dfw"
IMAGE="nh-xenserver"


def override_config_values(config, privkey_file, username, password, project_id):
	config.providers[PROVIDER].images[IMAGE].private_key = privkey_file
	config.providers[PROVIDER].username = username
	config.providers[PROVIDER].password = password
	config.providers[PROVIDER].project_id = project_id


def install_node():
	parser = argparse.ArgumentParser(description="Nodepool Harness")
	parser.add_argument('nodepool_dir', help='Point to a directory where nodepool lives')
	parser.add_argument('private_key', help='Point to your private key')
	parser.add_argument('username', help='Cloud username')
	parser.add_argument('password', help='Cloud password')
	parser.add_argument('project_id', help='Project id')
	args = parser.parse_args()

	import sys

	sys.path.append(os.path.abspath(args.nodepool_dir))

	privkey_file = os.path.abspath(args.private_key)

	logging.basicConfig(level=logging.DEBUG)
	import nodepool.nodepool
	np = nodepool.nodepool.NodePool('config.yaml')
	config = np.loadConfig()
	override_config_values(
		config, privkey_file, args.username, args.password, args.project_id)

	np.reconfigureDatabase(config)
	np.reconfigureManagers(config)
	np.setConfig(config)

	provider = config.providers[PROVIDER]
	image = provider.images[IMAGE]
	timeout = provider.boot_timeout

	import nodepool.nodedb
	with np.getDB().getSession() as session:
		snap_image = session.createSnapshotImage(
			provider_name=provider.name,
			image_name=image.name)

		updater = nodepool.nodepool.ImageUpdater(
			np, provider, image, snap_image.id)

		updater.run()
