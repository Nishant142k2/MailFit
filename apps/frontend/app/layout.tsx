import type { Metadata } from "next"
import { Outfit } from "next/font/google"
import "./globals.css"

const outfit = Outfit({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  variable: "--font-primary",
})

export const metadata: Metadata = {
  title: {
    default: "MailFit",
    template: "%s • MailFit",
  },
  description: "Professionally crafted job emails that actually get replies.",
  metadataBase: new URL("https://mailfit.app"), // optional, safe to keep
  openGraph: {
    title: "MailFit",
    description: "Professionally crafted job emails that actually get replies.",
    type: "website",
  },
  icons: {
    icon: "/favicon.ico",
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`
          ${outfit.variable}
          antialiased
          bg-[var(--light)]
          text-[var(--dark)]
        `}
      >
        {children}
      </body>
    </html>
  )
}
