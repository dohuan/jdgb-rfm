-- overwrite the default schema generation: (https://docs.getdbt.com/docs/building-a-dbt-project/building-models/using-custom-schemas/)
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set branch_name = var('branch_name', '') -%}
    {%- if target.dataset == 'main' -%}
        {{ custom_schema_name | trim }}
    {%- else -%}
        {{ custom_schema_name | trim }}__{{ target.dataset }}
    {%- endif -%}
{%- endmacro %}

