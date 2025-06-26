rule prepare_lines_links_buses:
    message:
        "Get lines, links and buses from PyPSA network."
    input:
        network="resources/user/network.nc",
        shapes_onshore="resources/user/shapes_onshore.geojson",
        shapes_offshore="resources/user/shapes_offshore.geojson",
    output:
        lines="results/lines.parquet",
        links="results/links.parquet",
        buses="results/buses.parquet",
        plot="results/electricity_grid.png"
    log:
        "logs/prepare_lines_links_buses.log",
    conda:
        "../envs/pypsa.yaml"
    script:
        "../scripts/prepare_lines_links_buses.py"
