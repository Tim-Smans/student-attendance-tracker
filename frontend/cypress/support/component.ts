// cypress/support/component.ts

import { mount } from 'cypress/vue'

// Declare mount as a Cypress command
declare global {
  namespace Cypress {
    interface Chainable {
      mount: typeof mount
    }
  }
}

// Voeg mount toe aan Cypress
Cypress.Commands.add('mount', mount)

// (optioneel) Styles importeren
// import '../../src/style.css'  // indien je globale styles hebt
