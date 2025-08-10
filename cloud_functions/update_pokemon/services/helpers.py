import re
import urllib.parse

def extract_product_id(url):
    """
    Extract the product ID from a TCG Player URL.
    
    Args:
        url (str): The TCG Player URL containing a product ID
        
    Returns:
        str or None: The extracted product ID if found, None otherwise
    """
    # First try the original pattern
    pattern = r'/product/(\d+)(?:/|$)'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    
    # If not found, try to decode the URL and search again
    try:
        # Extract the encoded URL from after the '?u=' parameter
        if '?u=' in url:
            encoded_url = url.split('?u=', 1)[1]
            decoded_url = urllib.parse.unquote(encoded_url)
            
            # Search for the product ID in the decoded URL
            match = re.search(pattern, decoded_url)
            if match:
                return match.group(1)
    except Exception:
        pass
        
    return None
