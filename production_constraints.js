describe('Platform navigation if steam is not linked', () => {

    // checks that there's no transition to predictons page if Steam account isn't linked
    // checks that there's no abilty to accept challenge if steam isn't linked

    beforeEach('Logins User', () => {
        cy.loginUser(/*url, login, password here*/);
    }) 

    it('Checks no thansition to predictions page', () => {


        cy.contains('Make a prediction').click();
        cy.location('pathname').should('eq', '/predictions');
        cy.get('header').children('a').contains('About').should('have.class', '!text-blueWhite');

        cy.get('button').contains('Go to predictions page').click();
        cy.get('h6').then((elem) => {
            let textOfElem = elem.text();
            expect(textOfElem).to.equal('Verify account');
        })
        cy.contains('Before you start add your Dota 2 account to GameGreed').should('be.visible');
        cy.contains('Sign up with Steam').should('be.visible');
        cy.contains('Go back').should('be.visible');
        cy.contains('Go back').click();

        cy.contains('Leader board').parents('div[class="css-s7vchs-cardContainer"]').find('button').contains('Go to predictions page').click();

        cy.get('h6').then((elem) => {
            let textOfElem = elem.text();
            expect(textOfElem).to.equal('Verify account');
        })
        cy.contains('Before you start add your Dota 2 account to GameGreed').should('be.visible');
        cy.contains('Sign up with Steam').should('be.visible');
        cy.contains('Go back').should('be.visible');
        cy.contains('Go back').click();
        cy.location('pathname').should('eq', '/predictions');

    })

    it('Checks no challenge acceptance with no steam linked', () => {

        cy.contains('Take a challenge').click();
        cy.contains('Go to challenge list').click();
        cy.location('pathname').should('eq', '/challenges/challengeList');

        cy.contains('Open', { timeout: 10000 }).click();
        cy.contains('Accept Challenge', { timeout: 5000 }).click();

        cy.get('h6').contains('Verify account').should('be.visible');
        cy.get('div').contains('Before you start add your Dota 2 account to GameGreed').should('be.visible');
        cy.get('button').contains('Sign up with Steam').should('be.visible');
        cy.get('button').contains('Go back').should('be.visible');
        cy.get('button').contains('Go back').click();
    })
})