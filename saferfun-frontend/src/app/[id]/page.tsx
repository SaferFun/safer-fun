"use client";
import { useParams } from "next/navigation";
import { useState, useEffect, useCallback } from "react";
import AuctionDetails from "../../components/layout/AuctionDetails";
import AuctionAction from "../../components/layout/AuctionAction";
import TokenAllocation from "@/src/components/layout/TokenAllocation";
import CommentSection from "@/src/components/layout/CommentSection";
import TokenDetails from "@/src/components/layout/TokenDetails";
import unicornSolami from "@/src/public/image/unicornSolami.jpeg";
import escapeMatrix from "@/src/public/image/escapeMatrix.png";
import sashaWifHat from "@/src/public/image/sashaWifHat.jpeg";
import twoFaceDog from "@/src/public/image/twoFaceDog.jpeg";
import onFire from "@/src/public/image/onFire.jpeg";
import { StaticImageData } from "next/image";

type Token = {
  name: string;
  creator: string;
  endsIn: Date;
  totalLockedValue: string;
  totalBids: number;
  description: string;
  symbol: string;
  users: {
    walletAddress: string;
    reservedToken: number;
    lockedSize: number;
    bidSize: number;
    auctionScore: number;
  }[];
  lockedAmount?: number;
  auctionPoint?: number;
  dateCreated?: string;
  auctionPointDetails?: string;
  image: StaticImageData;
};

// Extended mock data
const tokens: { [key: number]: Token } = {
  1: {
    name: "vega",
    creator: "DVviKYPAMwBLfKiYvw6USkRjTE3cm6mnqxrip614tYNX",
    endsIn: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000),
    totalLockedValue: "100 SOL",
    totalBids: 15,
    symbol: "$VGA",
    description: "vega is the brightest star in the universe.",
    users: [
      {
        walletAddress: "DVviKYPAMwBLfKiYvw6USkRjTE3cm6mnqxrip614tYNX",
        reservedToken: 1000,
        lockedSize: 50,
        bidSize: 0,
        auctionScore: 0,
      },
      {
        walletAddress: "7fEH4hR2Dh3Yut74Rq5QCwJ8gfoFK5bMdqcjqtpojv9k",
        reservedToken: 800,
        lockedSize: 30,
        bidSize: 8,
        auctionScore: 90,

      },
      {
        walletAddress: "9gKL6mT5Fm4Xvt96Ss7RCzN9hifGK7bPeqcjqtpojv0m",
        reservedToken: 100,
        lockedSize: 5,
        bidSize: 2,
        auctionScore: 80,

      },
      {
        walletAddress: "2hJN8nU6Kp5Zvw85Tt9RDzQ0hjeHK8bQeqcjqtpojv1n",
        reservedToken: 90,
        lockedSize: 4.5,
        bidSize: 2,
        auctionScore: 60,

      },
      {
        walletAddress: "3kNM9oW8Lp7Zyw96Vv1SDzS2hjfJK0bTeqcjqtpojv3q",
        reservedToken: 100,
        lockedSize: 10,
        bidSize: 3,
        auctionScore: 55,

      },
      {
        walletAddress: "1iQR0pX9Nq8Yxw63Ww2TDzU4hlfLK1bVeqcjqtpojv4r",
        reservedToken: 1,
        lockedSize: 0.5,
        bidSize: 0.05,
        auctionScore: 5,
      },
    ],
    image: onFire,
  },
  2: {
    name: "Unicorn Solami Donut Cat",
    symbol: "$USD",
    creator: "BzDt7eayDwhiGFfW7C58qKHPg7zvj2J6cTpf26fW421B",
    endsIn: new Date(Date.now() + 5*24 * 60 * 60 * 1000),
    totalLockedValue: "10 SOL",
    totalBids: 0.5,
    description: "mmm food...",
    users: [
      {
        walletAddress: "BzDt7eayDwhiGFfW7C58qKHPg7zvj2J6cTpf26fW421B",
        reservedToken: 120,
        lockedSize: 7,
        bidSize: 900,
        auctionScore: 113,
      },
      {
        walletAddress: "2hJN8nU6Kp5Zvw85Tt9RDzQ0hjeHK8bQeqcjqtpojv1n",
        reservedToken: 10,
        lockedSize: 1,
        bidSize: 0.25,
        auctionScore: 90,
      },
      {
        walletAddress: "3kNM9oW8Lp7Zyw96Vv1SDzS2hjfJK0bTeqcjqtpojv3q",
        reservedToken: 20,
        lockedSize: 0.5,
        bidSize: 0.1,
        auctionScore: 64,
      },
      {
        walletAddress: "1iQR0pX9Nq8Yxw63Ww2TDzU4hlfLK1bVeqcjqtpojv4r",
        reservedToken: 8,
        lockedSize: 0.2,
        bidSize: 0.05,
        auctionScore: 40,
      },
      {
        walletAddress: "5e5fE4hE3Ch2zut62Eq4QDwH7foEK4bNcqcjqtpojv8j",
        reservedToken: 6,
        lockedSize: 0.3,
        bidSize: 0.05,
        auctionScore: 35,
      },
      {
        walletAddress: "7fEH4hR2Dh3Yut74Rq5QCwJ8gfoFK5bMdqcjqtpojv9k",
        reservedToken: 30,
        lockedSize: 1,
        bidSize: 0.05,
        auctionScore: 5,
      },
    ],
    image: unicornSolami,
  },
  3: {
    name: "Escape the Matrix",
    creator: "6WmH8NjaC3wq9hZ3qeh72cQRtsL5ZziKLTr9xn2BDmVP",
    endsIn: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    totalLockedValue: "20 SOL",
    totalBids: 2,
    symbol: "$ETM",
    description: "i love tacos.",
    users: [
      {
        walletAddress: "6WmH8NjaC3wq9hZ3qeh72cQRtsL5ZziKLTr9xn2BDmVP",
        reservedToken: 800,
        lockedSize: 10,
        bidSize: 375,
        auctionScore: 70,
      },
      {
        walletAddress: "1iQR0pX9Nq8Yxw63Ww2TDzU4hlfLK1bVeqcjqtpojv4r",
        reservedToken: 700,
        lockedSize: 10,
        bidSize: 2,
        auctionScore: 428,
      },
    ],
    image: escapeMatrix,
  },
  4: {
    name: "SashaWifHat",
    creator: "8mPQ7rT4Gp9Zvu85Xx3UDzV6hibMK2bSeqcjqtpojv5s",
    endsIn: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    totalLockedValue: "5 SOL",
    totalBids: 0.1,
    symbol: "$SWH",
    description: "some meme desc.",
    users: [
      {
        walletAddress: "8mPQ7rT4Gp9Zvu85Xx3UDzV6hibMK2bSeqcjqtpojv5s",
        reservedToken: 150,
        lockedSize: 3,
        bidSize: 1125,
        auctionScore: 95,
      },
      {
        walletAddress: "6kRS6qW2Jp0Ywv74Yy4VDzX8hjeNK3bTeqcjqtpojv6t",
        reservedToken: 100,
        lockedSize: 2,
        bidSize: 0.1,
        auctionScore: 88,
      },
    ],
    image: sashaWifHat,
  },
  5: {
    name: "Two Face Dog",
    creator: "2Z2W9smAKPLSwYXAnardAPfHgZhWRES1pW3rmtRjk3Mh",
    endsIn: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
    totalLockedValue: "30 SOL",
    totalBids: 5,
    symbol: "$TFD",
    description: "very meme stuff.",
    users: [
      {
        walletAddress: "2Z2W9smAKPLSwYXAnardAPfHgZhWRES1pW3rmtRjk3Mh",
        reservedToken: 10,
        lockedSize: 1,
        bidSize: 1,
        auctionScore: 98,
      },
      {
        walletAddress: "2hJN8nU6Kp5Zvw85Tt9RDzQ0hjeHK8bQeqcjqtpojv1n",
        reservedToken: 120,
        lockedSize: 29,
        bidSize: 5,
        auctionScore: 822,
      },
    ],
    image: twoFaceDog,
  },
};

export default function TokenPage() {
  const params = useParams();
  const mintAddress = params.id as string;
  const [token, setToken] = useState<Token | null>(null);
  const [orders, setOrders] = useState<any[]>([]);
  const [comments, setComments] = useState<any[]>([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await fetch("https://saferfun-backend-production.up.railway.app/orders"); // Adjust the URL as needed
        if (!response.ok) {
          throw new Error('Failed to fetch orders');
        }
        let data = await response.json();
        data = data.map((order: any) => {
          console.log(order.endsAt);
          
          return {
            ...order,
            totalBids: order.users.reduce((acc: number, user: any) => acc + user.bidSize, 0),
            totalLockedValue: order.users.reduce((acc: number, user: any) => acc + user.lockedSize, 0),
            endsIn: new Date(order.endsAt).getTime() ,
            image:order.imageUrl

          };
        });
        const allData  = data.concat(Object.values(tokens));
        
        const foundToken =allData.find(
          (t:any) => t.creator === mintAddress,
        );


        setToken(foundToken || null);
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    };

    fetchOrders();
   
  }, [mintAddress]);

  const fetchComments = useCallback(async () => {
    if (!token) return;
    try {
      const response = await fetch(
        `https://saferfun-backend-production.up.railway.app/comments/${token.creator}`,
      );
      const data = await response.json();
      setComments(data);
    } catch (error) {
      console.error("Error fetching comments:", error);
    }
  }, [token]);

  useEffect(() => {
    fetchComments();
  }, [fetchComments]);

  if (!token) {
    return <div>Token not found</div>;
  }

  return (
    <div className="container flex flex-row mx-auto px-4 py-8 min-h-screen bg-notebook-squares bg-theme-bg text-theme-text transition-colors duration-300 gap-8">
      <div className="flex flex-col w-3/4 gap-8">
        <TokenAllocation symbol={token.symbol} allocations={token.users} />
        <CommentSection
          comments={comments}
          coinId={token.creator}
          refreshComments={fetchComments}
        />
      </div>
      <div className="flex flex-col w-1/4 gap-8">
        <TokenDetails 
          totalBids={`${token.totalBids} SOL`} 
          totalLockedValue={
        typeof token.totalLockedValue === 'number' 
          ? `${token.totalLockedValue} SOL` 
          : token.totalLockedValue
          } 
          name={token.name} 
          endsIn={token.endsIn} 
        />
        <AuctionAction devWalletAddress={token.creator} />
        <AuctionDetails
          createdBy={token.creator}
          name={token.name}
          description={token.description}
          image={token.image}
        />
      </div>
    </div>
  );
}
