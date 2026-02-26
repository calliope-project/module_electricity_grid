rule prepare_lines_links_buses:
    message:
        "Get lines, links and buses from PyPSA network."
    input:
        network="resources/user/network.nc",
        shapes_onshore="resources/user/shapes_onshore.geojson",
        shapes_offshore="resources/user/shapes_offshore.geojson",
    output:
        lines="resources/automatic/lines.parquet",
        links="resources/automatic/links.parquet",
        buses="resources/automatic/buses.parquet",
        plot="resources/automatic/electricity_grid.png"
    log:
        "logs/prepare_lines_links_buses.log",
    conda:
        "../envs/pypsa.yaml"
    script:
        "../scripts/prepare_lines_links_buses.py"
