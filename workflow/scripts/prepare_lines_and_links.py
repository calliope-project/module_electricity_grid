import pypsa
import geopandas as gpd
from shapely import LineString
from pathlib import Path
import matplotlib.pyplot as plt


def get_bus_coords(bus, shapes):
    shape = shapes[shapes["admin"] == bus]
    if len(shape) == 0:
        raise ValueError(f"Region for bus {bus} not found")
    if len(shape) > 1:
        raise ValueError(f"More than one region for bus {bus} found")
    
    # TODO: Project to appropriate CRS before computing centroid
    coords = shape.geometry.centroid.iloc[0]
    return coords


def get_line_from_points(point1, point2):
    return LineString([point1, point2])


def get_line_geometry(lines, shapes):
    for id, data in lines.iterrows():
        bus0 = data["bus0"]
        bus1 = data["bus1"]
        coords0 = get_bus_coords(bus0, shapes)
        coords1 = get_bus_coords(bus1, shapes)
        line = get_line_from_points(coords0, coords1)
        lines.loc[id, "geometry"] = line

    return gpd.GeoDataFrame(lines, geometry="geometry", crs=shapes.crs)

if __name__ == "__main__":
    # load network 
    n = pypsa.Network(snakemake.input.network)  # here / ".." / "resources/networks/base_s_adm.nc")
    shapes = gpd.read_file(snakemake.input.shapes)  # here / ".." / "resources/admin_shapes.geojson")
    
    # prepare lines and line geometries
    lines = n.lines
    links = n.links

    gdf_lines = get_line_geometry(lines, shapes)
    # TODO: use links geometry, which is type str currently.

    # save as csv and geojson
    lines.to_csv(snakemake.output.lines_table)
    links.to_csv(snakemake.output.links_table)

    gdf_lines.to_file(snakemake.output.lines_geo)

    # save as plot
    fig, ax = plt.subplots()
    shapes.to_crs("EPSG:3035").boundary.plot(ax=ax, color="black", linewidth=0.1, alpha=0.2)
    gdf_lines.to_crs("EPSG:3035").geometry.plot(ax=ax, linewidth=gdf_lines["s_nom"]*2e-4, color="red", alpha=0.5)
    plt.savefig(snakemake.output.lines_plot, dpi=300)
    plt.close()
