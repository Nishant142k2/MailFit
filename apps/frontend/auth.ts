import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"

export const { auth, handlers } = NextAuth({
  providers: [
    Credentials({
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email) return null

        // your logic
        return {
          id: "1",
          email: credentials.email,
          firstName: "Test",
          lastName: "User",
          userid: "u1",
          access_token: "token",
        }
      },
    }),
  ],
  session: { strategy: "jwt" },
})
