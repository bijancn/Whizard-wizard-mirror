// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"

//cut values
double cut_ptl = 0;
double cut_etal = 999999.;
double cut_dRlj = 0.0;      // lepton-jet speration


namespace Rivet {

  using namespace Cuts;

  class WHIZARD_4l2b_NLO : public Analysis {

#include "NLOHisto1D.cc"

  public:

    /// Constructor
    WHIZARD_4l2b_NLO()
      : Analysis("WHIZARD_4l2b_NLO")
    {    }

    /// Book histograms and initialise projections before the run
    void init() {
      const int stdbin = 20;

      //leptons
      const IdentifiedFinalState em(PID::ELECTRON);
      addProjection(em, "em");
      const IdentifiedFinalState ep(-PID::ELECTRON);
      addProjection(ep, "ep");
      const IdentifiedFinalState mm(PID::MUON);
      addProjection(mm, "mm");
      const IdentifiedFinalState mp(-PID::MUON);
      addProjection(mp, "mp");

      //neutrinos
      vector<PdgId> neu_ids;
      neu_ids += PID::NU_E, PID::NU_MU;
      const IdentifiedFinalState n(neu_ids);
      addProjection(n, "n");

      vector<PdgId> neubar_ids;
      neubar_ids += PID::NU_EBAR, PID::NU_MUBAR;
      const IdentifiedFinalState nb(neubar_ids);
      addProjection(nb, "nb");

      //b-quarks
      const IdentifiedFinalState b(PID::BQUARK);
      addProjection(b, "bquark");
      const IdentifiedFinalState bbar(-PID::BQUARK);
      addProjection(bbar, "bbarquark");

      // jets
      VetoedFinalState veto;
      veto.addVetoPairId(PID::MUON);
      veto.addVetoPairId(PID::ELECTRON);
      veto.addVetoPairId(PID::NU_MU);
      veto.addVetoPairId(PID::NU_E);

      const double R = 0.4; const double p = -1.0;      // Jet-Parameters
      fastjet::JetDefinition ee(fastjet::ee_genkt_algorithm, R, p, fastjet::E_scheme, fastjet::Best);
      FastJets jets(veto, ee);
      addProjection(jets, "Jets");

      _h["leadingjet_E"] = bookNLOHisto1D("leading-jet-E", stdbin, 0., 400.);
      _h["leadingjet_Pt"] = bookNLOHisto1D("leading-jet-pT", stdbin, 0., 400.);
      _h["leadingjet_Theta"] = bookNLOHisto1D("leading-jet-Theta", stdbin, -1.1, 1.1);

      _h["2ndleadingjet_E"] = bookNLOHisto1D("2nd-leading-jet-E", stdbin, 0., 300.);
      _h["2ndleadingjet_Pt"] = bookNLOHisto1D("2nd-leading-jet-pT", stdbin, 0., 300.);
      _h["2ndleadingjet_Theta"] = bookNLOHisto1D("2nd-leading-jet-Theta", stdbin, -1.1, 1.1);

      _h["jets_invMass"] = bookNLOHisto1D("jets-inv", stdbin, 0., 600.);
      _h["jets_invMass_Zpeak"] = bookNLOHisto1D("jets-inv-Zpeak", stdbin, 80., 100.);
      _h["jets_invMass_Hpeak"] = bookNLOHisto1D("jets-inv-Hpeak", stdbin, 115.1, 135.1);

      _h["bjet_E"] = bookNLOHisto1D("b-jet-E", stdbin, 0., 425.);
      _h["bjet_Pt"] = bookNLOHisto1D("b-jet-pT", stdbin, 0., 400.);
      _h["bjet_Theta"] = bookNLOHisto1D("b-jet-Theta", stdbin, -1.1, 1.1);

      _h["bbarjet_E"] = bookNLOHisto1D("bbar-jet-E", stdbin, 0., 425.);
      _h["bbarjet_Pt"] = bookNLOHisto1D("bbar-jet-pT", stdbin, 0., 400.);
      _h["bbarjet_Theta"] = bookNLOHisto1D("bbar-jet-Theta", stdbin, -1.1, 1.1);

      _h["Wm_E"] = bookNLOHisto1D("Wm-E", stdbin, 0., 425.);
      _h["Wm_Pt"] = bookNLOHisto1D("Wm-pT", stdbin, 0., 400.);
      _h["Wm_Theta"] = bookNLOHisto1D("Wm-Theta", stdbin, -1.1, 1.1);
      _h["Wm_invMass"] = bookNLOHisto1D("Wm-inv", stdbin, 0., 600.);
      _h["Wm_invMass_peak"] = bookNLOHisto1D("Wm-inv-peak", stdbin, 70., 90.);

      _h["Wp_E"] = bookNLOHisto1D("Wp-E", stdbin, 0., 425.);
      _h["Wp_Pt"] = bookNLOHisto1D("Wp-pT", stdbin, 0., 400.);
      _h["Wp_Theta"] = bookNLOHisto1D("Wp-Theta", stdbin, -1.1, 1.1);
      _h["Wp_invMass"] = bookNLOHisto1D("Wp-inv", stdbin, 0., 600.);
      _h["Wp_invMass_peak"] = bookNLOHisto1D("Wp-inv-peak", stdbin, 70., 90.);

      _h["BWm_E"] = bookNLOHisto1D("BWm-E", stdbin, 0., 700.);
      _h["BWm_Pt"] = bookNLOHisto1D("BWm-pT", stdbin, 0., 400.);
      _h["BWm_Theta"] = bookNLOHisto1D("BWm-Theta", stdbin, -1.1, 1.1);
      _h["BWm_Phi"] = bookNLOHisto1D("Phi(b,Wm)", stdbin, 0., M_PI);
      _h["BWm_R"] = bookNLOHisto1D("R(b,Wm)", stdbin, 0., 5.);
      _h["BWm_invMass"] = bookNLOHisto1D("BWm-inv", stdbin, 0., 600.);
      _h["BWm_invMass_peak"] = bookNLOHisto1D("BWm-inv-peak", stdbin, 160., 180.);

      _h["BWp_E"] = bookNLOHisto1D("BWp-E", stdbin, 0., 700.);
      _h["BWp_Pt"] = bookNLOHisto1D("BWp-pT", stdbin, 0., 400.);
      _h["BWp_Theta"] = bookNLOHisto1D("BWp-Theta", stdbin, -1.1, 1.1);
      _h["BWp_Phi"] = bookNLOHisto1D("Phi(b,Wp)", stdbin, 0., M_PI);
      _h["BWp_R"] = bookNLOHisto1D("R(b,Wp)", stdbin, 0., 5.);
      _h["BWp_invMass"] = bookNLOHisto1D("BWp-inv", stdbin, 0., 600.);
      _h["BWp_invMass_peak"] = bookNLOHisto1D("BWp-inv-peak", stdbin, 160., 180.);

      _h["Blm_E"] = bookNLOHisto1D("Blm-E", stdbin, 0., 525.);
      _h["Blm_Theta"] = bookNLOHisto1D("Blm-Theta", stdbin, -1.1, 1.1);
      _h["Blm_Pt"] = bookNLOHisto1D("Blm-pT", stdbin, 0., 400.);
      _h["Blm_invMass"] = bookNLOHisto1D("Blm-inv", stdbin, 0., 300.);
      _h["Blm_Phi"] = bookNLOHisto1D("Phi(b,lm)", stdbin, 0., M_PI);
      _h["Blm_R"] = bookNLOHisto1D("R(b,lm)", stdbin, 0., 5.);

      _h["Blp_E"] = bookNLOHisto1D("Blp-E", stdbin, 0., 525.);
      _h["Blp_Theta"] = bookNLOHisto1D("Blp-Theta", stdbin, -1.1, 1.1);
      _h["Blp_Pt"] = bookNLOHisto1D("Blp-pT", stdbin, 0., 400.);
      _h["Blp_invMass"] = bookNLOHisto1D("Blp-inv", stdbin, 0., 300.);
      _h["Blp_Phi"] = bookNLOHisto1D("Phi(b,lp)", stdbin, 0, M_PI);
      _h["Blp_R"] = bookNLOHisto1D("R(b,lp)", stdbin, 0., 5.);

      _h["BB_E"] = bookNLOHisto1D("BB-E", stdbin, 0., 625.);
      _h["BB_Theta"] = bookNLOHisto1D("BB-Theta", stdbin, -1.1, 1.1);
      _h["BB_Pt"] = bookNLOHisto1D("BB-pT", stdbin, 0., 400.);
      _h["BB_invMass"] = bookNLOHisto1D("BB-inv", stdbin, 0., 600.);
      _h["BB_invMass_Zpeak"] = bookNLOHisto1D("BB-inv-Zpeak", stdbin, 80., 100.);
      _h["BB_invMass_Hpeak"] = bookNLOHisto1D("BB-inv-Hpeak", stdbin, 115.1, 135.1);
      _h["BB_Phi"] = bookNLOHisto1D("Phi(b,b)", stdbin, 0, M_PI);
      _h["BB_R"] = bookNLOHisto1D("R(b,b)", stdbin, 0., 5.);

      _h["W_invMass"] = bookNLOHisto1D("W-inv", stdbin, 0., 600.);
      _h["W_invMass_peak"] = bookNLOHisto1D("W-inv-peak", stdbin, 70., 90.);
      _h["BW_invMass"] = bookNLOHisto1D("BW-inv", stdbin, 0., 700.);
      _h["BW_invMass_peak"] = bookNLOHisto1D("BW-inv-peak", stdbin, 160., 180.);
      _h["Bl_invMass"] = bookNLOHisto1D("Bl-inv", stdbin, 0., 300.);

      _h["hardest_lepton_E"] = bookNLOHisto1D("hardest-lepton-E", stdbin, 0., 400.);
      _h["hardest_lepton_Pt"] = bookNLOHisto1D("hardest-lepton-pT", stdbin, 0., 400.);
      _h["hardest_lepton_Eta"] = bookNLOHisto1D("hardest-lepton-eta", stdbin, -3., 3.);

      _h["2nd_hardest_lepton_E"] = bookNLOHisto1D("2nd-hardest-lepton-E", stdbin, 0., 400.);
      _h["2nd_hardest_lepton_Pt"] = bookNLOHisto1D("2nd-hardest-lepton-pT", stdbin, 0., 300.);
      _h["2nd_hardest_lepton_Eta"] = bookNLOHisto1D("2nd-hardest-lepton-Eta", stdbin, -3., 3.);

      _h["electron_E"] = bookNLOHisto1D("electron-E", stdbin, 0., 400.);
      _h["electron_Pt"] = bookNLOHisto1D("electron-Pt", stdbin, 0., 350.);
      _h["electron_Eta"] = bookNLOHisto1D("electron-Eta", stdbin, -3., 3.);

      _h["muon_E"] = bookNLOHisto1D("muon-E", stdbin, 0., 350.);
      _h["muon_Pt"] = bookNLOHisto1D("muon-Pt", stdbin, 0., 350.);
      _h["muon_Eta"] = bookNLOHisto1D("muon-Eta", stdbin, -3., 3.);

      _h["lepton_lepton_phi"] = bookNLOHisto1D("Phi(l+,l-)", stdbin, 0., M_PI+0.5);
      _h["lepton_lepton_R"] = bookNLOHisto1D("R(l+,l-)", stdbin, 0., 5.);
      _h["lepton_lepton_E"] = bookNLOHisto1D("lepton-lepton-E", stdbin, 0., 600.);
      _h["lepton_lepton_Pt"] = bookNLOHisto1D("lepton-lepton-Pt", stdbin, 0., 350.);
      _h["lepton_lepton_Theta"] = bookNLOHisto1D("lepton-lepton-Theta", stdbin, -1.1, 1.1);

      _h["MET"] = bookNLOHisto1D("MET", stdbin, 0, 450.0);
      _h["MPT"] = bookNLOHisto1D("MPT", stdbin, 0, 350.0);
      _h["electron_MET_phi"] = bookNLOHisto1D("Phi(l-,MET)", stdbin, 0., M_PI);
      _h["muon_MET_phi"] = bookNLOHisto1D("Phi(l+,MET)", stdbin, 0., M_PI);
      _h["muon_MET_R"] = bookNLOHisto1D("R(l+,MET)", stdbin, 0., 5.);
      _h["electron_MET_R"] = bookNLOHisto1D("R(l-,MET)", stdbin, 0., 5.);

      _h["b_MET_phi"] = bookNLOHisto1D("Phi(b,MET)", stdbin, 0., M_PI);
      _h["bbar_MET_phi"] = bookNLOHisto1D("Phi(bbar,MET)", stdbin, 0., M_PI);
      _h["b_MET_R"] = bookNLOHisto1D("R(b,MET)", stdbin, 0., 5.);
      _h["bbar_MET_R"] = bookNLOHisto1D("R(bbar,MET)", stdbin, 0., 5.);


      _h["jetcount"] = bookNLOHisto1D("jet-count", 4, 0.5, 4.5);
      _h["jetcount_incl"] = bookNLOHisto1D("jet-count-incl", 4, 0.5, 4.5);

      vetoCounter = 0;
      eventCounter = 0;
      acceptedWeights = 0.;
      low_energy_counts = 0;
      low_energy_weights = 0.;
    }

    void analyze(const Event& event) {
      double weight = event.weight();


      Jets jets, bjets, bbarjets, ljets;

      // get the b quarks
      ParticleVector bpartons    = applyProjection<IdentifiedFinalState>(event, "bquark").particlesByPt();
      ParticleVector bbarpartons = applyProjection<IdentifiedFinalState>(event, "bbarquark").particlesByPt();

      //get the jets
      const FastJets& fastjets = applyProjection<FastJets>(event, "Jets");
      double minjetE = 1. * GeV;
      const PseudoJets pseudo_jets = fastjets.pseudoJetsByE(minjetE);

      // tag b-jets
      foreach (const PseudoJet & pseudo_jet, pseudo_jets) {
        vector<PseudoJet> constituents = pseudo_jet.constituents();
        bool is_b=false;
        foreach (const PseudoJet& constituent, constituents) {
          foreach(const Particle & bparton, bpartons) {
            if (have_same_momentum (constituent, bparton)) { bjets.push_back(pseudo_jet); is_b=true; }    // b-jet
          }
          foreach(const Particle & bbarparton, bbarpartons) {
            if (have_same_momentum (constituent, bbarparton))  { bbarjets.push_back(pseudo_jet); is_b=true; } //bbar-jet
          }
        }
        if (!is_b) ljets.push_back(pseudo_jet); // if not bjet -> light-jet
        jets.push_back(pseudo_jet);   // all jets
      }


      // get the leptons
      ParticleVector cand_em = applyProjection<IdentifiedFinalState>(event, "em").particlesByPt();
      ParticleVector cand_ep = applyProjection<IdentifiedFinalState>(event, "ep").particlesByPt();
      ParticleVector cand_mm = applyProjection<IdentifiedFinalState>(event, "mm").particlesByPt();
      ParticleVector cand_mp = applyProjection<IdentifiedFinalState>(event, "mp").particlesByPt();
      // get the neutrinos
      ParticleVector n = applyProjection<IdentifiedFinalState>(event, "n").particlesByPt();
      ParticleVector nb = applyProjection<IdentifiedFinalState>(event, "nb").particlesByPt();

       // Lepton-Finder: apply lepton cuts and discard leptons that overlap with jets
       ParticleVector em;
       foreach ( const Particle & e, cand_em ) {
         if( fabs(e.eta()) > cut_etal || e.momentum().perp() < cut_ptl ) continue;
         bool e_near_jet = false;
         foreach ( const Jet& jet, jets ) {
           if(Rivet::deltaR(e.momentum(),jet.momentum()) < cut_dRlj) {
             e_near_jet = true;
             break;
           }
         }
         if ( e_near_jet ) continue;
         em.push_back(e);
       }

       ParticleVector ep;
       foreach ( const Particle & e, cand_ep ) {
         if( fabs(e.eta()) > cut_etal || e.momentum().perp() < cut_ptl ) continue;
         bool e_near_jet = false;
         foreach ( const Jet& jet, jets ) {
           if(Rivet::deltaR(e.momentum(),jet.momentum()) < cut_dRlj) {
             e_near_jet = true;
             break;
           }
         }
         if ( e_near_jet ) continue;
         ep.push_back(e);
        }

       ParticleVector mp;
       foreach ( const Particle & e, cand_mp ) {
         if( fabs(e.eta()) > cut_etal || e.momentum().perp() < cut_ptl ) continue;
         bool e_near_jet = false;
         foreach ( const Jet& jet, jets ) {
           if(Rivet::deltaR(e.momentum(),jet.momentum()) < cut_dRlj) {
             e_near_jet = true;
             break;
           }
         }
         if ( e_near_jet ) continue;
         mp.push_back(e);
       }

       ParticleVector mm;
       foreach ( const Particle & e, cand_mm ) {
         if( fabs(e.eta()) > cut_etal || e.momentum().perp() < cut_ptl ) continue;
         bool e_near_jet = false;
         foreach ( const Jet& jet, jets ) {
           if(Rivet::deltaR(e.momentum(),jet.momentum()) < cut_dRlj) {
             e_near_jet = true;
             break;
           }
         }
         if ( e_near_jet ) continue;
         mm.push_back(e);
       }


      // sort leptons
      ParticleVector e, m, l, lp, lm, neu;
      foreach (const Particle & p, em) { e.push_back(p); l.push_back(p); lm.push_back(p); }
      foreach (const Particle & p, ep) { e.push_back(p); l.push_back(p); lp.push_back(p); }
      foreach (const Particle & p, mm) { m.push_back(p); l.push_back(p); lm.push_back(p); }
      foreach (const Particle & p, mp) { m.push_back(p); l.push_back(p); lp.push_back(p); }
      foreach (const Particle & p, n)  { neu.push_back(p); }
      foreach (const Particle & p, nb) { neu.push_back(p); }

      sort(l.begin(),l.end(),cmpMomByPt);
      sort(lm.begin(),lm.end(),cmpMomByPt);
      sort(lp.begin(),lp.end(),cmpMomByPt);

      // pTmiss from neutrinos
      FourMomentum pTmiss;
      foreach ( const Particle & p, neu ) { pTmiss += p.momentum(); }
      double missingET = pTmiss.Et();
      double missingPT = pTmiss.pt();  // "missingET" = missingPT?

      bool cutHiggs = true;

      eventCounter++;
      bool vetoCondition = jets.size() < 2;
      ///if (cutHiggs and not vetoCondition) {
      ///   FourMomentum BB;
      ///   if (bjets.size() > 0 && bbarjets.size() > 0) {
      ///      BB = bjets[0].momentum()+bbarjets[0].momentum();
      ///      double mH = 125.;
      ///      int nGammaH = 200;
      ///      double GammaH = 0.004;
      ///      vetoCondition = abs (mH - BB.mass()) < nGammaH * GammaH;
      ///   }
      ///}
      if (vetoCondition) {
        vetoCounter++;
        vetoEvent;
      }
      else {
        acceptedWeights += weight;
      }

      //fill jet distributions
      _h["jetcount"]->fill(jets.size(), event);
      for (unsigned int i=0; i < jets.size(); i++) {
        _h["jetcount_incl"]->fill(i+1, event);
      }

      _h["leadingjet_E"]->fill(jets[0].E(), event);
      _h["leadingjet_Theta"]->fill(cos(jets[0].theta()), event);
      _h["leadingjet_Pt"]->fill(jets[0].pt(), event);

      _h["2ndleadingjet_E"]->fill(jets[1].E(), event);
      _h["2ndleadingjet_Theta"]->fill(std::cos(jets[1].momentum().theta()), event);
      _h["2ndleadingjet_Pt"]->fill(jets[1].pt(), event);

      if (bjets.size() > 0) _h["bjet_E"]->fill(bjets[0].E(), event);
      if (bjets.size() > 0) _h["bjet_Theta"]->fill(std::cos(bjets[0].theta()), event);
      if (bjets.size() > 0) _h["bjet_Pt"]->fill(bjets[0].pt(), event);

      if (bbarjets.size() > 0) _h["bbarjet_E"]->fill(bbarjets[0].E(), event);
      if (bbarjets.size() > 0) _h["bbarjet_Theta"]->fill(std::cos(bbarjets[0].theta()), event);
      if (bbarjets.size() > 0) _h["bbarjet_Pt"]->fill(bbarjets[0].pt(), event);

      double jetsMass = (jets[0].momentum() + jets[1].momentum()).mass();
      _h["jets_invMass"]->fill(jetsMass, event);
      _h["jets_invMass_Zpeak"]->fill(jetsMass, event);
      _h["jets_invMass_Hpeak"]->fill(jetsMass, event);

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

      //fill lepton distributions
      if(l.size() > 0) _h["hardest_lepton_Pt"]->fill(l[0].momentum().pt(), event);
      if(l.size() > 0) _h["hardest_lepton_Eta"]->fill(l[0].momentum().eta(), event);
      if(l.size() > 0) _h["hardest_lepton_E"]->fill(l[0].momentum().E(), event);

      if(l.size() > 1) _h["2nd_hardest_lepton_Pt"]->fill(l[1].momentum().pt(), event);
      if(l.size() > 1) _h["2nd_hardest_lepton_Eta"]->fill(l[1].momentum().eta(), event);
      if(l.size() > 1) _h["2nd_hardest_lepton_E"]->fill(l[1].momentum().E(), event);

      if(e.size() > 0) _h["electron_E"]->fill(e[0].momentum().E(), event);
      if(e.size() > 0) _h["electron_Pt"]->fill(e[0].momentum().pt(), event);
      if(e.size() > 0) _h["electron_Eta"]->fill(e[0].momentum().eta(), event);

      if(m.size() > 0) _h["muon_E"]->fill(m[0].momentum().E(), event);
      if(m.size() > 0) _h["muon_Pt"]->fill(m[0].momentum().pt(), event);
      if(m.size() > 0) _h["muon_Eta"]->fill(m[0].momentum().eta(), event);

      if(l.size() > 1) _h["lepton_lepton_phi"]->fill(Rivet::deltaPhi(l[0].momentum(), l[1].momentum()), event);
      if(l.size() > 1) _h["lepton_lepton_R"]->fill(Rivet::deltaR(l[0].momentum(), l[1].momentum()), event);
      if(l.size() > 1) _h["lepton_lepton_E"]->fill((l[0].momentum()+l[1].momentum()).E(), event);
      if(l.size() > 1) _h["lepton_lepton_Pt"]->fill((l[0].momentum()+l[1].momentum()).pt(), event);
      if(l.size() > 1) _h["lepton_lepton_Theta"]->fill(std::cos((l[0].momentum()+l[1].momentum()).theta()), event);

      //fill MET distributions
      _h["MET"]->fill(missingET, event);
      _h["MPT"]->fill(missingPT, event);

      if(e.size() > 0) _h["electron_MET_phi"]->fill(Rivet::deltaPhi(e[0].momentum(),pTmiss), event);
      if(e.size() > 0) _h["electron_MET_R"]->fill(Rivet::deltaR(e[0].momentum(),pTmiss), event);
      if(m.size() > 0) _h["muon_MET_phi"]->fill(Rivet::deltaPhi(m[0].momentum(),pTmiss), event);
      if(m.size() > 0) _h["muon_MET_R"]->fill(Rivet::deltaR(m[0].momentum(),pTmiss), event);

      if(bjets.size() > 0) _h["b_MET_phi"]->fill(Rivet::deltaPhi(bjets[0].momentum(),pTmiss), event);
      if(bjets.size() > 0) _h["b_MET_R"]->fill(Rivet::deltaR(bjets[0].momentum(),pTmiss), event);
      if(bbarjets.size() > 0) _h["bbar_MET_phi"]->fill(Rivet::deltaPhi(bbarjets[0].momentum(),pTmiss), event);
      if(bbarjets.size() > 0) _h["bbar_MET_R"]->fill(Rivet::deltaR(bbarjets[0].momentum(),pTmiss), event);

      //fill reconstructed distributions
      FourMomentum Wm;
      if(lm.size() > 0 && nb.size() > 0) {
        Wm = lm[0].momentum()+nb[0].momentum();
        _h["Wm_invMass"]->fill(Wm.mass(), event);
        _h["Wm_invMass_peak"]->fill(Wm.mass(), event);
        _h["W_invMass"]->fill(Wm.mass(), event);
        _h["W_invMass_peak"]->fill(Wm.mass(), event);
        _h["Wm_E"]->fill(Wm.E(), event);
        _h["Wm_Pt"]->fill(Wm.pt(), event);
        _h["Wm_Theta"]->fill(std::cos(Wm.theta()), event);
      }

      FourMomentum Wp;
      if(lp.size() > 0 && n.size()  > 0) {
        Wp = lp[0].momentum()+n[0].momentum();
        _h["Wp_invMass"]->fill(Wp.mass(), event);
        _h["Wp_invMass_peak"]->fill(Wp.mass(), event);
        _h["W_invMass"]->fill(Wp.mass(), event);
        _h["W_invMass_peak"]->fill(Wp.mass(), event);
        _h["Wp_E"]->fill(Wp.E(), event);
        _h["Wp_Pt"]->fill(Wp.pt(), event);
        _h["Wp_Theta"]->fill(std::cos(Wp.theta()), event);
      }

      FourMomentum Topbar;
      if(lm.size() > 0 && nb.size() > 0 && bbarjets.size() > 0) {
        Topbar = Wm+bbarjets[0].momentum();
        _h["BWm_invMass"]->fill(Topbar.mass(), event);
        _h["BWm_invMass_peak"]->fill(Topbar.mass(), event);
        _h["BW_invMass"]->fill(Topbar.mass(), event);
        _h["BW_invMass_peak"]->fill(Topbar.mass(), event);
        _h["BWm_E"]->fill(Topbar.E(), event);
        _h["BWm_Pt"]->fill(Topbar.pt(), event);
        _h["BWm_Theta"]->fill(std::cos(Topbar.theta()), event);
        _h["BWm_Phi"]->fill(Rivet::deltaPhi(bbarjets[0].momentum(),Wm), event);
        _h["BWm_R"]->fill(Rivet::deltaR(bbarjets[0].momentum(),Wm), event);
      }

      FourMomentum Top;
      if(lp.size() > 0 && n.size() > 0  && bjets.size() > 0) {
        Top = Wp+bjets[0].momentum();
        _h["BWp_invMass"]->fill(Top.mass(), event);
        _h["BWp_invMass_peak"]->fill(Top.mass(), event);
        _h["BW_invMass"]->fill(Top.mass(), event);
        _h["BW_invMass_peak"]->fill(Top.mass(), event);
        _h["BWp_E"]->fill(Top.E(), event);
        _h["BWp_Pt"]->fill(Top.pt(), event);
        _h["BWp_Theta"]->fill(std::cos(Top.theta()), event);
        _h["BWp_Phi"]->fill(Rivet::deltaPhi(bjets[0].momentum(),Wp), event);
        _h["BWp_R"]->fill(Rivet::deltaR(bjets[0].momentum(),Wp), event);
      }

      FourMomentum Blm;
      if(lm.size() > 0 && bbarjets.size() > 0) {
        Blm = lm[0].momentum()+bbarjets[0].momentum();
        _h["Blm_Phi"]->fill(Rivet::deltaPhi(bbarjets[0].momentum(),lm[0].momentum()), event);
        _h["Blm_R"]->fill(Rivet::deltaR(bbarjets[0].momentum(),lm[0].momentum()), event);
        _h["Blm_invMass"]->fill(Blm.mass(), event);
        _h["Bl_invMass"]->fill(Blm.mass(), event);
        _h["Blm_E"]->fill(Blm.E(), event);
        _h["Blm_Pt"]->fill(Blm.pt(), event);
        _h["Blm_Theta"]->fill(std::cos(Blm.theta()), event);
      }

      FourMomentum Blp;
      if(lp.size() > 0 && bjets.size() > 0) {
        Blp = lp[0].momentum()+bjets[0].momentum();
        _h["Blp_Phi"]->fill(Rivet::deltaPhi(bjets[0].momentum(),lp[0].momentum()), event);
        _h["Blp_R"]->fill(Rivet::deltaR(bjets[0].momentum(),lp[0].momentum()), event);
        _h["Blp_invMass"]->fill(Blp.mass(), event);
        _h["Bl_invMass"]->fill(Blp.mass(), event);
        _h["Blp_E"]->fill(Blp.E(), event);
        _h["Blp_Pt"]->fill(Blp.pt(), event);
        _h["Blp_Theta"]->fill(std::cos(Blp.theta()), event);
      }


    } // analyze


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
      cout << "Number of vetoed events: " << vetoCounter << endl;
      cout << "Share of vetoed events: " << vetoCounter * 1.0 / (eventCounter * 1.0) * 100 << " %" << endl;
      cout << "Final (fiducial) cross section (fb): " << fiducial_xsection << endl;
      cout << "Scale factor: " << scale_factor << endl;
      cout << "Gluon weights below 5 GeV: " << low_energy_weights << endl;
      cout << "Number of gluon emissions below 5 GeV: " << low_energy_counts << endl;

      typedef std::map<string, NLOHisto1DPtr>::iterator it;

      for(it iter = _h.begin(); iter != _h.end(); iter++) {
        iter->second->finalize();
        scale(iter->second,scale_factor);
      }

    } // finalyze


  private:

    std::map <string, NLOHisto1DPtr> _h;

    int vetoCounter, eventCounter;
    int low_energy_counts;
    double low_energy_weights;
    double acceptedWeights;
  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(WHIZARD_4l2b_NLO);

}
