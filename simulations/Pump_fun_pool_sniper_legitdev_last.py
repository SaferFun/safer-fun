#!/usr/bin/env python
# coding: utf-8

# In[3]:


import random
import matplotlib.pyplot as plt
import numpy as np

class PumpFunClass:
    def __init__(self, initial_sol_in_pool, total_tokens_in_pool):
        self.sol_pool = initial_sol_in_pool
        self.total_coin_supply = total_tokens_in_pool  # Set the total supply of tokens
        self.remaining_tokens_in_pool = total_tokens_in_pool  # Initially, all tokens are in the pool

    def get_token_price(self):
        # Token price = SOL in pool / tokens in pool (DEX-like pricing)
        return self.sol_pool / self.remaining_tokens_in_pool

    def get_mcap_statistics(self):
        # Market capitalization = Total supply * current token price
        return self.total_coin_supply * self.get_token_price() * 150  # Assuming 1 SOL = 150 USD for Mcap calculation

    def get_remaining_token_supply(self):
        # Return the remaining tokens available in the pool
        return self.remaining_tokens_in_pool

    def update_pool_with_buy(self, sol_amount):
        # Update the SOL pool when tokens are bought
        self.sol_pool += sol_amount
        tokens_bought = sol_amount / self.get_token_price()  # How many tokens can be bought at the current price
        self.remaining_tokens_in_pool -= tokens_bought  # Reduce the available token supply in the pool
        return tokens_bought

    def update_pool_with_sell(self, tokens_sold):
        # Update pool when tokens are sold
        self.remaining_tokens_in_pool += tokens_sold  # Return the tokens to the pool
        sol_to_receive = tokens_sold * self.get_token_price()  # Get SOL based on current price
        self.sol_pool -= sol_to_receive  # Deduct SOL from the pool
        return sol_to_receive

# Simulation Parameters
num_simulations = 1000  # Number of Monte Carlo simulations
sol_price = 150  # USD value of SOL
total_token_supply = 1_000_000_000  # 1 billion tokens total
interaction_duration_seconds = 300  # 5 minutes in seconds
interaction_interval_seconds = 10  # Buyers interact with the pool every 10 seconds

# Lists to store all results across simulations
all_token_prices_over_time = []
all_mcap_over_time = []
all_sniper_profits = []

# Monte Carlo Simulation Loop
for sim in range(num_simulations):
    # Initialize the pool with 10 SOL and 1 billion tokens
    initial_sol_in_pool = 10
    pump_fun = PumpFunClass(initial_sol_in_pool=initial_sol_in_pool, total_tokens_in_pool=total_token_supply)

    # Developer buys tokens (between 3 and 4 SOL)
    dev_buy_amount = random.uniform(3, 4)
    dev_tokens_bought = pump_fun.update_pool_with_buy(dev_buy_amount)

    # Sniper enters the pool
    sniper_buy_amount = random.uniform(0.5, 0.7)
    sniper_tokens_bought = pump_fun.update_pool_with_buy(sniper_buy_amount)

    # Lists to store data for each simulation
    token_prices_over_time = []
    mcap_over_time = []
    remaining_tokens_over_time = []

    # Store when the sniper sells
    sniper_sell_time = 20  # Sniper will sell after 20 seconds
    sniper_profit = 0  # Store sniper's profit

    # Buyers interact for the first 20 seconds
    for second in range(interaction_duration_seconds):
        if second % interaction_interval_seconds == 0:

            # Buyers buy for the first 20 seconds to drive the price up
            if second <= sniper_sell_time:
                for i in range(4):  # 4 buyers
                    buy_amount = random.uniform(0.15, 1.0)  # Buyers buy between 0.15 and 1 SOL
                    tokens_bought = pump_fun.update_pool_with_buy(buy_amount)

            # After sniper's buy, they sell after 20 seconds
            if second == sniper_sell_time:
                sol_received = pump_fun.update_pool_with_sell(sniper_tokens_bought)
                sniper_profit = sol_received - sniper_buy_amount  # Sniper profit calculation

            # After sniper sells, smaller buyers and sellers enter for zigzag effect
            if second > sniper_sell_time:
                for i in range(3):  # More buyers and sellers to create price fluctuations
                    small_buy_amount = random.uniform(0.05, 0.2)  # Small buy amounts
                    tokens_bought = pump_fun.update_pool_with_buy(small_buy_amount)

                    if pump_fun.remaining_tokens_in_pool > 0:
                        small_sell_amount = random.uniform(0.02, 0.1) * pump_fun.remaining_tokens_in_pool  # Small sell amounts
                        sol_received = pump_fun.update_pool_with_sell(small_sell_amount)

            # Compute the token price and remaining tokens in the pool
            token_price = pump_fun.get_token_price()
            token_prices_over_time.append(token_price)

            remaining_tokens = pump_fun.get_remaining_token_supply()
            remaining_tokens_over_time.append(remaining_tokens)

            # Compute and store the market capitalization
            mcap = pump_fun.get_mcap_statistics()
            mcap_over_time.append(mcap)

    # Append this simulation's data to the overall results
    all_sniper_profits.append(sniper_profit)
    all_token_prices_over_time.append(token_prices_over_time)
    all_mcap_over_time.append(mcap_over_time)

# Convert results to numpy arrays for plotting
all_token_prices_over_time = np.array(all_token_prices_over_time)
all_mcap_over_time = np.array(all_mcap_over_time)
all_sniper_profits = np.array(all_sniper_profits)

# Plot 1000 token price trajectories
plt.figure(figsize=(10, 6))
time_ticks = np.arange(0, interaction_duration_seconds, interaction_interval_seconds)
for token_prices in all_token_prices_over_time:
    plt.plot(time_ticks, token_prices, color='blue', alpha=0.1)
plt.xlabel("Time (seconds)")
plt.ylabel("Token Price (SOL)")
plt.title("Token Price Over Time (1000 Monte Carlo Simulations)")
plt.show()

# Plot market capitalization over time (continued)
plt.figure(figsize=(10, 6))
for mcap in all_mcap_over_time:
    plt.plot(time_ticks, mcap, color='green', alpha=0.1)
plt.xlabel("Time (seconds)")
plt.ylabel("Market Capitalization (USD)")
plt.title("Market Capitalization Over Time (1000 Monte Carlo Simulations)")
plt.show()

# Plot histogram of sniper profits (continued)
plt.figure(figsize=(10, 6))
plt.hist(all_sniper_profits, bins=20, color='purple', alpha=0.7)
plt.xlabel("Sniper Profit (SOL)")
plt.ylabel("Frequency")
plt.title("Distribution of Sniper Profits (1000 Simulations)")
plt.show()

# Calculate and print some statistics on sniper profits
mean_sniper_profit = np.mean(all_sniper_profits)
median_sniper_profit = np.median(all_sniper_profits)
max_sniper_profit = np.max(all_sniper_profits)
min_sniper_profit = np.min(all_sniper_profits)

print(f"Mean Sniper Profit: {mean_sniper_profit:.2f} SOL")
print(f"Median Sniper Profit: {median_sniper_profit:.2f} SOL")
print(f"Max Sniper Profit: {max_sniper_profit:.2f} SOL")
print(f"Min Sniper Profit: {min_sniper_profit:.2f} SOL")


# In[ ]:




