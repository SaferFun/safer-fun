![Project Logo](safer.fun_header.png)


*Safer.fun is a platform-agnostic protocol enhancing fairness in the memecoin market by introducing unique way of randomness and auctions. It combats malicious actors like snipers and unethical developers, preventing systematic, risk-free wins. It ensures equitable token launches and fair allocation for buyers, improving user experience across any platform or DEX.*



# App Structure


**[Backend](backend/) :** We use Nest.js in order to handle non-important functionalty eg. posting comments. This is not an obligation for solana program of Safer.fun



**[Simulations](simulations/) :** A monte carlo simulation of types of rugpulls in a classical pump.fun like_pool as well as a one for a mock safer.fun. 

**[Solana Program](solana-program/) :** We use [clockwork](https://docs.clockwork.xyz/) to handle worker-like functionalty on distribution phase. We use VRF to introduce randomness on clockwork calls 


# How To Calculate Auction Score

![1728424925663.png](./imgs/auction_score.png)


# How Do We Do

![1728425160027.png](./imgs/1728425160027.png)

![1728425177566.png](./imgs/1728425177566.png)

# Exploit Examples

![](https://cdn.discordapp.com/attachments/1284871708548792353/1292769967015727104/image.png?ex=6706eb9a&is=67059a1a&hm=63c0d08ee93daaad75eb1920103c74d38bdbd0705b6589123076344ef086b39b&=)

![](https://cdn.discordapp.com/attachments/1284871708548792353/1292774976973176885/image.png?ex=6706f045&is=67059ec5&hm=ee6acb37d9707a854b9584fe9746ca83d5c650b48a65cf4b2307eb72a682669d&=)

![](https://cdn.discordapp.com/attachments/1284871708548792353/1292787000700571670/image.png?ex=6706fb77&is=6705a9f7&hm=bd28546f43af10158ff78519c4c4172bd20c6851b75851f8930d8a0c71b07c7e&=)

![](https://cdn.discordapp.com/attachments/1284871708548792353/1292787169341083679/image.png?ex=6706fb9f&is=6705aa1f&hm=58c97fb740aa8a98f4deb4b7e7b3a88b90fc21ddbf8795c83d7d42d53b6396ed&=)
