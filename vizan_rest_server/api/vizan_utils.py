from cobra.flux_analysis import flux_variability_analysis
import cobra.io as cio
import vizan


def perform_visualisation(model_filename, svg_filename, analysis_type='FBA',
                          analysis_results=None):
    model = cio.load_json_model(model_filename)
    if analysis_results is None:
        fba_results = model.optimize()
        if analysis_type == 'FBA':
            fba_results.fluxes = fba_results.fluxes.round(5)
            analysis_results = fba_results
        elif analysis_type == 'FVA':
            fva_results = flux_variability_analysis(model, fraction_of_optimum=0.5)
            fva_results.round(3)
            analysis_results = fva_results

    prod = 'prod'
    subst = 'subst'
    count = '0'
    vizan.call_vizan_cli(model, svg_filename, analysis_results, analysis_type,
                         "{}_{}_{}.svg".format(prod, subst, count))
