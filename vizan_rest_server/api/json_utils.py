import json

import cobra
import pandas as pd


class CobraSolutionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, cobra.core.Solution):
            return dict(
                objective_value=obj.objective_value,
                status=obj.status,
                fluxes=json.loads(obj.fluxes.to_json()),
                reduced_costs=json.loads(obj.reduced_costs.to_json()),
                shadow_prices=json.loads(obj.shadow_prices.to_json()))
        # Let the base class default method raise the TypeError
        return super(CobraSolutionEncoder, self).default(obj)


class CobraSolutionDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(obj):
        if 'objective_value' not in obj:
            return obj
        objective_value = obj['objective_value']
        status = obj['status']
        fluxes = obj['fluxes']
        reduced_costs = obj['reduced_costs']
        shadow_prices = obj['shadow_prices']
        return cobra.core.Solution(
            objective_value,
            status,
            pd.read_json(json.dumps(fluxes), typ='series'),
            pd.read_json(json.dumps(reduced_costs), typ='series'),
            pd.read_json(json.dumps(shadow_prices), typ='series'),
        )
