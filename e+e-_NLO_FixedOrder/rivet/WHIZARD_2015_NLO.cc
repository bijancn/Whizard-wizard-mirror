// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

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
      const FinalState fs;
      const int stdbin = 50;
      addProjection(fs, "FS");
      addProjection(FastJets(fs, FastJets::ANTIKT, 0.7), "Jets");

      _h_Wp_Pt = bookHisto1D("W_plus-pT", stdbin, 0., 210. );
      _h_B_Pt = bookHisto1D("B-pT", stdbin, 0., 170.);

      _h_BB_invMass = bookHisto1D("BB-inv", stdbin, 0., 350.);
      _h_WW_invMass = bookHisto1D("WW-inv", stdbin, 150, 450.);
      _h_jets_invMass = bookHisto1D("jets-inv", stdbin, 100., 500.);

      _h_jetcount = bookHisto1D("jet-count", 5, 1.5, 6.5);
      _h_jetpt = bookHisto1D("jet-pT", stdbin, 0., 250.);
      _h_jetptlog = bookHisto1D("jet-pT-log", stdbin, 1., 6.);
      _h_leadingjetpt = bookHisto1D("leading-jet-pT", stdbin, 50., 225.);
      _h_secondleadingjetpt = bookHisto1D("second-leading-jet-pT", stdbin, 30., 200.);
    }

    void analyze(const Event& event) {
      const FastJets& fastjets = applyProjection<FastJets>(event, "Jets");
      double minjetpt = 0.0 * GeV;
      const Jets jets = fastjets.jetsByPt(minjetpt);
      double weight = event.weight();

      const FinalState& fs = applyProjection<FinalState>(event, "FS");
      if (fs.particles().size() < 2) {
        cout << "Less than two final state particles in the event";
        vetoEvent;
      }
      _h_jetcount->fill(jets.size(), weight);
      _h_leadingjetpt->fill(jets[0].pT(), weight);
      _h_secondleadingjetpt->fill(jets[1].pT(), weight);

      foreach(Jet j, jets) {
        _h_jetpt->fill(j.pT(), weight);
        _h_jetptlog->fill(log(j.pT()), weight);
      }

      foreach (const Particle& p, fs.particles()) {
        int id = p.pid();
        MSG_DEBUG("ID = " << id);
        if (id == PID::WPLUSBOSON) {
          _h_Wp_Pt->fill(p.pT()/GeV, weight);
        } else if(id == PID::BQUARK) {
          _h_B_Pt->fill(p.pT()/GeV, weight);
        }
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
      FourMomentum p_sum = jets[0].momentum() + jets[1].momentum();
      _h_jets_invMass->fill(p_sum.mass(), weight);
    }


    void finalize() {
      // scale(_h_YYYY, crossSection()/sumOfWeights()); // norm to cross section
      // normalize(_h_YYYY); // normalize to unity

      cout << "Sum of weights: " << sumOfWeights () << endl;
      scale(_h_Wp_Pt, crossSection()/sumOfWeights());
      scale(_h_B_Pt, crossSection()/sumOfWeights());

      scale(_h_BB_invMass, crossSection()/sumOfWeights());
      scale(_h_WW_invMass, crossSection()/sumOfWeights());
      scale(_h_jets_invMass, crossSection()/sumOfWeights());

      scale(_h_jetpt, crossSection()/sumOfWeights());
      scale(_h_jetptlog, crossSection()/sumOfWeights());
      scale(_h_leadingjetpt, crossSection()/sumOfWeights());
      scale(_h_secondleadingjetpt, crossSection()/sumOfWeights());

    }


  private:

    Histo1DPtr _h_Wp_Pt;
    Histo1DPtr _h_B_Pt;

    Histo1DPtr _h_BB_invMass;
    Histo1DPtr _h_WW_invMass;
    Histo1DPtr _h_jets_invMass;

    Histo1DPtr _h_jetcount;
    Histo1DPtr _h_jetpt;
    Histo1DPtr _h_jetptlog;
    Histo1DPtr _h_leadingjetpt;
    Histo1DPtr _h_secondleadingjetpt;
  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(WHIZARD_2015_NLO);

}
