// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"

double cut_ptl = 0;
double cut_etal = 999999.;
double cut_dRlj = 0.0;

namespace Rivet {

  using namespace Cuts;

  class WHIZARD_ttH_NLO : public Analysis {

#include "NLOHisto1D.cc"

  public:

    /// Constructor
    WHIZARD_ttH_NLO()
      : Analysis("WHIZARD_ttH_NLO")
    {    }

    /// Book histograms and initialise projections before the run
    void init() {
      const FinalState fs;
      const int stdbin = 20;
      addProjection(fs, "FS");

      const IdentifiedFinalState t(PID::TQUARK);
      addProjection(t, "top");
      const IdentifiedFinalState tbar(-PID::TQUARK);
      addProjection(tbar, "antitop");
      const IdentifiedFinalState H(PID::HIGGS);
      addProjection(H, "higgs");

      VetoedFinalState veto;
      veto.addVetoPairId(PID::HIGGS);

      const double R = 0.4; const double p = -1.0;
      fastjet::JetDefinition ee(fastjet::ee_genkt_algorithm, R, p,
          fastjet::E_scheme, fastjet::Best);
      FastJets jets(veto, ee);
      addProjection(jets, "Jets");

      _h["leadingjet_E"] = bookNLOHisto1D("leading-jet-E", stdbin,  150., 405.);
      _h["leadingjet_Pt"] = bookNLOHisto1D("leading-jet-pT", stdbin, 0., 350.);
      _h["leadingjet_Theta"] = bookNLOHisto1D("leading-jet-Theta", stdbin, -1.1, 1.1);

      _h["2ndleadingjet_E"] = bookNLOHisto1D("2nd-leading-jet-E", stdbin, 0., 405.);
      _h["2ndleadingjet_Pt"] = bookNLOHisto1D("2nd-leading-jet-pT", stdbin, 0., 350.);
      _h["2ndleadingjet_Theta"] = bookNLOHisto1D("2nd-leading-jet-Theta", stdbin, -1.1, 1.1);

      _h["top-E"] = bookNLOHisto1D("top-E", stdbin, 0., 405.);
      _h["antitop-E"] = bookNLOHisto1D("antitop-E", stdbin, 0., 405.);
      _h["top-pT"] = bookNLOHisto1D("top-pT", stdbin, 0., 350.);
      _h["antitop-pT"] = bookNLOHisto1D("antitop-pT", stdbin, 0., 350.);
      _h["top-theta"] = bookNLOHisto1D("top-theta", stdbin, -1.1, 1.1);
      _h["antitop-theta"] = bookNLOHisto1D("antitop-theta", stdbin, -1.1, 1.1);

      _h["Higgs_E"] = bookNLOHisto1D("Higgs-E", stdbin, 0., 350.);
      _h["Higgs_Pt"] = bookNLOHisto1D("Higgs-Pt", stdbin, 0., 350.);
      _h["Higgs_Theta"] = bookNLOHisto1D("Higgs-Theta", stdbin, -1.1, 1.1);

      _h["jets_invMass"] = bookNLOHisto1D("jets-inv", stdbin, 125., 750.);
      _h["jetcount"] = bookNLOHisto1D("jet-count", 4, 0.5, 4.5);
      _h["jetcount_incl"] = bookNLOHisto1D("jet-count-incl", 4, 0.5, 4.5);


      vetoCounter = 0;
      eventCounter = 0;
      acceptedWeights = 0.0;
    }

    void analyze(const Event& event) {
      double weight = event.weight();
    
      Jets jets, tjets, tbarjets;

      ParticleVector tpartons = applyProjection<IdentifiedFinalState>(event, "top").particlesByPt();
      ParticleVector tbarpartons = applyProjection<IdentifiedFinalState>(event, "antitop").particlesByPt();
      //get the jets
      const FastJets& fastjets = applyProjection<FastJets>(event, "Jets");
      double minjetE = 1. * GeV;
      const PseudoJets pseudo_jets = fastjets.pseudoJetsByE(minjetE);

      foreach (const PseudoJet & pseudo_jet, pseudo_jets) {
         vector<PseudoJet> constituents = pseudo_jet.constituents();
         bool is_t = false;
         foreach (const PseudoJet& constituent, constituents) {
            foreach (const Particle& tparton, tpartons) {
               if (have_same_momentum (constituent, tparton)) {tjets.push_back(pseudo_jet); is_t = true;}
            }
            foreach (const Particle& tbarparton, tbarpartons) {
               if (have_same_momentum (constituent, tbarparton)) {tbarjets.push_back(pseudo_jet); is_t = true;}
            }
         }
         jets.push_back (pseudo_jet);
      }

      //get the Higgs
      ParticleVector H_cand = applyProjection<IdentifiedFinalState>(event, "higgs").particlesByPt();
      ParticleVector H;
      foreach (const Particle & hi, H_cand) 
         H.push_back(hi);

      eventCounter++;
      bool vetoCondition = jets.size() < 2 or tjets.size() == 0 or tbarjets.size() == 0;
      if (vetoCondition) {
        vetoCounter++;
        vetoEvent;
      }
      else {
        acceptedWeights += weight;
      }

      _h["jetcount"]->fill(jets.size(), event);
      for (unsigned int i = 0; i < jets.size(); i++)
         _h["jetcount_incl"]->fill(i + 1, event);

      _h["top-E"]->fill(tjets[0].E(), event);
      _h["antitop-E"]->fill(tbarjets[0].E(), event);
      _h["top-pT"]->fill(tjets[0].pt(), event);
      _h["antitop-pT"]->fill(tbarjets[0].pt(), event);
      _h["top-theta"]->fill(std::cos(tjets[0].theta()), event);
      _h["antitop-theta"]->fill(std::cos(tbarjets[0].theta()), event);

      _h["leadingjet_E"]->fill(jets[0].E(), event);
      _h["leadingjet_Pt"]->fill(jets[0].pt(), event);
      _h["leadingjet_Theta"]->fill(std::cos(jets[0].theta()), event);

      _h["2ndleadingjet_E"]->fill(jets[1].E(), event);
      _h["2ndleadingjet_Pt"]->fill(jets[1].pt(), event);
      _h["2ndleadingjet_Theta"]->fill(std::cos(jets[1].theta()), event);

      _h["Higgs_E"]->fill(H[0].momentum().E(), event);
      _h["Higgs_Pt"]->fill(H[0].momentum().pt(), event);
      _h["Higgs_Theta"]->fill(std::cos (H[0].momentum().theta()), event);

      double jetsMass = (jets[0].momentum() + jets[1].momentum()).mass();
      _h["jets_invMass"]->fill(jetsMass, event);

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

      typedef std::map<string, NLOHisto1DPtr>::iterator it;

      for(it iter = _h.begin(); iter != _h.end(); iter++) {
        iter->second->finalize();
        scale(iter->second,scale_factor);
      }

    }

  private:

    std::map <string, NLOHisto1DPtr> _h;

    int vetoCounter, eventCounter;
    int low_energy_counts;
    double low_energy_weights;
    double acceptedWeights;
  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(WHIZARD_ttH_NLO);
}
