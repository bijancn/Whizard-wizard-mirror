// main31.cc is a part of the PYTHIA event generator.
// Copyright (C) 2015 Richard Corke, Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Example how to perform merging with PWOHEG-BOX events,
// based on the code found in include/Pythia8Plugins/PowhegHooks.h.

#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/PowhegHooks.h"
#include "Pythia8Plugins/HepMC2.h"
using namespace Pythia8;

//==========================================================================

int main() {

  // Generator
  Pythia pythia;

  // Load configuration file
  pythia.readFile("whizard_uu_powheg.cmnd");

  // Read in main settings
  int nEvent      = pythia.settings.mode("Main:numberOfEvents");
  int nError      = pythia.settings.mode("Main:timesAllowErrors");
  // Read in key POWHEG merging settings
  int vetoMode    = pythia.settings.mode("POWHEG:veto");
  int MPIvetoMode = pythia.settings.mode("POWHEG:MPIveto");
  bool loadHooks  = (vetoMode > 0 || MPIvetoMode > 0);

  // Add in user hooks for shower vetoing
  PowhegHooks *powhegHooks = NULL;
  loadHooks = true;
  if (loadHooks) {


    powhegHooks = new PowhegHooks();
    pythia.setUserHooksPtr((UserHooks *) powhegHooks);
  }
  // Set ISR and FSR to start at the kinematical limit
//  if (vetoMode > 0) {
//    pythia.readString("SpaceShower:pTmaxMatch = 0");
//    pythia.readString("TimeShower:pTmaxMatch = 0");
//    pythia.readString("TimeShower:pTmin = 0.5");
//    pythia.readString("TimeShower:alphaSvalue = 0.13");
//  }

  HepMC::Pythia8ToHepMC ToHepMC;
  HepMC::IO_GenEvent ascii_io("whizard_uu_powheg.hepmc", std::ios::out);

  // Initialise and list settings
  pythia.init();

  // Counters for number of ISR/FSR emissions vetoed
  unsigned long int nISRveto = 0, nFSRveto = 0;

  // Begin event loop; generate until nEvent events are processed
  // or end of LHEF file
  int iEvent = 0, iError = 0;
  while (true) {

    // Generate the next event
    if (!pythia.next()) {

      // If failure because reached end of file then exit event loop
      if (pythia.info.atEndOfFile()) break;

      // Otherwise count event failure and continue/exit as necessary
      cout << "Warning: event " << iEvent << " failed" << endl;
      if (++iError == nError) {
        cout << "Error: too many event failures.. exiting" << endl;
        break;
      }

      continue;
    }
      
    HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
    ToHepMC.fill_next_event(pythia, hepmcevt);

    ascii_io << hepmcevt;
    delete hepmcevt;


    /*
     * Process dependent checks and analysis may be inserted here
     */

    // Update ISR/FSR veto counters
    if (loadHooks) {
      nISRveto += powhegHooks->getNISRveto();
      nFSRveto += powhegHooks->getNFSRveto();
    }

    // If nEvent is set, check and exit loop if necessary
    ++iEvent;
    if (nEvent != 0 && iEvent == nEvent) break;

  } // End of event loop.

  // Statistics, histograms and veto information
  pythia.stat();
  cout << "Number of ISR emissions vetoed: " << nISRveto << endl;
  cout << "Number of FSR emissions vetoed: " << nFSRveto << endl;
  cout << endl;

  // Done.
  if (powhegHooks) delete powhegHooks;
  return 0;
}

