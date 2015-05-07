// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/Sphericity.hh"
#include "Rivet/Projections/Thrust.hh"
/// @todo Include more projections as required, e.g. ChargedFinalState, FastJets, ZFinder...

namespace Rivet {

  using namespace Cuts;

  class WHIZARD_2015_SINGLEEMISSION : public Analysis {
  public:

    /// Constructor
    WHIZARD_2015_SINGLEEMISSION()
      : Analysis("WHIZARD_2015_SINGLEEMISSION")
    {    }

    /// Book histograms and initialise projections before the run
    void init() {
      // Projections
      addProjection(ChargedFinalState(), "CFS");
      const FinalState fs;
      addProjection(fs, "FS");
      const Thrust thrust(fs);
      addProjection(thrust, "Thrust");
      addProjection(Sphericity(fs), "Sphericity");

      _h_Quark_Pt = bookHisto1D("q-pT", 30, 0., 260.);
      _h_Aquark_Pt = bookHisto1D("qbar-pT", 30, 0., 260.);
      _h_Gluon_Pt = bookHisto1D("gluon-pT", 30, 0., 260.);

      _h_Quark_E = bookHisto1D("q-E", 30, 0, 260.);
      _h_Aquark_E = bookHisto1D("qbar-E", 30, 0., 260.);
      _h_Gluon_E = bookHisto1D("gluon-E", 30, 0., 260.);

      _h_Quark_Phi = bookHisto1D("q-Phi", 30, 0, TWOPI);
      _h_Aquark_Phi = bookHisto1D("qbar-Phi", 30, 0, TWOPI);
      _h_Gluon_Phi = bookHisto1D("gluon-Phi", 30, 0, TWOPI);

      _h_Quark_Rapidity = bookHisto1D("q-Rapidity", 30, -5, 5);
      _h_Aquark_Rapidity = bookHisto1D("qbar-Rapidity", 30, -5, 5);
      _h_Gluon_Rapidity = bookHisto1D("gluon-Rapidity", 30, -5, 5);

      _h_Thrust = bookHisto1D("Thrust", 30, 0, 0.45);
      _h_ThrustMajor = bookHisto1D("ThrustMajor", 30, 0, 0.7);
      _h_ThrustMinor = bookHisto1D("ThrustMinor", 30, 0, 0.6);
      _h_Oblateness = bookHisto1D("Oblateness", 30, 0, 0.6);
      _h_Sphericity = bookHisto1D("Sphericity", 30, 0, 0.8);
      _h_Aplanarity = bookHisto1D("Aplanarity", 30, 0, 0.3);
      _h_Planarity = bookHisto1D("Planarity", 30, 0, 0.5);
//      _h_xy = bookScatter2D("xy");

      n_events = 0;
      n_photons = 0;

      //_histEta    = bookHisto1D("Eta", 30, -5, 5);
    }

    /// Perform the per-event analysis
    void analyze(const Event& event) {

      // Get event weight for histo filling
      const double weight = event.weight();

      const FinalState& fs = applyProjection<FinalState>(event, "FS");
      if (fs.particles().size() < 2) {
        cout << "Less than two final state particles in the event";
        vetoEvent;
      }

      const Thrust& thrust = applyProjection<Thrust>(event, "Thrust");
      _h_Thrust->fill(1-thrust.thrust(), weight);
      _h_ThrustMajor->fill(thrust.thrustMajor(), weight);
      _h_ThrustMinor->fill(thrust.thrustMinor(), weight);
      _h_Oblateness->fill(thrust.oblateness(), weight);
      const Sphericity& sphericity = applyProjection<Sphericity>(event, "Sphericity");
      const double sph = sphericity.sphericity();
      const double apl = sphericity.aplanarity();
      const double pl = sphericity.planarity();
      _h_Sphericity->fill(sph, weight);
      _h_Aplanarity->fill(apl, weight);
      _h_Planarity->fill(pl, weight);

      n_events++;

      double xval, yval, xerr, yerr, gl_fraction;
//      const double roots = 2 * lepton_energy;
//      const double roots = 2*fs.particles()[1].E();      
//      const double roots = 500;
      xval = 0.0; yval = 0.0;
      xerr = 0.0; yerr = 0.0;

      foreach (const Particle& p, fs.particles()) {
        int id = p.pid();
        // x and y are energy fractions and are in [0,1]
        MSG_DEBUG("ID = " << id);
        if(id == PID::UQUARK) {
//          xval = p.E()/roots;
          _h_Quark_Pt->fill(p.pT()/GeV, weight);
          _h_Quark_E->fill(p.E()/GeV, weight);
          _h_Quark_Phi->fill(p.phi(), weight);
          _h_Quark_Rapidity->fill(p.rapidity(), weight);
        } else if(id == - PID::UQUARK) {
//          yval = p.E()/roots;
          _h_Aquark_Pt->fill(p.pT()/GeV, weight);
          _h_Aquark_E->fill(p.E()/GeV, weight);
          _h_Aquark_Phi->fill(p.phi(), weight);
          _h_Aquark_Rapidity->fill(p.rapidity(), weight);
        } else if(id == PID::GLUON) {
          // momentum fraction
          // z = y / (2 - x) ?
          //if (2 - xval - yval != p.E()/roots)
          _h_Gluon_Pt->fill(p.pT()/GeV, weight);
          _h_Gluon_E->fill(p.E()/GeV, weight);
          _h_Gluon_Phi->fill(p.phi(), weight);
          _h_Gluon_Rapidity->fill(p.rapidity(), weight);
        } else if(id ==  PID::PHOTON) {
          n_photons ++;
          vetoEvent;
        }
        MSG_DEBUG( "x " << xval << " xerr " << xerr);
        MSG_DEBUG( "y " << yval << " yerr " << yerr);
//        _h_xy->addPoint(xval, yval, xerr, yerr);
      }
    }


    /// Normalise histograms etc., after the run
    void finalize() {
      /// @todo Normalise, scale and otherwise manipulate histograms here
      // scale(_h_YYYY, crossSection()/sumOfWeights()); // norm to cross section
      // normalize(_h_YYYY); // normalize to unity

      cout << "\nNumber of photons: " << n_photons << "\n";
      cout << "\nNumber of events: " << n_events << "\n";
      cout << "\nPhotons/Events: " << (1.0*n_photons) / n_events << "\n";

      scale(_h_Thrust, 1./sumOfWeights());
      scale(_h_ThrustMajor, 1./sumOfWeights());
      scale(_h_ThrustMinor, 1./sumOfWeights());
      scale(_h_Oblateness, 1./sumOfWeights());
      scale(_h_Sphericity, 1./sumOfWeights());
      scale(_h_Aplanarity, 1./sumOfWeights());
      scale(_h_Planarity, 1./sumOfWeights());
      

      scale(_h_Quark_Pt, 1./sumOfWeights());
      scale(_h_Aquark_Pt, 1./sumOfWeights());
      scale(_h_Gluon_Pt, 1./sumOfWeights());

      scale(_h_Quark_E, 1./sumOfWeights());
      scale(_h_Aquark_E, 1./sumOfWeights());
      scale(_h_Gluon_E, 1./sumOfWeights());

      scale(_h_Quark_Phi, 1./sumOfWeights());
      scale(_h_Aquark_Phi, 1./sumOfWeights());
      scale(_h_Gluon_Phi, 1./sumOfWeights());

      scale(_h_Quark_Rapidity, 1./sumOfWeights());
      scale(_h_Aquark_Rapidity, 1./sumOfWeights());
      scale(_h_Gluon_Rapidity, 1./sumOfWeights());

    }


  private:

    // Data members like post-cuts event weight counters go here

    Histo1DPtr _h_Thrust;
    Histo1DPtr _h_ThrustMajor;
    Histo1DPtr _h_ThrustMinor;
    Histo1DPtr _h_Oblateness;
    Histo1DPtr _h_Sphericity;
    Histo1DPtr _h_Aplanarity;
    Histo1DPtr _h_Planarity;

    Histo1DPtr _h_Quark_Pt;
    Histo1DPtr _h_Aquark_Pt;
    Histo1DPtr _h_Gluon_Pt;

    Histo1DPtr _h_Quark_E;
    Histo1DPtr _h_Aquark_E;
    Histo1DPtr _h_Gluon_E;

    Histo1DPtr _h_Quark_Phi;
    Histo1DPtr _h_Aquark_Phi;
    Histo1DPtr _h_Gluon_Phi;

    Histo1DPtr _h_Quark_Rapidity;
    Histo1DPtr _h_Aquark_Rapidity;
    Histo1DPtr _h_Gluon_Rapidity;

//    Scatter2DPtr _h_xy;

    int n_events, n_photons;

  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(WHIZARD_2015_SINGLEEMISSION);

}
