import pypsa
import geopandas as gpd
from shapely import LineString, Point, wkt
import matplotlib.pyplot as plt


def get_bus_coords(bus, buses):
    return buses.loc[bus, "geometry"]


def get_line_from_points(point1, point2):
    return LineString([point1, point2])


def get_line_geometry(lines, buses):
    for id, data in lines.iterrows():
        bus0 = data["bus0"]
        bus1 = data["bus1"]
        coords0 = get_bus_coords(bus0, buses)
        coords1 = get_bus_coords(bus1, buses)
        line = get_line_from_points(coords0, coords1)
        lines.loc[id, "geometry"] = line

    return gpd.GeoDataFrame(lines, geometry="geometry", crs=buses.crs)


if __name__ == "__main__":
    # load network 
    n = pypsa.Network(snakemake.input.network)
    shapes = gpd.read_file(snakemake.input.shapes)
    
    # extract lines, links, and buses
    lines = n.lines
    links = n.links
    buses = n.buses

    # simplify bus names
    def simplify_bus_name(name):
        return name.replace("+", "_").replace("-", "_")
    buses.index = buses.index.map(simplify_bus_name)
    lines["bus0"] = lines["bus0"].map(simplify_bus_name)
    lines["bus1"] = lines["bus1"].map(simplify_bus_name)
    links["bus0"] = links["bus0"].map(simplify_bus_name)
    links["bus1"] = links["bus1"].map(simplify_bus_name)

    # prepare geometries
    gdf_links = links.copy()
    gdf_links["geometry"] = gdf_links["geometry"].apply(wkt.loads)
    gdf_links = gpd.GeoDataFrame(gdf_links, geometry="geometry", crs="EPSG:4326")

    buses["geometry"] = buses.apply(lambda x: Point(x["x"], x["y"]), 1)
    gdf_buses = gpd.GeoDataFrame(buses, geometry=buses["geometry"], crs=n.crs)

    gdf_lines = get_line_geometry(lines, gdf_buses)

    # save as csv and geojson
    gdf_lines.to_parquet(snakemake.output.lines)
    gdf_links.to_parquet(snakemake.output.links)
    gdf_buses.to_parquet(snakemake.output.buses)

    # save a plot
    CRS = "EPSG:3035"
    fig, ax = plt.subplots(figsize=(6, 6))
    shapes.to_crs(CRS).boundary.plot(ax=ax, color="black", linewidth=0.1, alpha=0.2)
    gdf_buses.to_crs(CRS).geometry.plot(ax=ax, markersize=5, color="#700202", label="Buses")
    gdf_lines.to_crs(CRS).geometry.plot(ax=ax, linewidth=gdf_lines["s_nom"]*2e-4, color="#700202")
    gdf_links.to_crs(CRS).geometry.plot(ax=ax, linewidth=gdf_links["p_nom"]*2e-4, color="#6184AC")

    ax.set_axis_off()
    ax.set_title("Lines, links and buses", fontsize=16)

    handles, labels = ax.get_legend_handles_labels()
    lines_legend = plt.Line2D([0], [0], color="#700202", lw=2, label="Lines")
    links_legend = plt.Line2D([0], [0], color="#6184AC", lw=2, label="Links")
    buses_legend = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#700202', markersize=5, label="Buses")
    ax.legend(handles=[lines_legend, links_legend, buses_legend], loc="upper right", fontsize=12)

    plt.savefig(snakemake.output.plot, dpi=300, bbox_inches="tight")
    plt.close()
