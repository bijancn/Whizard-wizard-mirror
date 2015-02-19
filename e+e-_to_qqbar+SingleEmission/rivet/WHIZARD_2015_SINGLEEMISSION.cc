// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/Beam.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
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
      addProjection(Beam(), "Beams");
      addProjection(ChargedFinalState(), "FS");
      // Charged and neutral final state
      const FinalState cnfs;
      addProjection(cnfs, "CNFS");

      _hist_quarkpt = bookHisto1D("d01-x01-y01", 30, 1., 260.);
      _hist_aquarkpt = bookHisto1D("d02-x01-y01", 30, 1., 260.);
      _hist_gluonpt = bookHisto1D("d03-x01-y01", 30, 1., 260.);
    }

    /// Perform the per-event analysis
    void analyze(const Event& event) {

      // Get event weight for histo filling
      const double weight = event.weight();

      const FinalState& fs = applyProjection<FinalState>(event, "CNFS");
      if (fs.particles().size() < 2) {
        MSG_DEBUG("Less than two final state particles in the event");
        vetoEvent;
      }

      foreach (const Particle& p, fs.particles()) {
        int id = p.pid();
        MSG_DEBUG("ID" << id);
        if(id == PID::UQUARK) {
          _hist_quarkpt->fill(p.pT()/GeV, weight);
        } else if(id == - PID::UQUARK) {
          _hist_aquarkpt->fill(p.pT()/GeV, weight);
        } else if(id == PID::GLUON) {
          _hist_gluonpt->fill(p.pT()/GeV, weight);
        }
      }
    }


    /// Normalise histograms etc., after the run
    void finalize() {
      /// @todo Normalise, scale and otherwise manipulate histograms here
      // scale(_h_YYYY, crossSection()/sumOfWeights()); // norm to cross section
      // normalize(_h_YYYY); // normalize to unity
      scale(_hist_quarkpt, 1./sumOfWeights());
      scale(_hist_aquarkpt, 1./sumOfWeights());
      scale(_hist_gluonpt, 1./sumOfWeights());
    }


  private:

    // Data members like post-cuts event weight counters go here
    Histo1DPtr _hist_quarkpt;
    Histo1DPtr _hist_aquarkpt;
    Histo1DPtr _hist_gluonpt;

  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(WHIZARD_2015_SINGLEEMISSION);

}
