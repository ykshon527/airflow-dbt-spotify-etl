{{config(
    materialized = 'table',
    unique_key = 'id'
)}}

with source as (
    select *
    from {{source('raw', 'my_played_tracks')}}
),

de_dup as (
    select *,
    row_number() over (partition by played_at order by inserted_at) as rn 
    from source
)

select 
    id,
    song_name,
    artist_name,
    (played_at::timestamp AT TIME ZONE 'UTC' AT TIME ZONE 'America/Los_Angeles') AS played_at_pst,
    timestamp as played_date,
    inserted_at
from de_dup
where rn = 1