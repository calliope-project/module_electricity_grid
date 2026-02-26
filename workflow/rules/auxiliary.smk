rule clean_outputs:
    input:
        lines="resources/automatic/lines.parquet",
        links="resources/automatic/links.parquet",
        buses="resources/automatic/buses.parquet",
        shapes_onshore="resources/user/shapes_onshore.geojson",
        shapes_offshore="resources/user/shapes_offshore.geojson",
    output:
        lines="results/lines_clean.parquet",
        links="results/links_clean.parquet",
        nodes="results/nodes_clean.parquet",
        shapes="results/shapes_clean.parquet",
        map_shapes_to_nodes="results/map_shapes_to_nodes.parquet",
        renamed_nodes="results/renamed_nodes.yaml",
        renamed_country="results/renamed_country.yaml",
    script:
        "../scripts/clean_outputs.py"