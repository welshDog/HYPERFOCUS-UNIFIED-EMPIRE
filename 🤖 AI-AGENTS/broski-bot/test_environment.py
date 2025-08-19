"""
Quick test script to verify your BROski environment is working correctly
"""
import sys
import os

def test_imports():
    print("Testing required package imports...")
    
    packages = [
        "ccxt", "pandas", "numpy", "matplotlib", "colorama", "requests"
    ]
    
    all_passed = True
    for package in packages:
        try:
            module = __import__(package)
            version = getattr(module, "__version__", "unknown")
            print(f"✅ {package} (version {version}) - Successfully imported")
        except ImportError as e:
            print(f"❌ {package} - Import failed: {e}")
            all_passed = False
    
    return all_passed

def test_mexc():
    print("\nTesting MEXC API connection (public endpoints only)...")
    try:
        import ccxt
        mexc = ccxt.mexc()
        ticker = mexc.fetch_ticker('BTC/USDT')
        price = ticker['last']
        print(f"✅ MEXC API connection successful")
        print(f"   Current BTC price: ${price:.2f}")
        return True
    except Exception as e:
        print(f"❌ MEXC API connection failed: {e}")
        return False

def main():
    print(f"Python version: {sys.version}")
    print(f"Virtual environment: {sys.prefix}")
    print("-" * 50)
    
    imports_ok = test_imports()
    mexc_ok = test_mexc()
    
    print("\nTest Results:")
    print(f"Required packages: {'PASS ✅' if imports_ok else 'FAIL ❌'}")
    print(f"MEXC API access: {'PASS ✅' if mexc_ok else 'FAIL ❌'}")
    
    if imports_ok and mexc_ok:
        print("\n🎉 Your BROski environment is ready to go! 🎉")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
