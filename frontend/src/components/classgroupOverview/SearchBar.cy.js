import SearchBar from './SearchBar.vue'

describe('<SearchBar />', () => {
  it('renders the field', () => {
    cy.mount(SearchBar, {
      props: {
        modelValue: '',
      },
    })

    cy.get('input').should('exist')
    cy.get('input').should('have.value', '')
  })

  it('emits update:modelValue when typing', () => {
    const onUpdateModelValue = cy.stub().as('updateModelValue')

    cy.mount(SearchBar, {
      props: {
        modelValue: '',
        'onUpdate:modelValue': onUpdateModelValue,
      },
    })

    cy.get('input')
      .type('test')
      .then(() => {
        cy.get('@updateModelValue').should('have.been.calledWith', 't')
        cy.get('@updateModelValue').should('have.been.calledWith', 'te')
        cy.get('@updateModelValue').should('have.been.calledWith', 'tes')
        cy.get('@updateModelValue').should('have.been.calledWith', 'test')
      })
  })

  it('shows the correct placeholder', () => {
    cy.mount(SearchBar, {
      props: {
        modelValue: '',
      },
    })

    cy.get('input').should('have.attr', 'placeholder', 'Search classgroups or students...')
  })
})
