import pandas as pd

df8  = pd.read_csv('data/sales2019_8.csv')
df12 = pd.read_csv('data/sales2019_12.csv')


def deep_clean_sales_data(df, month_label):
    print(f"\ncleaning data {month_label}...")
    
    df = df.dropna(how='all')
    df = df.drop_duplicates()

    df = df[df['Order ID'] != 'Order ID']


    df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'], errors='coerce')
    df['Price Each'] = pd.to_numeric(df['Price Each'], errors='coerce')
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

    df = df.dropna()
    return df
 
df8_clean = deep_clean_sales_data(df8, "8/2019")
df12_clean = deep_clean_sales_data(df12, "12/2019")


def analyze_revenue_drivers(df_old, name_old, df_new, name_new):
    print(f"\n{'='*50}")
    print(f"REVENUE REPORT: {name_old} VS {name_new}")

#create new colomn call sale = quantity * price 
    df_old = df_old.copy()
    df_new = df_new.copy()
    df_old['Sales'] = df_old['Quantity Ordered'] * df_old['Price Each']
    df_new['Sales'] = df_new['Quantity Ordered'] * df_new['Price Each']

    # old month 
    rev_old = df_old['Sales'].sum() # total revenue 
    orders_old = df_old['Order ID'].nunique() # count unque values
    aov_old = rev_old / orders_old if orders_old > 0 else 0

    # new mouth 
    rev_new = df_new['Sales'].sum()   # total revenue 
    orders_new = df_new['Order ID'].nunique() # count unque values
    aov_new = rev_new / orders_new if orders_new > 0 else 0 # count unque values



#calculate percentage revenue 

    pct_rev = ((rev_new - rev_old) / rev_old) * 100
    pct_orders = ((orders_new - orders_old) / orders_old) * 100
    pct_aov = ((aov_new - aov_old) / aov_old) * 100

    print(f"[1] total revenue :  ${rev_old:,.2f} -> ${rev_new:,.2f} ({pct_rev:+.2f}%)")
    print(f"[2] total orders:     {orders_old:,} order -> {orders_new:,} orders({pct_orders:+.2f}%)")
    print(f"[3] revenue/orders (AOV): ${aov_old:,.2f} -> ${aov_new:,.2f} ({pct_aov:+.2f}%)\n")
    
    # report
    if rev_new > rev_old:
        print(f" {name_new} has highter revene than {name_old}.")

        if pct_orders > pct_aov:
            print("Because cumtomers purchased more products")
        else:
            print("Because cumtomers purchased higher - priced products")

    elif rev_new < rev_old:
        print(f"{name_new} has lower revene than {name_old}.")

        if pct_orders < pct_aov:
            print("Because cumtomers purchased fewer products")
        else:
            print("Because cumtomers purchased lower - priced products")
        
    else:
        print(" revenue in the two months is the same ")

    
    # ===== TOP & BOTTOM PRODUCTS BY REVENUE =====
    print(f"\n{'='*50}")
    print("PRODUCT ANALYSIS (BY REVENUE)")

    product_old = df_old.groupby('Product')['Sales'].sum()
    product_new = df_new.groupby('Product')['Sales'].sum()

    # best seller
    best_old = product_old.idxmax()
    best_new = product_new.idxmax()

    # poor seller
    worst_old = product_old.idxmin()
    worst_new = product_new.idxmin()

    print(f"\n[4] Best-selling product (by revenue):")
    print(f"    {name_old}: {best_old} (${product_old[best_old]:,.2f})")
    print(f"    {name_new}: {best_new} (${product_new[best_new]:,.2f})")

    print(f"\n[5] Worst-selling product (by revenue):")
    print(f"    {name_old}: {worst_old} (${product_old[worst_old]:,.2f})")
    print(f"    {name_new}: {worst_new} (${product_new[worst_new]:,.2f})")

    # ===== TOP 2 CITIES BY REVENUE =====
    print(f"\n{'='*50}")
    print("TOP 2 CITIES BY REVENUE")

    df_old['City'] = df_old['Purchase Address'].apply(lambda x: x.split(',')[1].strip())# Create a new column "City" by extracting the city name from the "Purchase Address" column
    df_new['City'] = df_new['Purchase Address'].apply(lambda x: x.split(',')[1].strip())   # Split the address by comma and take the second part, then remove extra spaces

    city_old = df_old.groupby('City')['Sales'].sum().nlargest(2)# Group data by City and calculate total Sales then get 2 cities highest revenue
    city_new = df_new.groupby('City')['Sales'].sum().nlargest(2)

    print(f"\n[6] {name_old}:")
    for rank, (city, revenue) in enumerate(city_old.items(), 1):
        print(f"    #{rank} {city}: ${revenue:,.2f}")

    print(f"\n    {name_new}:")
    for rank, (city, revenue) in enumerate(city_new.items(), 1):
        print(f"    #{rank} {city}: ${revenue:,.2f}")


analyze_revenue_drivers(df8_clean, "august", df12_clean, "december")


def analyze_bundled_products(df, name, top_n=5):
    print(f"\n{'='*50}")
    print(f"PRODUCTS FREQUENTLY BOUGHT TOGETHER — {name.upper()}")

    order_products = df.groupby('Order ID')['Product'].apply(list) # Group data by Order ID and collect all products in each order into a list

    order_products = order_products[order_products.apply(lambda x: len(x) > 1)] # only take orders with 2 or more items
    from itertools import combinations # create unique pairs
    from collections import Counter # coun
    pair_counter = Counter() # count how many time
    for products in order_products:
        # 
        pairs = combinations(sorted(set(products)), 2)
        pair_counter.update(pairs)

    # take the most common
    top_pairs = pair_counter.most_common(top_n)

    if not top_pairs:
        print("No products pairs found.")
        return

    for rank, ((product_a, product_b), count) in enumerate(top_pairs, 1):
        print(f"  #{rank} '{product_a}' + '{product_b}' — {count:,} time")



analyze_bundled_products(df8_clean,  "august")
analyze_bundled_products(df12_clean, "december")



