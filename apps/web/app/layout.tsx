import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MIZAN CORE | لوحة الحوكمة",
  description: "نواة حوكمة مستقلة — الدليل قبل الاستنتاج، ولا سلطة إلا للمعنى."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
