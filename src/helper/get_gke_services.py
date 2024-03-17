import pandas as pd
import numpy as np
import os

ENV_NAME = os.environ.get("ENV_NAME")

df = pd.read_csv("gke_services.csv", delimiter=";")

rfm_service_ip = (
    df[df["NAME"] == "rfm{}".format(ENV_NAME)]["EXTERNAL-IP"].iloc[0]
    + ":" + df[df["NAME"] == "rfm{}".format(ENV_NAME)]["PORT(S)"].iloc[0].split(":")[0]
)

with open('rfm_service_ip', 'w') as f:
    f.write(rfm_service_ip)
