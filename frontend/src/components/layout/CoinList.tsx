import { useState, useEffect } from "react";
import CoinCard from "../ui/CoinCard";
import CoinSearch from "../ui/CoinSearch";
import unicornSolami from "../../public/image/unicornSolami.jpeg";
import escapeMatrix from "../../public/image/escapeMatrix.png";
import sashaWifHat from "../../public/image/sashaWifHat.jpeg";
import twoFaceDog from "../../public/image/twoFaceDog.jpeg";

// Placeholder coin data
const placeholderCoins = [
  {
    mintAddress: "BzDt7eayDwhiGFfW7C58qKHPg7zvj2J6cTpf26fW421B",
    name: "Unicorn Solami Donut Cat",
    createdBy: "BzDt7eayDwhiGFfW7C58qKHPg7zvj2J6cTpf26fW421B",
    endsIn: "5 Days",
    totalLockedValue: "10 SOL",
    totalBids: "0.5 SOL",
    description: "mmm food...",
    image: unicornSolami,
  },
  {
    mintAddress: "6WmH8NjaC3wq9hZ3qeh72cQRtsL5ZziKLTr9xn2BDmVP",
    name: "Escape the Matrix",
    createdBy: "6WmH8NjaC3wq9hZ3qeh72cQRtsL5ZziKLTr9xn2BDmVP",
    endsIn: "1 week",
    totalLockedValue: "20 SOL",
    totalBids: "2 SOL",
    description: "i love tacos.",
    image: escapeMatrix,
  },
  {
    mintAddress: "8mPQ7rT4Gp9Zvu85Xx3UDzV6hibMK2bSeqcjqtpojv5s",
    name: "SashaWifHat",
    createdBy: "8mPQ7rT4Gp9Zvu85Xx3UDzV6hibMK2bSeqcjqtpojv5s",
    endsIn: "Finished",
    totalLockedValue: "5 SOL",
    totalBids: "0.1 SOL",
    description: "some meme desc.",
    image: sashaWifHat,
  },
  {
    mintAddress: "2Z2W9smAKPLSwYXAnardAPfHgZhWRES1pW3rmtRjk3Mh",
    name: "Two Face Dog",
    createdBy: "2Z2W9smAKPLSwYXAnardAPfHgZhWRES1pW3rmtRjk3Mh",
    endsIn: "Finished",
    totalLockedValue: "30 SOL",
    totalBids: "5 SOL",
    description: "very meme stuff.",
    image: twoFaceDog,
  },
];

export default function CoinListLayout() {
  const [searchQuery, setSearchQuery] = useState("");
  const [orders, setOrders] = useState([]);

  // Fetch orders from backend
  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await fetch("https://saferfun-backend-production.up.railway.app/orders"); // Adjust the URL as needed
        if (!response.ok) {
          throw new Error('Failed to fetch orders');
        }
        const data = await response.json();
        setOrders(data);
        
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    };

    fetchOrders();
  }, []);

  const calculateEndsIn = (createdAt:any, endsAt:any) => {
    const diffMs = new Date(endsAt).getTime() - new Date(createdAt).getTime();
  
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
  
    if (diffDays > 0) {
      return `${diffDays} Day${diffDays > 1 ? 's' : ''}`;
    } else if (diffHours > 0) {
      return `${diffHours} Hour${diffHours > 1 ? 's' : ''}`;
    } else {
      return `${diffMinutes} Minute${diffMinutes > 1 ? 's' : ''}`;
    }
  };

  // Combine fetched orders with placeholder coins

  const allCoins = [
    ...orders.map((order:any) => ({
      mintAddress: order.creator,
      name: order.name,
      createdBy: order.creator,
      endsIn:  calculateEndsIn(order.createdAt, order.endsAt),
      totalLockedValue: order.users.reduce(
        (acc:any, user:any) => acc + user.lockedSize,
        0
      ),
      totalBids: order.users.reduce(
        (acc:any, user:any) => acc + user.bidSize,
        0
      ),
      description: order.description,
      image: order.imageUrl, 
    })),
    ...placeholderCoins,
  ];

  return (
    <div className="container mx-auto p-4 border rounded-2xl bg-theme-bg text-theme-text transition-colors duration-300">
      <CoinSearch onSearch={setSearchQuery} />
      <div className="h-[400px] overflow-y-auto">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {allCoins.map((coin) => (
            <CoinCard
              key={coin.mintAddress}
              mintAddress={coin.mintAddress}
              name={coin.name}
              createdBy={coin.createdBy}
              endsIn={coin.endsIn}
              totalLockedValue={coin.totalLockedValue}
              totalBids={coin.totalBids}
              description={coin.description}
              image={coin.image}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
