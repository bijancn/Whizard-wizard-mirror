// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/Sphericity.hh"
#include "Rivet/Projections/Thrust.hh"

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
      const int stdbin = 30;
      addProjection(fs, "FS");
      //const Thrust thrust(fs);
      //addProjection(thrust, "Thrust");
      //addProjection(Sphericity(fs), "Sphericity");

      //_h_Thrust = bookHisto1D("Thrust", 30, 0, 0.45);
      //_h_ThrustMajor = bookHisto1D("ThrustMajor", 30, 0, 0.7);
      //_h_ThrustMinor = bookHisto1D("ThrustMinor", 30, 0, 0.6);
      //_h_Oblateness = bookHisto1D("Oblateness", 30, 0, 0.6);
      //_h_Sphericity = bookHisto1D("Sphericity", 30, 0, 0.8);
      //_h_Aplanarity = bookHisto1D("Aplanarity", 30, 0, 0.3);
      //_h_Planarity = bookHisto1D("Planarity", 30, 0, 0.5);

      // Definition of the Durham algorithm
      //fastjet::JetDefinition durham_def(fastjet::ee_kt_algorithm, fastjet::E_scheme, fastjet::Best);
      fastjet::JetDefinition gen_smallR(fastjet::ee_genkt_algorithm, 1.0, 1.0, fastjet::E_scheme, fastjet::Best);
      FastJets jets(fs, FastJets::ANTIKT, 1.0); // negative jet count
      //JetDefinition jet_def(ee_genkt_algorithm, 1.0, 1);
      //FastJets jets(fs, gen_smallR);
      //FastJets durhamJets = FastJets(fs, FastJets::DURHAM, 0.7); // negative jet count
      FastJets durhamJets = FastJets(fs, FastJets::DURHAM, 1.0);
      addProjection(jets, "Jets");
      addProjection(durhamJets, "DurhamJets");

      //_h_q_Pt = bookHisto1D("quark-pT", stdbin, 0., 260.);
      _h_g_Pt = bookHisto1D("gluon-pT", stdbin, 0., 260.);

      //_h_q_E = bookHisto1D("quark-E", stdbin, 0., 260.);
      _h_g_E = bookHisto1D("gluon-E", stdbin, 0., 260.);

      //_h_qq_invMass = bookHisto1D("qq-inv", stdbin, 0., 500.);
      _h_jets_invMass = bookHisto1D("jets-inv", stdbin, 10., 510.);

      //_h_jetcount = bookHisto1D("jet-count", 4, 0.5, 4.5);
      //_h_durhamjetcount = bookHisto1D("durhamjet-count", 4, 0.5, 4.5);
      //_h_jetpt = bookHisto1D("jet-pT", stdbin, 0., 200.);
      //_h_durhamjetpt = bookHisto1D("durhamjet-pT", stdbin, 0., 260.);
      //_h_jetptlog = bookHisto1D("jet-pT-log", stdbin, 1., 5.7);
      _h_leadingjetPt = bookHisto1D("leading-jet-pT", stdbin, 25., 260.);
      _h_leadingjetEta = bookHisto1D("leading-jet-eta", stdbin, -5., 5.);
      _h_secondleadingjetPt = bookHisto1D("second-leading-jet-pT", stdbin, 0., 260.);
      _h_secondleadingjetEta = bookHisto1D("second-leading-jet-eta", stdbin, -5., 5.);

      vetoCounter = 0;
      eventCounter = 0;
      acceptedWeights = 0.0;
    }

    void analyze(const Event& event) {

      const FastJets& fastjets = applyProjection<FastJets>(event, "Jets");
      const FastJets& durhamjets = applyProjection<FastJets>(event, "DurhamJets");
      const FinalState& fs = applyProjection<FinalState>(event, "FS");
      double minjetpt = 10.0 * GeV;
      const double m_delta = 1.0 * GeV;
      const double m_top = 173.0 * GeV;
      const Jets jets = fastjets.jetsByPt();
      const Jets durjets = fastjets.jetsByPt();
      double weight = event.weight();

      eventCounter++;
      bool vetoCondition = fs.particles().size() < 2 or jets.size() <= 1;
      vetoCondition = false;
      if (vetoCondition) {
        vetoCounter++;
        vetoEvent;
      }
      else {
        acceptedWeights += weight;
      }

      //const Thrust& thrust = applyProjection<Thrust>(event, "Thrust");
      //_h_Thrust->fill(1-thrust.thrust(), weight);
      //_h_ThrustMajor->fill(thrust.thrustMajor(), weight);
      //_h_ThrustMinor->fill(thrust.thrustMinor(), weight);
      //_h_Oblateness->fill(thrust.oblateness(), weight);
      //const Sphericity& sphericity = applyProjection<Sphericity>(event, "Sphericity");
      //const double sph = sphericity.sphericity();
      //const double apl = sphericity.aplanarity();
      //const double pl = sphericity.planarity();
      //_h_Sphericity->fill(sph, weight);
      //_h_Aplanarity->fill(apl, weight);
      //_h_Planarity->fill(pl, weight);

      //_h_jetcount->fill(jets.size(), weight);
      //_h_durhamjetcount->fill(jets.size(), weight);
      _h_leadingjetPt->fill(jets[0].pT(), weight);
      _h_leadingjetEta->fill(jets[0].eta(), weight);
      _h_secondleadingjetPt->fill(jets[1].pT(), weight);
      _h_secondleadingjetEta->fill(jets[1].eta(), weight);
      FourMomentum p_sum = jets[0].momentum() + jets[1].momentum();
      _h_jets_invMass->fill(p_sum.mass(), weight);
      //foreach(Jet j, jets) {
        //_h_jetpt->fill(j.pT(), weight / jets.size());
        //_h_durhamjetpt->fill(j.pT(), weight / jets.size());
        //_h_jetptlog->fill(log(j.pT()), weight / jets.size());
      //}

      // Register single particle properties
      foreach (const Particle& p, fs.particles()) {
        int id = p.pid();
        if(id == PID::UQUARK) {
          //_h_q_Pt->fill(p.pT()/GeV, weight);
          //_h_q_E->fill(p.E()/GeV, weight);
        } else if(id == PID::GLUON) {
          _h_g_Pt->fill(p.pT()/GeV, weight);
          _h_g_E->fill(p.E()/GeV, weight);
        }
      }

      // Compute invariant masses
      //foreach (const Particle& p1, fs.particles()) {
        //foreach (const Particle& p2, fs.particles()) {
          //int id1 = p1.pid(); int id2 = p2.pid();
          //if (id1 == PID::UQUARK && id2 == -PID::UQUARK) {
            //FourMomentum p_sum = p1.momentum() + p2.momentum();
            //_h_qq_invMass->fill(p_sum.mass(), weight);
          //}
        //}
      //}
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
      cout << "Number of vetoed events: " << vetoCounter << endl;
      cout << "Final (fiducial) cross section (fb): " << fiducial_xsection << endl;
      cout << "Scale factor: " << scale_factor << endl;

      //scale(_h_Thrust, scale_factor);
      //scale(_h_ThrustMajor, scale_factor);
      //scale(_h_ThrustMinor, scale_factor);
      //scale(_h_Oblateness, scale_factor);
      //scale(_h_Sphericity, scale_factor);
      //scale(_h_Aplanarity, scale_factor);
      //scale(_h_Planarity, scale_factor);

      //scale(_h_q_Pt, scale_factor);
      scale(_h_g_Pt, scale_factor);
      //scale(_h_q_E, scale_factor);
      scale(_h_g_E, scale_factor);

      //scale(_h_qq_invMass, scale_factor);
      scale(_h_jets_invMass, scale_factor);

      //scale(_h_jetcount, scale_factor);
      //scale(_h_durhamjetcount, scale_factor);
      //scale(_h_jetpt, scale_factor);
      //scale(_h_durhamjetpt, scale_factor);
      //scale(_h_jetptlog, scale_factor);
      scale(_h_leadingjetPt, scale_factor);
      scale(_h_leadingjetEta, scale_factor);
      scale(_h_secondleadingjetPt, scale_factor);
      scale(_h_secondleadingjetEta, scale_factor);
    }


  private:

    //Histo1DPtr _h_Thrust;
    //Histo1DPtr _h_ThrustMajor;
    //Histo1DPtr _h_ThrustMinor;
    //Histo1DPtr _h_Oblateness;
    //Histo1DPtr _h_Sphericity;
    //Histo1DPtr _h_Aplanarity;
    //Histo1DPtr _h_Planarity;

    //Histo1DPtr _h_q_Pt;
    Histo1DPtr _h_g_Pt;
    //Histo1DPtr _h_q_E;
    Histo1DPtr _h_g_E;

    //Histo1DPtr _h_qq_invMass;
    Histo1DPtr _h_jets_invMass;

    //Histo1DPtr _h_jetcount;
    //Histo1DPtr _h_durhamjetcount;
    //Histo1DPtr _h_jetpt;
    //Histo1DPtr _h_durhamjetpt;
    //Histo1DPtr _h_jetptlog;
    Histo1DPtr _h_leadingjetPt;
    Histo1DPtr _h_leadingjetEta;
    Histo1DPtr _h_secondleadingjetPt;
    Histo1DPtr _h_secondleadingjetEta;

    int vetoCounter, eventCounter;
    double acceptedWeights;
  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(WHIZARD_2015_NLO);

}
