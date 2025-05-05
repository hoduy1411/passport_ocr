import re


# Define all country codes on passport 
country_code = [
    "AFG", "ALB", "DZA", "AND", "AGO", "ATG", "ARG", "ARM",
    "AUS", "AUT", "AZE", "BHS", "BHR", "BGD", "BRB", "BLR",
    "BEL", "BLZ", "BEN", "BTN", "BOL", "BIH", "BWA", "BRA",
    "BRN", "BGR", "BFA", "BDI", "CPV", "KHM", "CMR", "CAN",
    "CAF", "TCD", "CHL", "CHN", "COL", "COM", "COD", "COG",
    "CRI", "HRV", "CUB", "CYP", "CZE", "DNK", "DJI", "DMA",
    "DOM", "ECU", "EGY", "SLV", "GNQ", "ERI", "EST", "SWZ",
    "ETH", "FJI", "FIN", "FRA", "GAB", "GMB", "GEO", "DEU",
    "GHA", "GRC", "GRD", "GTM", "GIN", "GNB", "GUY", "HTI",
    "HND", "HUN", "ISL", "IND", "IDN", "IRN", "IRQ", "IRL",
    "ISR", "ITA", "JAM", "JPN", "JOR", "KAZ", "KEN", "KIR",
    "PRK", "KOR", "KWT", "KGZ", "LAO", "LVA", "LBN", "LSO",
    "LBR", "LBY", "LIE", "LTU", "LUX", "MDG", "MWI", "MYS",
    "MDV", "MLI", "MLT", "MHL", "MRT", "MUS", "MEX", "FSM",
    "MDA", "MCO", "MNG", "MNE", "MAR", "MOZ", "MMR", "NAM",
    "NRU", "NPL", "NLD", "NZL", "NIC", "NER", "NGA", "MKD",
    "NOR", "OMN", "PAK", "PLW", "PSE", "PAN", "PNG", "PRY",
    "PER", "PHL", "POL", "PRT", "QAT", "ROU", "RUS", "RWA",
    "KNA", "LCA", "VCT", "WSM", "SMR", "STP", "SAU", "SEN",
    "SRB", "SYC", "SLE", "SGP", "SVK", "SVN", "SLB", "SOM",
    "ZAF", "SSD", "ESP", "LKA", "SDN", "SUR", "SWE", "CHE",
    "SYR", "TJK", "TZA", "THA", "TLS", "TGO", "TON", "TTO",
    "TUN", "TUR", "TKM", "TUV", "UGA", "UKR", "ARE", "GBR",
    "USA", "URY", "UZB", "VUT", "VAT", "VEN", "VNM", "YEM",
    "ZMB", "ZWE"
]


def format_nation_code(inp_nc):
    # Create regular expression
    pattern = '|'.join(re.escape(text) for text in country_code)

    # Find a reasonable result
    matches = re.findall(pattern, inp_nc, re.IGNORECASE)

    # Return the result
    if len(matches):
        return matches[0].upper()
    else:
        result = []
        for i in range(len(inp_nc) - 3):
            result.append(inp_nc[i:i+3] + inp_nc[i+3])
        
        for rst in result:
            if len(rst) == 3:
                pass
        return ""