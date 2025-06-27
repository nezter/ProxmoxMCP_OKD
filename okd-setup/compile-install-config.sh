#!/bin/bash

echo "Please edit okd-setup/ignitions/install-config.yaml.ORIG with your cluster details."
echo "Once edited, run the following command from the okd-setup directory to generate ignition configs:"
echo "./openshift-install create ignition-configs --dir=ignitions/"