import Navbar from './Navbar.vue'

describe('<Navbar />', () => {
  it('renders', () => {
    // see: https://on.cypress.io/mounting-vue
    cy.mount(Navbar)
  })
})