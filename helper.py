import logging
import json

BASE_URL = "https://www.myer.com.au/"
logging.basicConfig(filename='error.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def write_json_file(filename, data):
    with open("results/"+filename, "w") as file:
        # Write the JSON data to the file
        json.dump(data, file)
        print("writing to file: "+filename+" SUCCEED")
        print()

def route_intercept(route):
    if route.request.resource_type == "image":
        # print(f"Blocking the image request to: {route.request.url}")
        return route.abort()
    if "google" in route.request.url:
        print(f"blocking {route.request.url} as it contains Google")
        return route.abort()
    if "dynamicyield" in route.request.url:
        print(f"blocking {route.request.url} as it contains dynamicyield")
        return route.abort()
    if "bazaarvoice" in route.request.url:
        print(f"blocking {route.request.url} as it contains bazaarvoice")
        return route.abort()
    if "truefitcorp.com" in route.request.url:
        print(f"blocking {route.request.url} as it contains truefitcorp.com")
        return route.abort()
    if "reporting.cdndex.io" in route.request.url:
        print(f"blocking {route.request.url} as it contains reporting.cdndex.io")
        return route.abort()
    if "bam.nr-data.net" in route.request.url:
        print(f"blocking {route.request.url} as it contains bam.nr-data.net")
        return route.abort()
    if "ips.js" in route.request.url:
        print(f"blocking {route.request.url} as it contains ips.js")
        return route.abort()
    if "https://api-online.myer.com.au/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/tl" in route.request.url:
        print(f"blocking {route.request.url} as it contains /tl")
        return route.abort()
    return route.continue_()