import { useWallet } from "@solana/wallet-adapter-react";
import { useState, useCallback } from "react";
import Cookies from "js-cookie";
export const useWalletAuth = () => {
  const { publicKey, signMessage } = useWallet();
  const [token, setToken] = useState<string | null>(null);

  const login = useCallback(async () => {
    if (!publicKey || !signMessage) {
      throw new Error("Wallet not connected");
    }

    try {
      
      // Get the encrypted message from the server
      const messageResponse = await fetch("https://saferfun-backend-production.up.railway.app/auth/message");
      const { auth_message: encryptedMessage } = await messageResponse.json();

      console.log("Encrypted message received:", encryptedMessage);

      // Sign the encrypted message
      const messageUint8 = new TextEncoder().encode(encryptedMessage);
      const signedMessage = await signMessage(messageUint8);

      console.log(
        "Signed message:",
        Buffer.from(signedMessage).toString("base64"),
      );

      const response = await fetch("https://saferfun-backend-production.up.railway.app/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          walletAddress: publicKey.toBase58(),
          signedMessage: Buffer.from(signedMessage).toString("base64"),
          encryptedMessage: encryptedMessage,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Login failed:", response.status, errorText);
        throw new Error(`Login failed: ${response.status} ${errorText}`);
      }

      const { access_token } = await response.json();
      Cookies.set("jwt_token", access_token, { expires: 1 });
      setToken(access_token);
      return access_token;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  }, [publicKey, signMessage]);

  // Function to get the token from cookie
  const getTokenFromCookie = useCallback(() => {
    return Cookies.get("jwt_token") || null;
  }, []);

  const logout = useCallback(() => {
    Cookies.remove("jwt_token");
    setToken(null);
  }, []);

  return { login, token, getTokenFromCookie, logout };
};
