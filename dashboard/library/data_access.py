import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def get_engine():
    return create_engine(
        os.environ["DATABASE_URL"]
    )


@st.cache_data(ttl=1800)
def get_latest_national_reading():

    engine = get_engine()

    query = """
    SELECT
        p.period_from,
        p.period_to,
        nr.forecast_intensity,
        nr.actual_intensity,
        nr.intensity_index
    FROM national_readings nr
    JOIN period_id p
        ON nr.reading_id = p.id
    ORDER BY p.period_from DESC
    LIMIT 1;
    """

    return pd.read_sql(query, engine)

@st.cache_data(ttl=1800)
def get_latest_regional_readings():

    engine = get_engine()

    query = """
    SELECT
        p.period_from,
        p.period_to,
        r.region_name,
        rr.region_id,
        rr.forecast_intensity,
        rr.actual_intensity,
        rr.intensity_index
    FROM regional_readings rr

    JOIN period_id p
        ON rr.reading_id = p.id

    JOIN regions r
        ON rr.region_id = r.region_id

    WHERE p.period_from = (
        SELECT MAX(period_from)
        FROM period_id
    )

    ORDER BY rr.region_id;
    """

    return pd.read_sql(query, engine)

def get_national_generation():
    engine = get_engine()
    query = """
    SELECT
    p.period_from,
    p.period_to,
    ngm.fuel_type,
    ngm.percentage
    FROM national_generation_mix ngm
    
    JOIN period_id p
        ON ngm.reading_id = p.id
    ORDER BY p.period_from DESC;
    """
    return pd.read_sql(query, engine)