import urllib.parse
import requests
from user_agents import parse

def build_upi_deeplink(payee_vpa, payee_name, amount, txn_id=None, note=None, currency='INR'):
    """
    Construct an UPI deeplink like:
    upi://pay?pa=merchant@upi&pn=MerchantName&am=10.00&cu=INR&tn=Order+123
    """
    params = {
        'pa': payee_vpa,
        'pn': payee_name,
        'am': f"{amount:.2f}",
        'cu': currency,
    }
    if txn_id:
        params['tr'] = str(txn_id)  # merchant transaction reference (optional)
    if note:
        params['tn'] = note

    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    return f"upi://pay?{query}"




def get_client_ip(request):
    """Extract IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_geo_info(ip):
    """Fetch location info from IP"""
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        data = response.json()
        return {
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country_name')
        }
    except:
        return {'city': None, 'region': None, 'country': None}

def get_device_info(request):
    """Extract browser, OS, and device type"""
    user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
    return {
        'browser': user_agent.browser.family,
        'os': user_agent.os.family,
        'device': user_agent.device.family
    }