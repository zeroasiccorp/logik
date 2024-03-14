import os
from github import Github
from github import Auth


def __find_release_artifact(release, artifact_name):
    for asset in release.assets:
        if asset.name == artifact_name:
            return asset.url
    return None


def get_release_url(release_tag, artifact_name, token=None):
    if not token:
        token = os.environ.get('GIT_TOKEN')
    auth = Auth.Token(token)
    g = Github(auth=auth)
    repo = g.get_repo('zeroasiccorp/ebrick-fpga')
    releases = repo.get_releases()
    for release in releases:
        if release.tag_name == release_tag:
            return __find_release_artifact(release, artifact_name)
    return None


def get_efpga_release_url(release_tag, artifact_name, token=None):
    if not token:
        token = os.environ.get('GIT_TOKEN')
    auth = Auth.Token(token)
    g = Github(auth=auth)
    repo = g.get_repo('zeroasiccorp/zeroasic-efpga')
    releases = repo.get_releases()
    for release in releases:
        if release.tag_name == release_tag:
            return __find_release_artifact(release, artifact_name)
    return None


if __name__ == "__main__":
    print(get_release_url('v0.1.4', 'ebrick_fpga_demo_cad.tar.gz'))
