import streamlit as st
import psycopg2 as psql
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_lottie import st_lottie
import requests

# Function to fetch data from database
def fetch_data_from_db(limit=100):
    database_name=st.secrets["database"]
    user=st.secrets["user"]
    host=st.secrets["host"]
    password=st.secrets["password"]

    conn = psql.connect(
        database=database_name,
        user=user,
        host=host,
        password=password,
        port=5432
    )
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM student.de10_arba_test ORDER BY cmc_rank LIMIT {limit};")
    columns = [desc[0] for desc in cur.description]
    data = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in data]

# Streamlit UI
st.title('Welcome to Crypto Universe')
# Image at top
cover_url = "https://media.licdn.com/dms/image/C5612AQG01A_COK31ag/article-cover_image-shrink_600_2000/0/1570561273470?e=2147483647&v=beta&t=vvf-7TOub-T9WlsRIQtL-50bpDeYVWErIkNhE4CX7T8"
st.image(cover_url, width=750)

col1, col2= st.columns(2)
with col1:
    st.text("""
            Cryptocurrency is digital money that uses
        blockchain technology for secure
        transactions without intermediaries like
        banks. Bitcoin, the first cryptocurrency,
        launched in 2009, paved the way for
        others like Ethereum and Ripple. It
        promises fast, transparent transactions
        but faces challenges like regulatory
        uncertainty and price volatility.""")
with col2:
    st_lottie("https://lottie.host/7ca6f0d6-82ee-4069-a688-b16aea8161c4/QvmlP4Bp0C.json", height=200, width=400)

# Fetch data from the database
crypto_data = fetch_data_from_db(100)

# Ensure there is enough data to display
if len(crypto_data) > 0:
    # Display the first 10 cryptocurrencies in a table
    st.header("Here are the world's most loved coins ... ")
    top_10_df = pd.DataFrame(crypto_data[:10])
    top_10_df['logo'] = top_10_df['logo_url'].apply(lambda url: f"![logo]({url})")

    top_10_table = top_10_df[["name", "logo", "cmc_rank", "circulating_supply", "price_usd", "volume_24h_usd", "market_cap_usd"]]
    st.markdown(top_10_table.to_markdown(index=False), unsafe_allow_html=True)

    st.header("Market Cap Dominance $")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_10_df["name"], top_10_df["market_cap_dominance_usd"], color='navy')
    ax.set_xlabel('Cryptocurrencies')
    ax.set_ylabel('Market Cap Dominance (USD)')
    ax.set_title('Market Cap Dominance')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Prepare data for coin selection
    crypto_names = [crypto['name'] for crypto in crypto_data]

    # Input to select first and second coin by name
    first_coin_name = st.selectbox('Select first coin', crypto_names, key='coin1')
    second_coin_name = st.selectbox('Select second coin', crypto_names, key='coin2')

    # Find the selected cryptocurrencies based on the names
    coin1 = next(crypto for crypto in crypto_data if crypto['name'] == first_coin_name)
    coin2 = next(crypto for crypto in crypto_data if crypto['name'] == second_coin_name)

    # Display logos and descriptions
    col1, col2= st.columns(2)
    with col1:
        st.header("Crypto Descriptions")
    with col2:
       st_lottie("https://lottie.host/15b6cbe7-13f2-47e0-b1ed-b9441962ff23/B17ZRZSoHi.json", height=70, width=70)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(coin1["logo_url"], width=64)
        st.subheader(coin1["name"])
        st.write(coin1["description"])

    with col2:
        st.image(coin2["logo_url"], width=64)
        st.subheader(coin2["name"])
        st.write(coin2["description"])

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.header(f"{coin1['name']} VS {coin2['name']}")
    with col2:
        st_lottie("https://lottie.host/d88f1af2-b8b8-42d0-bf47-0dd635993547/pNr2iqp658.json", height=70, width=70)

    # Combine the data into a single DataFrame
    combined_data = {
        'Metric': [
            'Name', 'Symbol', 'CMC Rank', 'Circulating Supply', 'Date Added',
            'Price (USD)', 'Volume (24h USD)', 'Percent Change (1h USD)',
            'Percent Change (24h USD)', 'Percent Change (7d USD)',
            'Market Cap (USD)', 'Market Cap Dominance (USD)'
        ],
        'Coin 1': [
            coin1["name"], coin1["symbol"], coin1["cmc_rank"],
            coin1["circulating_supply"], coin1["date_added"], coin1["price_usd"],
            coin1["volume_24h_usd"], coin1["percent_change_1h_usd"],
            coin1["percent_change_24h_usd"], coin1["percent_change_7d_usd"],
            coin1["market_cap_usd"], coin1["market_cap_dominance_usd"]
        ],
        'Coin 2': [
            coin2["name"], coin2["symbol"], coin2["cmc_rank"],
            coin2["circulating_supply"], coin2["date_added"], coin2["price_usd"],
            coin2["volume_24h_usd"], coin2["percent_change_1h_usd"],
            coin2["percent_change_24h_usd"], coin2["percent_change_7d_usd"],
            coin2["market_cap_usd"], coin2["market_cap_dominance_usd"]
        ]
    }
    combined_df = pd.DataFrame(combined_data)

    # Display the combined DataFrame
    st.table(combined_df)

    # Plotting Percentage Change (1h USD)
    col1, col2 = st.columns(2)
with col1:
    st_lottie("https://lottie.host/9009de95-2ef6-4944-8186-1467da8a4393/b0Ne3OYuMy.json", height=270, width=300)
with col2:
    fig, ax = plt.subplots(figsize=(4, 4))
    coins = [coin1["name"], coin2["name"]]
    percent_change_1h = [coin1["percent_change_1h_usd"], coin2["percent_change_1h_usd"]]

    ax.bar(coins, percent_change_1h, color=['lightblue', 'navy'])
    ax.set_xlabel('Coins')
    ax.set_ylabel('Percent Change (1h USD)')
    ax.set_title('Comparison of Percentage Change (1h USD)')
    st.pyplot(fig)

col1, col2 = st.columns(2)
with col1:
    st.metric(
        label=f"Price and % Change of {coin1['name']}",
        value=f"{round(coin1['price_usd'], 2)} $",
        delta=f"(1h): {round(coin1['percent_change_1h_usd'], 2)}%, (24h): {round(coin1['percent_change_24h_usd'], 2)}%, (7 days): {round(coin1['percent_change_7d_usd'], 2)}%",
        delta_color="normal"
    )
with col2:
    st.metric(
        label=f"Price and % Change of {coin2['name']}",
        value=f"{round(coin2['price_usd'], 2)} $",
        delta=f"(1h): {round(coin2['percent_change_1h_usd'], 2)}%, (24h): {round(coin2['percent_change_24h_usd'], 2)}%, (7 days): {round(coin2['percent_change_7d_usd'], 2)}%",
        delta_color="normal"
    )    
st.header(" The world Currency")
st.text("""Fast currency exchange is crucial in today's global economy. It enables businesses
and individuals to swiftly and efficiently transfer funds across borders, supporting
international trade and investment. Quick exchange services reduce the risk
associated with currency fluctuations and ensure timely transactions, which is
essential for maintaining cash flow and meeting financial obligations. Furthermore,
rapid currency exchange enhances financial inclusivity, allowing people in different
regions to access and utilize global financial markets seamlessly. This speed and
efficiency ultimately contribute to economic growth.""")
# Currency conversion rates and countries information
usd_to_gbp_rate = 0.787235
usd_to_rus_rate = 87.080894
usd_to_inr_rate = 83.513928
usd_to_brl_rate = 5.676676
usd_to_thb_rate = 36.756722
usd_to_omr_rate = 0.384707
usd_to_arg_rate = 913.702272
usd_to_mxn_rate = 18.078256
usd_to_kwd_rate = 0.306260
usd_to_cop_rate = 4092.376234

countries = {
    "GBP": {"name": "United Kingdom", "flag_url": "https://flagsapi.com/GB/flat/32.png"},
    "RUS": {"name": "Russia", "flag_url": "https://flagsapi.com/RU/flat/32.png"},
    "INR": {"name": "India", "flag_url": "https://flagsapi.com/IN/flat/32.png"},
    "BRL": {"name": "Brazil", "flag_url": "https://flagsapi.com/BR/flat/32.png"},
    "THB": {"name": "Thailand", "flag_url": "https://flagsapi.com/TH/flat/32.png"},
    "OMR": {"name": "Oman", "flag_url": "https://flagsapi.com/OM/flat/32.png"},
    "ARG": {"name": "Argentina", "flag_url": "https://flagsapi.com/AR/flat/32.png"},
    "MXN": {"name": "Mexico", "flag_url": "https://flagsapi.com/MX/flat/32.png"},
    "KWD": {"name": "Kuwait", "flag_url": "https://flagsapi.com/KW/flat/32.png"},
    "COP": {"name": "Colombia", "flag_url": "https://flagsapi.com/CO/flat/32.png"}
}

# Prepare data for the table
table_data = []
for currency, country_info in countries.items():
    table_data.append({
        "Country": country_info["name"],
        "Flag": f'![Flag]({country_info["flag_url"]})',
        f"{coin1['name']}": f"{coin1['price_usd'] if currency == 'USD' else coin1['price_usd'] * locals()[f'usd_to_{currency.lower()}_rate']:.2f}",
        f"{coin2['name']}": f"{coin2['price_usd'] if currency == 'USD' else coin2['price_usd'] * locals()[f'usd_to_{currency.lower()}_rate']:.2f}"
    })

    # Display the table using Markdown for images
st.markdown("### Prices in Different Currencies")
st.markdown(pd.DataFrame(table_data).to_markdown(), unsafe_allow_html=True)

st_lottie("https://lottie.host/556bc5b3-b590-4d1e-993e-ce3ee3bbce02/DIfPjYxhgm.json")
