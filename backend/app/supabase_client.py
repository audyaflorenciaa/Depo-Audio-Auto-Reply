"""
DA AUTOLIGHT AI — Supabase Client Module

Initialises a Supabase client singleton using credentials from config.
All database operations go through this client.
"""

from supabase import create_client, Client

from app.config import settings

# ── Supabase client singleton ──────────────────────────────────
# Uses the SERVICE_ROLE key for full backend access (bypasses RLS).
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY,
)
