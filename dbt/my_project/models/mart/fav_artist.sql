{{config(
    materialized = 'table'
)}}

select played_date,
    artist_name,
    count(*) as played_cnt
from {{ref('spotify_report')}}
group by 
    played_date, 
    artist_name
order by 
    played_cnt desc