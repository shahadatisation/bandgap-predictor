import os
from mp_api.client import MPRester
import pandas as pd

api_key = os.environ.get("MP_API_KEY")

with MPRester(api_key=api_key) as mpr:
    docs = mpr.materials.summary.search(
        is_stable=True,
        fields=["material_id", "formula_pretty", "band_gap", "formation_energy_per_atom"]
    )
    print("Number of Results : ", len(docs))

    data_list = []

    for doc in docs:
        row = {
            "material_id": doc.material_id,
            "formula": doc.formula_pretty,
            "band_gap": doc.band_gap,
            "formation_energy": doc.formation_energy_per_atom
        }
        data_list.append(row)

    print("Number of dictionaries: ", len(data_list))

    df = pd.DataFrame(data_list)
    print(df.shape)
    print(df.head())

    df.to_csv("materials_data_full.csv", index=False)

print("Done!")