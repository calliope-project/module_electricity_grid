rule clean_outputs:
    input:
        lines="results/lines.parquet",
        links="results/links.parquet",
        buses="results/buses.parquet",
        shapes_onshore="resources/user/regions_onshore.geojson",
        shapes_offshore="resources/user/regions_offshore.geojson",
    output:
        lines="results/lines_clean.parquet",
        links="results/links_clean.parquet",
        buses="results/buses_clean.parquet",
        shapes_onshore="results/regions_onshore_clean.parquet",
        shapes_offshore="results/regions_offshore_clean.parquet",
        buses_map="results/buses_map.yaml",
        country_map="results/country_map.yaml",
    script:
        "../scripts/clean_outputs.py"