// main02.cc is a part of the PYTHIA event generator.
// Copyright (C) 2015 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// This is a simple test program. It fits on one slide in a talk.
// It studies the pT_Z spectrum at the Tevatron.

#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC2.h"
using namespace Pythia8;
int main() {
  int n_branchings;
  int n_events; 
  n_events = 10000;
  // Generator. Process selection. Tevatron initialization. Histogram.
  Pythia pythia;
  pythia.readString("Beams:idA = -11");
  pythia.readString("Beams:idB = 11");
  pythia.readString("Beams:frameType = 4");
  pythia.readString("Beams:LHEF = test.lhe");
  pythia.readString("ProcessLevel:all = off");
  pythia.readString("PartonLevel:all = off");
//  pythia.readString("HadronLevel:all = off");
  pythia.readString("HadronLevel:Hadronize = off");
  pythia.readString("HadronLevel:Decay = off");
  pythia.readString("HadronLevel:BoseEinstein = off");
  pythia.readString("Check:event = off");
  pythia.readString("SigmaProcess:alphaSvalue = 0.1178");
  pythia.readString("TimeShower:pTmin = 1.0");
//Switch off photon emissions (?)
  pythia.readString("StandardModel:alphaEM0 = 0.0");
  pdthia.readString("StandardModel:alphaEMmZ = 0.0");

  HepMC::Pythia8ToHepMC ToHepMC;
  HepMC::IO_GenEvent ascii_io("Test_hepmc_no_emission", std::ios::out);

  pythia.init();
  for (int iEvent = 0; iEvent < n_events; ++iEvent) {
     pythia.next ();
// Unless this values are set, there will be no emissions
     pythia.event[3].scale(500.0);
     pythia.event[4].scale(500.0);
// Performs splitting
     n_branchings = pythia.forceTimeShower (3,4,10000.0,1);
     HepMC::GenEvent* hepmcevt = new HepMC::GenEvent();
     ToHepMC.fill_next_event(pythia, hepmcevt);

     ascii_io << hepmcevt;
     delete hepmcevt;

  }
  return 0;
}
