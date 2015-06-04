// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/Thrust.hh"
/// @todo Include more projections as required, e.g. ChargedFinalState, FastJets, ZFinder...

namespace Rivet {

  using namespace Cuts;

  class WHIZARD_2015_NLO : public Analysis {
  public:

    /// Constructor
    WHIZARD_2015_NLO()
      : Analysis("WHIZARD_2015_NLO")
    {    }

    /// Book histograms and initialise projections before the run
    void init() {
      // Projections
      addProjection(ChargedFinalState(), "CFS");
      const FinalState fs;
      addProjection(fs, "FS");
      const Thrust thrust(fs);
      addProjection(thrust, "Thrust");

      _h_Quark_Pt = bookHisto1D("q-pT", 75, 0., 260.);
      _h_Aquark_Pt = bookHisto1D("qbar-pT", 75, 0., 260.);
      _h_Wp_Pt = bookHisto1D("W_plus-pT", 50, 0., 210. );
      _h_B_Pt = bookHisto1D("B-pT", 50, 0., 170.);

      _h_BB_invMass = bookHisto1D("BB-inv", 50, 0., 350.);
      _h_WW_invMass = bookHisto1D("WW-inv", 50, 150, 450.);

      _h_Quark_E = bookHisto1D("q-E", 50, 0, 260.);
      _h_Aquark_E = bookHisto1D("qbar-E", 75, 0., 260.);

      _h_Quark_Phi = bookHisto1D("q-Phi", 75, 0, TWOPI);
      _h_Aquark_Phi = bookHisto1D("qbar-Phi", 75, 0, TWOPI);

      _h_Quark_Rapidity = bookHisto1D("q-Rapidity", 75, -5, 5);
      _h_Aquark_Rapidity = bookHisto1D("qbar-Rapidity", 75, -5, 5);

      _h_Thrust = bookHisto1D("Thrust", 75, 0, 0.45);
      _h_ThrustMajor = bookHisto1D("ThrustMajor", 75, 0, 0.7);
      _h_ThrustMinor = bookHisto1D("ThrustMinor", 75, 0, 0.6);
      _h_Oblateness = bookHisto1D("Oblateness", 75, 0, 0.6);

      n_events = 0;
      n_photons = 0;

      //_histEta    = bookHisto1D("Eta", 50, -5, 5);
    }

    /// Perform the per-event analysis
    void analyze(const Event& event) {

      // Get event weight for histo filling
      double weight = event.weight();

      const FinalState& fs = applyProjection<FinalState>(event, "FS");
      if (fs.particles().size() < 2) {
        cout << "Less than two final state particles in the event";
        vetoEvent;
      }

      n_events++;

      double xval, yval, xerr, yerr, gl_fraction;
      /// const double roots = 2 * lepton_energy;
      const double roots = 300;
      xval = 0.0; yval = 0.0;
      xerr = 0.0; yerr = 0.0;
      const Thrust& thrust = applyProjection<Thrust>(event, "Thrust");
      _h_Thrust->fill(1-thrust.thrust(), weight);
      _h_ThrustMajor->fill(thrust.thrustMajor(), weight);
      _h_ThrustMinor->fill(thrust.thrustMinor(), weight);
      _h_Oblateness->fill(thrust.oblateness(), weight);

      foreach (const Particle& p, fs.particles()) {
        int id = p.pid();
//	if (weight < -10.0) cout << "Excess weight: " << weight << endl;
        // x and y are energy fractions and are in [0,1]
        MSG_DEBUG("ID = " << id);
        if(id == PID::UQUARK || id == PID::TQUARK) {
          xval = p.E()/roots;
          _h_Quark_Pt->fill(p.pT()/GeV, weight);
          _h_Quark_E->fill(p.E()/GeV, weight);
          _h_Quark_Phi->fill(p.phi(), weight);
          _h_Quark_Rapidity->fill(p.rapidity(), weight);
        } else if(id == - PID::UQUARK || id == - PID::TQUARK) {
          yval = p.E()/roots;
          _h_Aquark_Pt->fill(p.pT()/GeV, weight);
          _h_Aquark_E->fill(p.E()/GeV, weight);
          _h_Aquark_Phi->fill(p.phi(), weight);
          _h_Aquark_Rapidity->fill(p.rapidity(), weight);
       } else if(id == PID::WPLUSBOSON) {
	  _h_Wp_Pt->fill(p.pT()/GeV, weight);
       } else if(id == PID::BQUARK) {
	  _h_B_Pt->fill(p.pT()/GeV, weight);
       }
     //Compute invariant mass
     foreach (const Particle& p1, fs.particles()) {
	     foreach (const Particle& p2, fs.particles()) {
	     int id1 = p1.pid(); int id2 = p2.pid();
	     if (id1 == PID::BQUARK && id2 == -PID::BQUARK) {
	             FourMomentum p_sum = p1.momentum() + p2.momentum();
		     _h_BB_invMass->fill(p_sum.mass(), weight);
	     } else if (id1 == PID::WPLUSBOSON && id2 == PID::WMINUSBOSON) {
		     FourMomentum p_sum = p1.momentum() + p2.momentum();
		     _h_WW_invMass->fill(p_sum.mass(), weight);
             }
	 }
       }
    }
    }


    /// Normalise histograms etc., after the run
    void finalize() {
      /// @todo Normalise, scale and otherwise manipulate histograms here
      // scale(_h_YYYY, crossSection()/sumOfWeights()); // norm to cross section
      // normalize(_h_YYYY); // normalize to unity

      cout << "Processed " << n_events << " events" << endl;
      cout << "Sum of weights: " << sumOfWeights () << endl;
      scale(_h_Quark_Pt, 1./ abs(sumOfWeights()));
      scale(_h_Aquark_Pt, 1./abs(sumOfWeights()));
      scale(_h_Wp_Pt, crossSection()/sumOfWeights());
      scale(_h_B_Pt, crossSection()/sumOfWeights());
      scale(_h_BB_invMass, crossSection()/sumOfWeights());
      scale(_h_WW_invMass, crossSection()/sumOfWeights());

      scale(_h_Quark_E, 1./sumOfWeights());
      scale(_h_Aquark_E, 1./sumOfWeights());

      scale(_h_Quark_Phi, 1./sumOfWeights());
      scale(_h_Aquark_Phi, 1./sumOfWeights());

      scale(_h_Quark_Rapidity, 1./sumOfWeights());
      scale(_h_Aquark_Rapidity, 1./sumOfWeights());

      scale(_h_Thrust, 1./sumOfWeights());
      scale(_h_ThrustMajor, 1./sumOfWeights());
      scale(_h_ThrustMinor, 1./sumOfWeights());
      scale(_h_Oblateness, 1./sumOfWeights());

    }


  private:

    // Data members like post-cuts event weight counters go here
    Histo1DPtr _h_Quark_Pt;
    Histo1DPtr _h_Aquark_Pt;
    Histo1DPtr _h_Wp_Pt;
    Histo1DPtr _h_B_Pt;
    Histo1DPtr _h_BB_invMass;
    Histo1DPtr _h_WW_invMass;

    Histo1DPtr _h_Quark_E;
    Histo1DPtr _h_Aquark_E;

    Histo1DPtr _h_Quark_Phi;
    Histo1DPtr _h_Aquark_Phi;

    Histo1DPtr _h_Quark_Rapidity;
    Histo1DPtr _h_Aquark_Rapidity;

    Histo1DPtr _h_Thrust;
    Histo1DPtr _h_ThrustMajor;
    Histo1DPtr _h_ThrustMinor;
    Histo1DPtr _h_Oblateness;

    int n_events, n_photons;

  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(WHIZARD_2015_NLO);

}
