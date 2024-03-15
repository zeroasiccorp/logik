import os
from github import Github
from github import Auth


def set_fpga_resources(fpga):
    part_name = fpga.design

    fpga.add('fpga', part_name, 'resources', 'registers', [
        'dff',
        'dffr',
        'dffs',
        'dffe',
        'dffer',
        'dffes',
        'dffrs',
        'dffers'])
    fpga.add('fpga', part_name, 'resources', 'brams', [
        'spram_1024x64',
        'spram_2048x32',
        'spram_4096x16',
        'spram_8192x8',
        'spram_16384x4',
        'spram_32768x2',
        'spram_65536x1',
        'dpram_1024x32',
        'dpram_2048x16',
        'dpram_4096x8',
        'dpram_8192x4',
        'dpram_16384x2',
        'dpram_32768x1'])
    fpga.add('fpga', part_name, 'resources', 'dsps', [
        'adder',
        'adder_regi',
        'adder_rego',
        'adder_regio',
        'acc',
        'acc_regi',
        'mult',
        'mult_regi',
        'mult_rego',
        'mult_regio',
        'macc',
        'macc_regi',
        'macc_pipe',
        'macc_pipe_regi'])


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
