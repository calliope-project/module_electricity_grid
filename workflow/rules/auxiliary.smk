rule clean_outputs:
    input:
        lines="results/lines.parquet",
        links="results/links.parquet",
        buses="results/buses.parquet",
        shapes_onshore="resources/user/shapes_onshore.geojson",
        shapes_offshore="resources/user/shapes_offshore.geojson",
    output:
        lines="results/lines_clean.parquet",
        links="results/links_clean.parquet",
        buses="results/buses_clean.parquet",
        shapes="results/shapes_clean.parquet",
        buses_map="results/buses_map.yaml",
        country_map="results/country_map.yaml",
    script:
        "../scripts/clean_outputs.py"