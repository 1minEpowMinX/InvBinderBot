import ssl
from typing import Optional

import certifi


def create_ssl_context(
    cafile: Optional[str] = None, disable_strict_chain: bool = True
) -> ssl.SSLContext:
    """
    Create an SSL context for a client.

    Args:
        cafile (Optional[str]): Path to a file containing a set of concatenated
            "certification authority" certificates, which are used to verify the
            peer's identity. If not provided, the system's default certificate
            authority bundle will be used.
        disable_strict_chain (bool): If True, disable strict certificate chain
            verification. This can be useful for testing or development environments
            where the certificate chain may not be properly configured.

    Returns:
        ssl.SSLContext: An SSL context object that can be used to establish a secure
            connection to a server.
    """
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.check_hostname = True
    ctx.load_verify_locations(cafile or certifi.where())

    if disable_strict_chain:
        ctx.verify_flags &= ~(ssl.VERIFY_X509_PARTIAL_CHAIN | ssl.VERIFY_X509_STRICT)

    return ctx
