from cobra.flux_analysis import flux_variability_analysis
import cobra.io as cio
import vizan
import tempfile


def perform_visualisation(model_filename, svg_filename, analysis_type='FBA',
                          analysis_results=None, output_filename=None, intermediate_filename=None):
    model = cio.load_json_model(model_filename)
    if analysis_results is None:
        fba_results = model.optimize()
        if analysis_type == 'FBA':
            fba_results.fluxes = fba_results.fluxes.round(5)
            analysis_results = fba_results
        elif analysis_type == 'FVA':
            fva_results = flux_variability_analysis(model, fraction_of_optimum=0.5)
            fva_results = fva_results.round(3)
            analysis_results = fva_results
    if output_filename is None:
        output_file = tempfile.NamedTemporaryFile(mode="w")
        output_filename = output_file.name
    if intermediate_filename is None:
        intermediate_file = tempfile.NamedTemporaryFile(mode="w")
        intermediate_filename = intermediate_file.name
    vizan.call_vizan_cli(model, svg_filename, analysis_results, analysis_type, output_filename, intermediate_filename)
