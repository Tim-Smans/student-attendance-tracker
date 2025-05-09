import { defineStore } from 'pinia'
import { decodeCredential } from 'vue3-google-login'

interface GoogleUser {
  name: string
  email: string
  picture: string
  given_name: string
  hd?: string
  [key: string]: any
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as any
  }),
  actions: {
    loginWithGoogle(credential: string) {
      const decodedCredentials = decodeCredential(credential) as GoogleUser
      console.log(decodedCredentials)
      try{
        if (!decodedCredentials.hd || decodedCredentials.hd !== 'metropolia.fi') {
          console.log('Tried loggin in with a non-metropolia account.')
          return
        }
        this.user = decodedCredentials
      }catch{
        console.log('Something went wrong while loggin in.')
      }
    },
    logout() {
      this.user = null
    },
    isAuthenticated(): boolean {
      return !!this.user
    }
  }
})
