import difflib


data_code = [
    "AFG", "ALB", "DZA", "AND", "AGO", "ATG", "ARG", "ARM", "ABW", "AUS",
    "AUT", "AZE", "BHS", "BHR", "BGD", "BRB", "BEL", "BLZ", "BEN", "BTN",
    "BOL", "BES", "BIH", "BWA", "BVT", "BRA", "IOT", "BRN", "BGR", "BFA",
    "BDI", "KHM", "CMR", "CAN", "CPV", "CYM", "CAF", "TCD", "CHL", "CHN",
    "CXR", "CCK", "COL", "COM", "COG", "COD", "COK", "CRI", "CIV", "HRV",
    "CUB", "CUW", "CYM", "CYP", "CZE", "DNK", "DJI", "DMA", "DOM", "ECU",
    "EGY", "SLV", "GNQ", "ERI", "EST", "SWZ", "ETH", "FLK", "FRO", "FJI",
    "FIN", "FRA", "GAB", "GMB", "GEO", "DEU", "GHA", "GIB", "GRC", "GRD",
    "GLP", "GUM", "GTM", "GGY", "GIN", "GNB", "GUY", "HTI", "HMD", "VAT",
    "HND", "HKG", "HUN", "ISL", "IND", "IDN", "IRN", "IRQ", "IRL", "IMN",
    "ISR", "ITA", "JAM", "JPN", "JEY", "JOR", "KAZ", "KEN", "KIR", "KOR",
    "KOS", "KWT", "KGZ", "LAO", "LVA", "LBN", "LSO", "LBR", "LBY", "LIE",
    "LTU", "LUX", "MAC", "MDG", "MWI", "MYS", "MDV", "MLI", "MLT", "MHL",
    "MTQ", "MRU", "MRT", "MEX", "FSM", "MDA", "MCO", "MNG", "MNE", "MSR",
    "MAR", "MOZ", "MMR", "NAM", "NRU", "NPL", "NLD", "NCL", "NZL", "NIC",
    "NER", "NGA", "NIU", "NFK", "MNP", "NOR", "OMN", "PAK", "PLW", "PSE",
    "PAN", "PNG", "PRY", "PER", "PHL", "PCN", "POL", "PRT", "PRI", "QAT",
    "REU", "ROU", "RUS", "RWA", "BLM", "SHN", "KNA", "LCA", "MAF", "SPM",
    "VCT", "WSM", "SMR", "STP", "SAU", "SEN", "SRB", "SYC", "SLE", "SGP",
    "SXM", "SVK", "SVN", "SLB", "SOM", "ZAF", "SGS", "SSD", "ESP", "LKA",
    "SDN", "SUR", "SJM", "SWZ", "SWE", "CHE", "SYR", "TJK", "TZA", "THA",
    "TGO", "TKL", "TON", "TTO", "TUN", "TUR", "TKM", "TUV", "UGA", "UKR",
    "ARE", "GBR", "USA", "UMI", "URY", "UZB", "VUT", "VEN", "VNM", "VGB",
    "VIR", "WLF", "WSM", "ZMB", "ZWE"
]


data_address = [
    "AN GIANG", "BÀ RỊA-VŨNG TÀU", "BẮC GIANG", "BẮC KẠN", "BẠC LIÊU", "BẮC NINH",
    "BẾN TRE", "BÌNH ĐỊNH", "BÌNH DƯƠNG", "BÌNH PHƯỚC", "BÌNH THUẬN", "CÀ MAU",
    "CẦN THƠ", "CAO BẰNG", "ĐÀ NẴNG", "ĐẮK LẮK", "ĐẮK NÔNG", "ĐIỆN BIÊN",
    "ĐỒNG NAI", "ĐỒNG THÁP", "GIA LAI", "HÀ GIANG", "HÀ NAM", "HÀ NỘI", "HÀ TĨNH",
    "HẢI DƯƠNG", "HẢI PHÒNG", "HẬU GIANG", "HÒA BÌNH", "HƯNG YÊN", "KHÁNH HÒA", "KIÊN GIANG",
    "KON TUM", "LAI CHÂU", "LÀO CAI", "LẠNG SƠN", "LÂM ĐỒNG", "LONG AN", "NAM ĐỊNH", "NGHỆ AN",
    "NINH BÌNH", "NINH THUẬN", "PHÚ THỌ", "PHÚ YÊN", "QUẢNG BÌNH", "QUẢNG NAM",
    "QUẢNG NGÃI", "QUẢNG NINH", "SÓC TRĂNG", "SƠN LA", "TÂY NINH", "THÁI BÌNH",
    "THÁI NGUYÊN", "THANH HÓA", "THỪA THIÊN-HUẾ", "TIỀN GIANG", "TRÀ VINH", 
    "TUYÊN QUANG", "TP. HÀ NỘI", "TP. HỒ CHÍ MINH", "VĨNH LONG", "VĨNH PHÚC", "YÊN BÁI"
]


def correct_code(input_text):
    if (input_text in ['YNM']):
        return "VNM"
    else:
        return input_text

#     closest_match = difflib.get_close_matches(input_text, data_code, n=1, cutoff=0.6)
#     return closest_match[0] if closest_match else input_text


def correct_address(input_text):
    closest_match = difflib.get_close_matches(input_text, data_address, n=1, cutoff=0.6)
    return closest_match[0] if closest_match else input_text