#!/usr/bin/env sh

# Build a Jellyfin .rpm file with Docker on Linux
# Places the output .rpm file in the parent directory

set -o errexit
set -o xtrace
set -o nounset

package_temporary_dir="`mktemp -d`"
current_user="`whoami`"
image_name="jellyfin-rpmbuild"

cleanup() {
    set +o errexit
    docker image rm $image_name --force
    rm -rf "$package_temporary_dir"
}
trap cleanup EXIT INT

docker build . -t "$image_name" -f ./Dockerfile.fedora_package
docker run --rm -v "$package_temporary_dir:/temp" "$image_name" cp -r /jellyfin /temp/
sudo chown -R "$current_user" "$package_temporary_dir"
mv "$package_temporary_dir"/jellyfin/*.rpm ../
