{{config(
    materialized = 'table',
    unique_key = 'id'
)}}

select 
    song_name,
    artist_name,
    played_at_pst,
    played_date
from {{ref('stg_spotify_data')}}