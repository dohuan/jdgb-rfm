{{ config(
    materialized = 'incremental',
    unique_key = ['id_customer', 'meta_created_at'],
    partition_by={
      "field": "meta_created_at",
      "data_type": "date",
      "granularity": "month"
    }
) }}
with latest_order as (
    select
        id_customer,
        max(order_date) as latest_order_date
    from
        {{ source('BI_order_summary', 'order_summary') }}
    where
        order_date between date("{{ var("run_date") }}") - 720
        and date("{{ var("run_date") }}")
    group by
        id_customer
),
r as (
    select
        id_customer,
        date_diff(
            date("{{ var("run_date") }}"),
            lo.latest_order_date,
            day
        ) as recency
    from
        latest_order lo
),
fm as (
    select
        id_customer,
        count(*) as frequency,
        sum(sales_ar) as monetary
    from
        {{ source('BI_order_summary', 'order_summary') }}
    where
        order_date between date("{{ var("run_date") }}") - 720
        and date("{{ var("run_date") }}")
    group by
        id_customer
),
quantiles as (
    select
        r.id_customer,
        recency,
        frequency,
        monetary,
        r_perc.perc [offset(33)] as r33,
        r_perc.perc [offset(67)] as r67,
        m_perc.perc [offset(33)] as m33,
        m_perc.perc [offset(67)] as m67,
    from
        r
        left join fm on fm.id_customer = r.id_customer,
        (
            select
                approx_quantiles(recency, 100) as perc
            from
                r
        ) as r_perc,
        (
            select
                approx_quantiles(monetary, 100) as perc
            from
                fm
        ) as m_perc
),
rfm_score as (
    select
        quantiles.id_customer,
        quantiles.recency,
        quantiles.frequency,
        quantiles.monetary,
        case
            when recency >= r67 then 1
            when recency >= r33 then 2
            else 3
        end as r_score,
        case
            when frequency >= 5 then 3
            when frequency >= 2 then 2
            else 1
        end as f_score,
        case
            when monetary >= m67 then 3
            when monetary >= m33 then 2
            else 1
        end as m_score
    from
        quantiles
)
select
    *,
    date("{{ var("run_date") }}") as meta_created_at
from
    rfm_score