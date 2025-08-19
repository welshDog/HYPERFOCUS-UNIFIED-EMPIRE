# Understanding the "Notes" Field in MEXC API Key Creation

When creating API keys for your BROski Crypto Bot on MEXC Exchange, you'll notice a field labeled **"Notes (Required)"**. This guide explains what it is and how to use it properly.

## What Is the Notes Field?

The Notes field is a required description field that:
- Helps you identify what each API key is used for
- Serves as a reminder of the key's purpose
- Is visible in your API Management dashboard
- Cannot be left blank during key creation

## How to Fill Out the Notes Field

When creating your API key for BROski Bot, enter a clear, descriptive note:

### Good Examples:
- "BROski Trading Bot"
- "BROski Bot - PI/USDT Trading"
- "Automated Trading - BROski"
- "Trading Bot (Read + Trade permissions)"

### Poor Examples:
- "Test"
- "Key"
- "123"
- "My key"

## Best Practices for API Notes

1. **Be specific but concise** - Make notes that clearly identify the key's purpose
2. **Include the application name** - Mention "BROski" to identify which app uses this key
3. **Note the trading pairs** - If you're using specific trading pairs, include them
4. **Include permission scope** - Note whether the key has read, trade, or other permissions
5. **Don't include sensitive information** - Never put passwords or secrets in the notes field

## Managing Multiple API Keys

If you create multiple API keys for different purposes:

1. **Use distinct descriptions** - Make each key's purpose clear from its note
2. **Include date information** - Consider adding creation dates if you rotate keys regularly
3. **Note environment** - If you have separate keys for testing and production, label them

## Example Setup for BROski Bot

When creating your MEXC API key for BROski Bot:

1. Go to MEXC API Management
2. Click "Create API"
3. In the "Notes" field, enter: "BROski Trading Bot - Auto Trading"
4. Select appropriate permissions (Read + Trade, no withdrawals)
5. Set IP restrictions if using from a fixed location
6. Complete verification
7. Save your API key and secret key securely

Remember: The notes field is visible in your API Management dashboard and helps you identify which application or purpose each key serves, making it easier to manage multiple API keys.
