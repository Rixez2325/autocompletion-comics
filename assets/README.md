# Assets

This directory contains all the assets used by the project, it includes external tools, repository, static assets and more.

## [ogkalu/Comic-Diffusion](https://huggingface.co/ogkalu/Comic-Diffusion)

Make sure you have git-lfs installed (<https://git-lfs.com>), then clone the repository.

* `git lfs install`
* `git clone https://huggingface.co/ogkalu/Comic-Diffusion`

if you want to clone without large files – just their pointers
prepend your git clone with the following env var:
`GIT_LFS_SKIP_SMUDGE=1`

After cloning you can use script [remove_unused_from_comic_diffusion.ps1](remove_unused_from_comic_diffusion.ps1) in order to reduce space on disk (18.2Gb -> 5.97Gb)
