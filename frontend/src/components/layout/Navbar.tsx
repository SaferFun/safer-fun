"use client";
import { WalletMultiButton } from "@solana/wallet-adapter-react-ui";
import { useFont } from "../../contexts/FontContext";
import { useTheme } from "../../contexts/ThemeContext";
import Link from "next/link";
import { useWalletAuth } from "../../hooks/useWalletAuth";
import { useWallet } from "@solana/wallet-adapter-react";
import { useEffect } from "react";
import { SunDim, Moon } from "@phosphor-icons/react/dist/ssr";
import Image from "next/image";
import logoImg from "@/src/public/image/logo.png";

export default function Navbar() {
  const { isRoboto, toggleFont } = useFont();
  const { theme, toggleTheme } = useTheme();
  const { login, token } = useWalletAuth();
  const { connected } = useWallet();

  useEffect(() => {
    if (connected && !token) {
      login().catch(console.error);
    }
  }, [connected, token, login]);

  return (
    <div className="sticky top-0 z-50 bg-[var(--bg-color)] w-10/12 mx-auto">
      <div className="flex flex-row justify-between items-center w-full mx-auto p-4 border rounded-2xl mt-2 shadow-2xl">
        <div className="flex space-x-2">
          <Link href={"/"}>
            <Image
              src={logoImg}
              alt="logo"
              width={50}
              height={50}
              className="rounded-xl"
            />
          </Link>
          <button
            onClick={toggleFont}
            className="px-4 py-2 border border-[var(--text-color)] text-[var(--text-color)] rounded-xl hover:bg-gray-300 w-32"
          >
            {isRoboto ? "Use Fun" : "Use Normal"}
          </button>
          <button
            onClick={toggleTheme}
            className="px-4 py-2 border border-[var(--text-color)] text-[var(--text-color)] rounded-xl hover:bg-gray-300"
          >
            {theme === "light" ? (
              <Moon size={24} weight="thin" />
            ) : (
              <SunDim size={24} weight="thin" />
            )}
          </button>
        </div>
        <div className="flex flex-row gap-12">
          <Link href={"/"}>
            <p className="font-bold text-xl hover:underline decoration-purple-600 text-[var(--text-color)]">
              App
            </p>
          </Link>
          <Link href={"/create"}>
            <p className="font-bold text-xl hover:underline decoration-purple-600 text-[var(--text-color)]">
              Create
            </p>
          </Link>

          <Link href={"/team"}>
            <p className="font-bold text-xl hover:underline decoration-purple-600 text-[var(--text-color)]">
              Team
            </p>
          </Link>
        </div>
        <div className="flex items-center space-x-4">
          <WalletMultiButton
            style={{
              backgroundColor: "transparent",
              border: `1px solid var(--text-color)`,
              borderRadius: "12px",
              color: "var(--text-color)",
              fontFamily: "var(--font-indie-flower), cursive",
            }}
          />
          <Link href={"/"}>
            <Image
              src={logoImg}
              alt="logo"
              width={50}
              height={50}
              className="rounded-xl"
            />
          </Link>
        </div>
      </div>
    </div>
  );
}
