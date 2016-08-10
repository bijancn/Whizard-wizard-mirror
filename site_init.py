#!/usr/bin/env python
from SCons.Script import Builder
from glob import glob
import shutil


def generate_plot(source, target, env, for_signature):
  # ' --no-ratio' could be made an option
  plot_cmd = 'rivet-mkhtml --mc-errs --pdf --cm --single ' + \
      '--ignore-unvalidated --num-threads=$NUMTHREADS --config=$CONFIG '
  target_dir = target[0].dir
  try:
    descriptions = env['DESCRIPTIONS']
  except KeyError:
    descriptions = None
  if descriptions is not None:
    sources = ' '.join([str(s) + ':' + "'" + d + "'" for (s, d)
        in zip(source, descriptions)])
  else:
    sources = ' '.join([str(s) for s in source])
  return plot_cmd + '-o %s %s' % (target_dir, sources)


def generate_plot_with_lo_line_and_nlo_band(source, target, env, for_signature):
  return 'rivet-mkhtml -c $CONFIG %s:"Title=LO:LineColor=blue" \
     %s:"Title=NLO:ErrorBands=0:LineColor=red" \
     %s:"Title=:ErrorBands=1:ErrorBandColor=red:ErrorBandOpacity=0.5:LineColor=red"' \
     % (source[0], source[1], source[2])


def build_scale_variation_yodas(scale_variation_yodas, env):
  final_nlo_yodas = []
  for proc_string in ['proc_nlo_low', 'proc_nlo_central', 'proc_nlo_high']:
    if proc_string in scale_variation_yodas:
      print proc_string, scale_variation_yodas[proc_string]
      env.MergeYodasNoScale(target=proc_string + '.yoda',
          source=scale_variation_yodas[proc_string])
      final_nlo_yodas.append(proc_string)
  return final_nlo_yodas


def build_nlo_yodas(yoda_dict, env):
  final_nlo_yodas = []
  for key in yoda_dict:
    env.MergeYodasNoScale(target=key, source=yoda_dict[key])
    final_nlo_yodas.append(key)
  return final_nlo_yodas


def build_yodas_from_hepmcs(env, proc_list):
  hepmcs = [glob(p + '-*.hepmc') for p in proc_list]
  print 'Building Yodas from these hepmcs:', hepmcs
  return_yodas = []
  for h in hepmcs:
    for hh in h:
      return_yodas += [env.Yoda(hh)]
  return return_yodas


def build_merged_yodas(env, small_yoda_names, final_yoda_names):
  merged_yodas = []
  for small_yoda, yoda in zip(small_yoda_names, final_yoda_names):
    if len(small_yoda) > 1:
      merged_yodas.append(env.MergeYodas(target=yoda, source=small_yoda))
    else:
      try:
        shutil.copyfile(str(small_yoda[0]), yoda)
      except IOError:
        print 'File not there yet. This should be a builder'
      merged_yodas.append(yoda)
  return merged_yodas


def ADD_BUILDERS(env):
  build_yoda_from_hepmc = Builder(
      action='rivet --quiet --pwd -H $TARGET -a $ANALYSIS $SOURCES',
      suffix='.yoda', src_suffix='.hepmc')

  build_analysis = Builder(action='rivet-buildplugin $SOURCES',
                      suffix='.so', src_suffix='.cc')

  merge_yodas = Builder(action='yodamerge --assume-normalized -o $TARGET $SOURCES',
     suffix='.yoda', src_suffix='.yoda')

  merge_yodas_noscale = Builder(
      action='./yodamerge_noscale --assume-normalized -o $TARGET $SOURCES',
      suffix='.yoda', src_suffix='.yoda')

  build_envelope = Builder(action='./yodaenvelopes -o $TARGET -c $SOURCE $SOURCES',
     suffix='.yoda', src_suffix='.yoda')

  build_plot_with_lo_line_and_nlo_band = \
      Builder(generator=generate_plot_with_lo_line_and_nlo_band,
          suffix='.html',
          src_suffix='.yoda')

  build_plot = Builder(generator=generate_plot,
                      suffix='.html',
                      src_suffix='.yoda')

  env.Append(BUILDERS={'Yoda' : build_yoda_from_hepmc, 'Analysis' : build_analysis,
    'MergeYodas': merge_yodas, 'MergeYodasNoScale': merge_yodas_noscale,
    'BuildEnvelope': build_envelope,
    'Plot' : build_plot, 'PlotLOLineWithNLOBand': build_plot_with_lo_line_and_nlo_band})
