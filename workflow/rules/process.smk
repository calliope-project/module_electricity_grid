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
        lines_plot="results/lines.png"
    log:
        "logs/prepare_lines_and_links.log",
    conda:
        "../envs/pypsa.yaml"
    script:
        "../scripts/prepare_lines_and_links.py"


rule prepare_ntc:
    message:
        "Prepare NTC from electrical properties of lines."
    input:
        lines="results/lines.csv",
    output:
        lines_ntc="results/lines_ntc.csv",
    log:
        "logs/prepare_ntc.log",
    conda:
        "../envs/pypsa.yaml"
    script:
        "../scripts/prepare_ntc.py"
