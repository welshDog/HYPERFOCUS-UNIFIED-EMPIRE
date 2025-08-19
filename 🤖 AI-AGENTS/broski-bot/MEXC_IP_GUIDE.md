# Fixing MEXC API IP Whitelist Error

## The Error Explained

When you see this error:
```
IP [151.224.117.246] not in the ip white list
```

This means your API key is restricted to specific IP addresses, and your current IP address is not on the allowed list.

## Your Current IP

Your current public IP address is: **151.224.117.246**

## How to Update Your IP Whitelist

1. **Log in to MEXC**:
   - Go to [MEXC Exchange](https://www.mexc.com)
   - Sign in with your account

2. **Go to API Management**:
   - Click on your profile icon
   - Select "API Management"

3. **Edit Your API Key**:
   - Find the API key you're using with BROski
   - Click the "Edit" button

4. **Update IP Restrictions**:
   - In the "IP Restriction" section, you'll see a field with allowed IPs
   - Add your current IP: **151.224.117.246**
   - If there are already IPs listed, add yours with a comma (e.g., "123.45.67.89,151.224.117.246")
   - Save your changes

5. **Restart the Bot**:
   - After updating the whitelist, return to BROski and try again

## Common IP Whitelist Scenarios

### Multiple IP Addresses

If you use the bot from different locations, you can add multiple IP addresses separated by commas:
```
151.224.117.246,192.168.1.1,10.0.0.1
```

### Dynamic IP Address

If your home internet uses dynamic IP (changes periodically):

1. **Option 1**: Update your whitelist whenever your IP changes
2. **Option 2**: Contact your ISP to get a static IP
3. **Option 3**: Consider running the bot on a cloud server with static IP
4. **Option 4**: Some routers allow setting up dynamic DNS services

### Alternative: Disable IP Restrictions

If you prefer not to deal with IP restrictions:

1. Create a new API key without IP restrictions
2. Note that non-IP-restricted keys expire after 90 days
3. Update your BROski configuration with the new key

## Helper Tool

We've included an IP helper tool that detects your current IP and guides you through the update process:

```bash
python ip_whitelist_helper.py
```

This tool will:
- Show your current public IP address
- Provide step-by-step instructions
- Offer to open the MEXC API management page in your browser
