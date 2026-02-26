# Electricity grid capacities

This module prepares electricity grid capacities and net transfer capacities for Europe at different spatial resolution based on the [PyPSA-Eur](https://github.com/PyPSA/pypsa-eur/) workflow.

## Using this module

This module can be imported directly into any `snakemake` workflow.
Please consult the integration example in `tests/integration/Snakefile` for more information.

Currently, the workflow requires you to provide two ingredients manually: A PyPSA network at a given spatial resolution, and the associated shapes. Before running the module, you need to put two files in the following locations.

```
resources/user/network.nc
resources/user/shapes.geojson
```

You can use the [pre-build PyPSA-Eur models](https://zenodo.org/records/7646728) provided on Zenodo. However, networks clustered to administrative regions are not provided there. To get these, or to get a most recent version, you need to run the PyPSA-Eur workflow yourself. For details, please consult the documentation. Here are the steps to prepare the electricity network at NUTS3 resolution.

```shell
git clone pypsa-eur

conda env create -f envs/linux-64.lock.yaml # select the appropriate file for your platform

conda activate pypsa-eur
    
snakemake resources/networks/base_s_adm.nc --configfile config/config.network_adm.yaml
```

Here, `config.network_adm.yaml` only contains the following.

```yaml
clustering:
mode: administrative
administrative:
    level: 3
transmission_projects:
  enable: true
  include:
    tyndp2020: true
    nep: true
    manual: true
  skip:
  - upgraded_lines
  - upgraded_links
  status:
  - under_construction
  - in_permitting
  - confirmed
  new_link_capacity: zero #keep or zero
```

In future versions of the module, the preparation of the network may be performed internally.

## Development

We use [`pixi`](https://pixi.sh/) as our package manager for development.
Once installed, run the following to clone this repo and install all dependencies.

```shell
git clone git@github.com:calliope-project/module_electricity_grid.git
cd module_electricity_grid
pixi install --all
```

For testing, simply run:

```shell
pixi run test
```

To view the documentation locally, use:

```shell
pixi run serve-docs
```

To test a minimal example of a workflow using this module:

```shell
pixi shell    # activate this project's environment
cd tests/integration/  # navigate to the integration example
snakemake --use-conda  # run the workflow!
```
