#!/usr/bin/env python
from SCons.Script import Builder, Depends
import sconstruct_utils as su
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


def main(env, analysiss, processes, plot_together, configs,
    lo_nlo_lines_and_nlo_band, descriptions):
  analysis = env.Analysis("RivetAnalysis", analysiss)
  make_plot_dir = lambda d : d + '/index.html'
  control_plots = map(make_plot_dir, processes)
  plot_targets = [pt['target'] for pt in plot_together]
  plot_targets = map(make_plot_dir, plot_targets)
  for idx, pd in enumerate(plot_together):
    plot_together[idx]['target'] = make_plot_dir(pd['target'])

  print 'processes: ', processes
  yodas = build_yodas_from_hepmcs(env, processes)
  Depends(yodas, analysis)
  small_yoda_names = su.get_yodas_from_proc_list(processes)
  print 'small_yoda_names: ', small_yoda_names
  n_yodas = len(sum(small_yoda_names, []))
  if n_yodas > 0:
    final_yoda_names = su.get_final_yoda_names(small_yoda_names)
    print 'final_yoda_names: ', final_yoda_names
    merged_yodas = build_merged_yodas(env, small_yoda_names, final_yoda_names)
    nlo_yodas = su.find_nlo_yodas(merged_yodas)
    build_nlo_yodas(nlo_yodas, env)
    scale_variation_yodas = su.find_scale_variation_yodas(merged_yodas)
    final_scale_yodas = build_scale_variation_yodas(scale_variation_yodas, env)
    if len(final_scale_yodas) > 0:
      small_yoda_names = small_yoda_names + final_scale_yodas
      control_plots += map(make_plot_dir, final_scale_yodas)
      env.BuildEnvelope(target='envelope.yoda', source=final_scale_yodas)

    print 'Control plots: ', control_plots
    for (small_yodas, control_plot) in zip(small_yoda_names, control_plots):
      # TODO: (bcn 2016-05-26) Use all given configs
      try:
        if len(small_yodas) == 0:
          raise IndexError
        plot = env.Plot(target=control_plot, source=small_yodas, CONFIG=configs[0])
        Depends(plot, configs[0])
      except IndexError:
        print 'Could not build', control_plot, 'from', small_yodas

    if len(lo_nlo_lines_and_nlo_band) > 0:
      env.PlotLOLineWithNLOBand(target=plot_targets[0],
          source=lo_nlo_lines_and_nlo_band, CONFIG=configs[0])

    if len(plot_together) > 0:
      for plot_dict in plot_together:
        env.Plot(target=plot_dict['target'], source=plot_dict['lines'],
            CONFIG=configs[0], DESCRIPTIONS=descriptions)
