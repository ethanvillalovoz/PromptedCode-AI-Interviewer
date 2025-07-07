import "react"
import { SignIn, SignUp, SignedIn, SignedOut } from "@clerk/clerk-react"

// AuthenticationPage handles user sign-in and sign-up using Clerk
export function AuthenticationPage() {
  return (
    <div className="auth-container">
      {/* Show sign-in and sign-up forms if the user is signed out */}
      <SignedOut>
        <SignIn path="/sign-in" routing="path" />
        <SignUp path="/sign-up" routing="path" />
      </SignedOut>
      {/* Show a message if the user is already signed in */}
      <SignedIn>
        <div className="redirect-message">
          <p>You are signed in!</p>
        </div>
      </SignedIn>
    </div>
  )
}