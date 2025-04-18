"""
Debugging utilities for Taco Quest.
This module provides functions for testing and troubleshooting.
"""
import logging
import json
import os
import sys
from typing import Dict, Any, Optional, List

from app.config.settings import (
    SUPABASE_URL, SUPABASE_KEY, SUPABASE_PUBLIC_KEY,
    SUPABASE_DB_HOST, SUPABASE_DB_PORT, SUPABASE_DB_NAME,
    SUPABASE_DB_USER, DATABASE_URL, USE_SUPABASE
)
from app.database.supabase import test_supabase_connection

logger = logging.getLogger(__name__)

def debug_environment():
    """Log information about the environment and configuration."""
    logger.info("Environment and Configuration Debug Information:")
    
    # Python version
    logger.info(f"Python Version: {sys.version}")
    
    # Current working directory
    logger.info(f"Current Working Directory: {os.getcwd()}")
    
    # Database settings (masked for security)
    logger.info(f"Using Supabase: {USE_SUPABASE}")
    
    if SUPABASE_URL:
        masked_url = SUPABASE_URL.replace(
            SUPABASE_URL.split("//")[1].split(".")[0], 
            "****"
        )
        logger.info(f"Supabase URL: {masked_url}")
    else:
        logger.info("Supabase URL: Not set")
    
    if SUPABASE_KEY:
        logger.info(f"Supabase Key: {'*' * 8}{SUPABASE_KEY[-4:]}")
    else:
        logger.info("Supabase Key: Not set")
    
    if SUPABASE_PUBLIC_KEY:
        logger.info(f"Supabase Public Key: {'*' * 8}{SUPABASE_PUBLIC_KEY[-4:]}")
    else:
        logger.info("Supabase Public Key: Not set")
    
    if SUPABASE_DB_HOST:
        masked_host = SUPABASE_DB_HOST.replace(
            SUPABASE_DB_HOST.split(".")[0], 
            "****"
        )
        logger.info(f"Supabase DB Host: {masked_host}")
    else:
        logger.info("Supabase DB Host: Not set")
    
    logger.info(f"Database URL Type: {DATABASE_URL.split(':')[0]}")

def test_supabase():
    """Test only the Supabase connection and report results."""
    logger.info("Testing Supabase Connection...")
    
    # Check if Supabase credentials are set
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Supabase credentials are not set in environment variables")
        return False
    
    # Test connection
    connection_ok = test_supabase_connection()
    
    if connection_ok:
        logger.info("Supabase connection successful!")
        return True
    else:
        logger.error("Supabase connection failed!")
        return False
