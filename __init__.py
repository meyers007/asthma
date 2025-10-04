import os, sys

sys.path.append("/opt/utils/geo_utils/")
try:
    import asthma.update
except Exception as e:
    print(f"\n*******\n***** ERROR LOADING\n{e}\n*******\n*******")
    pass


