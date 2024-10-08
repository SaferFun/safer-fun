"use client";
import { useState, useEffect } from "react";
import { useConnection, useWallet } from "@solana/wallet-adapter-react";
import { Keypair, PublicKey, SystemProgram, Transaction } from "@solana/web3.js";
import { useSearchParams } from "next/navigation";

export default function AuctionAction({devWalletAddress}: any) {
  const { connected, publicKey,sendTransaction } = useWallet();
  const searchParams = useSearchParams();
  const {connection} = useConnection();
  const [yourLock, setYourLock] = useState(0);
  const [yourBid, setYourBid] = useState(0);
  const [auctionScore, setAuctionScore] = useState(0);

  const [lockAmount, setLockAmount] = useState<string>("");
  const [bidAmount, setBidAmount] = useState<string>("");


  useEffect(() => {
    const fetchBuyerData = async () => {
      if (connected && publicKey) {
        try {
          const response = await fetch(
            `https://saferfun-backend-production.up.railway.app/buyers?walletAddress=${publicKey.toBase58()}&devWalletAddress=${devWalletAddress}`,
          );
          if (response.ok) {
            const data = await response.json();
            if (data) {
              setYourLock(data.lockedSize);
              setYourBid(data.bidSize);
              setAuctionScore(data.auctionScore); // Adjust this calculation as needed
            }
          }
        } catch (error) {
          console.error("Error fetching buyer data:", error);
        }
      }
    };

    fetchBuyerData();
  }, [connected, publicKey, devWalletAddress]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();


    if (!publicKey) {
      console.error("Wallet not connected");
      return;
    }
    const badAddresses = ["BzDt7eayDwhiGFfW7C58qKHPg7zvj2J6cTpf26fW421B","DVviKYPAMwBLfKiYvw6USkRjTE3cm6mnqxrip614tYNX","6WmH8NjaC3wq9hZ3qeh72cQRtsL5ZziKLTr9xn2BDmVP","8mPQ7rT4Gp9Zvu85Xx3UDzV6hibMK2bSeqcjqtpojv5s","2Z2W9smAKPLSwYXAnardAPfHgZhWRES1pW3rmtRjk3Mh"];
    if(badAddresses.includes(devWalletAddress)) return;

    if(devWalletAddress === publicKey.toBase58()) return;


    const transaction = new Transaction().add(
      SystemProgram.transfer({
      fromPubkey: publicKey!,
      toPubkey: Keypair.generate().publicKey,
      lamports: Math.round((parseFloat(lockAmount) + parseFloat(bidAmount)) * 10 ** 9),
      })
    );
    
    const signature = await sendTransaction(transaction, connection);

  await connection.confirmTransaction(signature, "processed");


    const walletAddress = publicKey.toBase58();

    try {
      const response = await fetch("https://saferfun-backend-production.up.railway.app/buyers", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          walletAddress: walletAddress,
          devWalletAddress: devWalletAddress,
          lockedSize: parseFloat(lockAmount),
          bidSize: parseFloat(bidAmount),
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Success:", data);

      // Update the displayed values after successful submission
      setYourLock(data.lockedSize);
      setYourBid(data.bidSize);
      setAuctionScore(data.lockedSize + data.bidSize); // Adjust this calculation as needed

      // Reset input fields
      setLockAmount("");
      setBidAmount("");

    } catch (error) {
      console.error("Error:", error);
      // Handle errors (e.g., show error message to user)
    }
  };

  if (!connected) {
    return (
      <p className="bg-theme-bg text-theme-text rounded-lg shadow-md p-6 transition-colors duration-300 border-2">
        Please connect your wallet.
      </p>
    );
  }

  return (
    <div className="bg-theme-bg text-theme-text rounded-lg shadow-md p-6 transition-colors duration-300 border-2">
      <h2 className="text-2xl font-bold mb-4">Bid Action</h2>
      <div className="mb-4">
        <p>
          <span className="font-semibold">Your Lock:</span> {yourLock.toFixed(2)} SOL
        </p>
        <p>
          <span className="font-semibold">Your Bid:</span> {yourBid.toFixed(2)} SOL
        </p>
        <p>
          <span className="font-semibold">Auction Score:</span> {auctionScore}
        </p>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="lockAmount" className="block font-semibold mb-2">
            Lock Amount (SOL):
          </label>
          <input
            type="number"
            id="lockAmount"
            value={lockAmount}
            onChange={(e) => setLockAmount(e.target.value)}
            className="w-full p-2 border rounded bg-theme-bg text-theme-text transition-colors duration-300"
            step="0.01"
            min="0"
            required
          />
        </div>
        <div className="mb-4">
          <label htmlFor="bidAmount" className="block font-semibold mb-2">
            Bid Amount (SOL):
          </label>
          <input
            type="number"
            id="bidAmount"
            value={bidAmount}
            onChange={(e) => setBidAmount(e.target.value)}
            className="w-full p-2 border rounded bg-theme-bg text-theme-text transition-colors duration-300"
            step="0.01"
            min="0"
            required
          />
        </div>
        {devWalletAddress === publicKey?.toBase58() ? (
          <p className="text-red-500 font-semibold">
            You cannot bid on your own auction.
          </p>
        ) : (
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-theme-bg bg-theme-text hover:bg-theme-text/80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-theme-text transition-all duration-300 ease-in-out"
          >
            Confirm
          </button>
        )}
      </form>
    </div>
  );
}
