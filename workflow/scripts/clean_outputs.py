import yaml
import geopandas as gpd
import pandas as pd
import pycountry
import logging

logger = logging.getLogger(__name__)

# Add Kosovo to pycountry
pycountry.countries.add_entry(
    alpha_2="XK", alpha_3="XXK", name="Kosovo", numeric="926"
)

def save_yaml(data, path):
    """Save dictionary to yaml file."""
    with open(path, 'w') as file:
        yaml.dump(data, file)


def map_to_iso_countries(countries_alpha_2):
    """Map ISO 3166-1 alpha-2 country codes to alpha-3 codes."""

    map_alpha_2_to_alpha_3 = {
        alpha_2: pycountry.countries.get(alpha_2=alpha_2)
        for alpha_2 in countries_alpha_2
    }
    not_found = [
        alpha_2 for alpha_2, cntr in map_alpha_2_to_alpha_3.items() if cntr is None
    ]
    print("Countries not found in pycountry are dropped:", not_found)
    map_alpha_2_to_alpha_3 = {
        alpha_2: cntr.alpha_3
        for alpha_2, cntr in map_alpha_2_to_alpha_3.items()
        if cntr is not None
    }
    return map_alpha_2_to_alpha_3


def clean_lines_or_links(lines_or_links):
    lines_or_links["bus0"] = lines_or_links["bus0"].apply(lambda x: x + "_land")
    lines_or_links["bus1"] = lines_or_links["bus1"].apply(lambda x: x + "_land")
    return lines_or_links

def clean_buses(buses):
    buses.index = buses.index.map(lambda bus: bus + "_land")
    return buses


def main(
    path_lines,
    path_links,
    path_buses,
    path_shapes_onshore,
    path_shapes_offshore,
    path_lines_clean,
    path_links_clean,
    path_buses_clean,
    path_shapes_clean,
    path_map_buses,
    path_map_countries
):
    # Load the data
    lines = gpd.read_parquet(path_lines)
    links = gpd.read_parquet(path_links)
    buses = gpd.read_parquet(path_buses)
    shapes_onshore = gpd.read_file(path_shapes_onshore)
    shapes_offshore = gpd.read_file(path_shapes_offshore)

    map_buses = {bus: map_to_iso_countries([bus[:2]])[bus[:2]] + bus[2:] for bus in buses.index}
    map_countries = map_to_iso_countries(buses["country"])
    map_buses["GBI"] = "GBI"  # Special case for London area
    map_countries["GBI"] = "GBI"  # Special case for London area

    # map buses and countries to alpha-3
    buses.index = buses.index.map(map_buses)
    buses["country"] = buses["country"].map(map_countries)
    buses.loc["GBI", "country"] = "GBI"

    # map lines bus0 and bus1 to alpha-3
    lines["bus0"] = lines["bus0"].map(map_buses)
    lines["bus1"] = lines["bus1"].map(map_buses)

    # map links bus0 and bus1 to alpha-3
    links["bus0"] = links["bus0"].map(map_buses)
    links["bus1"] = links["bus1"].map(map_buses)

    # map shapes to alpha-3
    def country_of_bus(bus):
        return buses.loc[bus, "country"] if bus in buses.index else None

    shapes_onshore["shape_class"] = "land"
    shapes_offshore["shape_class"] = "maritime"

    shapes = pd.concat([shapes_onshore, shapes_offshore], ignore_index=True)
    shapes = gpd.GeoDataFrame(shapes, geometry="geometry")

    shapes["name"] = shapes["name"].map(map_buses)
    shapes = shapes.rename(columns={"name": "shape_id"})
    shapes["country_id"] = shapes["shape_id"].map(country_of_bus)

    shapes.loc[shapes["shape_class"]=="land","shape_id"] += "_land"
    shapes.loc[shapes["shape_class"]=="maritime","shape_id"] += "_maritime"

    columns = ["shape_id", "country_id", "shape_class", "geometry"]
    shapes = shapes[columns]

    # add land to bus names
    lines = clean_lines_or_links(lines)
    links = clean_lines_or_links(links)
    buses = clean_buses(buses)

    # Save cleaned data
    lines.to_parquet(path_lines_clean)
    links.to_parquet(path_links_clean)
    buses.to_parquet(path_buses_clean)
    shapes.to_parquet(path_shapes_clean)
    save_yaml(map_buses, path_map_buses)
    save_yaml(map_countries, path_map_countries)

if __name__ == "__main__":
    main(
        snakemake.input.lines,
        snakemake.input.links,
        snakemake.input.buses,
        snakemake.input.shapes_onshore,
        snakemake.input.shapes_offshore,
        snakemake.output.lines,
        snakemake.output.links,
        snakemake.output.buses,
        snakemake.output.shapes,
        snakemake.output.buses_map,
        snakemake.output.country_map,
    )