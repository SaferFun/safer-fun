#!/usr/bin/env python
# coding: utf-8

# # Developper class

# In[43]:


class DevClass:
    def __init__(self, token_name: str, sol_amount: float, buyback_amount: float, order_lifetime: int):
        self.token_name = token_name
        self.sol_amount = sol_amount
        self.buyback_amount = buyback_amount
        self.order_lifetime = order_lifetime
        self.pump_fee = self.compute_pump_fee()  # 1% pump.fun fee applied on the developer's SOL contribution
        self.token_allocation = 0.0  # Developer's total token allocation
        self.profit = 0.0  # Developer's profit

    def compute_pump_fee(self):
        return 0.01 * self.sol_amount

    def start_pool(self):
        pool_details = {
            "token_name": self.token_name,
            "sol_amount": self.sol_amount,
            "pump_fee": self.pump_fee,
            "buyback_amount": self.buyback_amount,
            "order_lifetime": self.order_lifetime
        }
        return pool_details

    def set_token_allocation(self, allocation):
        """ Set the initial token allocation for the developer. """
        self.token_allocation = allocation

    def sell_received_tokens(self, token_amount: float, token_price: float):
        """
        Sell all received tokens immediately and track profit.
        :param token_amount: The number of tokens the dev receives.
        :param token_price: The price of the token at the time of sale.
        """
        sol_earned = token_amount * token_price  # Calculate how much SOL is earned from selling tokens
        self.profit += sol_earned  # Add to profit

    def get_profit(self):
        """
        Return the total profit made by the developer at the end of the simulation.
        """
        return self.profit


# In[44]:


class PreBuyerClass:
    def __init__(self, sol_amount: float, coin_name: str, bidding_strategy: str):
        self.sol_amount = sol_amount
        self.coin_name = coin_name
        self.bidding_strategy = bidding_strategy
        self.current_bid = 0.0  # Tracks how much SOL the pre-buyer has bid so far.
        self.tokens_allocated = 0.0  # Tokens allocated to the pre-buyer after the bidding process.

    def choose_strategy(self, current_time: int, total_time: int):
        if self.bidding_strategy == 'bid_once':
            return self.bid_once()
        elif self.bidding_strategy == 'rebid_every_2_minutes':
            return self.rebid_every_2_minutes(current_time)
        elif self.bidding_strategy == 'bid_at_end':
            return self.bid_at_end(current_time, total_time)
        elif self.bidding_strategy == 'always_bid_highest':  
            return self.always_bid_highest(current_time, total_time)
        else:
            raise ValueError("Invalid bidding strategy")

    def bid_once(self):
        if self.current_bid == 0.0:  
            bid_amount = min(0.1, self.sol_amount)  
            self.current_bid += bid_amount
            return bid_amount
        return 0.0

    def rebid_every_2_minutes(self, current_time: int):
        if current_time % 120 == 0:  
            random_bid = random.uniform(0.05, 0.1)  
            bid_amount = min(random_bid, self.sol_amount - self.current_bid)  
            self.current_bid += bid_amount
            return bid_amount
        return 0.0

    def bid_at_end(self, current_time: int, total_time: int):
        if current_time >= total_time - 60:  
            bid_amount = min(0.1, self.sol_amount - self.current_bid)  
            self.current_bid += bid_amount
            return bid_amount
        return 0.0

    def always_bid_highest(self, current_time: int, total_time: int):
        max_bid = min(0.2, self.sol_amount - self.current_bid)  
        self.current_bid += max_bid
        return max_bid

    def place_bid(self, current_time: int, total_time: int):
        return self.choose_strategy(current_time, total_time)

    def receive_token_allocation(self, tokens_allocated: float):
        self.tokens_allocated = tokens_allocated

    def sell_received_tokens(self, token_amount: float, token_price: float):
        if token_amount > self.tokens_allocated:
            token_amount = self.tokens_allocated  
        sol_earned = token_amount * token_price  
        self.tokens_allocated -= token_amount  
        return sol_earned


# # Unlocking mechanism

# In[45]:


class UnlockingMechanism:
    def __init__(self, total_liquidity, buyback_amount, buyer_id, is_developer=False):
        self.total_liquidity = total_liquidity
        self.buyback_amount = buyback_amount  # Maximum liquidity to unlock
        self.buyer_id = buyer_id
        self.is_developer = is_developer
        self.unlocked_liquidity = 0  # Track total unlocked liquidity
        self.current_mcap_threshold = None  # Mcap threshold initialized to None
        self.time_thresholds = []  # List to store time thresholds
        self.current_time_threshold_index = 0  # Track which time threshold we are using
        self.unlock_percentage = None  # Percentage of liquidity to unlock

    def generate_time_thresholds(self):
        first_threshold = np.random.randint(1, 301)
        second_threshold = np.random.randint(first_threshold, 601)
        third_threshold = np.random.randint(second_threshold, 1001)
        fourth_threshold = np.random.randint(1000, 1200)
        self.time_thresholds = [first_threshold, second_threshold, third_threshold, fourth_threshold]

    def generate_unlock_conditions(self, current_mcap):
        mcap_variation = np.random.uniform(-0.1, 0.1)
        self.current_mcap_threshold = current_mcap * (1 + mcap_variation)
        self.unlock_percentage = random.uniform(0.05, 0.25)

    def unlock_liquidity(self, current_time, total_time, mcap):
        if not self.time_thresholds:
            self.generate_time_thresholds()

        current_time_threshold = self.time_thresholds[self.current_time_threshold_index]

        if self.current_mcap_threshold is None:
            self.generate_unlock_conditions(mcap)

        if current_time >= current_time_threshold and mcap >= self.current_mcap_threshold:
            unlocked_amount = self.total_liquidity * self.unlock_percentage

            if self.unlocked_liquidity + unlocked_amount > self.buyback_amount:
                unlocked_amount = self.buyback_amount - self.unlocked_liquidity

            self.unlocked_liquidity += unlocked_amount

            if self.current_time_threshold_index < len(self.time_thresholds) - 1:
                self.current_time_threshold_index += 1
                self.current_mcap_threshold = None

            return unlocked_amount
        return 0.0


# # Pumpfun_like class

# In[46]:


class PumpFunClass:
    def __init__(self, initial_sol_in_pool, total_tokens_in_pool):
        self.sol_pool = initial_sol_in_pool
        self.total_coin_supply = total_tokens_in_pool  # Total supply of tokens (1 billion initially)
        self.remaining_tokens_in_pool = total_tokens_in_pool  # Initially, all tokens are in the pool
        self.virtual_remaining_tokens = total_tokens_in_pool  # Tokens left for virtual allocation in pre-bidding

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

    def compute_bonding_curve(self, sol_amount, remaining_virtual_tokens):
        """
        Compute the number of tokens allocated based on the bonding curve formula.
        
        :param sol_amount: The amount of SOL contributed by a pre-buyer or the developer.
        :param remaining_virtual_tokens: Virtual token supply left for allocation.
        :return: The number of tokens allocated and the updated virtual token pool.
        """
        # Update the SOL pool as part of the bonding curve
        self.sol_pool += sol_amount

        # Token allocation from the virtual pool
        tokens_allocated = sol_amount / self.get_token_price()  # Using the DEX price formula

        # Ensure we don't allocate more tokens than the remaining virtual supply
        if tokens_allocated > remaining_virtual_tokens:
            tokens_allocated = remaining_virtual_tokens

        # Update the remaining virtual token pool after allocation
        remaining_virtual_tokens -= tokens_allocated

        return tokens_allocated, remaining_virtual_tokens

    def update_mcap(self, sol_amount):
        """
        Update market capitalization based on the contribution of SOL.
        
        :param sol_amount: The amount of SOL added to the pool.
        """
        self.sol_pool += sol_amount  # Add the SOL to the pool
        mcap = self.get_mcap_statistics()  # Recalculate the market cap
        return mcap


# # Protocol_class (safer.fun)

# In[47]:


class ProtocolClass:
    def __init__(self, total_coin_supply: int = 1_000_000_000, dev_pool: dict = None, prebuyers: list = None):
        """
        Initialize the protocol with the developer's pool and pre-buyers.
        
        :param total_coin_supply: The total supply of tokens available for pre-buyers (capped at 1 billion).
        :param dev_pool: The developer's pool containing the initial parameters.
        :param prebuyers: The list of pre-buyers who are participating in the bidding process.
        """
        self.total_coin_supply = total_coin_supply  # Total token supply, capped at 1 billion
        self.sol_pool = dev_pool['sol_amount'] if dev_pool else 0  # SOL contributed to the pool
        self.k_value = self.total_coin_supply * self.sol_pool  # Initial product for the bonding curve
        self.dev_pool = dev_pool
        self.prebuyers = prebuyers or []
        self.ranking = []  # Stores ranking of pre-buyers
        self.time_elapsed = 0  # Track time in the bidding process
        self.pump_fun = PumpFunClass(self.sol_pool, self.total_coin_supply)  # Initialize pump.fun with SOL and tokens
        self.dev_token_allocation = 0  # Tracks developer's token allocation
        self.remaining_virtual_tokens = self.total_coin_supply  # Initialize with total tokens for virtual allocation

    def create_virtual_pool(self):
        """
        Create the virtual pool using the bonding curve formula (x * y = k).
        """
        self.k_value = self.total_coin_supply * self.sol_pool  # Update k value based on SOL pool

    def compute_bonding_curve(self, sol_amount: float):
        """
        Compute the number of tokens allocated based on the bonding curve formula.
        
        :param sol_amount: The amount of SOL contributed by a pre-buyer or the developer.
        :return: The number of tokens allocated to the contributor.
        """
        allocated_tokens, self.remaining_virtual_tokens = self.pump_fun.compute_bonding_curve(
            sol_amount, self.remaining_virtual_tokens
        )
        return allocated_tokens

    def compute_dev_allocation(self):
        """
        Compute the token allocation for the developer based on their initial SOL contribution.
        The developer's allocation is fixed based on the bonding curve at the start, unaffected by later market changes.
        
        :return: The number of tokens allocated to the developer.
        """
        dev_sol_contribution = self.dev_pool['sol_amount']
        self.dev_token_allocation = self.compute_bonding_curve(dev_sol_contribution)
        return self.dev_token_allocation

    def rank_prebuyers(self, total_bidding_time: int, beta: float = 0.1):
        """
        Rank the pre-buyers based on their bid amount, SOL, and time weighting.
        
        :param total_bidding_time: The total time allocated for the bidding process.
        :param beta: A time-weighting parameter (default: 0.1).
        """
        for prebuyer in self.prebuyers:
            bid_amount = prebuyer.current_bid
            sol_amount = prebuyer.sol_amount
            rank = (bid_amount / sol_amount) * (1 + beta * (total_bidding_time - self.time_elapsed) / total_bidding_time)
            self.ranking.append((prebuyer, rank))

        # Sort by rank in descending order
        self.ranking.sort(key=lambda x: x[1], reverse=True)

    def display_ranking(self):
        """
        Display the current ranking of the pre-buyers.
        """
        ranking_output = ["Developer is ranked first."]
        for idx, (prebuyer, rank) in enumerate(self.ranking):
            ranking_output.append(f"Pre-buyer {idx+1}: {prebuyer.coin_name} with rank {rank:.2f}")
        return ranking_output

    def compute_coin_allocation(self):
        """
        Compute the coin allocation for pre-buyers based on their bids.
        :return: List of allocations for each pre-buyer (numeric values).
        """
        allocations = []
        for prebuyer, _ in self.ranking:
            sol_bid = prebuyer.current_bid
            allocated_coins = self.compute_bonding_curve(sol_bid)  # Allocate tokens based on the bonding curve
            allocations.append(allocated_coins)  # Append only the numeric value, not the description
        return allocations

    def place_prebuyer_bid(self, prebuyer, total_bidding_time: int):
        """
        Place a bid for a pre-buyer, update the pool, and display Mcap after each bid.
        
        :param prebuyer: The pre-buyer placing the bid.
        :param total_bidding_time: Total bidding time in seconds.
        """
        bid_amount = prebuyer.place_bid(self.time_elapsed, total_bidding_time)
        if bid_amount > 0:
            self.sol_pool += bid_amount  # Add the bid to the SOL pool
            self.pump_fun.update_mcap(bid_amount)  # Update Mcap with the new SOL in the pool

    def start_bidding(self, total_bidding_time: int):
        """
        Start the bidding process and update the rankings every 2 minutes.
        
        :param total_bidding_time: The total time allocated for the bidding process (in seconds).
        :return: The final ranking of the pre-buyers.
        """
        for t in range(total_bidding_time):
            self.time_elapsed = t
            for prebuyer in self.prebuyers:
                self.place_prebuyer_bid(prebuyer, total_bidding_time)  # Process each pre-buyer's bid
            if t % 120 == 0:  # Every 2 minutes, update rankings
                self.rank_prebuyers(total_bidding_time)
        return self.display_ranking()

    def unlock_liquidity(self, current_time, total_time, mcap, unlocking_mechanism):
        """
        Unlock liquidity using the randomized unlocking mechanism based on time and Mcap thresholds.
        
        :param current_time: The current time in the unlocking process.
        :param total_time: The total available time for unlocking.
        :param mcap: The current Mcap of the pool.
        :param unlocking_mechanism: The unlocking mechanism object for either the developer or pre-buyers.
        """
        unlocked_amount = unlocking_mechanism.unlock_liquidity(current_time, total_time, mcap)
        return unlocked_amount


# # Agressive dev class

# In[48]:


class AggressiveDevClass:
    def __init__(self, token_name: str, sol_amount: float, buyback_amount: float, order_lifetime: int):
        self.token_name = token_name
        self.sol_amount = sol_amount
        self.buyback_amount = buyback_amount
        self.order_lifetime = order_lifetime
        self.token_allocation = 0
        self.profit = 0  # Track profit

    def start_pool(self):
        return {
            "token_name": self.token_name,
            "sol_amount": self.sol_amount,
            "buyback_amount": self.buyback_amount,
            "order_lifetime": self.order_lifetime
        }

    def sell_received_tokens(self, token_amount: float, token_price: float):
        sol_earned = token_amount * token_price
        self.profit += sol_earned

    def get_profit(self):
        return self.profit


# # Buyer_class (its actually for buyers and sellers interacting with the pumpfun pool)

# In[49]:


class BuyerClass:
    def __init__(self, sol_amount: float, buyer_id: int):
        """
        Initialize a real buyer who interacts with the pump.fun pool.
        
        :param sol_amount: The amount of SOL the buyer wants to use to interact with the pool.
        :param buyer_id: A unique ID for each buyer.
        """
        self.sol_amount = sol_amount
        self.buyer_id = buyer_id  # Unique ID to track buyers
        self.tokens = 0  # Tokens start at 0 and accumulate through buying

    def buy_tokens(self, pump_fun_pool, sol_price: float, buy_amount: float):
        """
        The buyer buys a specified amount of tokens from the pump.fun pool.
        
        :param pump_fun_pool: The pump.fun pool where the buyer interacts.
        :param sol_price: The current price of SOL (used to compute the purchase).
        :param buy_amount: The amount of SOL the buyer wants to use for this purchase.
        :return: The number of tokens bought.
        """
        if self.sol_amount >= buy_amount:  # Ensure the buyer has enough SOL to spend
            tokens_bought = buy_amount / sol_price  # Calculate tokens bought based on SOL price
            self.tokens += tokens_bought  # Add bought tokens to buyer's balance
            self.sol_amount -= buy_amount  # Deduct the spent SOL from buyer's total SOL
            pump_fun_pool.update_mcap(buy_amount)  # Update pool's Mcap based on the SOL used
            return tokens_bought
        else:
            return 0  # Removed the print statement

    def sell_tokens(self, pump_fun_pool, sol_price: float, sell_amount: float):
        """
        The buyer sells a specified amount of tokens back to the pool.
        
        :param pump_fun_pool: The pump.fun pool where the buyer interacts.
        :param sol_price: The current price of SOL (used to compute the sale).
        :param sell_amount: The amount of tokens the buyer wants to sell.
        :return: The amount of SOL earned from selling.
        """
        if self.tokens >= sell_amount:  # Ensure the buyer has enough tokens to sell
            sol_earned = sell_amount * sol_price  # Calculate SOL earned from selling tokens
            pump_fun_pool.update_mcap(-sol_earned)  # Update Mcap negatively for selling
            self.tokens -= sell_amount  # Deduct sold tokens from buyer's balance
            self.sol_amount += sol_earned  # Add earned SOL to buyer's SOL balance
            return sol_earned
        else:
            return 0  # Removed the print statement


# In[50]:


import random
import matplotlib.pyplot as plt
import numpy as np

# Simulation Parameters
num_simulations = 1000  # Number of Monte Carlo simulations
sol_price = 150  # USD value of SOL
total_token_supply = 1_000_000_000  # 1 billion tokens total
withdrawal_duration_seconds = 1200  # 20 minutes in seconds
interaction_interval_seconds = 10  # Buyers interact with the pool every 10 seconds

# Class Definitions
class PumpFunClass:
    def __init__(self, initial_sol_in_pool, total_tokens_in_pool):
        self.sol_pool = initial_sol_in_pool
        self.total_coin_supply = total_tokens_in_pool
        self.remaining_tokens_in_pool = total_tokens_in_pool

    def get_token_price(self):
        return self.sol_pool / self.remaining_tokens_in_pool

    def get_mcap_statistics(self):
        return self.total_coin_supply * self.get_token_price() * 150  # Assuming SOL price is 150 USD

    def get_remaining_token_supply(self):
        return self.remaining_tokens_in_pool

    def update_pool_with_buy(self, sol_amount):
        self.sol_pool += sol_amount
        tokens_bought = sol_amount / self.get_token_price()
        self.remaining_tokens_in_pool -= tokens_bought
        return tokens_bought

    def update_pool_with_sell(self, tokens_sold):
        self.remaining_tokens_in_pool += tokens_sold
        sol_to_receive = tokens_sold * self.get_token_price()
        self.sol_pool -= sol_to_receive
        return sol_to_receive

    def update_mcap(self, sol_amount):
        self.sol_pool += sol_amount
        return self.get_mcap_statistics()

    def compute_bonding_curve(self, sol_amount, remaining_virtual_tokens):
        """
        Compute the number of tokens allocated using the bonding curve formula.
        
        :param sol_amount: Amount of SOL contributed to the pool.
        :param remaining_virtual_tokens: Virtual token supply remaining after each contribution.
        :return: The number of tokens allocated to the contributor.
        """
        tokens_allocated = (sol_amount / self.sol_pool) * remaining_virtual_tokens
        remaining_virtual_tokens -= tokens_allocated
        return tokens_allocated, remaining_virtual_tokens

# Simulation Workflow
for sim in range(num_simulations):
    dev = AggressiveDevClass(token_name="MemeCoin", sol_amount=10, buyback_amount=3, order_lifetime=15)
    dev_pool = dev.start_pool()

    num_prebuyers = random.randint(5, 15)
    prebuyers = []
    aggressive_prebuyer = PreBuyerClass(sol_amount=2.0, coin_name="MemeCoin", bidding_strategy="always_bid_highest")
    prebuyers.append(aggressive_prebuyer)

    for i in range(num_prebuyers):
        sol_amount = random.uniform(0.1, 0.5)
        strategy = random.choice(["bid_once", "rebid_every_2_minutes", "bid_at_end"])
        prebuyers.append(PreBuyerClass(sol_amount=sol_amount, coin_name="MemeCoin", bidding_strategy=strategy))

    protocol = ProtocolClass(dev_pool=dev_pool, prebuyers=prebuyers)
    total_bidding_time = 900  # 15 minutes
    final_ranking = protocol.start_bidding(total_bidding_time)

    dev_token_allocation = protocol.compute_dev_allocation()
    token_allocations = protocol.compute_coin_allocation()

    pump_fun = PumpFunClass(initial_sol_in_pool=protocol.sol_pool, total_tokens_in_pool=protocol.total_coin_supply)

    num_buyers = random.randint(5, 10)
    buyers = []
    for i in range(num_buyers):
        sol_amount = random.uniform(0.5, 2.0)
        buyers.append(BuyerClass(sol_amount=sol_amount, buyer_id=i+1))

    unlock_mechanism_dev = UnlockingMechanism(
        total_liquidity=dev_token_allocation, buyback_amount=dev.buyback_amount, buyer_id='Dev', is_developer=True
    )

    unlock_mechanism_prebuyers = {}
    for prebuyer, allocation in zip(prebuyers, token_allocations):
        unlock_mechanism_prebuyers[prebuyer] = UnlockingMechanism(
            total_liquidity=allocation, buyback_amount=prebuyer.sol_amount, buyer_id=prebuyer
        )

    token_prices_over_time = []
    mcap_over_time = []
    price_differences = []
    previous_price = None

    for second in range(withdrawal_duration_seconds):
        if second % interaction_interval_seconds == 0:
            for buyer in buyers:
                action = random.random()
                if action <= 0.5:
                    buy_amount = random.uniform(0.05, 0.2)
                    buyer.buy_tokens(pump_fun, sol_price, buy_amount)
                else:
                    if buyer.tokens > 0:
                        sell_amount = random.uniform(0.01, buyer.tokens)
                        buyer.sell_tokens(pump_fun, sol_price, sell_amount)

            dev_unlocked_tokens = unlock_mechanism_dev.unlock_liquidity(second, withdrawal_duration_seconds, pump_fun.get_mcap_statistics())
            if dev_unlocked_tokens > 0:
                dev.sell_received_tokens(token_amount=dev_unlocked_tokens, token_price=pump_fun.get_token_price())

            for prebuyer, unlock_mechanism in unlock_mechanism_prebuyers.items():
                prebuyer_unlocked_tokens = unlock_mechanism.unlock_liquidity(second, withdrawal_duration_seconds, pump_fun.get_mcap_statistics())
                if prebuyer_unlocked_tokens > 0:
                    prebuyer.sell_received_tokens(token_amount=prebuyer_unlocked_tokens, token_price=pump_fun.get_token_price())

            token_price = pump_fun.get_token_price()
            token_prices_over_time.append(token_price)

            current_mcap = pump_fun.get_mcap_statistics()
            mcap_over_time.append(current_mcap)

            if previous_price is not None:
                price_difference = token_price - previous_price
                price_differences.append(price_difference)
            previous_price = token_price

# Plotting Results for a single simulation
time_ticks = np.arange(0, withdrawal_duration_seconds, interaction_interval_seconds)
plt.figure(figsize=(10, 6))
plt.plot(time_ticks, token_prices_over_time, label="Token Price (SOL)")
plt.xlabel("Time (seconds)")
plt.ylabel("Token Price (SOL)")
plt.title("Token Price Over Time")
plt.legend()
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(time_ticks, mcap_over_time, label="Mcap (USD)", color='green')
plt.xlabel("Time (seconds)")
plt.ylabel("Market Capitalization (USD)")
plt.title("Market Capitalization Over Time")
plt.legend()
plt.show()


# # A simulation with aggressive developper that sells his unlocked amount

# In[51]:


import random
import matplotlib.pyplot as plt
import numpy as np

# Simulation Parameters
num_simulations = 1000  # Number of Monte Carlo simulations
sol_price = 150  # USD value of SOL
total_token_supply = 1_000_000_000  # 1 billion tokens total
withdrawal_duration_seconds = 1200  # 20 minutes in seconds
interaction_interval_seconds = 10  # Buyers interact with the pool every 10 seconds

# Lists to store results across simulations
all_token_prices_over_time = []
all_mcap_over_time = []
unlocking_events = []  # Store unlocking event times and amounts

# Monte Carlo Simulation Loop
for sim in range(num_simulations):
    # Step 1: Developer creates the pool (Aggressive Dev)
    dev = AggressiveDevClass(token_name="MemeCoin", sol_amount=10, buyback_amount=3, order_lifetime=15)
    dev_pool = dev.start_pool()

    # Step 2: Randomly generate pre-buyers (including aggressive pre-buyer)
    num_prebuyers = random.randint(5, 15)
    prebuyers = []
    aggressive_prebuyer = PreBuyerClass(sol_amount=2.0, coin_name="MemeCoin", bidding_strategy="always_bid_highest")
    prebuyers.append(aggressive_prebuyer)

    for i in range(num_prebuyers):
        sol_amount = random.uniform(0.1, 0.5)
        strategy = random.choice(["bid_once", "rebid_every_2_minutes", "bid_at_end"])
        prebuyers.append(PreBuyerClass(sol_amount=sol_amount, coin_name="MemeCoin", bidding_strategy=strategy))

    protocol = ProtocolClass(dev_pool=dev_pool, prebuyers=prebuyers)
    total_bidding_time = 900  # 15 minutes
    final_ranking = protocol.start_bidding(total_bidding_time)

    dev_token_allocation = protocol.compute_dev_allocation()
    token_allocations = protocol.compute_coin_allocation()

    pump_fun = PumpFunClass(initial_sol_in_pool=protocol.sol_pool, total_tokens_in_pool=protocol.total_coin_supply)

    num_buyers = random.randint(5, 10)
    buyers = []
    for i in range(num_buyers):
        sol_amount = random.uniform(0.5, 2.0)
        buyers.append(BuyerClass(sol_amount=sol_amount, buyer_id=i+1))

    unlock_mechanism_dev = UnlockingMechanism(
        total_liquidity=dev_token_allocation, buyback_amount=dev.buyback_amount, buyer_id='Dev', is_developer=True
    )

    unlock_mechanism_prebuyers = {}
    for prebuyer, allocation in zip(prebuyers, token_allocations):
        unlock_mechanism_prebuyers[prebuyer] = UnlockingMechanism(
            total_liquidity=allocation, buyback_amount=prebuyer.sol_amount, buyer_id=prebuyer
        )

    token_prices_over_time = []
    mcap_over_time = []
    previous_price = None

    unlockings_this_sim = []  # Store the unlocking events for each simulation

    # Step 7: Simulate the withdrawal process
    for second in range(withdrawal_duration_seconds):
        if second % interaction_interval_seconds == 0:
            # Buyers either buy or sell randomly at this tick
            for buyer in buyers:
                action = random.random()
                if action <= 0.5:
                    buy_amount = random.uniform(0.05, 0.2)
                    buyer.buy_tokens(pump_fun, sol_price, buy_amount)
                else:
                    if buyer.tokens > 0:
                        sell_amount = random.uniform(0.01, buyer.tokens)
                        buyer.sell_tokens(pump_fun, sol_price, sell_amount)

            # Unlock tokens for developer and pre-buyers, track events
            dev_unlocked_tokens = unlock_mechanism_dev.unlock_liquidity(second, withdrawal_duration_seconds, pump_fun.get_mcap_statistics())
            if dev_unlocked_tokens > 0:
                dev.sell_received_tokens(token_amount=dev_unlocked_tokens, token_price=pump_fun.get_token_price())
                unlockings_this_sim.append((second, dev_unlocked_tokens))  # Track unlocking event for dev

            for prebuyer, unlock_mechanism in unlock_mechanism_prebuyers.items():
                prebuyer_unlocked_tokens = unlock_mechanism.unlock_liquidity(second, withdrawal_duration_seconds, pump_fun.get_mcap_statistics())
                if prebuyer_unlocked_tokens > 0:
                    prebuyer.sell_received_tokens(token_amount=prebuyer_unlocked_tokens, token_price=pump_fun.get_token_price())
                    unlockings_this_sim.append((second, prebuyer_unlocked_tokens))  # Track unlocking event for pre-buyers

            # Track token price and Mcap over time
            token_price = pump_fun.get_token_price()
            token_prices_over_time.append(token_price)

            current_mcap = pump_fun.get_mcap_statistics()
            mcap_over_time.append(current_mcap)

    # Store results for the current simulation
    all_token_prices_over_time.append(token_prices_over_time)
    all_mcap_over_time.append(mcap_over_time)
    unlocking_events.append(unlockings_this_sim)

# Plot Results from 1000 Simulations
time_ticks = np.arange(0, withdrawal_duration_seconds, interaction_interval_seconds)

# Plot Token Prices over Time
plt.figure(figsize=(10, 6))
for token_prices in all_token_prices_over_time:
    plt.plot(time_ticks, token_prices, color='blue', alpha=0.1)

mean_price = np.mean(all_token_prices_over_time, axis=0)
plt.plot(time_ticks, mean_price, color='red', label='Mean Price')
plt.xlabel("Time (seconds)")
plt.ylabel("Token Price (SOL)")
plt.title("Token Price Over Time (Monte Carlo Simulation)")
plt.legend()
plt.show()

# Plot Mcap over Time
plt.figure(figsize=(10, 6))
for mcap in all_mcap_over_time:
    plt.plot(time_ticks, mcap, color='green', alpha=0.1)

mean_mcap = np.mean(all_mcap_over_time, axis=0)
plt.plot(time_ticks, mean_mcap, color='orange', label='Mean Mcap')
plt.xlabel("Time (seconds)")
plt.ylabel("Market Capitalization (USD)")
plt.title("Market Capitalization Over Time (Monte Carlo Simulation)")
plt.legend()
plt.show()


# # Simulation in the case of a honest developer

# In[52]:


import random
import matplotlib.pyplot as plt
import numpy as np

# Simulation Parameters
num_simulations = 1000  # Number of Monte Carlo simulations
sol_price = 150  # USD value of SOL
total_token_supply = 1_000_000_000  # 1 billion tokens total
withdrawal_duration_seconds = 1200  # 20 minutes in seconds
interaction_interval_seconds = 10  # Buyers interact with the pool every 10 seconds

# Lists to store simulation results
all_token_prices_over_time = []
all_mcap_over_time = []

# Monte Carlo Simulation Loop
for sim in range(num_simulations):
    # Step 1: Developer creates the pool (Normal Dev)
    dev = DevClass(token_name="MemeCoin", sol_amount=10, buyback_amount=3, order_lifetime=15)
    dev_pool = dev.start_pool()

    # Step 2: Randomly generate pre-buyers (including aggressive pre-buyer)
    num_prebuyers = random.randint(5, 15)  # Random number of pre-buyers between 5 and 15
    prebuyers = []
    aggressive_prebuyer = PreBuyerClass(sol_amount=2.0, coin_name="MemeCoin", bidding_strategy="always_bid_highest")
    prebuyers.append(aggressive_prebuyer)

    # Add normal pre-buyers
    for i in range(num_prebuyers):
        sol_amount = random.uniform(0.1, 0.5)  # Each pre-buyer has a random SOL amount
        strategy = random.choice(["bid_once", "rebid_every_2_minutes", "bid_at_end"])  # Different strategies
        prebuyers.append(PreBuyerClass(sol_amount=sol_amount, coin_name="MemeCoin", bidding_strategy=strategy))

    # Step 3: Protocol manages the pre-buying bidding process
    protocol = ProtocolClass(dev_pool=dev_pool, prebuyers=prebuyers)
    total_bidding_time = 900  # 15 minutes in seconds
    final_ranking = protocol.start_bidding(total_bidding_time)

    # Step 4: Compute token allocation for pre-buyers and dev
    dev_token_allocation = protocol.compute_dev_allocation()  # Dev’s token allocation
    token_allocations = protocol.compute_coin_allocation()  # Pre-buyers' token allocation

    # Initialize pump.fun with SOL in pool and total tokens in pool (1 billion tokens)
    pump_fun = PumpFunClass(initial_sol_in_pool=protocol.sol_pool, total_tokens_in_pool=protocol.total_coin_supply)

    # Step 6: Introduce real buyers into the pump.fun pool
    num_buyers = random.randint(5, 10)  # Number of real buyers
    buyers = []
    for i in range(num_buyers):
        sol_amount = random.uniform(0.5, 2.0)  # Each buyer has a random amount of SOL
        buyers.append(BuyerClass(sol_amount=sol_amount, buyer_id=i+1))

    # Lists to store data for plotting within this simulation
    token_prices_over_time = []
    mcap_over_time = []
    previous_price = None

    # Simulate the 20-minute withdrawal process with buyer interactions every 10 seconds
    for second in range(withdrawal_duration_seconds):
        if second % interaction_interval_seconds == 0:
            # Each buyer either buys or sells randomly at this tick
            for buyer in buyers:
                action = random.random()  # Generate a random number to decide action (50/50 chance of buying/selling)
                if action <= 0.5:  # 50% probability of buying
                    buy_amount = random.uniform(0.05, 0.2)  # Buyers buy a random amount of tokens
                    buyer.buy_tokens(pump_fun, sol_price, buy_amount)
                else:  # 50% probability of selling
                    if buyer.tokens > 0:
                        sell_amount = random.uniform(0.01, buyer.tokens)  # Sell a random fraction of tokens
                        buyer.sell_tokens(pump_fun, sol_price, sell_amount)

            # Unlock tokens for the developer and pre-buyers (they sell gradually)
            dev_unlocked_tokens = dev.buyback_amount / 4  # Gradual unlocking over 4 stages
            dev.sell_received_tokens(token_amount=dev_unlocked_tokens, token_price=pump_fun.get_token_price())

            for prebuyer, unlock_mechanism in unlock_mechanism_prebuyers.items():
                prebuyer_unlocked_tokens = unlock_mechanism.unlock_liquidity(
                    current_time=second, total_time=withdrawal_duration_seconds, mcap=pump_fun.get_mcap_statistics())
                if prebuyer_unlocked_tokens > 0:
                    prebuyer.sell_received_tokens(token_amount=prebuyer_unlocked_tokens, token_price=pump_fun.get_token_price())

            # Update token price and Mcap
            token_price = pump_fun.get_token_price()
            token_prices_over_time.append(token_price)

            current_mcap = pump_fun.get_mcap_statistics()
            mcap_over_time.append(current_mcap)

            previous_price = token_price

    # Store results for this simulation
    all_token_prices_over_time.append(token_prices_over_time)
    all_mcap_over_time.append(mcap_over_time)

# Calculate mean price and mcap trajectories
mean_token_prices = np.mean(all_token_prices_over_time, axis=0)
mean_mcap = np.mean(all_mcap_over_time, axis=0)

# Plot token price trajectories and mean trajectory
time_ticks = np.arange(0, withdrawal_duration_seconds, interaction_interval_seconds)

plt.figure(figsize=(10, 6))
for token_prices in all_token_prices_over_time:
    plt.plot(time_ticks, token_prices, color='blue', alpha=0.1)
plt.plot(time_ticks, mean_token_prices, color='red', linewidth=2, label="Mean Token Price")
plt.xlabel("Time (seconds)")
plt.ylabel("Token Price (SOL)")
plt.title("Token Price Over Time (1000 Monte Carlo Simulations)")
plt.legend()
plt.show()

# Plot market capitalization trajectories and mean trajectory
plt.figure(figsize=(10, 6))
for mcap in all_mcap_over_time:
    plt.plot(time_ticks, mcap, color='green', alpha=0.1)
plt.plot(time_ticks, mean_mcap, color='red', linewidth=2, label="Mean Mcap")
plt.xlabel("Time (seconds)")
plt.ylabel("Market Capitalization (USD)")
plt.title("Market Capitalization Over Time (1000 Monte Carlo Simulations)")
plt.legend()
plt.show()


# In[ ]:




