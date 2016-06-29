#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"
#include "Rivet/Projections/VetoedFinalState.hh"
#include "Rivet/Projections/ChargedFinalState.hh"
#include "Rivet/Projections/IdentifiedFinalState.hh"

namespace Rivet {

  using namespace Cuts;

  class WHIZARD : public Analysis {

  public:

    /// Constructor
    WHIZARD()
      : Analysis("WHIZARD")
    {    }

    /// Book histograms and initialise projections before the run
    void init() {
      const FinalState fs;
      const int stdbin = 15;


      const double R = 0.4; const double p = -1.0;
      fastjet::JetDefinition ee(fastjet::ee_genkt_algorithm, R, p,
          fastjet::E_scheme, fastjet::Best);
      FastJets jets(fs, ee);

      addProjection(fs, "FS");
      addProjection(jets, "Jets");
      addProjection(ChargedFinalState(), "CFS");
      addProjection(VisibleFinalState(), "VFS");

      _h["numberOfChargedTracks"] = bookHisto1D("numberOfChargedTracks",
          stdbin, 0., 100.);

      _h["numberOfJets"] = bookHisto1D("numberOfJets",
          stdbin, 0., 20.);

      _h["numberOfParticles"] = bookHisto1D("numberOfParticles",
          stdbin, 0., 200.);

      _h["numberOfVisibleParticles"] = bookHisto1D("numberOfVisibleParticles",
          stdbin, 0., 200.);

      _h["numberOfPhotons"] = bookHisto1D("numberOfPhotons",
          stdbin, 0., 100.);

      _h["energyPhotons"] = bookHisto1D("energyPhotons",
          stdbin, 0., 250.);

      vetoCounter = 0;
      eventCounter = 0;
      acceptedWeights = 0.;
    }

    void analyze(const Event& event) {
      const Particles all_particles =
        applyProjection<FinalState>(event, "FS").particles();
      const Particles charged_tracks =
        applyProjection<ChargedFinalState>(event, "CFS").particles();
      const Particles visible_particles =
        applyProjection<VisibleFinalState>(event, "VFS").particles();
      const FastJets& fastjets =
        applyProjection<FastJets>(event, "Jets");
      double minjetE = 1. * GeV;
      const PseudoJets pseudo_jets = fastjets.pseudoJetsByE(minjetE);
      double weight = event.weight();

      eventCounter++;
      bool vetoCondition = false;
      if (vetoCondition) {
        vetoCounter++;
        vetoEvent;
      } else {
        acceptedWeights += weight;
      }

      int n = 0;
      foreach (const PseudoJet & j, pseudo_jets) {
        n++;
      };
      _h["numberOfJets"]->fill(n, weight);

      n = 0;
      int n_photons = 0;
      double e_photons = 0.;
      foreach (const Particle& p, all_particles) {
        n++;
        if (p.pid() == PID::PHOTON) {
          n_photons++;
          e_photons += p.energy();
        }
      };
      _h["numberOfPhotons"]->fill(n_photons, weight);
      _h["energyPhotons"]->fill(e_photons, weight);
      _h["numberOfParticles"]->fill(n, weight);

      n = 0;
      foreach (const Particle& p, charged_tracks) {
        n++;
      };
      _h["numberOfChargedTracks"]->fill(n, weight);

      n = 0;
      foreach (const Particle& p, visible_particles) {
        n++;
      };
      _h["numberOfVisibleParticles"]->fill(n, weight);
    }


    void finalize() {
      // normalize(_h_YYYY); // normalize to unity
      const double fb_per_pb = 1000.0;
      //const double crossSec = crossSection ();
      const double crossSec = 1.0;
      double fiducial_xsection = crossSec * fb_per_pb *
        acceptedWeights / sumOfWeights();
      //double scale_factor = crossSection() * fb_per_pb / sumOfWeights();
      double scale_factor = 1.0 * fb_per_pb / sumOfWeights();

      cout << "Sum of weights: " << sumOfWeights () << endl;
      cout << "Sum of weights / N: " << sumOfWeights () / eventCounter << endl;
      cout << "Original cross section (pb): " << crossSec << endl;
      cout << "Number of total events: " << eventCounter << endl;
      cout << "Sum of weights / n_events: " << sumOfWeights () / eventCounter << endl;
      cout << "Numer of vetoed events: " << vetoCounter << endl;
      cout << "Final (fiducial) cross section (fb): " << fiducial_xsection << endl;
      cout << "Scale factor: " << scale_factor << endl;

      typedef std::map<string, Histo1DPtr>::iterator it;
      for(it iter = _h.begin(); iter != _h.end(); iter++) {
        //iter->second->finalize();
        scale(iter->second,scale_factor);
      }
    }


  private:

    std::map <string, Histo1DPtr> _h;

    int vetoCounter, eventCounter;
    double acceptedWeights;
  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(WHIZARD);

}
