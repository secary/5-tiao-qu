import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "5 条区",
  description: "可信、可追溯的桌游规则查询助手"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
