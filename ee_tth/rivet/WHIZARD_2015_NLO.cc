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
      veto.addVetoId(PID::HIGGS);

      const double R = 1.0; const double p = -1.0;
      fastjet::JetDefinition ee(fastjet::ee_genkt_algorithm, R, p, fastjet::E_scheme, fastjet::Best);
      FastJets jets(veto, ee);
      addProjection(jets, "Jets");

      _h_t_E = bookHisto1D("t-quark-E", stdbin, 172., 195.);
      _h_g_E = bookHisto1D("gluon-E", stdbin, 0., 20.);
      _h_h_E = bookHisto1D("higgs-E", stdbin, 124., 148.);
      _h_leadingjet_E = bookHisto1D("leading-jet-E", stdbin, 172., 198.);
      _h_secondleadingjet_E = bookHisto1D("second-leading-jet-E", stdbin, 172., 190.);

      _h_t_Theta = bookHisto1D("t-quark-Theta", stdbin, -1.1, 1.1);
      _h_g_Theta = bookHisto1D("gluon-Theta", stdbin, -1.1, 1.1);
      _h_h_Theta = bookHisto1D("higgs-Theta", stdbin, -1.1, 1.1);
      _h_leadingjet_Theta = bookHisto1D("leading-jet-Theta", stdbin, -1.1, 1.1);
      _h_secondleadingjet_Theta = bookHisto1D("second-leading-jet-Theta", stdbin, -1.1, 1.1);

      _h_jets_invMass = bookHisto1D("jets-inv", stdbin, 346., 378.);
      _h_jetcount = bookHisto1D("jet-count", 4, 0.5, 4.5);

      vetoCounter = 0;
      eventCounter = 0;
      acceptedWeights = 0.0;
    }

    void analyze(const Event& event) {
      const FastJets& fastjets = applyProjection<FastJets>(event, "Jets");
      const FinalState& fs = applyProjection<FinalState>(event, "FS");
      double minjetE = 1 * GeV;
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

      double polarangle, costheta;
      _h_leadingjet_E->fill(jets[0].E(), weight);
      polarangle = atan2(sqrt(jets[0].px()*jets[0].px()+jets[0].py()*jets[0].py()), jets[0].pz());
      costheta = cos(polarangle);
      _h_leadingjet_Theta->fill(costheta, weight);

      _h_secondleadingjet_E->fill(jets[1].E(), weight);
      polarangle = atan2(sqrt(jets[1].px()*jets[1].px()+jets[1].py()*jets[1].py()), jets[1].pz());
      costheta = cos(polarangle);
      _h_secondleadingjet_Theta->fill(costheta, weight);

      PseudoJet p_sum = jets[0] + jets[1];
      _h_jets_invMass->fill(p_sum.m(), weight);

      // Register single particle properties
      foreach (const Particle& p, fs.particles()) {
        int id = p.pid();
        double E = p.E()/GeV;
        double costheta = cos(p.theta());
        if(id == PID::TQUARK) {
          _h_t_E->fill(E, weight);
          _h_t_Theta->fill(costheta, weight);
        } else if(id == PID::GLUON) {
          _h_g_E->fill(E, weight);
          _h_g_Theta->fill(costheta, weight);
        } else if(id == PID::HIGGS) {
          _h_h_E->fill(E, weight);
          _h_h_Theta->fill(costheta, weight);
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

      scale(_h_t_E, scale_factor);
      scale(_h_g_E, scale_factor);
      scale(_h_h_E, scale_factor);
      scale(_h_leadingjet_E, scale_factor);
      scale(_h_secondleadingjet_E, scale_factor);

      scale(_h_t_Theta, scale_factor);
      scale(_h_g_Theta, scale_factor);
      scale(_h_h_Theta, scale_factor);
      scale(_h_leadingjet_Theta, scale_factor);
      scale(_h_secondleadingjet_Theta, scale_factor);

      scale(_h_jets_invMass, scale_factor);
      scale(_h_jetcount, scale_factor);
    }


  private:

    Histo1DPtr _h_t_E;
    Histo1DPtr _h_g_E;
    Histo1DPtr _h_h_E;
    Histo1DPtr _h_leadingjet_E;
    Histo1DPtr _h_secondleadingjet_E;

    Histo1DPtr _h_t_Theta;
    Histo1DPtr _h_g_Theta;
    Histo1DPtr _h_h_Theta;
    Histo1DPtr _h_leadingjet_Theta;
    Histo1DPtr _h_secondleadingjet_Theta;

    Histo1DPtr _h_jets_invMass;
    Histo1DPtr _h_jetcount;

    int vetoCounter, eventCounter;
    double acceptedWeights;
  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(WHIZARD_2015_NLO);

}
