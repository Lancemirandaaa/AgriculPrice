import pandas as pd
import os

# File paths (must be in same folder)
PRICE_FILES = [
    "Fruit-Vegetables-Food-Prices.csv",
    "Condiments-Food-Prices.csv",
    "Rootcrops-Food-Prices.csv",
    "Fruits-Food-Prices.csv",
    "Leafy-Vegetables-Food-Prices.csv"
]
TYPHOON_FILE = "Typhoon_Dataset-Sheet8.csv"

# --- Load and combine all price files ---
all_prices_list = []
for file_name in PRICE_FILES:
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        all_prices_list.append(df)
        print(f"✅ Loaded: {file_name}")
    else:
        print(f"⚠️ Missing file: {file_name}")

if not all_prices_list:
    print("❌ No price files found. Exiting...")
    exit()

all_prices = pd.concat(all_prices_list, ignore_index=True)
print(f"\nCombined price data shape: {all_prices.shape}")

# --- Calculate Price Spikes ---
if 'Commodity_Name' in all_prices.columns and 'Retail_Price' in all_prices.columns:
    stats = all_prices.groupby('Commodity_Name')['Retail_Price'].agg(['mean', 'std']).reset_index()
    all_prices = all_prices.merge(stats, on='Commodity_Name', how='left')
    all_prices['Price_Spike'] = all_prices['Retail_Price'] > (all_prices['mean'] + 1.5 * all_prices['std'])
    print("📈 Added 'Price_Spike' column based on price anomalies.")
else:
    print("⚠️ Missing columns: Commodity_Name or Retail_Price")

# --- Save merged dataset ---
output_file = os.path.join(os.getcwd(), "merged_price_data.csv")
all_prices.to_csv(output_file, index=False)
print(f"\n💾 Saved merged dataset as: {output_file}")
