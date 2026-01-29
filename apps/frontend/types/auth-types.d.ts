import NextAuth from "next-auth"
import { JWT } from "next-auth/jwt"

declare module "next-auth" {
  interface Session {
    user: {
      id: string
      email: string
      firstName: string
      lastName: string
      userid: string
      access_token: string
    }
  }

  interface User {
    id: string
    email: string
    firstName: string
    lastName: string
    userid: string
    access_token: string
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    id: string
    email: string
    firstName: string
    lastName: string
    userid: string
    access_token: string
  }
}