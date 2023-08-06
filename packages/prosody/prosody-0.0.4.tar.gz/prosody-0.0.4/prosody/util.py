"""Utility functions for prosody_api"""
import requests


def server_required(func):
    """Decorates function that needs to be connected to the API server."""
    def exception_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError:
            error_message = 'Connection not established, The server may be down for maintenance'
            raise ConnectionError(error_message)
    return exception_handler
