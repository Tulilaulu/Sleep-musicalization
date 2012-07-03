
import gzip

from sleepmusicalization import controller


def main():
    analysis_result_json_string = gzip.open("sample_sleep_measurements/sample_analysis_result.json.gz").read()
    sleep_result_json_string = gzip.open("sample_sleep_measurements/sample_sleep_result.json.gz").read()
    
    controller.composeSong(analysis_result_json_string, sleep_result_json_string)

if __name__ == "__main__":
    main()
