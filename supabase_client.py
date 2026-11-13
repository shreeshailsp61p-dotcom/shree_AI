
import os
import streamlit as st

from dotenv import load_dotenv
from supabase import create_client, Client


# Load environment variables from project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

load_dotenv(ENV_PATH)


# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PUBLISHABLE_KEY = os.getenv(
    "SUPABASE_PUBLISHABLE_KEY"
)


# Create Supabase connection
def get_supabase_client() -> Client:

    if not SUPABASE_URL or not SUPABASE_PUBLISHABLE_KEY:
        raise ValueError(
            "Supabase credentials are missing. "
            "Check your root .env file."
        )

    client = create_client(
        SUPABASE_URL,
        SUPABASE_PUBLISHABLE_KEY
    )

    return client


# Test Supabase connection
def test_supabase_connection():

    try:

        client = get_supabase_client()

        # A simple client initialization test.
        # No database tables or records are accessed.
        if client:
            return True, "Supabase client initialized successfully."

    except Exception as error:

        return False, str(error)

    return False, "Unable to initialize Supabase."
