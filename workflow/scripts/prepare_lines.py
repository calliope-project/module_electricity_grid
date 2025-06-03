import pypsa
import geopandas as gpd
from shapely import LineString
from pathlib import Path


def get_bus_coords(bus, shapes):
    shape = shapes[shapes["admin"] == bus]
    if len(shape) == 0:
        raise ValueError(f"Region for bus {bus} not found")
    if len(shape) > 1:
        raise ValueError(f"More than one region for bus {bus} found")
    
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

    gdf_lines = get_line_geometry(lines, shapes)

    # save as csv and geojson
    lines.to_csv(snakemake.output.lines_table)  # here / "data" / "lines.csv")

    gdf_lines.to_file(snakemake.output.lines_geo)  # here / "data" / "lines.geojson", driver="GeoJSON")
