# Electricity grid capacities

This module prepares electricity grid capacities and net transfer capacities for Europe at different spatial resolution based on the [PyPSA-Eur](https://github.com/PyPSA/pypsa-eur/) workflow.

A modular `snakemake` workflow built for [`clio`](https://clio.readthedocs.io/) data modules.

## Using this module

This module can be imported directly into any `snakemake` workflow.
Please consult the integration example in `tests/integration/Snakefile` for more information.

The workflow requires you to provide two ingredients manually: A PyPSA-EUR network at some spatial resolution, and the associated shapes. 

The [pre-build models](https://zenodo.org/records/7646728) provided on Zenodo do not include networks clustered to administrative regions yet. To get these, or to get the latest version of the data, you need to run the PyPSA-Eur workflow yourself. For details, please consult the documentation. Here we list the steps to prepare the electricity network at NUTS3 resolution.

```shell
git clone pypsa-eur

conda env create -f envs/linux-64.lock.yaml # select the appropriate file for your platform

conda activate pypsa-eur

snakemake data/bundle/ppp_2019_1km_Aggregated.tif --configfile config/config.default.yaml
    
snakemake resources/networks/base_s_adm.nc --configfile config/config.network_adm.yaml
```

Here, `config.network_adm.yaml` only contains the following few lines.

```yaml
clustering:
mode: administrative
administrative:
    level: 3
```

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
