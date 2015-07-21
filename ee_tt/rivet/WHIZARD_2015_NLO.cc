// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"

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

      VetoedFinalState veto;
      veto.addVetoPairId(PID::WPLUSBOSON);

      //FastJets jets(veto, FastJets::ANTIKT, 0.4);
      const double R = 0.1; const double p = -1.0;
      fastjet::JetDefinition ee(fastjet::ee_genkt_algorithm,
          R, p, fastjet::E_scheme, fastjet::Best);
      FastJets jets(veto, ee);
      addProjection(jets, "Jets");

      const double sqrts = 500.; const double mTop = 173.;
      _h_T_Pt = bookHisto1D("t-quark-pT", stdbin, 0., 190.);
      _h_g_Pt = bookHisto1D("gluon-pT", stdbin, 0., 20.);

      _h_T_E = bookHisto1D("t-quark-E", stdbin, 150., 260.);
      _h_g_E = bookHisto1D("gluon-E", stdbin, 0., 20.);
      _h_alljet_E = bookHisto1D("all-jet-E", stdbin, 0., sqrts + 1.);
      _h_leadingjet_E = bookHisto1D("leading-jet-E", stdbin, mTop + 9., sqrts/2.+20.);
      _h_secondleadingjet_E = bookHisto1D("second-leading-jet-E", stdbin, mTop -1., sqrts/2.+10.);

      _h_TT_invMass = bookHisto1D("TT-inv", stdbin, 0., 550.);
      _h_jets_invMass = bookHisto1D("jets-inv", stdbin, 0., 550.);

      _h_jetcount = bookHisto1D("jet-count", 4, 0.5, 4.5);
      _h_jetpt = bookHisto1D("jet-pT", stdbin, 0., 200.);
      _h_jetptlog = bookHisto1D("jet-pT-log", stdbin, 1., 5.7);
      _h_leadingjetpt = bookHisto1D("leading-jet-pT", stdbin, 25., 190.);
      _h_secondleadingjetpt = bookHisto1D("second-leading-jet-pT", stdbin, 0., 190.);

      vetoCounter = 0;
      eventCounter = 0;
      acceptedWeights = 0.0;
    }

    void analyze(const Event& event) {
      const FastJets& fastjets = applyProjection<FastJets>(event, "Jets");
      const FinalState& fs = applyProjection<FinalState>(event, "FS");
      double minjetE = 1. * GeV;
      const PseudoJets jets = fastjets.pseudoJetsByE(minjetE);
      double weight = event.weight();

      eventCounter++;
      bool vetoCondition = jets.size() < 2;
      if (vetoCondition) {
        vetoCounter++;
        vetoEvent;
      }
      else {
        acceptedWeights += weight;
      }

      _h_jetcount->fill(jets.size(), weight);

      PseudoJet alljets;
      foreach (const PseudoJet& j, jets){
        alljets += j;
      }
      _h_alljet_E->fill(alljets.E(), weight);
      _h_leadingjet_E->fill(jets[0].E(), weight);
      _h_secondleadingjet_E->fill(jets[1].E(), weight);
      PseudoJet p_sum = jets[0] + jets[1];
      _h_jets_invMass->fill(p_sum.m(), weight);
      _h_leadingjetpt->fill(jets[0].pt(), weight);
      _h_secondleadingjetpt->fill(jets[1].pt(), weight);
      //FourMomentum p_sum = jets[0].momentum() + jets[1].momentum();
      //foreach(Jet j, jets) {
        //_h_jetpt->fill(j.pt(), weight / jets.size());
        //_h_jetptlog->fill(log(j.pt()), weight / jets.size());
      //}

      // Register single particle properties
      foreach (const Particle& p, fs.particles()) {
        int id = p.pid();
        if(id == PID::TQUARK) {
          _h_T_Pt->fill(p.pT()/GeV, weight);
          _h_T_E->fill(p.E()/GeV, weight);
        } else if(id == PID::GLUON) {
          _h_g_Pt->fill(p.pT()/GeV, weight);
          _h_g_E->fill(p.E()/GeV, weight);
        }
      }

      // Compute invariant masses
      foreach (const Particle& p1, fs.particles()) {
        foreach (const Particle& p2, fs.particles()) {
          int id1 = p1.pid(); int id2 = p2.pid();
          if (id1 == PID::TQUARK && id2 == -PID::TQUARK) {
            FourMomentum p_sum = p1.momentum() + p2.momentum();
            _h_TT_invMass->fill(p_sum.mass(), weight);
          }
        }
      }
    }


    void finalize() {
      // normalize(_h_YYYY); // normalize to unity
      const double fb_per_pb = 1000.0;
      double fiducial_xsection = crossSection() * fb_per_pb * acceptedWeights / sumOfWeights();
      double scale_factor = crossSection() * fb_per_pb / sumOfWeights();

      cout << "Sum of weights: " << sumOfWeights () << endl;
      cout << "Sum of weights / N: " << sumOfWeights () / eventCounter << endl;
      cout << "Original cross section (pb): " << crossSection () << endl;
      cout << "Number of total events: " << eventCounter << endl;
      cout << "Sum of weights / n_events: " << sumOfWeights () / eventCounter << endl;
      cout << "Numer of vetoed events: " << vetoCounter << endl;
      cout << "Final (fiducial) cross section (fb): " << fiducial_xsection << endl;
      cout << "Scale factor: " << scale_factor << endl;

      scale(_h_T_Pt, scale_factor);
      scale(_h_g_Pt, scale_factor);
      scale(_h_T_E, scale_factor);
      scale(_h_g_E, scale_factor);
      scale(_h_alljet_E, scale_factor);
      scale(_h_leadingjet_E, scale_factor);
      scale(_h_secondleadingjet_E, scale_factor);

      scale(_h_TT_invMass, scale_factor);
      scale(_h_jets_invMass, scale_factor);

      scale(_h_jetcount, scale_factor);
      scale(_h_jetpt, scale_factor);
      scale(_h_jetptlog, scale_factor);
      scale(_h_leadingjetpt, scale_factor);
      scale(_h_secondleadingjetpt, scale_factor);
    }


  private:

    Histo1DPtr _h_T_Pt;
    Histo1DPtr _h_g_Pt;
    Histo1DPtr _h_T_E;
    Histo1DPtr _h_g_E;
    Histo1DPtr _h_alljet_E;
    Histo1DPtr _h_leadingjet_E;
    Histo1DPtr _h_secondleadingjet_E;

    Histo1DPtr _h_TT_invMass;
    Histo1DPtr _h_jets_invMass;

    Histo1DPtr _h_jetcount;
    Histo1DPtr _h_jetpt;
    Histo1DPtr _h_jetptlog;
    Histo1DPtr _h_leadingjetpt;
    Histo1DPtr _h_secondleadingjetpt;

    int vetoCounter, eventCounter;
    double acceptedWeights;
  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(WHIZARD_2015_NLO);

}
