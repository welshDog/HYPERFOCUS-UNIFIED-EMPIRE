# API Key Security Guide: IP Address Restrictions

## Why IP Linking Is Important

When creating API keys for MEXC, you'll see this option:
> **Link IP Address (optional)** - Keys that are not linked to an IP address are valid for 90 days only (not recommended)

### Understanding the Options:

1. **Keys WITH IP Restriction**: 
   - Higher security - Only allow access from specified IP addresses
   - No 90-day expiration - Keys remain valid until you revoke them
   - Recommended for production use

2. **Keys WITHOUT IP Restriction**:
   - Lower security - Can be used from any IP address
   - Automatically expire after 90 days
   - Require regular renewal
   - Not recommended for automated systems

## How to Link Your IP Address

### Step 1: Find Your IP Address
Before creating your API key, you need to know your public IP address.

- Visit [whatismyip.com](https://www.whatismyip.com/) or [ipify.org](https://api.ipify.org/)
- Note your public IPv4 address (looks like: 123.45.67.89)

### Step 2: During API Key Creation
1. In MEXC, go to "Account" → "API Management"
2. Click "Create API"
3. When you see the IP restriction option, select "Link IP address"
4. Enter your public IP address in the field provided
5. You can add multiple IP addresses separated by commas if needed

### Step 3: Verify Restrictions
After creating your key, check that it shows "IP restricted" status in your API key list.

## Special Scenarios

### When Using a Home Network
- Most home networks use dynamic IP addresses that change occasionally
- Options:
  1. Update your API key IP restrictions when your IP changes
  2. Contact your ISP about getting a static IP address
  3. Use a VPN service with a static IP option

### When Using a VPS (Virtual Private Server)
- Most VPS providers assign static IP addresses
- Add the VPS IP address to your API key restrictions
- For redundancy, you can add multiple VPS IPs if using multiple servers

### When Using Multiple Locations
If you need to access your API from different locations:
1. Create separate API keys for each location with appropriate IP restrictions
2. Limit the permissions of each key to only what's needed for that location

## Handling IP Address Changes

If your IP address changes and your bot stops working:

1. Log in to MEXC in your browser
2. Go to Account → API Management
3. Find your API key and click "Edit"
4. Update the IP restriction with your new IP address
5. Save changes

## Security Best Practices

Even with IP restrictions:
1. Set minimum necessary permissions (avoid withdrawal permission)
2. Monitor your account for any suspicious activity
3. Regenerate API keys periodically (every few months)
4. Never share your secret key with anyone
5. Never store API keys in public repositories

## Recommendations

- **For BROski Bot on Home Network**: 
  Enable IP restrictions, but be prepared to update them if your IP changes

- **For BROski Bot on VPS**:
  Always use IP restrictions with your VPS's static IP address

- **For Testing/Development**:
  You can temporarily use keys without IP restrictions, but switch to restricted keys for production use

Remember: The small inconvenience of managing IP restrictions is far outweighed by the security benefits they provide.
