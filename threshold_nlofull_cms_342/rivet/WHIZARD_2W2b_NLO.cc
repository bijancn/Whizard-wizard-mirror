// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"
#include "Rivet/Projections/Sphericity.hh"
#include "Rivet/Projections/Thrust.hh"

namespace Rivet {

  using namespace Cuts;

  class WHIZARD_2W2b_NLO : public Analysis {

#include "NLOHisto1D.cc"

  public:

    /// Constructor
    WHIZARD_2W2b_NLO()
      : Analysis("WHIZARD_2W2b_NLO")
    {    }

    /// Book histograms and initialise projections before the run
    void init() {
      const FinalState fs;
      const int stdbin = 1000;

      addProjection(fs, "FS");
      const Thrust thrust(fs);
      addProjection(thrust, "Thrust");
      addProjection(Sphericity(fs), "Sphericity");
      const IdentifiedFinalState b(PID::BQUARK);
      addProjection(b, "bquark");
      const IdentifiedFinalState bbar(-PID::BQUARK);
      addProjection(bbar, "bbarquark");
      const IdentifiedFinalState wp(PID::WPLUSBOSON);
      addProjection(wp, "wp");
      const IdentifiedFinalState wm(-PID::WPLUSBOSON);
      addProjection(wm, "wm");


      VetoedFinalState veto;
      veto.addVetoPairId(PID::WPLUSBOSON);

      const double R = 0.4; const double p = -1.0;
      fastjet::JetDefinition ee(fastjet::ee_genkt_algorithm, R, p, fastjet::E_scheme, fastjet::Best);
      FastJets jets(veto, ee);
      addProjection(jets, "Jets");

      _h["leadingjet_E"] = bookNLOHisto1D("leading-jet-E", stdbin, 0., 200.);
      _h["leadingjet_Pt"] = bookNLOHisto1D("leading-jet-pT", stdbin, 0., 200.);
      _h["leadingjet_Theta"] = bookNLOHisto1D("leading-jet-Theta", stdbin, -1.1, 1.1);

      _h["2ndleadingjet_E"] = bookNLOHisto1D("2nd-leading-jet-E", stdbin, 0., 100.);
      _h["2ndleadingjet_Pt"] = bookNLOHisto1D("2nd-leading-jet-pT", stdbin, 0., 100.);
      _h["2ndleadingjet_Theta"] = bookNLOHisto1D("2nd-leading-jet-Theta", stdbin, -1.1, 1.1);

      _h["jets_invMass"] = bookNLOHisto1D("jets-inv", stdbin, 0., 250.);
      _h["jets_invMass_Zpeak"] = bookNLOHisto1D("jets-inv-Zpeak", stdbin, 80., 100.);
      _h["jets_invMass_Hpeak"] = bookNLOHisto1D("jets-inv-Hpeak", stdbin, 115.1, 135.1);

      _h["bjet_E"] = bookNLOHisto1D("b-jet-E", stdbin, 0., 150.);
      _h["bjet_Pt"] = bookNLOHisto1D("b-jet-pT", stdbin, 0., 150.);
      _h["bjet_Theta"] = bookNLOHisto1D("b-jet-Theta", stdbin, -1.1, 1.1);

      _h["bbarjet_E"] = bookNLOHisto1D("bbar-jet-E", stdbin, 0., 150.);
      _h["bbarjet_Pt"] = bookNLOHisto1D("bbar-jet-pT", stdbin, 0., 150.);
      _h["bbarjet_Theta"] = bookNLOHisto1D("bbar-jet-Theta", stdbin, -1.1, 1.1);

      _h["Wm_E"] = bookNLOHisto1D("Wm-E", stdbin, 75., 200.);
      _h["Wm_Pt"] = bookNLOHisto1D("Wm-pT", stdbin, 0., 200.);
      _h["Wm_Theta"] = bookNLOHisto1D("Wm-Theta", stdbin, -1.1, 1.1);

      _h["Wp_E"] = bookNLOHisto1D("Wp-E", stdbin, 75., 200.);
      _h["Wp_Pt"] = bookNLOHisto1D("Wp-pT", stdbin, 0., 200.);
      _h["Wp_Theta"] = bookNLOHisto1D("Wp-Theta", stdbin, -1.1, 1.1);

      _h["BWm_E"] = bookNLOHisto1D("BWm-E", stdbin, 75., 300.);
      _h["BWm_Pt"] = bookNLOHisto1D("BWm-pT", stdbin, 0., 150.);
      _h["BWm_ThreeMom"] = bookNLOHisto1D("BWm-ThreeMom", stdbin, 0., 120.);
      _h["BWm_Theta"] = bookNLOHisto1D("BWm-Theta", stdbin, -1.1, 1.1);
      _h["BWm_Phi"] = bookNLOHisto1D("Phi(b,Wm)", stdbin, 0., M_PI);
      _h["BWm_R"] = bookNLOHisto1D("R(b,Wm)", stdbin, 0., 5.);
      _h["BWm_invMass"] = bookNLOHisto1D("BWm-inv", stdbin, 50., 300.);
      _h["BWm_invMass_peak"] = bookNLOHisto1D("BWm-inv-peak", stdbin, 160., 180.);

      _h["BWp_E"] = bookNLOHisto1D("BWp-E", stdbin, 75., 300.);
      _h["BWp_Pt"] = bookNLOHisto1D("BWp-pT", stdbin, 0., 150.);
      _h["BWp_ThreeMom"] = bookNLOHisto1D("BWp-ThreeMom", stdbin, 0., 120.);
      _h["BWp_Theta"] = bookNLOHisto1D("BWp-Theta", stdbin, -1.1, 1.1);
      _h["BWp_Phi"] = bookNLOHisto1D("Phi(b,Wp)", stdbin, 0., M_PI);
      _h["BWp_R"] = bookNLOHisto1D("R(b,Wp)", stdbin, 0., 5.);
      _h["BWp_invMass"] = bookNLOHisto1D("BWp-inv", stdbin, 50., 300.);
      _h["BWp_invMass_peak"] = bookNLOHisto1D("BWp-inv-peak", stdbin, 160., 180.);

      _h["BB_E"] = bookNLOHisto1D("BB-E", stdbin, 0., 300.);
      _h["BB_Theta"] = bookNLOHisto1D("BB-Theta", stdbin, -1.1, 1.1);
      _h["BB_Pt"] = bookNLOHisto1D("BB-pT", stdbin, 0., 300.);
      _h["BB_invMass"] = bookNLOHisto1D("BB-inv", stdbin, 0., 200.);
      _h["BB_invMass_Zpeak"] = bookNLOHisto1D("BB-inv-Zpeak", stdbin, 80., 100.);
      _h["BB_invMass_Hpeak"] = bookNLOHisto1D("BB-inv-Hpeak", stdbin, 115.1, 135.1);
      _h["BB_Phi"] = bookNLOHisto1D("Phi(b,b)", stdbin, 0, M_PI);
      _h["BB_R"] = bookNLOHisto1D("R(b,b)", stdbin, 0., 5.);

      _h["BW_invMass"] = bookNLOHisto1D("BW-inv", stdbin, 100., 300);
      _h["BW_invMass_peak"] = bookNLOHisto1D("BW-inv-peak", stdbin, 160., 180.);
      // _h2["BWm_BWp_invMass_peak"] = bookHisto2D("BWm_BWp_invMass_peak", stdbin, 160., 180., stdbin, 160., 180.);

      _h["jetcount"] = bookNLOHisto1D("jet-count", 4, 0.5, 4.5);
      _h["jetcount_incl"] = bookNLOHisto1D("jet-count-incl", 4, 0.5, 4.5);

      _h["A_FB"] = bookNLOHisto1D("A_FB", 1, 0., 1.);
      _h["A_FBbar"] = bookNLOHisto1D("A_FBbar", 1, 0., 1.);
      _h["Sum_Weights"] = bookNLOHisto1D("Sum_Weights", 1, 0., 1.);
      _h["Sum_Weightsbar"] = bookNLOHisto1D("Sum_Weightsbar", 1, 0., 1.);

      _h["Thrust"] = bookNLOHisto1D("Thrust", stdbin, 0, 0.5);
      _h["ThrustMajor"] = bookNLOHisto1D("ThrustMajor", stdbin, 0, 1.0);
      _h["ThrustMinor"] = bookNLOHisto1D("ThrustMinor", stdbin, 0, 0.5);
      _h["Oblateness"] = bookNLOHisto1D("Oblateness", stdbin, 0, 1.0);
      _h["Sphericity"] = bookNLOHisto1D("Sphericity", stdbin, 0, 1.0);
      _h["Aplanarity"] = bookNLOHisto1D("Aplanarity", stdbin, 0, 1.0);
      _h["Planarity"] = bookNLOHisto1D("Planarity", stdbin, 0, 1.0);

      _h["2jettiness"] = bookNLOHisto1D("2jettiness", stdbin, 0, 0.5);
      _h["Cparameter"] = bookNLOHisto1D("Cparameter", stdbin, 0, 1);

      vetoCounter = 0;
      eventCounter = 0;
      acceptedWeights = 0.;
    }

    void analyze(const Event& event) {
      const FastJets& fastjets = applyProjection<FastJets>(event, "Jets");
      double minjetE = 1. * GeV;
      const PseudoJets pseudo_jets = fastjets.pseudoJetsByE(minjetE);
      double weight = event.weight();
 
      Jets jets, bjets, bbarjets;

      ParticleVector bpartons    = applyProjection<IdentifiedFinalState>(event, "bquark").particlesByPt();
      ParticleVector bbarpartons = applyProjection<IdentifiedFinalState>(event, "bbarquark").particlesByPt();

      // tag b-jets
      foreach (const PseudoJet & pseudo_jet, pseudo_jets) {
        vector<PseudoJet> constituents = pseudo_jet.constituents();
        foreach (const PseudoJet& constituent, constituents) {
          foreach(const Particle & bparton, bpartons) {
            if (have_same_momentum (constituent, bparton))
               bjets.push_back(pseudo_jet);
          }
          foreach(const Particle & bbarparton, bbarpartons) {
            if (have_same_momentum (constituent, bbarparton))
               bbarjets.push_back(pseudo_jet);
          }
        }
        jets.push_back(pseudo_jet);   // all jets
      }

      // get the Ws
      ParticleVector cand_wm = applyProjection<IdentifiedFinalState>(event, "wm").particlesByPt();
      ParticleVector cand_wp = applyProjection<IdentifiedFinalState>(event, "wp").particlesByPt();

       // W-Finder: apply W cuts and discard Ws that overlap with jets
       ParticleVector wm;
       foreach ( const Particle & p, cand_wm ) {
         wm.push_back(p);
       }

       ParticleVector wp;
       foreach ( const Particle & p, cand_wp ) {
         wp.push_back(p);
        }

      eventCounter++;
      FourMomentum Wm = wm[0].momentum();
      FourMomentum Wp = wp[0].momentum();
      bool vetoCondition = jets.size () < 2;
      if (vetoCondition) {
        vetoCounter++;
        vetoEvent;
      }
      else {
        acceptedWeights += weight;
      }

      const Thrust& thrust = applyProjection<Thrust>(event, "Thrust");
      _h["Thrust"]->fill(1-thrust.thrust(), event);
      _h["ThrustMajor"]->fill(thrust.thrustMajor(), event);
      _h["ThrustMinor"]->fill(thrust.thrustMinor(), event);
      _h["Oblateness"]->fill(thrust.oblateness(), event);
      const Sphericity& sphericity = applyProjection<Sphericity>(event, "Sphericity");
      _h["Sphericity"]->fill(sphericity.sphericity(), event);
      _h["Aplanarity"]->fill(sphericity.aplanarity(), event);
      _h["Planarity"]->fill(sphericity.planarity(), event);

      ParticleVector fs = applyProjection<FinalState>(event, "FS").particlesByPt();
      double sum_abs_momenta = 0.0;
      FourVector total_vec(0.0, 0.0, 0.0, 0.0);
      foreach (const FourVector & finst, fs) {
        sum_abs_momenta += finst.vector3().mod();
        total_vec += finst;
      }
      double Q = total_vec.t();
      cout << "Total energy " << Q << endl;
      _h["2jettiness"]->fill(1 - thrust.thrust() / Q * sum_abs_momenta, event);
      double sum_p = 0.0;
      foreach (const FourVector & finst_i, fs) {
      // for (unsigned int i=0; i < fs.size(); i++) {
        foreach (const FourVector & finst_j, fs) {
        // for (unsigned int j=0; j < fs.size(); j++) {
          if (finst_i != finst_j) {
          // if (i != j) {
            sum_p += pow(finst_i * finst_j, 2.0) / (finst_i.t() * finst_j.t());
            // sum_p += pow(fs[i] * fs[j], 2.0) / (fs[i].t() * fs[j].t());
            cout << "not equal" << endl;
          } else {
            cout << "equal" << endl;
          }
        }
      }
      _h["Cparameter"]->fill(1.5 * (2 - 1 / (Q*Q) * sum_p), event);

      _h["jetcount"]->fill(jets.size(), event);
      for (unsigned int i=0; i < jets.size(); i++)
        _h["jetcount_incl"]->fill(i+1, event);

      _h["leadingjet_E"]->fill(jets[0].E(), event);
      _h["leadingjet_Theta"]->fill(cos(jets[0].theta()), event);
      _h["leadingjet_Pt"]->fill(jets[0].pt(), event);

      _h["2ndleadingjet_E"]->fill(jets[1].E(), event);
      _h["2ndleadingjet_Theta"]->fill(std::cos(jets[1].momentum().theta()), event);
      _h["2ndleadingjet_Pt"]->fill(jets[1].pt(), event);

      if (bjets.size() > 0) {
        _h["bjet_E"]->fill(bjets[0].E(), event);
        _h["bjet_Theta"]->fill(std::cos(bjets[0].theta()), event);
        _h["bjet_Pt"]->fill(bjets[0].pt(), event);
      }

      if (bbarjets.size() > 0) {
        _h["bbarjet_E"]->fill(bbarjets[0].E(), event);
        _h["bbarjet_Theta"]->fill(std::cos(bbarjets[0].theta()), event);
        _h["bbarjet_Pt"]->fill(bbarjets[0].pt(), event);
      }

      double jetsMass = (jets[0].momentum() + jets[1].momentum()).mass();
      _h["jets_invMass"]->fill(jetsMass, event);
      _h["jets_invMass_Zpeak"]->fill(jetsMass, event);
      _h["jets_invMass_Hpeak"]->fill(jetsMass, event);

      _h["Wm_E"]->fill(Wm.E(), event);
      _h["Wm_Pt"]->fill(Wm.pt(), event);
      _h["Wm_Theta"]->fill(std::cos(Wm.theta()), event);

      _h["Wp_E"]->fill(Wp.E(), event);
      _h["Wp_Pt"]->fill(Wp.pt(), event);
      _h["Wp_Theta"]->fill(std::cos(Wp.theta()), event);


      FourMomentum BB;
      if (bjets.size() > 0 && bbarjets.size() > 0) {
        BB = bjets[0].momentum()+bbarjets[0].momentum();
        _h["BB_Phi"]->fill(Rivet::deltaPhi(bjets[0].momentum(),bbarjets[0].momentum()), event);
        _h["BB_R"]->fill(Rivet::deltaR(bjets[0].momentum(),bbarjets[0].momentum()), event);
        _h["BB_invMass"]->fill(BB.mass(), event);
        _h["BB_invMass_Zpeak"]->fill(BB.mass(), event);
        _h["BB_invMass_Hpeak"]->fill(BB.mass(), event);
        _h["BB_E"]->fill(BB.E(), event);
        _h["BB_Pt"]->fill(BB.pt(), event);
        _h["BB_Theta"]->fill(std::cos(BB.theta()), event);
      }

      FourMomentum Topbar;
      if(wm.size() > 0 and bbarjets.size() > 0) {
        Topbar = Wm+bbarjets[0].momentum();
        _h["BWm_invMass"]->fill(Topbar.mass(), event);
        _h["BWm_invMass_peak"]->fill(Topbar.mass(), event);
        _h["BW_invMass"]->fill(Topbar.mass(), event);
        _h["BW_invMass_peak"]->fill(Topbar.mass(), event);
        _h["BWm_E"]->fill(Topbar.E(), event);
        _h["BWm_Pt"]->fill(Topbar.pt(), event);
        _h["BWm_ThreeMom"]->fill(Topbar.p3().mod(), event);
        _h["BWm_Theta"]->fill(std::cos(Topbar.theta()), event);
        _h["BWm_Phi"]->fill(Rivet::deltaPhi(bbarjets[0].momentum(),Wm), event);
        _h["BWm_R"]->fill(Rivet::deltaR(bbarjets[0].momentum(),Wm), event);
        if (std::cos(Topbar.theta()) > 0) {
          _h["A_FBbar"]->fillBin(0, event, +1.0);
        } else {
          _h["A_FBbar"]->fillBin(0, event, -1.0);
        }
        _h["Sum_Weightsbar"]->fillBin(0, event, +1.0);
      }

      FourMomentum Top;
      if(wp.size() > 0 and bjets.size() > 0) {
        Top = Wp+bjets[0].momentum();
        _h["BWp_invMass"]->fill(Top.mass(), event);
        _h["BWp_invMass_peak"]->fill(Top.mass(), event);
        _h["BW_invMass"]->fill(Top.mass(), event);
        _h["BW_invMass_peak"]->fill(Top.mass(), event);
        _h["BWp_E"]->fill(Top.E(), event);
        _h["BWp_Pt"]->fill(Top.pt(), event);
        _h["BWp_ThreeMom"]->fill(Top.p3().mod(), event);
        _h["BWp_Theta"]->fill(std::cos(Top.theta()), event);
        if (std::cos(Top.theta()) > 0) {
          _h["A_FB"]->fillBin(0, event, +1.0);
        } else {
          _h["A_FB"]->fillBin(0, event, -1.0);
        }
        _h["Sum_Weights"]->fillBin(0, event, +1.0);
        _h["BWp_Phi"]->fill(Rivet::deltaPhi(bjets[0].momentum(),Wp), event);
        _h["BWp_R"]->fill(Rivet::deltaR(bjets[0].momentum(),Wp), event);
      }
      // if(wm.size() > 0 and bbarjets.size() > 0 and wp.size() > 0 and bjets.size() > 0) {
      //   _h2["BWm_BWp_invMass_peak"]->fill(Top.mass(), Topbar.mass(), weight);
      // }

    }


    void finalize() {
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

      // scale(_h2["BWm_BWp_invMass_peak"], scale_factor);
      scale(_h["A_FB"], 1.0 / (crossSection() * fb_per_pb));
      scale(_h["A_FBbar"], 1.0 / (crossSection() * fb_per_pb));
      scale(_h["Sum_Weights"], 1.0 / (crossSection() * fb_per_pb));
      scale(_h["Sum_Weightsbar"], 1.0 / (crossSection() * fb_per_pb));

    }


  private:

    std::map <string, NLOHisto1DPtr> _h;
    // std::map <string, Histo2DPtr> _h2;

    int vetoCounter, eventCounter;
    double acceptedWeights;
  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(WHIZARD_2W2b_NLO);

}
