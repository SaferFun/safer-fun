"use client";
import React, { useState, ChangeEvent } from "react";
import CreateInput from "../../components/ui/CreateInput";
import { Transaction, SystemProgram, Keypair, VersionedTransaction } from "@solana/web3.js";
import { useAnchorWallet, useConnection, useWallet } from "@solana/wallet-adapter-react";

export default function CreatePage() {
  const {sendTransaction,connected,publicKey} = useWallet();
  const {connection} = useConnection();
  const [formData, setFormData] = useState({
    platform: "pump.fun",
    name: "",
    symbol: "",
    description: "",
    website: "",
    x: "",
    telegram: "",
    discord: "",
    initialBuySize: "",
    imageUrl: "",
    endsAt: "",
  });

  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const handleInputChange = (
    e: ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const calculateFee = () => {
    const fee = Number(formData.initialBuySize) * 0.011 + 0.0151156;
    return fee.toFixed(5);
  }

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {};

    if (!formData.name.trim()) newErrors.name = "Name is required";
    if (!formData.symbol.trim()) newErrors.symbol = "Symbol is required";
    if (!formData.description.trim())
      newErrors.description = "Description is required";
    if (!formData.website.trim()) newErrors.website = "Website is required";
    if (!formData.x.trim()) newErrors.x = "X (Twitter) is required";
    if (!formData.telegram.trim()) newErrors.telegram = "Telegram is required";
    if (!formData.discord.trim()) newErrors.discord = "Discord is required";
    if (!formData.initialBuySize)
      newErrors.initialBuySize = "Initial buy size is required";
    if (!formData.imageUrl.trim()) newErrors.imageUrl = "Image URL is required";
    if (!formData.endsAt) newErrors.endsAt = "End date is required";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const createOrder = async () => {
    if (!connected) return;
    // Assume sol program
    const transaction = new Transaction().add(
      SystemProgram.transfer({
      fromPubkey: publicKey!,
      toPubkey: Keypair.generate().publicKey,
      lamports: Math.round((Number(calculateFee()) + Number(formData.initialBuySize)) * 10 ** 9),
      })
    );
    
    const signature = await sendTransaction(transaction, connection);

  await connection.confirmTransaction(signature, "processed");
    try {
      const response = await fetch('https://saferfun-backend-production.up.railway.app/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({creator:publicKey?.toBase58(), ...formData}),
      });
      if (!response.ok) {
        throw new Error('Failed to create order');
      }
      const data = await response.json();
      console.log('Order created successfully:', data);
    } catch (error) {
      console.error('Error creating order:', error);
    }
    window.location.href = "/";
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      createOrder();
    } else {
      console.log("Form has errors, please correct them");
    }
  };

  return (
    <div className="min-h-screen bg-notebook-squares bg-theme-bg transition-colors duration-300">
      <div className="h-full w-10/12 mx-auto flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-theme-bg bg-opacity-90 rounded-2xl shadow my-4 transition-colors duration-300">
        <div className="max-w-md w-full space-y-8">
          <h2 className="mt-6 text-center text-3xl font-extrabold text-theme-text transition-colors duration-300">
            Create New Token
          </h2>
          <form onSubmit={handleSubmit} className="mt-8 space-y-6">
            <select
              name="platform"
              value={formData.platform}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-theme-text/30 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 bg-theme-bg text-theme-text transition-colors duration-300"
            >
              <option value="pump.fun">pump.fun</option>
              <option value="moonshot" disabled>
                moonshot
              </option>
              <option value="raydium" disabled>
                raydium
              </option>
              <option value="meteora" disabled>
                meteora
              </option>
            </select>
            <CreateInput label="Name *" type="text" value={formData.name} onChange={handleInputChange} name="name" error={errors.name} />
            <CreateInput label="Symbol *" type="text" value={formData.symbol} onChange={handleInputChange} name="symbol" error={errors.symbol} />
            <CreateInput label="Description *" type="text" value={formData.description} onChange={handleInputChange} name="description" error={errors.description} />
            <CreateInput label="Website *" type="url" value={formData.website} onChange={handleInputChange} name="website" error={errors.website} />
            <CreateInput label="X (Twitter) *" type="text" value={formData.x} onChange={handleInputChange} name="x" error={errors.x} />
            <CreateInput label="Telegram *" type="text" value={formData.telegram} onChange={handleInputChange} name="telegram" error={errors.telegram} />
            <CreateInput label="Discord *" type="text" value={formData.discord} onChange={handleInputChange} name="discord" error={errors.discord} />
            <CreateInput label="Image URL *" type="url" value={formData.imageUrl} onChange={handleInputChange} name="imageUrl" error={errors.imageUrl} />
            <CreateInput label="Initial Buy Size (SOL) *" type="number" value={formData.initialBuySize} onChange={handleInputChange} name="initialBuySize" error={errors.initialBuySize} />
            <CreateInput label="End Date *" type="datetime-local" value={formData.endsAt} onChange={handleInputChange} name="endsAt" error={errors.endsAt} />

            <div className="mb-4">
              <label className="block text-sm font-medium text-theme-text mb-1 transition-colors duration-300">
                Total Fee: pump.fun fee (1% + 0.0151156 SOL) + our fee (0.1%)
              </label>
              <p className="text-lg font-medium">{calculateFee()} SOL</p>
            </div>
            {connected ? (
              <button type="submit" className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-theme-bg bg-theme-text hover:bg-theme-text/80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-theme-text transition-all duration-300 ease-in-out">
              Create Token
              </button>
            ) : (
              <p className="bg-theme-bg text-theme-text rounded-lg shadow-md p-6 transition-colors duration-300 border-2">
                Please connect your wallet.
              </p>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}
