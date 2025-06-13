rule prepare_lines_and_links:
    message:
        "Get lines from PyPSA network."
    input:
        network="resources/user/network.nc",
        shapes="resources/user/shapes.geojson",
    output:
        lines_table="results/lines.csv",
        links_table="results/links.csv",
        lines_geo="results/lines.geojson",
        links_geo="results/links.geojson",
        lines_plot="results/lines_and_links.png"
    log:
        "logs/prepare_lines_and_links.log",
    conda:
        "../envs/pypsa.yaml"
    script:
        "../scripts/prepare_lines_and_links.py"
