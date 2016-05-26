#!/usr/bin/env python
from SCons.Script import Builder


def generate_plot(source, target, env, for_signature):
  plot_cmd = 'rivet-mkhtml --mc-errs --pdf --cm --single ' + \
      '--ignore-unvalidated --num-threads=$NUMTHREADS --config=$CONFIG --no-ratio '
  target_dir = target[0].dir
  try:
    descriptions = env['DESCRIPTIONS'].split('::')
  except KeyError:
    descriptions = None
  if descriptions is not None:
    sources = ' '.join([str(s) + ':' + "'" + d + "'" for (s, d)
        in zip(source, descriptions)])
  else:
    sources = ' '.join([str(s) for s in source])
  return plot_cmd + '-o %s %s' % (target_dir, sources)


def generate_plot_with_errors(source, target, env, for_signature):
  return 'rivet-mkhtml -c $CONFIG %s:"Title=LO:LineColor=blue" \
     %s:"Title=NLO:ErrorBands=0:LineColor=red" \
     %s:"Title=:ErrorBands=1:ErrorBandColor=red:ErrorBandOpacity=0.5:LineColor=red"' \
     % (source[0], source[1], source[2])


def ADD_BUILDERS(env):
  build_yoda_from_hepmc = Builder(
      action='rivet --quiet --pwd -H $TARGET $ANALYSIS $SOURCES',
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

  build_plot_with_errors = Builder(generator=generate_plot_with_errors,
                                   suffix='.html',
                                   src_suffix='.yoda')

  build_plot = Builder(generator=generate_plot,
                      suffix='.html',
                      src_suffix='.yoda')

  env.Append(BUILDERS={'Yoda' : build_yoda_from_hepmc, 'Analysis' : build_analysis,
    'MergeYodas': merge_yodas, 'MergeYodasNoScale': merge_yodas_noscale,
    'BuildEnvelope': build_envelope,
    'Plot' : build_plot, 'PlotWithErrorBand': build_plot_with_errors})
