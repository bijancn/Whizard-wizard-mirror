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

  class WHIZARD_dy_NLO : public Analysis {

#include "NLOHisto1D.cc"

  public:

    /// Constructor
    WHIZARD_dy_NLO()
      : Analysis("WHIZARD_dy_NLO")
    {    }

    /// Book histograms and initialise projections before the run
    void init() {
      const FinalState fs;
      const int stdbin = 30;
      addProjection(fs, "FS");

      const IdentifiedFinalState el(PID::ELECTRON);
      addProjection(el, "electron");
      const IdentifiedFinalState pos(-PID::ELECTRON);
      addProjection(pos, "positron");

      VetoedFinalState veto;
      veto.addVetoPairId(PID::ELECTRON);

      const double R = 0.4; const double p = -1.0;
      fastjet::JetDefinition ee(fastjet::ee_genkt_algorithm, R, p,
          fastjet::E_scheme, fastjet::Best);
      FastJets jets(fs, ee);
      addProjection(jets, "Jets");

      _h["leadingjet_E"] = bookNLOHisto1D("leading-jet-E", stdbin, 250., 600.);
      _h["leadingjet_Pt"] = bookNLOHisto1D("leading-jet-pT", stdbin, 0., 405.);
      _h["leadingjet_Theta"] = bookNLOHisto1D("leading-jet-Theta", stdbin, -1.1, 1.1);

      _h["2ndleadingjet_E"] = bookNLOHisto1D("2nd-leading-jet-E", stdbin, 0., 450.);
      _h["2ndleadingjet_Pt"] = bookNLOHisto1D("2nd-leading-jet-pT", stdbin, 0., 405.);
      _h["2ndleadingjet_Theta"] = bookNLOHisto1D("2nd-leading-jet-Theta", stdbin, -1.1, 1.1);

      _h["jets_invMass"] = bookNLOHisto1D("jets-inv", 25, 780.1, 805.1);
      _h["jetcount"] = bookNLOHisto1D("jet-count", 4, 0.5, 4.5);
      _h["jetcount_incl"] = bookNLOHisto1D("jet-count-incl", 4, 0.5, 4.5);

      _h["lepton_invMass"] = bookNLOHisto1D("lepton-inv", stdbin, 10., 200.);
      _h["electron_pT"] = bookNLOHisto1D("electron-pT", stdbin, 0., 200.);
      _h["positron_pT"] = bookNLOHisto1D("positron-pT", stdbin, 0., 200.);
      _h["electron_Theta"] = bookNLOHisto1D("electron-Theta", stdbin, 0., 200.);
      _h["positron_Theta"] = bookNLOHisto1D("positron-Theta", stdbin, 0., 200.);

      _h["Z_eta"] = bookNLOHisto1D("Z-Eta", stdbin, -5.0, 5.0);


      vetoCounter = 0;
      eventCounter = 0;
      acceptedWeights = 0.0;
    }

    void analyze(const Event& event) {
      double weight = event.weight();
    
      Jets jets, tjets, tbarjets;

      const FastJets& fastjets = applyProjection<FastJets>(event, "Jets");
      double minjetE = 1. * GeV;
      //double minjetE = 0. * GeV;
      const PseudoJets pseudo_jets = fastjets.pseudoJetsByE(minjetE);
      //cout << "Size of pseudojets: " << pseudo_jets.size() << endl;
      //if (pseudo_jets.size() > 0) {
      //  foreach (const PseudoJet & pseudo_jet, pseudo_jets) {
      //     vector<PseudoJet> constituents = pseudo_jet.constituents();
      //     foreach(const PseudoJet & constituent, constituents) {
      //        cout << "Constituent: " << constituent.E() << " , " << constituent.px() << endl;
      //     }
      //  }
      //}
      eventCounter++;

      ParticleVector cand_el = 
         applyProjection<IdentifiedFinalState>(event, "electron").particlesByPt();
      ParticleVector cand_pos = 
         applyProjection<IdentifiedFinalState>(event, "positron").particlesByPt();

       ParticleVector el;
       foreach ( const Particle & p, cand_el ) {
         el.push_back(p);
       }

       ParticleVector pos;
       foreach ( const Particle & p, cand_pos ) {
         pos.push_back(p);
        }

      FourMomentum Pel = el[0].momentum();
      FourMomentum Ppos = pos[0].momentum();
      FourMomentum PZ = Pel + Ppos;
      //cout << Pel << endl;
      //cout << Ppos << endl;


      foreach (const PseudoJet & pseudo_jet, pseudo_jets) {
         vector<PseudoJet> constituents = pseudo_jet.constituents();
         jets.push_back (pseudo_jet);
      }

      bool vetoCondition = jets.size() < 2;
      //if (vetoCondition) {
      //  vetoCounter++;
      //  vetoEvent;
      //}
      //else {
        acceptedWeights += weight;
      //}

      double m = PZ.mass();
      double z_eta = PZ.rapidity();
      _h["lepton_invMass"]->fill(m, event);
      _h["Z_eta"]->fill(z_eta, event);
      _h["electron_pT"]->fill(Pel.pt(), event);
      _h["positron_pT"]->fill(Ppos.pt(), event);
      _h["electron_Theta"]->fill(std::cos(Pel.theta()), event);
      _h["positron_Theta"]->fill(std::cos(Ppos.theta()), event);

      //_h["jetcount"]->fill(jets.size(), event);
      //for (unsigned int i = 0; i < jets.size(); i++)
      //   _h["jetcount_incl"]->fill(i + 1, event);

      //_h["leadingjet_E"]->fill(jets[0].E(), event);
      //_h["leadingjet_Pt"]->fill(jets[0].pt(), event);
      //_h["leadingjet_Theta"]->fill(std::cos(jets[0].theta()), event);

      //_h["2ndleadingjet_E"]->fill(jets[1].E(), event);
      //_h["2ndleadingjet_Pt"]->fill(jets[1].pt(), event);
      //_h["2ndleadingjet_Theta"]->fill(std::cos(jets[1].theta()), event);


      //double jetsMass = (jets[0].momentum() + jets[1].momentum()).mass();
      //_h["jets_invMass"]->fill(jetsMass, event);

    }

    void finalize() {
      // normalize(_h_YYYY); // normalize to unity
      const double fb_per_pb = 1000.0;
      double fiducial_xsection = crossSection() * fb_per_pb * acceptedWeights / sumOfWeights();
      double scale_factor = crossSection() * fb_per_pb / sumOfWeights();
      //double scale_factor = 1;

      cout << "Event Counter: " << eventCounter << endl;
      cout << "Sum of weights: " << sumOfWeights () << endl;
      cout << "Sum of accepted weights: " << acceptedWeights << endl;
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
  DECLARE_RIVET_PLUGIN(WHIZARD_dy_NLO);
}
