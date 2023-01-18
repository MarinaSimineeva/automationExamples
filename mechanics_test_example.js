import { navigateTo } from '../support/page_objects/navigation_left';
import { tabTo } from '../support/page_objects/navigation_top';
import { predictions } from '../support/page_objects/predictions';

describe('Checks predictions functionality', () => {

  beforeEach('Set up', () => {
    cy.loginUser(/*url, login, password*/)

  })


  it('Checks if no prediction was made', () => {

    cy.intercept('GET', /*url*/, {fixture: 'predictionActiveNone.json'});
    cy.intercept('GET', /*url*/).as('matches');

    navigateTo.predictionsPage();
    tabTo.predictions();
    cy.wait(2000);

    cy.fixture('predictionActiveNone.json').then(resp => {
      cy.wait('@matches').its('response.body').then((matches) => {
        let totalMatches = Number(matches['total']);

          // checks prediction block appearance
          predictions.statusNone();

          // adding a match
          cy.add_match(413463215, true);
          let newTotal;


          for (let i = 0; i < 3; i++) {
            cy.intercept(/*url*/).as('newMatches');
            cy.reload();
            let breakable = false;
            cy.wait('@newMatches').its('response.body').then((body) => {
              newTotal = body.total;

              // asserts the content of the added match in matches table
              if (totalMatches !== newTotal) {
                predictions.matchDataCheck(body);
                cy.wait(2000);
                predictions.statusNone();
                breakable = true;
                return;

              }
              else {
                cy.wait(30000);
                cy.reload();
              }

            })
            if (breakable) {
              break;
            }
          
        }

      })
    });
  });

  it.only('Checks if prediction was made', () => {
    cy.intercept('GET', /*url*/, {fixture: 'predictionActiveWin.json'});
    cy.intercept('GET', /*url*/).as('matches');

    navigateTo.predictionsPage();
    tabTo.predictions();
    cy.wait(2000);

    cy.fixture('predictionActiveWin.json').then(resp => {
      cy.wait('@matches').its('response.body').then((matches) => {
        let totalMatches = Number(matches['total']);

          // checks prediction block appearance
          predictions.statusActiveWin();

          // adding a match
          cy.add_match(413463215, true);
          let newTotal;


          for (let i = 0; i < 3; i++) {
            cy.intercept(/*url goes here*/).as('newMatches');
            cy.reload();
            let breakable = false;
            cy.wait('@newMatches').its('response.body').then((body) => {
              newTotal = body.total;

              // asserts the content of the added match in matches table
              if (totalMatches !== newTotal) {
                predictions.matchDataCheck(body);
                cy.wait(2000);
                predictions.statusActiveWin();
                breakable = true;
                return;

              }
              else {
                cy.wait(30000);
                cy.reload();
              }

            })
            if (breakable) {
              break;
            }
          
        }
    })

  })

})
})
